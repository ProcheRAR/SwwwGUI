import os
import json
from pathlib import Path
import locale
import logging

logger = logging.getLogger(__name__)

class Translator:
    """A translator for the application.
    
    This class loads translations from JSON files in the translations directory,
    making it easy for users to add new translations without modifying the code.
    """
    
    def __init__(self):
        """Initialize the translator."""
        self.translations = {}
        self.current_language = "en"  # Default language
        self.language_names = {}  # Will be populated from translation files
        
        # Load translations
        self._load_translations()
        
        # Set default language from system locale
        self._set_language_from_locale()
    
    def _get_translations_dir(self):
        """Get the path to the translations directory."""
        # User config directory should be the primary location for translations
        user_config_dir = Path.home() / '.config' / 'swww-gui' / 'translations'
        
        # Create the directory if it doesn't exist
        os.makedirs(user_config_dir, exist_ok=True)
        
        # Always return the user config directory
        return user_config_dir
    
    def _load_translations(self):
        """Load all available translations from JSON files."""
        translations_dir = self._get_translations_dir()
        logger.debug(f"Loading translations from {translations_dir}")
        
        # First, ensure we have at least English and Russian
        self._ensure_default_translations(translations_dir)
        
        # Load all JSON files in the translations directory
        for file_path in translations_dir.glob('*.json'):
            # Skip the template file
            if file_path.stem.lower() == 'template':
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Extract language code from filename (e.g., "en.json" -> "en")
                lang_code = file_path.stem
                
                # Store the translations
                if isinstance(data, dict) and 'name' in data and 'translations' in data:
                    self.translations[lang_code] = data['translations']
                    self.language_names[lang_code] = data['name']
                    logger.debug(f"Loaded translations for {lang_code} ({data['name']})")
                else:
                    logger.warning(f"Invalid translation file format: {file_path}")
            except Exception as e:
                logger.error(f"Failed to load translation file {file_path}: {e}")
        
        # If no translations were loaded, use hardcoded fallback
        if not self.translations:
            logger.warning("No translation files found, using fallback translations")
            self._load_fallback_translations()
    
    def _ensure_default_translations(self, translations_dir):
        """Create default English and Russian translation files if they don't exist."""
        self._create_translation_file_if_not_exists(translations_dir / 'en.json', 'English', self._get_default_english())
        self._create_translation_file_if_not_exists(translations_dir / 'ru.json', 'Русский', self._get_default_russian())
    
    def _create_translation_file_if_not_exists(self, file_path, language_name, translations):
        """Create a translation file if it doesn't exist."""
        if not file_path.exists():
            try:
                data = {
                    'name': language_name,
                    'translations': translations
                }
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                logger.debug(f"Created default translation file: {file_path}")
            except Exception as e:
                logger.error(f"Failed to create translation file {file_path}: {e}")
    
    def _get_default_english(self):
        """Get default English translations."""
        return {
            # App
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
            
            # Effects
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
            "no": "No",
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
            "random": "Random",
            
            # Filter types
            "Nearest": "Nearest",
            "Bilinear": "Bilinear",
            "CatmullRom": "Catmull-Rom",
            "Mitchell": "Mitchell",
            "Lanczos3": "Lanczos3",
            
            # matugen options
            "matugen_settings": "matugen",
            "matugen_integration": "matugen Integration",
            "use_matugen": "Use matugen Theme",
            "matugen_description": "Generate matugen theme based on wallpaper",
            "matugen_enabled": "matugen theme generation enabled",
            
            # Position values for transitions
            "center": "Center",
            "top": "Top",
            "left": "Left",
            "right": "Right",
            "bottom": "Bottom",
            "top-left": "Top-Left",
            "top-right": "Top-Right",
            "bottom-left": "Bottom-Left",
            "bottom-right": "Bottom-Right",
            
            # About dialog
            "about": "About",
            "version": "Version",
            "github_repo": "GitHub Repository",
            "visit_repo": "Visit Repository",
            "reset_settings": "Reset Settings",
            "settings_reset": "Settings reset to defaults",
            "reset_settings_title": "Reset Settings",
            "reset_settings_confirmation": "Are you sure you want to reset all settings to default values?",
            "reset": "Reset",
            "settings_reset_success": "Settings reset successfully",
            "reset_transition_settings": "Reset transition settings",
            "reset_resize_settings": "Reset resize settings",
            "reset_advanced_settings": "Reset advanced settings",
            "transition_settings_reset": "Transition settings reset",
            "resize_settings_reset": "Resize settings reset",
            "advanced_settings_reset": "Advanced settings reset",
            "reset_all_settings": "Reset All Settings",
            
            # Image view
            "maximize_view": "Maximize view",
            "maximized_view": "Maximized view",
            "normal_view": "Normal view",
            
            # Wave dimensions 
            "wave_dimensions": "Wave Dimensions (x,y)",
            
            # Bezier curve
            "bezier_curve": "Bezier Curve",
            
            # Translation tools
            "translation_tools": "Translation Tools",
            "create_translation_template": "Create Translation Template",
            "create_template_description": "Create a template file for adding a new language",
            "template_created": "Template created at: {0}"
        }
    
    def _get_default_russian(self):
        """Get default Russian translations."""
        return {
            # App
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
            
            # Effects
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
            "no": "Нет",
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
            "random": "Случайный",
            
            # Filter types
            "Nearest": "Ближайший",
            "Bilinear": "Билинейный",
            "CatmullRom": "Кэтмулл-Ром",
            "Mitchell": "Митчелл",
            "Lanczos3": "Ланцош3",
            
            # matugen options
            "matugen_settings": "matugen",
            "matugen_integration": "Интеграция matugen",
            "use_matugen": "Использовать matugen",
            "matugen_description": "Генерировать тему matugen на основе обоев",
            "matugen_enabled": "Генерация тем matugen включена",
            
            # Position values for transitions
            "center": "Центр",
            "top": "Верх",
            "left": "Лево",
            "right": "Право",
            "bottom": "Низ",
            "top-left": "Верх-Лево",
            "top-right": "Верх-Право",
            "bottom-left": "Низ-Лево",
            "bottom-right": "Низ-Право",
            
            # About dialog
            "about": "О Программе",
            "version": "Версия",
            "github_repo": "Репозиторий GitHub",
            "visit_repo": "Перейти в репозиторий",
            "reset_settings": "Сбросить настройки",
            "settings_reset": "Настройки сброшены",
            "reset_settings_title": "Сбросить настройки",
            "reset_settings_confirmation": "Вы уверены, что хотите сбросить все настройки по умолчанию?",
            "reset": "Сбросить",
            "settings_reset_success": "Настройки успешно сброшены",
            "reset_transition_settings": "Сбросить настройки перехода",
            "reset_resize_settings": "Сбросить настройки изменения размера",
            "reset_advanced_settings": "Сбросить дополнительные настройки",
            "transition_settings_reset": "Настройки перехода сброшены",
            "resize_settings_reset": "Настройки изменения размера сброшены",
            "advanced_settings_reset": "Дополнительные настройки сброшены",
            "reset_all_settings": "Сбросить все настройки",
            
            # Image view
            "maximize_view": "Увеличить просмотр",
            "maximized_view": "Просмотр увеличен",
            "normal_view": "Обычный просмотр",
            
            # Wave dimensions 
            "wave_dimensions": "Размеры волны (x,y)",
            
            # Bezier curve
            "bezier_curve": "Кривая Безье",
            
            # Translation tools
            "translation_tools": "Инструменты перевода",
            "create_translation_template": "Создать шаблон перевода",
            "create_template_description": "Создать файл-шаблон для добавления нового языка",
            "template_created": "Шаблон создан: {0}"
        }
    
    def _load_fallback_translations(self):
        """Load fallback hardcoded translations."""
        logger.warning("Using fallback translations")
        self.translations = {
            "en": self._get_default_english(),
            "ru": self._get_default_russian()
        }
        self.language_names = {"en": "English", "ru": "Русский"}
    
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
        """Translate a string.
        
        Args:
            key: The translation key to look up
            
        Returns:
            str: The translated string, or the key itself if no translation found
        """
        # Get translation dictionary for current language
        lang_dict = self.translations.get(self.current_language, {})
        
        # Try current language first
        if key in lang_dict:
            return lang_dict[key]
        
        # Log warning if key not found in current language
        logger.warning(f"Translation key '{key}' not found in language '{self.current_language}'")
        
        # Try English as fallback
        if self.current_language != "en":
            en_dict = self.translations.get("en", {})
            if key in en_dict:
                return en_dict[key]
            # Log warning if key not found in English either
            logger.warning(f"Translation key '{key}' not found in fallback language 'en'")
        
        # Last resort: return the key itself
        return key
    
    def get_supported_languages(self):
        """Return list of supported languages.
        
        Returns:
            list: List of dictionaries with language code and name
        """
        languages = []
        for code in self.translations:
            languages.append({
                "code": code,
                "name": self.language_names.get(code, code)
            })
        
        return languages
    
    def get_current_language(self):
        """Get the current language code.
        
        Returns:
            str: The current language code
        """
        return self.current_language
    
    def set_language(self, lang_code):
        """Set the current language.
        
        Args:
            lang_code: The language code to set
            
        Returns:
            bool: True if successful, False if language is not supported
        """
        if lang_code in self.translations:
            self.current_language = lang_code
            logger.debug(f"Language set to: {lang_code}")
            return True
        logger.warning(f"Unsupported language: {lang_code}")
        return False
        
    def create_translation_template(self, output_path=None):
        """Create a translation template with all keys.
        
        This method creates a template file with all translation keys
        that can be used as a starting point for new translations.
        
        Args:
            output_path: Path to save the template file
                        If None, uses the translations directory
        
        Returns:
            str: Path to the created template file
        """
        if output_path is None:
            output_path = self._get_translations_dir() / 'template.json'
        else:
            # If output_path is a string, convert to Path
            if isinstance(output_path, str):
                output_path = Path(output_path)
            
            # Ensure the directory exists
            os.makedirs(output_path.parent, exist_ok=True)
        
        # Get all keys from English translations
        en_dict = self.translations.get("en", {})
        
        # Create template with empty values
        template = {
            "name": "Language Name",
            "translations": {key: "" for key in en_dict}
        }
        
        try:
            # Write the template JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, ensure_ascii=False, indent=2)
            
            # Create a README.md file with instructions in the same directory
            readme_path = output_path.parent / "README.md"
            readme_content = """# SwwwGUI Translation Instructions

SwwwGUI loads translations exclusively from ~/.config/swww-gui/translations/

## To create a new translation:

1. Copy the template file to a new file named with your language code:
   ```
   cp template.json your-language-code.json
   ```
   (e.g., `de.json` for German, `fr.json` for French)

2. Edit the new file:
   - Set the "name" field to your language name (e.g., "Deutsch" for German)
   - Translate all strings in the "translations" section

3. Restart SwwwGUI to see your new language in the settings

## Tips

- Keep formatting elements like `%s`, `{0}`, etc. as they are—these are placeholders for variables
- If you're unsure about a technical term, it's often better to leave it in English or transliterate it
"""
            
            # Only write the README file if it doesn't exist
            if not readme_path.exists():
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(readme_content)
            
            logger.info(f"Created translation template at {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Failed to create translation template: {e}")
            return None 