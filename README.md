# SwwwGui

A modern GTK 4 GUI for swww - an efficient animated wallpaper daemon for Wayland, with Material You theme integration.

## Features

- Modern libadwaita-based interface
- File browsing with image thumbnails and efficient caching
- Fast preview of wallpapers before applying
- Multiple language support (English and Russian)
- Configuration of all swww transition effects:
  - Simple fade
  - Wipe
  - Center
  - Outer
  - Random
  - Any
  - Directional (left, right, top, bottom)
- Material You theme integration with Matugen
- Reset settings button to quickly restore defaults
- JSON settings for storing preferences
- Search functionality
- Remembers last used folder and settings
- About page with GitHub repository link

## Dependencies

- Python 3.6+
- GTK 4.0
- libadwaita 1.0
- PyGObject
- swww (must be installed and in your PATH)
- Optional: matugen (for Material You theme generation)

## Installation

### AUR (Arch User Repository)

If you're using Arch Linux or an Arch-based distribution, you can install SwwwGui from the AUR:

```bash
yay -S swwwgui
```

or 

```bash
paru -S swwwgui
```

### Manual Installation

1. Clone this repository:
```bash
git clone https://github.com/ProcheRAR/SwwwGUI.git
cd SwwwGUI
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Compile the GResource file:
```bash
python compile_resources.py
```

4. Make the main script executable:
```bash
chmod +x swwwgui.py
```

## Running

Launch the application:
```bash
./swwwgui.py
```

Or install it system-wide:
```bash
# Copy to a location in your PATH
sudo cp swwwgui.py /usr/local/bin/swwwgui
sudo chmod +x /usr/local/bin/swwwgui

# Copy the application files
sudo mkdir -p /usr/local/share/swwwgui
sudo cp -r src/ data/ compile_resources.py requirements.txt /usr/local/share/swwwgui/

# Compile resources in the installed location
cd /usr/local/share/swwwgui
sudo python compile_resources.py

# Create desktop entry
sudo cp data/swwwgui.desktop /usr/share/applications/
sudo cp data/icons/swwwgui.svg /usr/share/icons/hicolor/scalable/apps/
```

## Usage

1. **Browse Files**: Navigate through your file system to find wallpaper images.
2. **Preview**: Select an image to see it in the preview panel.
3. **Configure Effects**: Choose transition type, speed, and other effects.
4. **Apply**: Click the "Apply" button to set the wallpaper using swww.
5. **Material You**: Enable Material You theme generation in Settings → Matugen to automatically generate a matching color theme.
6. **Reset Settings**: Use the reset button in the effects panel to restore default settings.

## Initial Setup

On first run, if swww-daemon is not running, SwwwGui will offer to start it for you.

## Matugen Integration

SwwwGui can integrate with Matugen to generate Material You themes based on your wallpaper. To use this feature:

1. Install Matugen: [https://github.com/InExtremo/matugen](https://github.com/InExtremo/matugen)
2. Enable Matugen integration in SwwwGui settings
3. When you apply a wallpaper, Matugen will generate a matching theme

## Note

This application requires swww to be installed on your system. It will not run on Gnome, because swww requires the wlr-layer-shell protocol which is not implemented in Gnome.

## License

This project is licensed under the GPL-3.0 License.
