import os
import json
from pathlib import Path


class SwwwGuiConfig:
    """Configuration handler for SwwwGui."""
    
    def __init__(self):
        """Initialize the configuration manager."""
        self.config_dir = os.path.join(Path.home(), ".config", "swww-gui")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.config = {}
        
        # Create config directory if it doesn't exist
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
        
        # Load configuration from file if it exists
        self.load()
    
    def load(self):
        """Load configuration from file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted or inaccessible, use defaults
                self.config = self._get_defaults()
        else:
            # If file doesn't exist, use defaults
            self.config = self._get_defaults()
    
    def save(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError:
            return False
    
    def get(self, key, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value."""
        self.config[key] = value
    
    def _get_defaults(self):
        """Get default configuration values."""
        return {
            'last_image': '',
            'transition_type': 'simple',
            'transition_step': 2,
            'transition_fps': 30,
            'monitor': '',
            'favorites': [],
            'recent_folders': [],
            'theme': 'system',
            'startup_folder': str(Path.home() / 'Pictures'),
            'language': 'en'  # Default language is English
        }
        
    def get_supported_languages(self):
        """Get list of supported languages."""
        return [
            {"code": "en", "name": "English"},
            {"code": "ru", "name": "Русский"}
        ]
