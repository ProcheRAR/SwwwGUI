import os
import json
from pathlib import Path
import logging
from typing import Dict, Any, Optional, List, Union

from .constants import (
    DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_FILE, DEFAULT_PICTURES_DIR,
    DEFAULT_TRANSITION_TYPE, DEFAULT_TRANSITION_STEP, DEFAULT_TRANSITION_FPS,
    DEFAULT_TRANSITION_DURATION, DEFAULT_TRANSITION_ANGLE, DEFAULT_TRANSITION_WAVE,
    DEFAULT_TRANSITION_POS, DEFAULT_TRANSITION_BEZIER, DEFAULT_RESIZE_MODE,
    DEFAULT_FILL_COLOR, DEFAULT_FILTER_TYPE, SUPPORTED_LANGUAGES
)

logger = logging.getLogger(__name__)

class SwwwGuiConfig:
    """Configuration handler for SwwwGui.
    
    Manages loading, saving, and accessing application settings.
    Configuration is stored in JSON format in the user's config directory.
    """
    
    def __init__(self, config_path: Optional[Path] = None) -> None:
        """Initialize the configuration manager.
        
        Args:
            config_path: Optional custom path for the config file.
                         If None, uses the default location.
        """
        self.config_dir = config_path.parent if config_path else DEFAULT_CONFIG_DIR
        self.config_file = config_path if config_path else DEFAULT_CONFIG_FILE
        self.config: Dict[str, Any] = {}
        
        # Create config directory if it doesn't exist
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Load configuration from file if it exists
        self.load()
    
    def load(self) -> None:
        """Load configuration from file.
        
        If the file doesn't exist or is corrupted, falls back to default values.
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                logger.debug(f"Configuration loaded from {self.config_file}")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load config from {self.config_file}: {e}")
                self.config = self._get_defaults()
        else:
            logger.info(f"Config file {self.config_file} not found, using defaults")
            self.config = self._get_defaults()
    
    def save(self) -> bool:
        """Save configuration to file.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.debug(f"Configuration saved to {self.config_file}")
            return True
        except IOError as e:
            logger.error(f"Failed to save config to {self.config_file}: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: The configuration key to retrieve.
            default: The value to return if the key doesn't exist.
            
        Returns:
            The value associated with the key, or the default if not found.
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: The configuration key to set.
            value: The value to associate with the key.
        """
        self.config[key] = value
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values.
        
        Maintains some user-specific values like language preference and
        recently accessed files/folders.
        """
        # Save important values that shouldn't be lost on reset
        last_image = self.config.get('last_image', '')
        startup_folder = self.config.get('startup_folder', str(DEFAULT_PICTURES_DIR))
        language = self.config.get('language', 'en')
        
        # Replace with defaults
        self.config = self._get_defaults()
        
        # Restore values that should be preserved
        self.config['last_image'] = last_image
        self.config['startup_folder'] = startup_folder
        self.config['language'] = language
        
        # Save to file
        logger.info("Configuration reset to defaults")
        self.save()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """Get default configuration values.
        
        Returns:
            Dict[str, Any]: Dictionary with default configuration values.
        """
        return {
            'last_image': '',
            'transition_type': DEFAULT_TRANSITION_TYPE,
            'transition_step': DEFAULT_TRANSITION_STEP,
            'transition_fps': DEFAULT_TRANSITION_FPS,
            'transition_duration': DEFAULT_TRANSITION_DURATION,
            'transition_angle': DEFAULT_TRANSITION_ANGLE,
            'transition_wave': DEFAULT_TRANSITION_WAVE,
            'transition_pos': DEFAULT_TRANSITION_POS,
            'transition_bezier': DEFAULT_TRANSITION_BEZIER,
            'resize_mode': DEFAULT_RESIZE_MODE,
            'fill_color': DEFAULT_FILL_COLOR,
            'filter': DEFAULT_FILTER_TYPE,
            'invert_y': False,
            'monitor': '',
            'favorites': [],
            'recent_folders': [],
            'use_matugen': False,
            'startup_folder': str(DEFAULT_PICTURES_DIR),
            'language': 'en'  # Default language is English
        }
        
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages.
        
        Returns:
            List of dictionaries with language code and name.
        """
        return SUPPORTED_LANGUAGES
