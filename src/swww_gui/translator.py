import os
import json
from pathlib import Path
import locale
import logging

logger = logging.getLogger(__name__)

class Translator:
    """A translator for the application."""
    
    def __init__(self):
        """Initialize the translator."""
        self.translations = {}
        self.current_language = "en"  # Default language
        self.language_names = {"en": "English", "ru": "Русский"}  # Cache language names
        
        # Load translations
        self._load_translations()
        
        # Set default language from system locale
        self._set_language_from_locale()
    
    def _load_translations(self):
        """Load all available translations."""
        # Hard-coded translations for better performance
        self.translations = {
            "en": {
                "app_title": "SwwwGui",
                "app_subtitle": "Wayland Wallpaper Tool",
                "settings": "Settings",
                "language": "Language",
                "language_settings": "Language",
                "theme_settings": "Theme",
                "theme": "Theme",
                "system": "System",
                "light": "Light",
                "dark": "Dark",
                "apply": "Apply",
                "preview": "Preview",
                "error": "Error",
                "ok": "OK",
                "cancel": "Cancel",
                "daemon_not_running": "swww-daemon not running",
                "daemon_start_question": "swww-daemon is not running. Do you want to start it now?",
                "start_daemon": "Start daemon",
                "daemon_start_failed": "Failed to start swww-daemon.",
                "wallpaper_applied": "Wallpaper applied successfully!",
                "wallpaper_set_failed": "Failed to set wallpaper.",
                "preview_applied": "Preview applied",
                "preview_failed": "Failed to apply preview",
                "search_placeholder": "Search wallpapers...",
                "effects": "Effects",
                "transition": "Transition",
                "transition_type": "Transition Type",
                "transition_step": "Transition Step",
                "transition_fps": "Transition FPS",
                "transition_duration": "Duration (seconds)",
                "resize": "Resize",
                "resize_mode": "Resize Mode",
                "crop": "Crop",
                "fit": "Fit",
                "none": "None",
                "fill_color": "Fill Color",
                "filter": "Filter",
                "advanced": "Advanced Settings",
                "transition_angle": "Transition Angle",
                "transition_wave": "Transition Wave (x,y)",
                "transition_position": "Transition Position",
                "invert_y": "Invert Y",
                "transition_bezier": "Transition Bezier",
                "language_change_restart": "Some changes will take full effect after restart.",
                
                # Transition types
                "simple": "Simple",
                "wipe": "Wipe",
                "center": "Center",
                "outer": "Outer",
                "wave": "Wave",
                "grow": "Grow",
                "any": "Any Position",
                "fade": "Fade",
                "left": "Left",
                "right": "Right",
                "top": "Top",
                "bottom": "Bottom",
                "none": "None",
                "random": "Random",
                
                # Filter types
                "Nearest": "Nearest",
                "Bilinear": "Bilinear",
                "CatmullRom": "Catmull-Rom",
                "Mitchell": "Mitchell",
                "Lanczos3": "Lanczos3",
                
                # Material You options
                "matugen_settings": "Material You",
                "matugen_integration": "Material You Integration",
                "use_matugen": "Use Matugen Theme",
                "matugen_description": "Generate Material You theme based on wallpaper",
                "matugen_enabled": "Material You theme generation enabled",
                
                # About dialog
                "about": "About",
                "version": "Version",
                "github_repo": "GitHub Repository",
                "visit_repo": "Visit Repository",
                "reset_settings": "Reset settings to defaults",
                "settings_reset": "Settings reset to defaults",
                
                # Image view
                "maximize_view": "Maximize view",
                "maximized_view": "Maximized view",
                "normal_view": "Normal view"
            },
            "ru": {
                "app_title": "SwwwGui",
                "app_subtitle": "Менеджер обоев для Wayland",
                "settings": "Настройки",
                "language": "Язык",
                "language_settings": "Язык",
                "theme_settings": "Тема",
                "theme": "Тема",
                "system": "Системная",
                "light": "Светлая",
                "dark": "Темная",
                "apply": "Применить",
                "preview": "Просмотр",
                "error": "Ошибка",
                "ok": "OK",
                "cancel": "Отмена",
                "daemon_not_running": "swww-daemon не запущен",
                "daemon_start_question": "swww-daemon не запущен. Запустить его сейчас?",
                "start_daemon": "Запустить демон",
                "daemon_start_failed": "Не удалось запустить swww-daemon.",
                "wallpaper_applied": "Обои успешно применены!",
                "wallpaper_set_failed": "Не удалось установить обои.",
                "preview_applied": "Предпросмотр применен",
                "preview_failed": "Не удалось применить предпросмотр",
                "search_placeholder": "Поиск обоев...",
                "effects": "Эффекты",
                "transition": "Переходы",
                "transition_type": "Тип перехода",
                "transition_step": "Шаг перехода",
                "transition_fps": "FPS перехода",
                "transition_duration": "Длительность (секунды)",
                "resize": "Размер",
                "resize_mode": "Режим изменения",
                "crop": "Обрезать",
                "fit": "Подогнать",
                "none": "Нет",
                "fill_color": "Цвет заполнения",
                "filter": "Фильтр",
                "advanced": "Дополнительные настройки",
                "transition_angle": "Угол перехода",
                "transition_wave": "Волна перехода (x,y)",
                "transition_position": "Позиция перехода",
                "invert_y": "Инвертировать Y",
                "transition_bezier": "Кривая Безье",
                "language_change_restart": "Некоторые изменения вступят в силу после перезапуска.",
                
                # Transition types
                "simple": "Простой",
                "wipe": "Вытирание",
                "center": "Центр",
                "outer": "Снаружи",
                "wave": "Волна",
                "grow": "Рост",
                "any": "Любая позиция",
                "fade": "Затухание",
                "left": "Слева",
                "right": "Справа",
                "top": "Сверху",
                "bottom": "Снизу",
                "none": "Нет",
                "random": "Случайный",
                
                # Filter types
                "Nearest": "Ближайший",
                "Bilinear": "Билинейный",
                "CatmullRom": "Кэтмулл-Ром",
                "Mitchell": "Митчелл",
                "Lanczos3": "Ланцош3",
                
                # Material You options
                "matugen_settings": "Material You",
                "matugen_integration": "Интеграция Matugen",
                "use_matugen": "Использовать Matugen",
                "matugen_description": "Генерировать тему Material You на основе обоев",
                "matugen_enabled": "Генерация тем Material You включена",
                
                # About dialog
                "about": "О Программе",
                "version": "Версия",
                "github_repo": "Репозиторий GitHub",
                "visit_repo": "Перейти в репозиторий",
                "reset_settings": "Сбросить настройки",
                "settings_reset": "Настройки сброшены",
                
                # Image view
                "maximize_view": "Увеличить просмотр",
                "maximized_view": "Просмотр увеличен",
                "normal_view": "Обычный просмотр"
            }
        }
    
    def _set_language_from_locale(self):
        """Set language based on system locale."""
        try:
            # Get system locale
            loc = locale.getlocale()[0]
            if loc:
                # Extract language code
                lang_code = loc.split('_')[0]
                # If it's a supported language, use it
                if lang_code in self.translations:
                    self.current_language = lang_code
                    logger.debug(f"Using system language: {lang_code}")
        except Exception as e:
            # Fall back to English on error
            logger.debug(f"Error detecting system locale, falling back to English: {e}")
            self.current_language = "en"
    
    def translate(self, key):
        """Translate a string."""
        # Get translation dictionary for current language
        lang_dict = self.translations.get(self.current_language, {})
        
        # Try current language first
        if key in lang_dict:
            return lang_dict[key]
        
        # Try English as fallback
        if self.current_language != "en":
            en_dict = self.translations.get("en", {})
            if key in en_dict:
                return en_dict[key]
        
        # Last resort: return the key itself
        return key
    
    def get_supported_languages(self):
        """Return list of supported languages."""
        languages = []
        for code in self.translations:
            languages.append({
                "code": code,
                "name": self.language_names.get(code, code)
            })
        
        return languages
    
    def get_current_language(self):
        """Get the current language code."""
        return self.current_language
    
    def set_language(self, lang_code):
        """Set the current language."""
        if lang_code in self.translations:
            self.current_language = lang_code
            logger.debug(f"Language set to: {lang_code}")
            return True
        logger.warning(f"Unsupported language: {lang_code}")
        return False 