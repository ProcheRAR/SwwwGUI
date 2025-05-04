"""
Файл с константами для приложения SwwwGui.
Все жестко заданные значения должны быть определены здесь.
"""

from pathlib import Path

# Размеры окна по умолчанию
DEFAULT_WINDOW_WIDTH = 1000
DEFAULT_WINDOW_HEIGHT = 680

# Значения для отступов в UI
MARGIN_SMALL = 6
MARGIN_MEDIUM = 12
MARGIN_LARGE = 24

# Значения для таймаутов тостов
TOAST_TIMEOUT_SHORT = 2
TOAST_TIMEOUT_MEDIUM = 3
TOAST_TIMEOUT_LONG = 5

# Значения по умолчанию для эффектов
DEFAULT_TRANSITION_TYPE = 'simple'
DEFAULT_TRANSITION_STEP = 2
DEFAULT_TRANSITION_FPS = 30
DEFAULT_TRANSITION_DURATION = 3.0
DEFAULT_TRANSITION_ANGLE = 45
DEFAULT_TRANSITION_WAVE = '20,20'
DEFAULT_TRANSITION_POS = 'center'
DEFAULT_TRANSITION_BEZIER = '.54,0,.34,.99'

# Значения по умолчанию для изображений
DEFAULT_RESIZE_MODE = 'crop'
DEFAULT_FILL_COLOR = '000000'
DEFAULT_FILTER_TYPE = 'Lanczos3'

# Пути
DEFAULT_CONFIG_DIR = Path.home() / '.config' / 'swww-gui'
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / 'config.json'
DEFAULT_PICTURES_DIR = Path.home() / 'Pictures'

# Для matugen
MATUGEN_CONFIG_PATH = Path.home() / '.config' / 'matugen' / 'config.toml'

# Версия приложения
APP_VERSION = '1.0.0'

# Идентификатор приложения
APP_ID = 'io.github.swwwgui'

# Репозиторий
GITHUB_REPO_URL = 'https://github.com/ProcheRAR/SwwwGUI'
GITHUB_REPO_DISPLAY = 'github.com/ProcheRAR/SwwwGUI'

# Поддерживаемые языки
SUPPORTED_LANGUAGES = [
    {"code": "en", "name": "English"},
    {"code": "ru", "name": "Русский"}
]

# Минимальная ширина контента бокового меню
MIN_SIDEBAR_WIDTH = 400 