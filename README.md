# SwwwGUI

A modern GTK4 and Libadwaita based GUI for the swww wallpaper manager for Wayland.

## Features

- Intuitive GUI for setting wallpapers using swww
- Transition effects with live preview
- Categorized wallpaper browsing
- Material You integration with matugen
- Multilingual support with easy translation system
- Modern interface based on GTK4 and Libadwaita

## Installation

1. Ensure you have swww installed:
   ```
   git clone https://github.com/LGFae/swww
   cd swww
   cargo build --release
   ```

2. Install Python dependencies:
   ```
   pip install PyGObject
   ```

3. Run the application:
   ```
   python -m src.swww_gui
   ```

## Translations

SwwwGUI supports multiple languages through a simple JSON-based translation system. Currently supported languages:

- English
- Russian

Additional languages can be added by placing translation files in the `~/.config/swww-gui/translations/` directory.

To add a new language or learn more about the translation system, see [TRANSLATIONS.md](TRANSLATIONS.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.
