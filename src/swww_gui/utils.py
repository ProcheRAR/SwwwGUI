"""
Утилиты для приложения SwwwGUI.
Общие функции, которые используются в разных частях приложения.
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Union, Tuple, Callable

logger = logging.getLogger(__name__)

def run_command(cmd: List[str], check: bool = True) -> Tuple[bool, str, str]:
    """Запускает команду в терминале и возвращает статус и вывод.
    
    Args:
        cmd: Список строк с командой и аргументами
        check: Проверять статус выхода
        
    Returns:
        Tuple[bool, str, str]: (успех, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check
        )
        return True, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {' '.join(cmd)}\nError: {e.stderr}")
        return False, e.stdout, e.stderr
    except Exception as e:
        logger.error(f"Error running command: {' '.join(cmd)}\nError: {e}")
        return False, "", str(e)

def is_executable_available(name: str) -> bool:
    """Проверяет, доступна ли программа в системе.
    
    Args:
        name: Имя исполняемого файла
        
    Returns:
        bool: True если программа доступна, False иначе
    """
    try:
        return subprocess.run(
            ["which", name], 
            capture_output=True, 
            check=False
        ).returncode == 0
    except Exception:
        return False

def get_image_files_in_directory(directory: Union[str, Path]) -> List[str]:
    """Возвращает список путей к файлам изображений в указанной директории.
    
    Args:
        directory: Путь к директории для поиска
        
    Returns:
        List[str]: Список путей к файлам изображений
    """
    if not os.path.isdir(directory):
        logger.warning(f"Directory not found: {directory}")
        return []
        
    # Поддерживаемые форматы изображений
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
    
    result = []
    try:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                if ext in image_extensions:
                    result.append(file_path)
    except Exception as e:
        logger.error(f"Error listing directory {directory}: {e}")
    
    return sorted(result)

def ensure_directory_exists(path: Union[str, Path]) -> bool:
    """Создаёт директорию, если она не существует.
    
    Args:
        path: Путь к директории
        
    Returns:
        bool: True если директория существует или была создана,
              False если произошла ошибка
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            logger.debug(f"Created directory: {path}")
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        return False 