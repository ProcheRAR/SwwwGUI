import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, GdkPixbuf, Gdk

import os
import json
import subprocess
from pathlib import Path
import logging

from swww_gui.ui.image_view import ImageView
from swww_gui.ui.file_chooser import FileChooser
from swww_gui.ui.effects_panel import EffectsPanel
from swww_gui.swww_manager import SwwwManager

logger = logging.getLogger(__name__)

class SwwwGuiWindow(Adw.ApplicationWindow):
    """The main application window."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.application = kwargs.get('application')
        self.config = self.application.config
        
        # Set window properties
        self.set_default_size(1000, 680)
        self.set_title("SwwwGui")
        
        # Load CSS provider
        self._load_css()
        
        # Initialize swww manager
        self.swww_manager = SwwwManager()
        
        # Create UI widgets
        self.main_stack = None
        self.main_content = None
        self.search_entry = None
        self.image_container = None
        self.settings_button = None
        self.apply_button = None
        self.maximize_button = None
        self.title_label = None
        
        # Build UI manually
        self.build_ui()
        
        # Setup UI components
        self.setup_ui()
        
        # Connect signals
        self.connect_signals()
        
        # Check if swww is running
        self.check_swww_daemon()
        
        # Load last settings if available
        self.load_settings()
        
        # Apply localization
        self.update_localization()

    def _load_css(self):
        """Load CSS styles from resources."""
        css_provider = Gtk.CssProvider()
        try:
            css_provider.load_from_resource('/io/github/swwwgui/css/style.css')
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
            logger.info("CSS loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load CSS: {e}")
        
    def build_ui(self):
        """Build the UI programmatically instead of using GTK templates."""
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Add toast overlay
        self.toast_overlay = Adw.ToastOverlay()
        self.toast_overlay.set_child(main_box)
        self.set_content(self.toast_overlay)
        
        # Header bar
        header_bar = Adw.HeaderBar()
        header_bar.set_centering_policy(Adw.CenteringPolicy.STRICT)
        main_box.append(header_bar)
        
        # Title widget
        self.title_label = Adw.WindowTitle()
        self.title_label.set_title(self.application.translator.translate("app_title"))
        self.title_label.set_subtitle(self.application.translator.translate("app_subtitle"))
        header_bar.set_title_widget(self.title_label)
        
        # Settings button
        self.settings_button = Gtk.Button()
        self.settings_button.set_icon_name("emblem-system-symbolic")
        self.settings_button.set_tooltip_text(self.application.translator.translate("settings"))
        header_bar.pack_start(self.settings_button)
        
        # Apply and side panel toggle buttons
        button_box = Gtk.Box(spacing=6)
        
        # Maximize view button (toggles side panel visibility)
        self.maximize_button = Gtk.Button()
        self.maximize_button.set_icon_name("view-fullscreen-symbolic")
        self.maximize_button.set_tooltip_text(self.application.translator.translate("maximize_view"))
        button_box.append(self.maximize_button)
        
        self.apply_button = Gtk.Button(label=self.application.translator.translate("apply"))
        self.apply_button.set_tooltip_text(self.application.translator.translate("apply"))
        self.apply_button.add_css_class("suggested-action")
        button_box.append(self.apply_button)
        
        header_bar.pack_end(button_box)
        
        # Search entry (without SearchBar container)
        search_box = Gtk.Box()
        search_box.set_margin_start(12)
        search_box.set_margin_end(12)
        search_box.set_margin_top(6)
        search_box.set_margin_bottom(6)
        main_box.append(search_box)
        
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_hexpand(True)
        self.search_entry.set_placeholder_text(self.application.translator.translate("search_placeholder"))
        search_box.append(self.search_entry)
        
        # Main stack
        self.main_stack = Gtk.Stack()
        self.main_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.main_stack.set_vexpand(True)
        main_box.append(self.main_stack)
        
        # Main content area with adaptive layout using AdwFlap
        self.content_flap = Adw.Flap()
        self.content_flap.set_fold_policy(Adw.FlapFoldPolicy.AUTO)
        self.content_flap.set_transition_type(Adw.FlapTransitionType.OVER)
        self.content_flap.set_modal(False)
        self.content_flap.set_swipe_to_open(True)
        self.content_flap.set_swipe_to_close(True)
        self.main_stack.add_named(self.content_flap, "main")
        
        # Image container for preview
        self.image_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.image_container.set_hexpand(True)
        self.image_container.set_vexpand(True)
        self.image_container.set_margin_start(12)
        self.image_container.set_margin_end(12)
        self.image_container.set_margin_top(12)
        self.image_container.set_margin_bottom(12)
        
        # Use an overlay to show preview and info
        image_overlay = Gtk.Overlay()
        image_overlay.set_child(self.image_container)
        
        # Flap content - main content for panels
        self.main_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.main_content.set_hexpand(True)
        
        # ScrolledWindow for the flap content
        content_scroll = Gtk.ScrolledWindow()
        content_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        content_scroll.set_min_content_width(400)
        content_scroll.set_child(self.main_content)
        
        # Add content to flap
        self.content_flap.set_content(image_overlay)
        self.content_flap.set_flap(content_scroll)
        
    def setup_ui(self):
        """Set up the main UI components."""
        # Image view
        self.image_view = ImageView()
        self.image_container.append(self.image_view)
        
        # File chooser
        self.file_chooser = FileChooser(self)
        self.main_content.append(self.file_chooser)
        
        # Effects panel
        self.effects_panel = EffectsPanel(self)
        self.main_content.append(self.effects_panel)
        
        # Set default image if available
        if self.config.get('last_image'):
            path = self.config.get('last_image')
            if os.path.exists(path):
                self.image_view.load_image(path)
                self.title_label.set_title(os.path.basename(path))

    def connect_signals(self):
        """Connect UI signals to callbacks."""
        self.apply_button.connect('clicked', self.on_apply_clicked)
        self.maximize_button.connect('clicked', self.on_maximize_clicked)
        self.settings_button.connect('clicked', self.on_settings_clicked)
        self.search_entry.connect('search-changed', self.on_search_changed)
        
    def on_maximize_clicked(self, button):
        """Toggle side panel visibility to maximize image view."""
        is_revealed = self.content_flap.get_reveal_flap()
        self.content_flap.set_reveal_flap(not is_revealed)
        
        # Update the button icon based on the panel state
        if is_revealed:
            # Panel is now hidden (maximized view)
            self.maximize_button.set_icon_name("view-restore-symbolic")
        else:
            # Panel is now visible (normal view)
            self.maximize_button.set_icon_name("view-fullscreen-symbolic")

    def check_swww_daemon(self):
        """Check if swww-daemon is running and start it if needed."""
        if not self.swww_manager.is_daemon_running():
            dialog = Adw.MessageDialog(
                transient_for=self,
                heading=self.application.translator.translate("daemon_not_running"),
                body=self.application.translator.translate("daemon_start_question"),
                close_response="cancel"
            )
            dialog.add_response("cancel", self.application.translator.translate("cancel"))
            dialog.add_response("start", self.application.translator.translate("start_daemon"))
            dialog.set_response_appearance("start", Adw.ResponseAppearance.SUGGESTED)
            dialog.connect("response", self.on_daemon_dialog_response)
            dialog.present()

    def on_daemon_dialog_response(self, dialog, response):
        """Handle response from daemon start dialog."""
        if response == "start":
            success = self.swww_manager.start_daemon()
            if not success:
                error_dialog = Adw.MessageDialog(
                    transient_for=self,
                    heading=self.application.translator.translate("error"),
                    body=self.application.translator.translate("daemon_start_failed"),
                    close_response="ok"
                )
                error_dialog.add_response("ok", self.application.translator.translate("ok"))
                error_dialog.present()

    def on_apply_clicked(self, button):
        """Apply the selected wallpaper with chosen effects."""
        if not self.image_view.current_image_path:
            return
            
        # Get all options from the effects panel
        options = self.effects_panel.get_all_options()
        
        # Удалены опции монитора
        # Monitor всегда будет пустой строкой, чтобы влиять на все мониторы
        options['monitor'] = ''
        
        # Save current settings
        self.save_settings()
        
        # Check if matugen is enabled
        use_matugen = self.config.get('use_matugen', False)
        
        if use_matugen:
            # Use matugen and update its config
            success = self._apply_with_matugen(self.image_view.current_image_path, options)
        else:
            # Use standard swww
            success = self.swww_manager.set_wallpaper(
                self.image_view.current_image_path,
                options
            )
        
        if success:
            # Show success toast
            toast = Adw.Toast.new(self.application.translator.translate("wallpaper_applied"))
            toast.set_timeout(2)
            self.add_toast(toast)
        else:
            # Show error dialog
            error_dialog = Adw.MessageDialog(
                heading=self.application.translator.translate("error"),
                body=self.application.translator.translate("wallpaper_set_failed"),
                close_response="ok"
            )
            error_dialog.add_response("ok", self.application.translator.translate("ok"))
            error_dialog.present()

    def on_settings_clicked(self, button):
        """Open settings popover."""
        # Create settings dialog
        dialog = Adw.PreferencesDialog()
        dialog.set_title(self.application.translator.translate("settings"))
        
        # Add language settings page
        self._add_language_settings_page(dialog)
        
        # Add matugen settings page
        self._add_matugen_settings_page(dialog)
        
        # Add about page
        self._add_about_page(dialog)
        
        # Сохраняем ссылку на текущий диалог
        self.settings_dialog = dialog
        
        # Show dialog
        dialog.present()
    
    def _add_language_settings_page(self, dialog):
        """Add language settings page to preferences dialog."""
        # Create language page
        page = Adw.PreferencesPage()
        page.set_title(self.application.translator.translate("language_settings"))
        page.set_icon_name("preferences-desktop-locale-symbolic")
        
        # Language selection group
        group = Adw.PreferencesGroup()
        page.add(group)
        
        # Language combo row
        language_row = Adw.ComboRow()
        language_row.set_title(self.application.translator.translate("language"))
        
        # Create language model
        languages = self.application.translator.get_supported_languages()
        string_list = Gtk.StringList()
        for lang in languages:
            string_list.append(lang["name"])
        
        language_row.set_model(string_list)
        
        # Set current language
        current_language = self.application.translator.get_current_language()
        for i, lang in enumerate(languages):
            if lang["code"] == current_language:
                language_row.set_selected(i)
                break
        
        # Connect signal
        language_row.connect("notify::selected", self._on_language_changed)
        
        # Store languages for later use
        self.available_languages = languages
        self.language_row = language_row
        
        # Сохраняем ссылки на элементы для обновления перевода
        self.language_page = page
        
        group.add(language_row)
        dialog.add(page)
    
    def _add_matugen_settings_page(self, dialog):
        """Add matugen settings page to preferences dialog."""
        # Create matugen page
        page = Adw.PreferencesPage()
        
        # Use capitalized Matugen
        if self.application.translator.get_current_language() == "ru":
            page.set_title("Matugen")
        else:
            page.set_title("Matugen")
            
        page.set_icon_name("color-select-symbolic")
        
        # Matugen group
        group = Adw.PreferencesGroup()
        
        # Use capitalized Matugen
        if self.application.translator.get_current_language() == "ru":
            group.set_title("Интеграция Matugen")
        else:
            group.set_title("Matugen Integration")
            
        page.add(group)
        
        # Matugen switch row
        matugen_row = Adw.SwitchRow()
        
        # Use capitalized Matugen
        if self.application.translator.get_current_language() == "ru":
            matugen_row.set_title("Использовать Matugen")
            matugen_row.set_subtitle("Генерировать тему Material You на основе обоев")
        else:
            matugen_row.set_title("Use Matugen")
            matugen_row.set_subtitle("Generate Material You theme based on wallpaper")
        
        # Set current state from config
        use_matugen = self.config.get('use_matugen', False)
        matugen_row.set_active(use_matugen)
        
        # Connect signal
        matugen_row.connect("notify::active", self._on_matugen_toggled)
        
        # Store reference for localization updates
        self.matugen_page = page
        self.matugen_row = matugen_row
        self.matugen_group = group
        
        group.add(matugen_row)
        dialog.add(page)
    
    def _add_about_page(self, dialog):
        """Add about page to preferences dialog."""
        # Create about page
        page = Adw.PreferencesPage()
        
        # Используем явные строки вместо переводов
        about_title = "О Программе" if self.application.translator.get_current_language() == "ru" else "About"
        page.set_title(about_title)
        page.set_icon_name("help-about-symbolic")
        
        # About group
        group = Adw.PreferencesGroup()
        page.add(group)
        
        # Version
        version_row = Adw.ActionRow()
        version_title = "Версия" if self.application.translator.get_current_language() == "ru" else "Version"
        version_row.set_title(version_title)
        version_row.set_subtitle("1.0.0")
        group.add(version_row)
        
        # GitHub repository
        repo_row = Adw.ActionRow()
        repo_row.set_title("Github")
        repo_row.set_subtitle("github.com/ProcheRAR/SwwwGUI")
        
        # Visit button
        visit_button = Gtk.Button()
        visit_button.set_icon_name("web-browser-symbolic")
        visit_repo_text = "Перейти в репозиторий" if self.application.translator.get_current_language() == "ru" else "Visit Repository"
        visit_button.set_tooltip_text(visit_repo_text)
        visit_button.set_valign(Gtk.Align.CENTER)
        visit_button.connect("clicked", self._on_visit_repo_clicked)
        repo_row.add_suffix(visit_button)
        
        group.add(repo_row)
        
        # Reset settings group
        reset_group = Adw.PreferencesGroup()
        reset_title = "Сброс настроек" if self.application.translator.get_current_language() == "ru" else "Reset Settings"
        reset_group.set_title(reset_title)
        page.add(reset_group)
        
        # Reset settings button
        reset_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        reset_box.set_halign(Gtk.Align.CENTER)
        reset_box.set_margin_top(24)  # Увеличенный отступ сверху
        reset_box.set_margin_bottom(24)  # Увеличенный отступ снизу
        reset_box.set_hexpand(True)
        reset_box.set_margin_start(24)
        reset_box.set_margin_end(24)
        
        reset_button = Gtk.Button()
        reset_text = "Сбросить все настройки" if self.application.translator.get_current_language() == "ru" else "Reset All Settings"
        
        # Добавляем иконку к кнопке
        reset_icon = Gtk.Image.new_from_icon_name("edit-clear-all-symbolic")
        reset_button.set_child(reset_icon)  # Установим сначала иконку
        reset_button.set_label(reset_text)  # А потом добавим текст - это создаст box с иконкой и текстом
        
        # Добавляем больше CSS классов для заметности
        reset_button.add_css_class("destructive-action")
        reset_button.add_css_class("pill")
        reset_button.add_css_class("suggested-action")
        reset_button.add_css_class("large-button")
        
        reset_button.set_hexpand(True)
        reset_button.connect("clicked", self._on_reset_all_settings)
        reset_box.append(reset_button)
        
        reset_group.add(reset_box)
        
        # Save references
        self.about_page = page
        self.reset_group = reset_group
        self.reset_button = reset_button
        
        dialog.add(page)

    def _on_reset_all_settings(self, button):
        """Reset all settings to defaults without confirmation."""
        # Reset all settings directly without confirmation
        self.config.reset_to_defaults()
        
        # Reload settings
        self.load_settings()
        
        # Show success toast with hardcoded strings
        success_text = "Настройки успешно сброшены" if self.application.translator.get_current_language() == "ru" else "Settings reset successfully"
        toast = Adw.Toast.new(success_text)
        toast.set_timeout(2)
        self.add_toast(toast)

    def _on_language_changed(self, row, pspec):
        """Handle language change."""
        selected = row.get_selected()
        if 0 <= selected < len(self.available_languages):
            language_code = self.available_languages[selected]["code"]
            if self.application.translator.set_language(language_code):
                # Обновить локализацию в текущем окне
                self.update_localization()
                
                # Заставить EffectsPanel обновиться
                if hasattr(self, 'effects_panel'):
                    # Передаем новый язык в EffectsPanel
                    self.effects_panel.update_localization()
                
                # Обновить диалог настроек
                if hasattr(self, 'settings_dialog') and self.settings_dialog:
                    # Обновляем заголовок диалога
                    self.settings_dialog.set_title(self.application.translator.translate("settings"))
                    
                    # Обновляем страницы, используя сохраненные ссылки
                    self._update_settings_pages()

    def _on_matugen_toggled(self, row, pspec):
        """Handle matugen integration toggle."""
        is_active = row.get_active()
        self.config.set('use_matugen', is_active)
        self.config.save()
        
        if is_active:
            # Show info message about matugen
            toast = Adw.Toast.new(self.application.translator.translate("matugen_enabled"))
            toast.set_timeout(3)
            self.add_toast(toast)

    def _update_settings_pages(self):
        """Update settings dialog pages with current translations."""
        tr = self.application.translator
        is_russian = tr.get_current_language() == "ru"
        
        # Update language settings
        if hasattr(self, 'language_page'):
            self.language_page.set_title(tr.translate("language_settings"))
            
        if hasattr(self, 'language_row'):
            self.language_row.set_title(tr.translate("language"))
        
        # Update matugen settings - use hardcoded strings instead of translations
        if hasattr(self, 'matugen_page'):
            self.matugen_page.set_title("Matugen")  # Brand name - no translation needed
            
        if hasattr(self, 'matugen_group'):
            matugen_group_title = "Интеграция Matugen" if is_russian else "Matugen Integration"
            self.matugen_group.set_title(matugen_group_title)
            
        if hasattr(self, 'matugen_row'):
            matugen_row_title = "Использовать Matugen" if is_russian else "Use Matugen"
            matugen_subtitle = "Генерировать тему Material You на основе обоев" if is_russian else "Generate Material You theme based on wallpaper"
            self.matugen_row.set_title(matugen_row_title)
            self.matugen_row.set_subtitle(matugen_subtitle)
        
        # Update about page
        if hasattr(self, 'about_page'):
            about_title = "О Программе" if is_russian else "About"
            self.about_page.set_title(about_title)
            
        # Update reset group title and button in About page using hardcoded strings
        if hasattr(self, 'reset_group') and hasattr(self, 'reset_button'):
            reset_title = "Сброс настроек" if is_russian else "Reset Settings"
            reset_button_text = "Сбросить все настройки" if is_russian else "Reset All Settings"
            self.reset_group.set_title(reset_title)
            self.reset_button.set_label(reset_button_text)

    def on_search_changed(self, entry):
        """Handle search in the file chooser."""
        search_text = entry.get_text()
        self.file_chooser.filter_files(search_text)

    def load_settings(self):
        """Load settings from config."""
        # Load basic transition settings
        transition_type = self.config.get('transition_type', 'simple')
        transition_step = self.config.get('transition_step', 2)
        transition_fps = self.config.get('transition_fps', 30)
        transition_duration = self.config.get('transition_duration', 3.0)
        
        self.effects_panel.set_transition_type(transition_type)
        self.effects_panel.set_transition_step(transition_step)
        self.effects_panel.set_transition_fps(transition_fps)
        self.effects_panel.set_transition_duration(transition_duration)
        
        # Load image settings
        resize_mode = self.config.get('resize_mode', 'crop')
        fill_color = self.config.get('fill_color', '000000')
        filter_type = self.config.get('filter', 'Lanczos3')
        
        self.effects_panel.set_resize_mode(resize_mode)
        self.effects_panel.set_fill_color(fill_color)
        self.effects_panel.set_filter(filter_type)
        
        # Load advanced settings
        transition_angle = self.config.get('transition_angle', 45)
        transition_wave = self.config.get('transition_wave', '20,20')
        transition_pos = self.config.get('transition_pos', 'center')
        invert_y = self.config.get('invert_y', False)
        transition_bezier = self.config.get('transition_bezier', '.54,0,.34,.99')
        
        self.effects_panel.set_transition_angle(transition_angle)
        self.effects_panel.set_transition_wave(transition_wave)
        self.effects_panel.set_transition_position(transition_pos)
        self.effects_panel.set_invert_y(invert_y)
        self.effects_panel.set_transition_bezier(transition_bezier)
        
        # Удалены настройки монитора

    def save_settings(self):
        """Save current settings to config."""
        if self.image_view.current_image_path:
            self.config.set('last_image', self.image_view.current_image_path)
        
        # Get all options
        options = self.effects_panel.get_all_options()
        
        # Save all settings to config
        for key, value in options.items():
            self.config.set(key, value)
        
        # Удалены настройки монитора
        
        # Save config to file
        self.config.save()
        
    def add_toast(self, toast):
        """Add a toast notification to the overlay."""
        self.toast_overlay.add_toast(toast)

    def update_localization(self):
        """Update all UI elements with current language."""
        # Update title bar
        self.title_label.set_title(self.application.translator.translate("app_title"))
        self.title_label.set_subtitle(self.application.translator.translate("app_subtitle"))
        
        # Update buttons
        self.settings_button.set_tooltip_text(self.application.translator.translate("settings"))
        self.maximize_button.set_tooltip_text(self.application.translator.translate("maximize_view"))
        self.apply_button.set_label(self.application.translator.translate("apply"))
        self.apply_button.set_tooltip_text(self.application.translator.translate("apply"))
        
        # Update search entry
        self.search_entry.set_placeholder_text(self.application.translator.translate("search_placeholder"))

    def _apply_with_matugen(self, image_path, options):
        """Apply wallpaper using matugen."""
        try:
            # First, update matugen config file
            config_updated = self._update_matugen_config(options)
            if not config_updated:
                # Fallback to standard swww if config update failed
                logger.warning("Failed to update matugen config")
                return self.swww_manager.set_wallpaper(image_path, options)
            
            # Then run matugen command
            logger.debug(f"Running matugen with image: {image_path}")
            result = subprocess.run(
                ["matugen", "image", image_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.warning(f"Matugen failed with exit code {result.returncode}: {result.stderr}")
                # Fallback to standard swww if matugen failed
                return self.swww_manager.set_wallpaper(image_path, options)
                
            return True
        except Exception as e:
            logger.error(f"Error applying with matugen: {e}")
            # Fallback to standard swww
            return self.swww_manager.set_wallpaper(image_path, options)
    
    def _update_matugen_config(self, options):
        """Update matugen config file with swww options."""
        config_path = os.path.expanduser("~/.config/matugen/config.toml")
        
        try:
            # Check if the directory exists, create if not
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # Convert swww options to matugen arguments
            args = ["img"]
            
            # Add transition type
            transition_type = options.get('transition_type', 'simple')
            args.extend(["--transition-type", transition_type])
            
            # Add transition fps and step
            args.extend(["--transition-fps", str(options.get('transition_fps', 30))])
            args.extend(["--transition-step", str(options.get('transition_step', 2))])
            
            # Add resize mode if specified
            if 'resize_mode' in options and options['resize_mode'] != 'none':
                args.extend(["--resize", options['resize_mode']])
            
            # Add filter if specified
            if 'filter' in options:
                args.extend(["--filter", options['filter']])
                
            # Add fill color if specified
            if 'fill_color' in options:
                args.extend(["--fill-color", options['fill_color']])
                
            # Add transition specific options based on type
            if transition_type == 'wipe':
                args.extend(["--transition-angle", str(options.get('transition_angle', 45))])
            elif transition_type == 'wave':
                args.extend(["--transition-wave", options.get('transition_wave', '20,20')])
            elif transition_type in ['grow', 'outer', 'any']:
                args.extend(["--transition-pos", options.get('transition_pos', 'center')])
            
            if options.get('invert_y', False):
                args.append("--invert-y")
                
            # Прочитаем существующий конфиг или создадим новый
            config_content = ""
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config_content = f.read()
            
            # Создаем новый контент на основе существующего, но с обновленной секцией wallpaper
            new_config_content = ""
            
            # Если конфиг пустой, создаем с нуля
            if not config_content.strip():
                new_config_content = f"""[config.wallpaper]
command = "swww"
arguments = {json.dumps(args)}
set = true
"""
            else:
                # Разбиваем конфиг на секции
                sections = []
                current_section = ""
                current_section_name = ""
                lines = config_content.split("\n")
                
                for line in lines:
                    # Если встретили начало новой секции
                    if line.strip().startswith("[") and line.strip().endswith("]"):
                        # Если в текущей секции есть содержимое, добавляем её
                        if current_section:
                            # Пропускаем секцию wallpaper, она будет обновлена позже
                            if current_section_name != "[config.wallpaper]":
                                sections.append((current_section_name, current_section))
                        # Начинаем новую секцию
                        current_section_name = line.strip()
                        current_section = line + "\n"
                    else:
                        # Добавляем строку в текущую секцию
                        if current_section_name:  # Если есть имя секции
                            current_section += line + "\n"
                
                # Добавляем последнюю секцию, если она есть и это не wallpaper
                if current_section and current_section_name != "[config.wallpaper]":
                    sections.append((current_section_name, current_section))
                
                # Собираем все обратно, добавляя обновленную секцию wallpaper
                for name, content in sections:
                    new_config_content += content
                
                # Добавляем обновленную секцию wallpaper
                if new_config_content and not new_config_content.endswith("\n\n"):
                    if not new_config_content.endswith("\n"):
                        new_config_content += "\n"
                    new_config_content += "\n"
                
                new_config_content += f"""[config.wallpaper]
command = "swww"
arguments = {json.dumps(args)}
set = true
"""
            
            # Записываем обновленный конфиг
            with open(config_path, "w") as f:
                f.write(new_config_content)
            
            return True
        
        except Exception as e:
            logger.error(f"Error updating matugen config: {e}")
            return False

    def _on_visit_repo_clicked(self, button):
        """Open the GitHub repository in browser."""
        # Use xdg-open to open the URL
        try:
            subprocess.Popen(["xdg-open", "https://github.com/ProcheRAR/SwwwGUI"])
        except Exception as e:
            logger.error(f"Failed to open URL: {e}")
            # Show error toast
            toast = Adw.Toast.new(self.application.translator.translate("error"))
            toast.set_timeout(2)
            self.add_toast(toast)
