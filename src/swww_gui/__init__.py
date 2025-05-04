"""SwwwGUI - GUI для утилиты swww (дисплейный менеджер для Wayland).

Этот модуль предоставляет удобный графический интерфейс пользователя 
для управления обоями в системах Wayland через утилиту swww.

Особенности:
- Интуитивный графический интерфейс на GTK4 и libadwaita
- Предварительный просмотр и установка обоев
- Настройка эффектов переходов
- Интеграция с Material You (через matugen)
- Мультиязычный интерфейс
"""

__version__ = "1.0.0"

import os
import logging
import gi
from gi.repository import Gio

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Register resources
resource_path = os.path.join(os.path.dirname(__file__), 'resources.gresource')
try:
    resource = Gio.Resource.load(resource_path)
    Gio.resources_register(resource)
    logger.debug("Resources loaded successfully")
except Exception as e:
    logger.error(f"Failed to load resources: {e}")

# Импортируем после настройки ресурсов
from .application import SwwwGuiApplication, main
from .window import SwwwGuiWindow
from .config import SwwwGuiConfig
from .swww_manager import SwwwManager
from .translator import Translator

__all__ = [
    'SwwwGuiApplication', 
    'SwwwGuiWindow', 
    'SwwwGuiConfig', 
    'SwwwManager', 
    'Translator',
    'main'
]
