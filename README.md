# SwwwGUI

A modern GTK4 and Libadwaita based GUI for the swww wallpaper manager for Wayland.

## Features

- Intuitive GUI for setting wallpapers using swww
- Transition effects with live preview
- Categorized wallpaper browsing
- matugen integration with dynamic themes
- Multilingual support with easy translation system
- Modern interface based on GTK4 and Libadwaita

## Installation

### Arch Linux (AUR)

SwwwGUI is available in the Arch User Repository:

```bash
# Using yay
yay -S swwwgui

# Using paru
paru -S swwwgui
```

For more detailed instructions, see [INSTALL_AUR.md](INSTALL_AUR.md).

### From Source

1. Ensure you have swww installed:
   ```bash
   git clone https://github.com/LGFae/swww
   cd swww
   cargo build --release
   ```

2. Clone and install SwwwGUI:
   ```bash
   git clone https://github.com/ProcheRAR/SwwwGUI.git
   cd SwwwGUI
   
   # Compile resources first
   python compile_resources.py
   
   # Install the package
   pip install -e .
   ```

3. Run the application:
   ```bash
   swwwgui
   ```

## Dependencies

- Python 3.8+
- PyGObject
- GTK4
- Libadwaita
- swww (daemon)
- Optional: matugen (for dynamic theme generation)

## Development Setup

If you're developing for SwwwGUI, make sure to follow these steps:

1. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. After any change to files in the `data` directory, regenerate resources:
   ```bash
   python compile_resources.py
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

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.
