import subprocess
import json
import os
import shutil
from pathlib import Path


class SwwwManager:
    """Interface for interacting with swww command-line tool."""
    
    def __init__(self):
        """Initialize the swww manager."""
        self.swww_path = self._find_swww_binary()
        self.daemon_path = self._find_swww_daemon_binary()
        
    def _find_swww_binary(self):
        """Find the swww binary in PATH."""
        return shutil.which("swww") or ""
        
    def _find_swww_daemon_binary(self):
        """Find the swww-daemon binary in PATH."""
        return shutil.which("swww-daemon") or ""
        
    def is_swww_installed(self):
        """Check if swww is installed."""
        return bool(self.swww_path and self.daemon_path)
        
    def is_daemon_running(self):
        """Check if swww-daemon is running."""
        try:
            result = subprocess.run(
                [self.swww_path, "query"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                timeout=2
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
            
    def start_daemon(self):
        """Start the swww-daemon."""
        if not self.daemon_path:
            return False
            
        try:
            # Run daemon in background
            subprocess.Popen(
                [self.daemon_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            # Check if daemon started successfully
            import time
            time.sleep(1)  # Give daemon time to start
            return self.is_daemon_running()
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
            
    def get_monitors(self):
        """Get list of available monitors."""
        if not self.is_daemon_running():
            return []
            
        try:
            result = subprocess.run(
                [self.swww_path, "query"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                timeout=2
            )
            
            if result.returncode != 0:
                return []
                
            # Parse monitor names from output
            monitors = []
            for line in result.stdout.splitlines():
                if "Output:" in line:
                    name = line.split("Output:")[1].strip()
                    monitors.append(name)
            return monitors
        except (subprocess.SubprocessError, FileNotFoundError):
            return []
            
    def get_transitions(self):
        """Get list of available transition types."""
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
        
    def get_resize_modes(self):
        """Get list of available resize modes."""
        return [
            "crop",
            "fit",
            "no"
        ]
        
    def get_filters(self):
        """Get list of available filters for scaling."""
        return [
            "Nearest", 
            "Bilinear", 
            "CatmullRom", 
            "Mitchell", 
            "Lanczos3"
        ]
        
    def set_wallpaper(self, image_path, options=None):
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
            return False
        
        # Default options
        if options is None:
            options = {}
            
        # Base command
        cmd = [self.swww_path, "img", image_path]
        
        # Add monitor if specified
        if options.get('monitor'):
            cmd.extend(["--outputs", options['monitor']])
        
        # Add resize mode
        resize_mode = options.get('resize_mode', 'crop')
        if resize_mode == 'no':
            cmd.append("--no-resize")
        else:
            cmd.extend(["--resize", resize_mode])
            
        # Add fill color
        fill_color = options.get('fill_color', '000000')
        cmd.extend(["--fill-color", fill_color])
        
        # Add filter - only if not doing a fast preview
        # Lanczos3 is high quality but slower
        if options.get('transition_type') == 'none':
            # For fast preview, use Nearest filter (fastest)
            cmd.extend(["--filter", "Nearest"])
        else:
            # For normal mode, use specified filter or default
            filter_type = options.get('filter', 'Lanczos3')
            cmd.extend(["--filter", filter_type])
        
        # Add transition type
        transition_type = options.get('transition_type', 'simple')
        cmd.extend(["--transition-type", transition_type])
        
        # Add transition step (defaults differ by transition type)
        default_step = 2 if transition_type == 'simple' else 90
        transition_step = options.get('transition_step', default_step)
        cmd.extend(["--transition-step", str(transition_step)])
        
        # Add transition duration
        if 'transition_duration' in options:
            cmd.extend(["--transition-duration", str(options['transition_duration'])])
        
        # Add transition fps
        transition_fps = options.get('transition_fps', 30)
        cmd.extend(["--transition-fps", str(transition_fps)])
        
        # Add transition angle for wipe/wave
        if transition_type in ['wipe', 'wave'] and 'transition_angle' in options:
            cmd.extend(["--transition-angle", str(options['transition_angle'])])
        
        # Add transition position for grow/outer
        if transition_type in ['grow', 'outer', 'center', 'any'] and 'transition_pos' in options:
            cmd.extend(["--transition-pos", options['transition_pos']])
        
        # Add invert-y if needed
        if options.get('invert_y', False):
            cmd.append("--invert-y")
        
        # Add bezier curve for fade transition
        if transition_type == 'fade' and 'transition_bezier' in options:
            cmd.extend(["--transition-bezier", options['transition_bezier']])
        
        # Add wave parameters for wave transition
        if transition_type == 'wave' and 'transition_wave' in options:
            cmd.extend(["--transition-wave", options['transition_wave']])
        
        try:
            # Для предпросмотра и обычного применения используем одинаковый подход
            # но не ждем завершения процесса, чтобы не блокировать интерфейс
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,  # Не перехватываем вывод, чтобы ускорить
                stderr=subprocess.DEVNULL,
                start_new_session=True  # Запускаем в фоне
            )
            
            # Просто проверяем, что процесс успешно запустился
            return process.poll() is None
            
        except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
            print(f"Error setting wallpaper: {e}")  # Для отладки
            return False
            
    def clear_wallpaper(self, color="#000000"):
        """Clear wallpaper with specified color."""
        if not self.is_daemon_running():
            return False
            
        try:
            result = subprocess.run(
                [self.swww_path, "clear", color],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                timeout=2
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
            
    def kill_daemon(self):
        """Kill the swww-daemon."""
        if not self.is_daemon_running():
            return True
            
        try:
            result = subprocess.run(
                [self.swww_path, "kill"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                timeout=2
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
