# SwwwGUI Translation Guide

SwwwGUI supports multiple languages through an easy-to-use JSON-based translation system. This makes it simple for anyone to add or contribute translations without having to modify the source code.

## Available Languages

Currently, the following languages are supported:

- English (en)
- Russian (ru)

## How to Add a New Translation

You can add translations for a new language by following these simple steps:

1. **Create a Translation Template**:
   - Run SwwwGUI once to ensure the translations directory is created
   - If it doesn't exist, create a directory at `~/.config/swww-gui/translations/`
   - Use the template.json file (if available) or copy an existing translation file

2. **Naming the Translation File**:
   - Name your file using the ISO language code (e.g., `de.json` for German, `fr.json` for French)
   - The language code will be used to identify the language in the application

3. **File Structure**:
   - Your translation file should follow this format:
   ```json
   {
     "name": "Your Language Name",
     "translations": {
       "app_title": "Translated Title",
       "app_subtitle": "Translated Subtitle",
       ...
     }
   }
   ```
   - The `name` field should contain the name of the language in that language (e.g., "Deutsch" for German)
   - The `translations` object contains all the translation keys and their translated values

4. **Place the File**:
   - Put your translation file in one of these locations:
     - `~/.config/swww-gui/translations/` (user-specific)
     - `<app-directory>/src/swww_gui/translations/` (application directory)
     - `/usr/share/swww-gui/translations/` (system-wide)

## Creating a New Translation from a Template

The easiest way to create a new translation is to:

1. Run SwwwGUI at least once to ensure the translations directory exists
2. Look for a `template.json` file in the translations directory, or create one using the commands below:

```python
from swww_gui.translator import Translator
translator = Translator()
translator.create_translation_template()
```

3. Copy the template to a new file with your language code: `cp template.json fr.json`
4. Edit the new file, providing translations for each key
5. Restart SwwwGUI to see your new language in the settings menu

## Translation Keys

The most important translation keys include:

- General UI: `app_title`, `app_subtitle`, `settings`, `apply`, etc.
- Effects: `effects`, `transition`, `transition_type`, etc.
- Image settings: `resize`, `resize_mode`, `fill_color`, etc.
- Advanced settings: `advanced`, `transition_angle`, `wave_dimensions`, etc.
- About dialog: `about`, `version`, `github_repo`, etc.

## Contributing Translations

If you've created a translation for a new language, consider contributing it back to the SwwwGUI project:

1. Fork the repository
2. Add your translation file to the `src/swww_gui/translations/` directory
3. Submit a pull request

Your contribution will help make SwwwGUI accessible to more users around the world!

## Tips for Translators

- Keep formatting elements like `%s`, `{0}`, etc. as they are—these are placeholders for variables
- Test your translation by running the application and switching to your language
- Make sure to translate all keys for a complete translation experience
- If you're unsure about a technical term, it's often better to leave it in English or transliterate it 