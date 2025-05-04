import logging
from typing import List, Dict, Any, Optional, Union
import time
import os
from pathlib import Path

from .utils import run_command, is_executable_available
from .constants import (
    DEFAULT_TRANSITION_TYPE, DEFAULT_TRANSITION_STEP, DEFAULT_TRANSITION_FPS,
    DEFAULT_TRANSITION_DURATION, DEFAULT_RESIZE_MODE, DEFAULT_FILL_COLOR,
    DEFAULT_FILTER_TYPE
)

logger = logging.getLogger(__name__)

class SwwwManager:
    """Interface for interacting with swww command-line tool.
    
    Provides methods to interact with swww for setting wallpapers,
    managing daemon, and querying available options.
    """
    
    def __init__(self) -> None:
        """Initialize the swww manager."""
        self.swww_binary = "swww"
        self.daemon_binary = "swww-daemon"
        
    def is_swww_installed(self) -> bool:
        """Check if swww is installed.
        
        Returns:
            bool: True if both swww and swww-daemon are available, False otherwise.
        """
        return (is_executable_available(self.swww_binary) and 
                is_executable_available(self.daemon_binary))
        
    def is_daemon_running(self) -> bool:
        """Check if swww-daemon is running.
        
        Returns:
            bool: True if daemon is running, False otherwise.
        """
        success, _, _ = run_command([self.swww_binary, "query"], check=False)
        return success
            
    def start_daemon(self) -> bool:
        """Start the swww-daemon.
        
        Returns:
            bool: True if daemon started successfully, False otherwise.
        """
        if not is_executable_available(self.daemon_binary):
            logger.error("swww-daemon binary not found")
            return False
            
        try:
            # Run daemon in background using Popen
            import subprocess
            subprocess.Popen(
                [self.daemon_binary],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            # Check if daemon started successfully after a short delay
            time.sleep(1)  # Give daemon time to start
            return self.is_daemon_running()
        except Exception as e:
            logger.error(f"Failed to start swww-daemon: {e}")
            return False
            
    def get_monitors(self) -> List[str]:
        """Get list of available monitors.
        
        Returns:
            List[str]: Names of available monitors, or empty list if failed.
        """
        if not self.is_daemon_running():
            return []
            
        success, stdout, _ = run_command([self.swww_binary, "query"], check=False)
        if not success:
            return []
                
        # Parse monitor names from output
        monitors = []
        for line in stdout.splitlines():
            if "Output:" in line:
                name = line.split("Output:")[1].strip()
                monitors.append(name)
        return monitors
            
    def get_transitions(self) -> List[str]:
        """Get list of available transition types.
        
        Returns:
            List[str]: Available transition types.
        """
        return [
            "none",
            "simple",
            "fade",
            "left",
            "right",
            "top",
            "bottom",
            "wipe",
            "wave", 
            "grow",
            "center",
            "any",
            "outer",
            "random"
        ]
        
    def get_resize_modes(self) -> List[str]:
        """Get list of available resize modes.
        
        Returns:
            List[str]: Available resize modes.
        """
        return [
            "crop",
            "fit",
            "no"
        ]
        
    def get_filters(self) -> List[str]:
        """Get list of available filters for scaling.
        
        Returns:
            List[str]: Available scaling filters.
        """
        return [
            "Nearest", 
            "Bilinear", 
            "CatmullRom", 
            "Mitchell", 
            "Lanczos3"
        ]
        
    def set_wallpaper(self, image_path: str, options: Optional[Dict[str, Any]] = None) -> bool:
        """Set wallpaper using swww with all available options.
        
        Args:
            image_path: Path to the image file
            options: Dictionary with the following possible keys:
                'monitor': Output name(s) to target (comma-separated)
                'resize_mode': Resize mode (crop, fit, no)
                'fill_color': Color to fill padding when image doesn't fill screen
                'filter': Scaling filter to use
                'transition_type': Type of transition effect
                'transition_step': How fast transition approaches new image
                'transition_duration': Duration in seconds for transition
                'transition_fps': Frame rate for transition effect
                'transition_angle': Angle for wipe/wave transitions
                'transition_pos': Position for grow/outer transitions
                'invert_y': Whether to invert Y position
                'transition_bezier': Bezier curve for fade transition
                'transition_wave': Wave width/height for wave transition
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_daemon_running() or not os.path.exists(image_path):
            logger.error(f"Cannot set wallpaper: daemon not running or image not found - {image_path}")
            return False
        
        # Default options
        if options is None:
            options = {}
            
        # Base command
        cmd = [self.swww_binary, "img", image_path]
        
        # Add monitor if specified
        if options.get('monitor'):
            cmd.extend(["--outputs", options['monitor']])
        
        # Add resize mode
        resize_mode = options.get('resize_mode', DEFAULT_RESIZE_MODE)
        if resize_mode == 'no':
            cmd.append("--no-resize")
        else:
            cmd.extend(["--resize", resize_mode])
            
        # Add fill color
        fill_color = options.get('fill_color', DEFAULT_FILL_COLOR)
        cmd.extend(["--fill-color", fill_color])
        
        # Add filter - only if not doing a fast preview
        # Lanczos3 is high quality but slower
        if options.get('transition_type') == 'none':
            # For fast preview, use Nearest filter (fastest)
            cmd.extend(["--filter", "Nearest"])
        else:
            # For normal mode, use specified filter or default
            filter_type = options.get('filter', DEFAULT_FILTER_TYPE)
            cmd.extend(["--filter", filter_type])
        
        # Add transition type
        transition_type = options.get('transition_type', DEFAULT_TRANSITION_TYPE)
        cmd.extend(["--transition-type", transition_type])
        
        # Add transition step (defaults differ by transition type)
        default_step = DEFAULT_TRANSITION_STEP if transition_type == 'simple' else 90
        transition_step = options.get('transition_step', default_step)
        cmd.extend(["--transition-step", str(transition_step)])
        
        # Add transition duration
        if 'transition_duration' in options:
            cmd.extend(["--transition-duration", str(options['transition_duration'])])
        
        # Add transition fps
        transition_fps = options.get('transition_fps', DEFAULT_TRANSITION_FPS)
        cmd.extend(["--transition-fps", str(transition_fps)])
        
        # Add transition-specific options
        if transition_type == 'wipe':
            # Add transition angle for wipe
            if 'transition_angle' in options:
                cmd.extend(["--transition-angle", str(options['transition_angle'])])
                
        elif transition_type == 'wave':
            # Add transition angle for wave
            if 'transition_angle' in options:
                cmd.extend(["--transition-angle", str(options['transition_angle'])])
                
            # Add transition wave
            if 'transition_wave' in options:
                cmd.extend(["--transition-wave", str(options['transition_wave'])])
                
        elif transition_type in ['grow', 'outer', 'center', 'any']:
            # Add transition position
            if 'transition_pos' in options:
                cmd.extend(["--transition-pos", str(options['transition_pos'])])
                
            # Add invert_y if specified
            if options.get('invert_y'):
                cmd.append("--invert-y")
                
        elif transition_type == 'fade':
            # Add transition bezier
            if 'transition_bezier' in options:
                cmd.extend(["--transition-bezier", str(options['transition_bezier'])])
        
        # Run command
        success, _, stderr = run_command(cmd)
        if not success:
            logger.error(f"Failed to set wallpaper: {stderr}")
            
        return success
        
    def clear_wallpaper(self, color: str = "#000000") -> bool:
        """Clear wallpaper and set a solid color.
        
        Args:
            color: Color to set as background (in hex format).
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.is_daemon_running():
            return False
            
        cmd = [self.swww_binary, "clear", color]
        success, _, _ = run_command(cmd)
        return success
        
    def kill_daemon(self) -> bool:
        """Kill swww-daemon.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.is_daemon_running():
            return True  # Already not running
            
        cmd = [self.swww_binary, "kill"]
        success, _, _ = run_command(cmd)
        return success
