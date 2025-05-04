import gi
import threading
import os
from pathlib import Path
import time

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GdkPixbuf, Gio, GLib, Gdk


class ImageCache:
    """Simple cache for loaded images to avoid reloading the same images."""
    
    def __init__(self, max_size=10):
        self.cache = {}
        self.max_size = max_size
        self.access_times = {}
    
    def get(self, file_path):
        """Get an image from the cache."""
        if file_path in self.cache:
            self.access_times[file_path] = time.time()
            return self.cache[file_path]
        return None
    
    def put(self, file_path, pixbuf):
        """Add an image to the cache."""
        # Purge oldest items if cache is full
        if len(self.cache) >= self.max_size:
            oldest_path = min(self.access_times.items(), key=lambda x: x[1])[0]
            del self.cache[oldest_path]
            del self.access_times[oldest_path]
        
        self.cache[file_path] = pixbuf
        self.access_times[file_path] = time.time()


class ImageView(Gtk.Picture):
    """Widget for displaying and previewing wallpaper images."""
    
    def __init__(self):
        super().__init__()
        
        self.current_image_path = None
        self.image_cache = ImageCache(max_size=20)  # Cache for loaded images
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components."""
        self.set_content_fit(Gtk.ContentFit.CONTAIN)
        self.set_size_request(400, 300)
        self.set_hexpand(True)
        self.set_vexpand(True)
        
        # Set default placeholder image
        self.set_placeholder()
        
    def set_placeholder(self):
        """Set a placeholder image."""
        self.set_filename(None)
        self.current_image_path = None
        
        # Create a simple placeholder
        self.add_css_class("dim-label")
        self.add_css_class("card")
        
    def load_image(self, file_path):
        """Load an image from the given file path."""
        if not file_path or not os.path.exists(file_path):
            self.set_placeholder()
            return False
            
        # Check cache first
        cached_pixbuf = self.image_cache.get(file_path)
        if cached_pixbuf:
            # Use cached image
            self._set_from_pixbuf(cached_pixbuf)
            self.current_image_path = file_path
            return True
            
        # Start a thread to load the image asynchronously
        threading.Thread(
            target=self._load_image_thread,
            args=(file_path,),
            daemon=True
        ).start()
        
        # Show loading indicator or placeholder
        self.add_css_class("dim-label")
        self.add_css_class("card")
        return True
        
    def _load_image_thread(self, file_path):
        """Thread function to load image."""
        try:
            # Load the image
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(file_path)
            except gi.repository.GLib.Error:
                GLib.idle_add(lambda: self.set_placeholder())
                return
            
            # Cache the pixbuf
            self.image_cache.put(file_path, pixbuf)
            
            # Update UI in the main thread
            GLib.idle_add(lambda p=pixbuf, fp=file_path: self._set_from_pixbuf(p, fp))
            
            # Preload adjacent images for faster navigation
            self._preload_adjacent_images(file_path)
        except Exception:
            # If loading fails, show placeholder
            GLib.idle_add(lambda: self.set_placeholder())
    
    def _set_from_pixbuf(self, pixbuf, file_path=None):
        """Set the image from a pixbuf."""
        if file_path:
            self.current_image_path = file_path
        
        # Convert GdkPixbuf to GdkTexture for GTK4
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        self.set_paintable(texture)
        
        # Remove placeholder styling
        self.remove_css_class("dim-label")
        self.remove_css_class("card")
        
        return False  # Remove from idle queue
    
    def _preload_adjacent_images(self, file_path):
        """Preload images before and after the current one."""
        try:
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            
            # Get all image files in the directory
            image_files = []
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.tga']
            
            for entry in os.scandir(directory):
                if entry.is_file():
                    ext = os.path.splitext(entry.name)[1].lower()
                    if ext in valid_extensions:
                        image_files.append(entry.name)
            
            # Sort files
            image_files.sort()
            
            # Find current index
            if filename in image_files:
                index = image_files.index(filename)
                
                # Preload next and previous
                indices_to_load = []
                if index > 0:
                    indices_to_load.append(index - 1)  # Previous
                if index < len(image_files) - 1:
                    indices_to_load.append(index + 1)  # Next
                
                # Load images at low priority
                for idx in indices_to_load:
                    preload_path = os.path.join(directory, image_files[idx])
                    if preload_path not in self.image_cache.cache:
                        try:
                            pixbuf = GdkPixbuf.Pixbuf.new_from_file(preload_path)
                            self.image_cache.put(preload_path, pixbuf)
                        except Exception:
                            pass  # Ignore errors in preloading
        except Exception:
            pass  # Don't let preloading errors affect the main functionality
