import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class EffectsPanel(Gtk.Box):
    """Panel for configuring wallpaper transition effects and image settings."""
    
    def __init__(self, parent_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.parent_window = parent_window
        self.swww_manager = parent_window.swww_manager
        self.translator = parent_window.application.translator
        
        # Create view stack for organizing settings
        self.stack = Adw.ViewStack()
        self.stack.set_vexpand(True)
        
        # Setup UI components
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components."""
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_vexpand(True)
        
        # Create switcher bar
        switcher = Adw.ViewSwitcherBar()
        switcher.set_stack(self.stack)
        switcher.set_reveal(True)
        self.switcher = switcher  # Сохраняем ссылку для обновления локализации
        
        # Add stack
        self.append(self.stack)
        
        # Add switcher at the bottom
        self.append(switcher)
        
        # Add pages
        self.setup_transition_tab()
        self.setup_image_tab()
        self.setup_advanced_tab()
    
    def setup_transition_tab(self):
        """Set up the transition effects tab."""
        # Create scrolled window for tab content
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        # Main container for transition tab
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        scroll.set_child(box)
        
        # Create the preferences group
        title = "Эффекты" if self.translator.get_current_language() == "ru" else "Effects"
        group = Adw.PreferencesGroup(title=title)
        box.append(group)
        
        # Transition type
        transition_row = Adw.ComboRow()
        transition_row.set_title(self.translator.translate("transition_type"))
        
        # Create string list for transition types
        transitions = self.swww_manager.get_transitions()
        string_list = Gtk.StringList()
        
        # Прямое задание переводов для типов переходов
        translations = {
            "none": "Нет" if self.translator.get_current_language() == "ru" else "None",
            "simple": "Простой" if self.translator.get_current_language() == "ru" else "Simple",
            "fade": "Затухание" if self.translator.get_current_language() == "ru" else "Fade",
            "left": "Слева" if self.translator.get_current_language() == "ru" else "Left",
            "right": "Справа" if self.translator.get_current_language() == "ru" else "Right",
            "top": "Сверху" if self.translator.get_current_language() == "ru" else "Top",
            "bottom": "Снизу" if self.translator.get_current_language() == "ru" else "Bottom",
            "wipe": "Вытирание" if self.translator.get_current_language() == "ru" else "Wipe",
            "wave": "Волна" if self.translator.get_current_language() == "ru" else "Wave",
            "grow": "Рост" if self.translator.get_current_language() == "ru" else "Grow",
            "center": "Центр" if self.translator.get_current_language() == "ru" else "Center",
            "any": "Любая позиция" if self.translator.get_current_language() == "ru" else "Any Position",
            "outer": "Снаружи" if self.translator.get_current_language() == "ru" else "Outer",
            "random": "Случайный" if self.translator.get_current_language() == "ru" else "Random"
        }
        
        for transition in transitions:
            string_list.append(translations.get(transition, transition))
        
        transition_row.set_model(string_list)
        transition_row.set_selected(1)  # Default to 'simple'
        self.transition_type_row = transition_row
        self.transition_types = transitions  # Сохраняем исходные значения
        self.transition_translations = translations  # Сохраняем переводы
        group.add(transition_row)
        
        # Transition step
        step_row = Adw.SpinRow.new_with_range(1, 255, 1)
        step_row.set_title(self.translator.translate("transition_step"))
        step_row.set_value(2)  # Default value
        self.transition_step_row = step_row
        group.add(step_row)
        
        # Transition FPS
        fps_row = Adw.SpinRow.new_with_range(1, 255, 1)
        fps_row.set_title(self.translator.translate("transition_fps"))
        fps_row.set_value(30)  # Default value
        self.transition_fps_row = fps_row
        group.add(fps_row)
        
        # Transition duration
        duration_row = Adw.SpinRow.new_with_range(0.1, 10.0, 0.1)
        duration_row.set_title(self.translator.translate("transition_duration"))
        duration_row.set_value(3.0)  # Default value
        self.transition_duration_row = duration_row
        group.add(duration_row)
        
        # Add page to stack with icon
        title = "Переходы" if self.translator.get_current_language() == "ru" else "Transition"
        self.stack.add_titled_with_icon(scroll, "transitions", title, "view-refresh-symbolic")
        
        # Connect signals
        self.transition_type_row.connect("notify::selected", self.on_transition_changed)
    
    def setup_image_tab(self):
        """Set up the image settings tab."""
        # Create scrolled window for tab content
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        # Main container for image tab
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        scroll.set_child(box)
        
        # Create the preferences group
        title = "Размер изображения" if self.translator.get_current_language() == "ru" else "Resize"
        group = Adw.PreferencesGroup(title=title)
        box.append(group)
        
        # Resize mode
        resize_row = Adw.ComboRow()
        resize_row.set_title(self.translator.translate("resize_mode"))
        
        # Create string list for resize modes
        resize_modes = self.swww_manager.get_resize_modes()
        string_list = Gtk.StringList()
        
        # Прямое задание переводов для режимов изменения размера
        resize_translations = {
            "crop": "Обрезать" if self.translator.get_current_language() == "ru" else "Crop",
            "fit": "Подогнать" if self.translator.get_current_language() == "ru" else "Fit",
            "no": "Нет" if self.translator.get_current_language() == "ru" else "No"
        }
        
        for mode in resize_modes:
            string_list.append(resize_translations.get(mode, mode))
        
        resize_row.set_model(string_list)
        resize_row.set_selected(0)  # Default to 'crop'
        self.resize_mode_row = resize_row
        self.resize_modes = resize_modes  # Сохраняем исходные значения
        self.resize_translations = resize_translations  # Сохраняем переводы
        group.add(resize_row)
        
        # Fill color - using ActionRow with Entry since EntryRow doesn't support subtitle
        fill_row = Adw.ActionRow()
        fill_row.set_title(self.translator.translate("fill_color"))
        
        # Create entry widget
        fill_entry = Gtk.Entry()
        fill_entry.set_text("000000")  # Default black
        fill_entry.set_valign(Gtk.Align.CENTER)
        fill_entry.set_max_width_chars(10)
        fill_entry.set_hexpand(False)
        fill_row.add_suffix(fill_entry)
        
        self.fill_color_entry = fill_entry
        group.add(fill_row)
        
        # Scaling filter
        filter_row = Adw.ComboRow()
        filter_title = "Фильтр" if self.translator.get_current_language() == "ru" else "Filter"
        filter_row.set_title(filter_title)
        
        # Create string list for filters
        filters = self.swww_manager.get_filters()
        string_list = Gtk.StringList()
        
        # Оставляем только оригинальные технические обозначения фильтров
        filter_translations = {
            "Nearest": "Nearest",
            "Bilinear": "Bilinear",
            "CatmullRom": "CatmullRom",
            "Mitchell": "Mitchell",
            "Lanczos3": "Lanczos3"
        }
        
        for filter_name in filters:
            string_list.append(filter_translations.get(filter_name, filter_name))
        
        filter_row.set_model(string_list)
        filter_row.set_selected(4)  # Default to 'Lanczos3'
        self.filter_row = filter_row
        self.filters = filters  # Сохраняем исходные значения
        self.filter_translations = filter_translations  # Сохраняем переводы
        group.add(filter_row)
        
        # Add page to stack with icon
        title = "Размер" if self.translator.get_current_language() == "ru" else "Resize"
        self.stack.add_titled_with_icon(scroll, "image", title, "image-x-generic-symbolic")
    
    def setup_advanced_tab(self):
        """Set up the advanced settings tab."""
        # Create scrolled window for tab content
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        # Main container for advanced tab
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        scroll.set_child(box)
        
        # Create the preferences group for wipe/wave settings
        title = "Дополнительные настройки" if self.translator.get_current_language() == "ru" else "Advanced Settings"
        wipe_group = Adw.PreferencesGroup(title=title)
        box.append(wipe_group)
        
        # Transition angle
        angle_row = Adw.SpinRow.new_with_range(0, 359, 1)
        angle_row.set_title(self.translator.translate("transition_angle"))
        angle_row.set_value(45)  # Default value
        self.transition_angle_row = angle_row
        wipe_group.add(angle_row)
        
        # Wave dimensions (for wave transition)
        wave_row = Adw.ActionRow()
        wave_title = "Размеры волны (x,y)" if self.translator.get_current_language() == "ru" else "Wave Dimensions (x,y)"
        wave_row.set_title(wave_title)
        
        # Create entry widget
        wave_entry = Gtk.Entry()
        wave_entry.set_text("20,20")  # Default value
        wave_entry.set_valign(Gtk.Align.CENTER)
        wave_entry.set_max_width_chars(10)
        wave_entry.set_hexpand(False)
        wave_row.add_suffix(wave_entry)
        
        self.transition_wave_entry = wave_entry
        wipe_group.add(wave_row)
        
        # Create the preferences group for grow/outer settings
        position_title = "Положение перехода" if self.translator.get_current_language() == "ru" else "Transition Position"
        grow_group = Adw.PreferencesGroup(title=position_title)
        box.append(grow_group)
        
        # Transition position
        position_row = Adw.ComboRow()
        position_row.set_title(self.translator.translate("transition_position"))
        
        # Create string list for positions
        positions = ["center", "top", "left", "right", "bottom", 
                     "top-left", "top-right", "bottom-left", "bottom-right"]
        string_list = Gtk.StringList()
        
        # Прямое задание переводов для позиций
        position_translations = {
            "center": "Центр" if self.translator.get_current_language() == "ru" else "Center",
            "top": "Верх" if self.translator.get_current_language() == "ru" else "Top",
            "left": "Лево" if self.translator.get_current_language() == "ru" else "Left",
            "right": "Право" if self.translator.get_current_language() == "ru" else "Right",
            "bottom": "Низ" if self.translator.get_current_language() == "ru" else "Bottom",
            "top-left": "Верх-Лево" if self.translator.get_current_language() == "ru" else "Top-Left",
            "top-right": "Верх-Право" if self.translator.get_current_language() == "ru" else "Top-Right",
            "bottom-left": "Низ-Лево" if self.translator.get_current_language() == "ru" else "Bottom-Left",
            "bottom-right": "Низ-Право" if self.translator.get_current_language() == "ru" else "Bottom-Right"
        }
        
        for pos in positions:
            string_list.append(position_translations.get(pos, pos))
        
        position_row.set_model(string_list)
        position_row.set_selected(0)  # Default to 'center'
        self.transition_pos_row = position_row
        self.positions = positions  # Сохраняем исходные значения
        self.position_translations = position_translations  # Сохраняем переводы
        grow_group.add(position_row)
        
        # Invert Y
        invert_y_row = Adw.SwitchRow()
        invert_y_row.set_title(self.translator.translate("invert_y"))
        self.invert_y_row = invert_y_row
        grow_group.add(invert_y_row)
        
        # Transition Bezier
        bezier_row = Adw.ActionRow()
        bezier_title = "Кривая Безье" if self.translator.get_current_language() == "ru" else "Bezier Curve"
        bezier_row.set_title(bezier_title)
        
        # Create entry widget
        bezier_entry = Gtk.Entry()
        bezier_entry.set_text(".54,0,.34,.99")  # Default value
        bezier_entry.set_valign(Gtk.Align.CENTER)
        bezier_entry.set_max_width_chars(15)
        bezier_entry.set_hexpand(False)
        bezier_row.add_suffix(bezier_entry)
        
        self.transition_bezier_entry = bezier_entry
        grow_group.add(bezier_row)
        
        # Add page to stack with icon 
        title = self.translator.translate("advanced")
        self.stack.add_titled_with_icon(scroll, "advanced", title, "preferences-other-symbolic")
        
    def on_transition_changed(self, row, pspec):
        """Handle transition type change."""
        transition_type = self.get_transition_type()
        
        # Update step value based on transition type
        if transition_type == "simple":
            self.transition_step_row.set_value(2)
        else:
            # For other transitions, 90 is swww's default
            self.transition_step_row.set_value(90)
    
    def get_all_options(self):
        """Get all options as a dictionary to pass to SwwwManager."""
        options = {}
        
        # Basic transition options
        options['transition_type'] = self.get_transition_type()
        options['transition_step'] = self.get_transition_step()
        options['transition_fps'] = self.get_transition_fps()
        options['transition_duration'] = self.get_transition_duration()
        
        # Image options
        options['resize_mode'] = self.get_resize_mode()
        options['fill_color'] = self.get_fill_color()
        options['filter'] = self.get_filter()
        
        # Advanced options based on transition type
        transition_type = options['transition_type']
        
        # Add wipe/wave specific options
        if transition_type in ['wipe', 'wave']:
            options['transition_angle'] = self.get_transition_angle()
            
            if transition_type == 'wave':
                options['transition_wave'] = self.get_transition_wave()
        
        # Add grow/outer specific options
        if transition_type in ['grow', 'outer', 'center', 'any']:
            options['transition_pos'] = self.get_transition_position()
            options['invert_y'] = self.get_invert_y()
        
        # Add fade specific options
        if transition_type == 'fade':
            options['transition_bezier'] = self.get_transition_bezier()
        
        return options
    
    # Basic transition getters and setters
    def get_transition_type(self):
        """Get the selected transition type."""
        selected = self.transition_type_row.get_selected()
        if 0 <= selected < len(self.transition_types):
            return self.transition_types[selected]
        return "simple"
    
    def set_transition_type(self, transition_type):
        """Set the selected transition type."""
        transitions = self.swww_manager.get_transitions()
        if transition_type in transitions:
            index = transitions.index(transition_type)
            self.transition_type_row.set_selected(index)
    
    def get_transition_step(self):
        """Get the transition step value."""
        return int(self.transition_step_row.get_value())
    
    def set_transition_step(self, step):
        """Set the transition step value."""
        self.transition_step_row.set_value(int(step))
    
    def get_transition_fps(self):
        """Get the transition FPS value."""
        return int(self.transition_fps_row.get_value())
    
    def set_transition_fps(self, fps):
        """Set the transition FPS value."""
        self.transition_fps_row.set_value(int(fps))
        
    def get_transition_duration(self):
        """Get the transition duration value."""
        return float(self.transition_duration_row.get_value())
    
    def set_transition_duration(self, duration):
        """Set the transition duration value."""
        self.transition_duration_row.set_value(float(duration))
    
    # Image settings getters and setters
    def get_resize_mode(self):
        """Get the selected resize mode."""
        selected = self.resize_mode_row.get_selected()
        if 0 <= selected < len(self.resize_modes):
            return self.resize_modes[selected]
        return "crop"
    
    def set_resize_mode(self, resize_mode):
        """Set the selected resize mode."""
        resize_modes = self.swww_manager.get_resize_modes()
        if resize_mode in resize_modes:
            index = resize_modes.index(resize_mode)
            self.resize_mode_row.set_selected(index)
    
    def get_fill_color(self):
        """Get the fill color value."""
        return self.fill_color_entry.get_text()
    
    def set_fill_color(self, color):
        """Set the fill color value."""
        self.fill_color_entry.set_text(color)
    
    def get_filter(self):
        """Get the selected filter type."""
        selected = self.filter_row.get_selected()
        if 0 <= selected < len(self.filters):
            return self.filters[selected]
        return "Lanczos3"
    
    def set_filter(self, filter_name):
        """Set the selected filter."""
        filters = self.swww_manager.get_filters()
        if filter_name in filters:
            index = filters.index(filter_name)
            self.filter_row.set_selected(index)
    
    # Advanced settings getters and setters
    def get_transition_angle(self):
        """Get the transition angle value."""
        return int(self.transition_angle_row.get_value())
    
    def set_transition_angle(self, angle):
        """Set the transition angle value."""
        self.transition_angle_row.set_value(int(angle))
    
    def get_transition_wave(self):
        """Get the transition wave dimensions."""
        return self.transition_wave_entry.get_text()
    
    def set_transition_wave(self, wave):
        """Set the transition wave dimensions."""
        self.transition_wave_entry.set_text(wave)
    
    def get_transition_position(self):
        """Get the selected transition position."""
        selected = self.transition_pos_row.get_selected()
        if 0 <= selected < len(self.positions):
            return self.positions[selected]
        return "center"
    
    def set_transition_position(self, position):
        """Set the selected transition position."""
        positions = ["center", "top", "left", "right", "bottom", 
                    "top-left", "top-right", "bottom-left", "bottom-right"]
        if position in positions:
            index = positions.index(position)
            self.transition_pos_row.set_selected(index)
    
    def get_invert_y(self):
        """Get whether to invert Y position."""
        return self.invert_y_row.get_active()
    
    def set_invert_y(self, invert):
        """Set whether to invert Y position."""
        self.invert_y_row.set_active(invert)
    
    def get_transition_bezier(self):
        """Get the transition bezier curve."""
        return self.transition_bezier_entry.get_text()
    
    def set_transition_bezier(self, bezier):
        """Set the transition bezier curve."""
        self.transition_bezier_entry.set_text(bezier)

    def update_localization(self):
        """Update the UI with the current language."""
        # Сохраняем текущую страницу
        current_visible = self.stack.get_visible_child_name()
        
        # Удаляем все страницы из стека
        for name in ["transitions", "image", "advanced"]:
            child = self.stack.get_child_by_name(name)
            if child:
                self.stack.remove(child)
                
        # Заново создаем все вкладки с правильными переводами
        self.setup_transition_tab()
        self.setup_image_tab()
        self.setup_advanced_tab()
        
        # Восстанавливаем выбранную страницу
        if current_visible:
            child = self.stack.get_child_by_name(current_visible)
            if child:
                self.stack.set_visible_child(child)
        
        # Обновляем переключатель
        if hasattr(self, 'switcher'):
            self.switcher.set_stack(None)
            self.switcher.set_stack(self.stack)
            
        # Обновляем заголовки строк
        self.transition_type_row.set_title(self.translator.translate("transition_type"))
        self.transition_step_row.set_title(self.translator.translate("transition_step"))
        self.transition_fps_row.set_title(self.translator.translate("transition_fps"))
        self.transition_duration_row.set_title(self.translator.translate("transition_duration"))
        
        self.resize_mode_row.set_title(self.translator.translate("resize_mode"))
        self.filter_row.set_title(self.translator.translate("filter"))
        
        # Get parent elements for fill color and wave settings
        fill_parent = self.fill_color_entry.get_parent()
        if isinstance(fill_parent, Adw.ActionRow):
            fill_parent.set_title(self.translator.translate("fill_color"))
        
        wave_parent = self.transition_wave_entry.get_parent()
        if isinstance(wave_parent, Adw.ActionRow):
            wave_parent.set_title(self.translator.translate("transition_wave"))
        
        bezier_parent = self.transition_bezier_entry.get_parent()
        if isinstance(bezier_parent, Adw.ActionRow):
            bezier_parent.set_title(self.translator.translate("transition_bezier"))
        
        self.transition_angle_row.set_title(self.translator.translate("transition_angle"))
        self.transition_pos_row.set_title(self.translator.translate("transition_position"))
        self.invert_y_row.set_title(self.translator.translate("invert_y"))
        
        # Обновляем переводы для элементов выпадающих списков
        # Transition types
        string_list = Gtk.StringList()
        for transition in self.transition_types:
            string_list.append(self.transition_translations.get(transition, transition))
        
        current_selected = self.transition_type_row.get_selected()
        self.transition_type_row.set_model(string_list)
        self.transition_type_row.set_selected(current_selected)
        
        # Resize modes
        string_list = Gtk.StringList()
        for mode in self.resize_modes:
            string_list.append(self.resize_translations.get(mode, mode))
        
        current_selected = self.resize_mode_row.get_selected()
        self.resize_mode_row.set_model(string_list)
        self.resize_mode_row.set_selected(current_selected)
        
        # Filters
        string_list = Gtk.StringList()
        for filter_name in self.filters:
            string_list.append(self.filter_translations.get(filter_name, filter_name))
        
        current_selected = self.filter_row.get_selected()
        self.filter_row.set_model(string_list)
        self.filter_row.set_selected(current_selected)
