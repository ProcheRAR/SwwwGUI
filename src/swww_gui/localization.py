"""Localization support for SwwwGui."""

# Dictionary with translations
TRANSLATIONS = {
    "en": {
        # General UI
        "app_title": "SwwwGui",
        "app_subtitle": "Wayland Wallpaper Manager",
        "settings": "Settings",
        "apply": "Apply",
        "preview": "Preview",
        "search_placeholder": "Search images...",
        "cancel": "Cancel",
        "ok": "OK",
        "error": "Error",
        "start_daemon": "Start Daemon",
        
        # Messages
        "wallpaper_applied": "Wallpaper applied successfully",
        "preview_applied": "Preview applied",
        "settings_not_implemented": "Settings not yet implemented",
        "daemon_not_running": "swww daemon not running",
        "daemon_start_question": "The swww-daemon is not running. Would you like to start it now?",
        "daemon_start_failed": "Failed to start swww-daemon. Please check if swww is installed correctly.",
        "wallpaper_set_failed": "Failed to set wallpaper. Please check if swww-daemon is running.",
        "preview_failed": "Failed to preview wallpaper. Please check if swww-daemon is running.",
        "no_images_found": "No images found in this folder",
        "loading": "Loading...",
        "error_loading_folder": "Error loading folder",
        
        # Settings
        "language_settings": "Language Settings",
        "language": "Language",
        "language_change_restart": "Language changed. The application needs to be restarted for changes to take effect.",
        "theme_settings": "Theme Settings",
        "theme": "Theme",
        "system": "System",
        "light": "Light",
        "dark": "Dark",
        "startup_folder": "Startup Folder",
        "select_folder": "Select Folder",
        "open_folder": "Open Folder",
        
        # Tabs
        "transitions": "Transitions",
        "image": "Image",
        "advanced": "Advanced",
        
        # Transitions tab
        "transition_effects": "Transition Effects",
        "transition_type": "Transition Type",
        "transition_type_subtitle": "Effect when changing wallpaper",
        "transition_step": "Transition Step",
        "transition_step_subtitle": "Smaller values = smoother transition",
        "transition_fps": "Transition FPS",
        "transition_fps_subtitle": "Frames per second during transition",
        "transition_duration": "Transition Duration",
        "transition_duration_subtitle": "Duration in seconds (not used with 'simple')",
        
        # Image tab
        "image_settings": "Image Settings",
        "resize_mode": "Resize Mode",
        "resize_mode_subtitle": "How to resize the image to fit the screen",
        "fill_color": "Fill Color",
        "fill_color_subtitle": "Hex color (RRGGBB) for padding when image doesn't fill screen",
        "scaling_filter": "Scaling Filter",
        "scaling_filter_subtitle": "Filter to use when scaling images",
        
        # Advanced tab
        "wipe_wave_settings": "Wipe and Wave Settings",
        "transition_angle": "Transition Angle",
        "transition_angle_subtitle": "Angle for wipe/wave transitions (0-359 degrees)",
        "wave_dimensions": "Wave Dimensions",
        "wave_dimensions_subtitle": "Width,Height for wave transition (e.g., 20,20)",
        "grow_outer_settings": "Grow and Outer Settings",
        "transition_position": "Transition Position",
        "transition_position_subtitle": "Position for grow/outer transitions",
        "invert_y": "Invert Y Position",
        "invert_y_subtitle": "Invert the Y position for transitions",
        "fade_settings": "Fade Settings",
        "bezier_curve": "Bezier Curve",
        "bezier_curve_subtitle": "Control points for fade transition (e.g., .54,0,.34,.99)"
    },
    
    "ru": {
        # General UI
        "app_title": "SwwwGui",
        "app_subtitle": "Менеджер обоев для Wayland",
        "settings": "Настройки",
        "apply": "Применить",
        "preview": "Предпросмотр",
        "search_placeholder": "Поиск изображений...",
        "cancel": "Отмена",
        "ok": "OK",
        "error": "Ошибка",
        "start_daemon": "Запустить демон",
        
        # Messages
        "wallpaper_applied": "Обои успешно применены",
        "preview_applied": "Предпросмотр применен",
        "settings_not_implemented": "Настройки ещё не реализованы",
        "daemon_not_running": "Демон swww не запущен",
        "daemon_start_question": "Демон swww-daemon не запущен. Хотите запустить его сейчас?",
        "daemon_start_failed": "Не удалось запустить swww-daemon. Пожалуйста, проверьте, правильно ли установлен swww.",
        "wallpaper_set_failed": "Не удалось установить обои. Пожалуйста, проверьте, запущен ли swww-daemon.",
        "preview_failed": "Не удалось выполнить предпросмотр обоев. Пожалуйста, проверьте, запущен ли swww-daemon.",
        "no_images_found": "В этой папке не найдено изображений",
        "loading": "Загрузка...",
        "error_loading_folder": "Ошибка загрузки папки",
        
        # Settings
        "language_settings": "Настройки языка",
        "language": "Язык",
        "language_change_restart": "Язык изменен. Для применения изменений необходимо перезапустить приложение.",
        "theme_settings": "Настройки темы",
        "theme": "Тема",
        "system": "Системная",
        "light": "Светлая",
        "dark": "Тёмная",
        "startup_folder": "Папка запуска",
        "select_folder": "Выбрать папку",
        "open_folder": "Открыть папку",
        
        # Tabs
        "transitions": "Переходы",
        "image": "Изображение",
        "advanced": "Дополнительно",
        
        # Transitions tab
        "transition_effects": "Эффекты перехода",
        "transition_type": "Тип перехода",
        "transition_type_subtitle": "Эффект при смене обоев",
        "transition_step": "Шаг перехода",
        "transition_step_subtitle": "Меньшие значения = более плавный переход",
        "transition_fps": "FPS перехода",
        "transition_fps_subtitle": "Кадров в секунду во время перехода",
        "transition_duration": "Длительность перехода",
        "transition_duration_subtitle": "Длительность в секундах (не используется с 'simple')",
        
        # Image tab
        "image_settings": "Настройки изображения",
        "resize_mode": "Режим изменения размера",
        "resize_mode_subtitle": "Как изменить размер изображения для соответствия экрану",
        "fill_color": "Цвет заливки",
        "fill_color_subtitle": "Цвет в формате HEX (RRGGBB) для заливки, когда изображение не заполняет экран",
        "scaling_filter": "Фильтр масштабирования",
        "scaling_filter_subtitle": "Фильтр для масштабирования изображений",
        
        # Advanced tab
        "wipe_wave_settings": "Настройки Wipe и Wave",
        "transition_angle": "Угол перехода",
        "transition_angle_subtitle": "Угол для переходов wipe/wave (0-359 градусов)",
        "wave_dimensions": "Размеры волны",
        "wave_dimensions_subtitle": "Ширина,Высота для перехода wave (напр., 20,20)",
        "grow_outer_settings": "Настройки Grow и Outer",
        "transition_position": "Положение перехода",
        "transition_position_subtitle": "Положение для переходов grow/outer",
        "invert_y": "Инвертировать положение Y",
        "invert_y_subtitle": "Инвертировать положение Y для переходов",
        "fade_settings": "Настройки Fade",
        "bezier_curve": "Кривая Безье",
        "bezier_curve_subtitle": "Контрольные точки для перехода fade (напр., .54,0,.34,.99)"
    }
}

class Translator:
    """Translator class for SwwwGui."""
    
    def __init__(self, config):
        """Initialize the translator with a config object."""
        self.config = config
        self.current_language = config.get('language', 'en')
        
    def translate(self, key):
        """Translate a key to the current language."""
        if key in TRANSLATIONS.get(self.current_language, {}):
            return TRANSLATIONS[self.current_language][key]
        elif key in TRANSLATIONS["en"]:
            return TRANSLATIONS["en"][key]  # Fallback to English
        else:
            return key  # If translation not found, return the key itself
    
    def set_language(self, language_code):
        """Set the current language."""
        if language_code in TRANSLATIONS:
            self.current_language = language_code
            self.config.set('language', language_code)
            self.config.save()
            return True
        return False
    
    def get_current_language(self):
        """Get the current language code."""
        return self.current_language
    
    def get_supported_languages(self):
        """Get a list of supported languages."""
        return self.config.get_supported_languages()
        
# Create a short alias for translate function
def _(key, translator):
    """Shorthand function for translation."""
    return translator.translate(key) 