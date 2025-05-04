# SwwwGUI Translations

SwwwGUI supports a multi-language interface with a simple JSON-based translation system.

## Supported Languages

By default, SwwwGUI comes with two languages:
- English (en)
- Russian (ru)

## How to Add a New Translation

1. **Create a translation template**:
   - Launch SwwwGUI, go to "Settings" -> "Language"
   - Click the "Create Translation Template" button
   - The template will be created in `~/.config/swww-gui/translations/template.json`

2. **Create a translation file**:
   - Copy the template to a new file named with the language code, for example:
     ```
     cp ~/.config/swww-gui/translations/template.json ~/.config/swww-gui/translations/fr.json
     ```
     (where `fr` is for French)

3. **Edit the translation file**:
   - Set the "name" field to the language name in its native form (e.g., "Français")
   - Translate all strings in the "translations" section
   - Save the file

4. **Restart SwwwGUI**, your new language should appear in the settings

## Important Notes

- Translation strings must contain exactly the same formatting elements (e.g., `{0}`) as the original
- Technical terms are often better left untranslated
- Translations are stored exclusively in the user directory `~/.config/swww-gui/translations/`

## Example JSON Translation File

```json
{
  "name": "Français",
  "translations": {
    "app_title": "SwwwGui",
    "app_subtitle": "Gestionnaire de fond d'écran Wayland",
    "settings": "Paramètres",
    "language": "Langue",
    "apply": "Appliquer",
    "preview": "Aperçu"
    // ... other translation strings
  }
}
``` 