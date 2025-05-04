import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, GdkPixbuf, Gdk

import os
import threading
import time
from pathlib import Path


# Global thumbnail cache
class ThumbnailCache:
    """Cache for thumbnails to avoid reloading."""
    
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
        self.access_times = {}
    
    def get(self, file_path):
        """Get a thumbnail from the cache."""
        if file_path in self.cache:
            self.access_times[file_path] = time.time()
            return self.cache[file_path]
        return None
    
    def put(self, file_path, pixbuf):
        """Add a thumbnail to the cache."""
        # Purge oldest items if cache is full
        if len(self.cache) >= self.max_size:
            oldest_path = min(self.access_times.items(), key=lambda x: x[1])[0]
            del self.cache[oldest_path]
            del self.access_times[oldest_path]
        
        self.cache[file_path] = pixbuf
        self.access_times[file_path] = time.time()


# Create a single global cache instance
_THUMBNAIL_CACHE = ThumbnailCache(max_size=200)


class ImageItem(Gtk.FlowBoxChild):
    """A thumbnail item for the image grid."""

    def __init__(self, file_path, parent):
        super().__init__()
        self.file_path = file_path
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI components."""
        self.set_size_request(150, 120)

        # Create box for thumbnail and label
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_top(6)
        box.set_margin_bottom(6)
        box.set_margin_start(6)
        box.set_margin_end(6)

        # Create thumbnail image
        self.image = Gtk.Picture()
        self.image.set_size_request(140, 105)  # Larger display size
        self.image.set_content_fit(Gtk.ContentFit.CONTAIN)  # CONTAIN preserves image quality better than COVER
        self.image.add_css_class("card")
        box.append(self.image)

        # Create label for filename
        filename = os.path.basename(self.file_path)
        if len(filename) > 15:
            filename = filename[:12] + "..."
        label = Gtk.Label(label=filename)
        label.set_ellipsize(True)
        label.set_tooltip_text(os.path.basename(self.file_path))
        box.append(label)

        self.set_child(box)
        self.load_thumbnail()

    def load_thumbnail(self):
        """Load the thumbnail image."""
        # Check cache first
        cached_thumb = _THUMBNAIL_CACHE.get(self.file_path)
        if cached_thumb:
            self._set_thumbnail(cached_thumb)
            return
            
        # Start a thread to load the thumbnail
        threading.Thread(target=self._load_thumbnail_thread, daemon=True).start()

    def _load_thumbnail_thread(self):
        """Thread function to load thumbnail."""
        try:
            # Try to use more efficient loading method first
            try:
                # Create higher quality image by loading at double size and using best quality
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    self.file_path, 240, 180, True)
            except:
                # If failed, load entire image
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.file_path)
                # And scale manually with high quality
                orig_width = pixbuf.get_width()
                orig_height = pixbuf.get_height()
                scale = min(240 / orig_width, 180 / orig_height)
                new_width = int(orig_width * scale)
                new_height = int(orig_height * scale)
                # Use HYPER interpolation for highest quality
                pixbuf = pixbuf.scale_simple(new_width, new_height, GdkPixbuf.InterpType.HYPER)
            
            # Cache the thumbnail
            _THUMBNAIL_CACHE.put(self.file_path, pixbuf)
            
            # Update UI in the main thread
            GLib.idle_add(lambda: self._set_thumbnail(pixbuf))
        except Exception:
            # If loading fails, show a placeholder
            GLib.idle_add(lambda: self._set_placeholder())

    def _set_thumbnail(self, pixbuf):
        """Set the thumbnail image."""
        # В GTK4 для Gtk.Picture нужно использовать GdkTexture вместо GdkPixbuf
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        self.image.set_paintable(texture)
        return False  # Remove this idle callback

    def _set_placeholder(self):
        """Set a placeholder image."""
        self.image.add_css_class("dim-label")
        return False  # Remove this idle callback


class FileChooser(Gtk.Box):
    """File chooser component for browsing and selecting wallpapers."""

    def __init__(self, parent_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.parent_window = parent_window
        
        # Get last opened folder from config, fallback to user's Pictures folder
        last_folder = parent_window.config.get('last_folder')
        if last_folder and os.path.exists(last_folder):
            self.current_folder = last_folder
        else:
            self.current_folder = str(Path.home() / "Pictures")
            
        self.current_files = []
        self.selected_item = None  # Track currently selected item
        
        # For batch loading of thumbnails
        self.batch_size = 20  # Number of thumbnails to load in each batch
        self.loading_batch = False
        
        self.setup_ui()
        self.load_folder(self.current_folder)

    def setup_ui(self):
        """Set up the UI components."""
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(12)
        self.set_margin_end(12)

        # Header with path bar and buttons
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        # Back button
        self.back_button = Gtk.Button()
        self.back_button.set_icon_name("go-previous-symbolic")
        self.back_button.set_tooltip_text("Go to Parent Directory")
        self.back_button.connect("clicked", self.on_back_clicked)
        header_box.append(self.back_button)
        
        # Path label
        self.path_label = Gtk.Label()
        self.path_label.set_ellipsize(True)
        self.path_label.set_hexpand(True)
        self.path_label.set_xalign(0)
        self.path_label.add_css_class("heading")
        header_box.append(self.path_label)
        
        # Open folder button
        open_button = Gtk.Button()
        open_button.set_icon_name("folder-open-symbolic")
        open_button.set_tooltip_text("Open Folder")
        open_button.connect("clicked", self.on_open_folder_clicked)
        header_box.append(open_button)
        
        self.append(header_box)
        
        # Create scrolled window for file grid
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        
        # Create flow box for file grid
        self.flow_box = Gtk.FlowBox()
        self.flow_box.set_valign(Gtk.Align.START)
        self.flow_box.set_homogeneous(True)
        self.flow_box.set_column_spacing(8)  # Add column spacing
        self.flow_box.set_row_spacing(8)     # Add row spacing
        
        # Calculate how many thumbnails can fit based on window size
        window_width = self.parent_window.get_width()
        thumbnail_width = 160  # Thumbnail width with margins
        max_per_line = max(1, int(window_width / thumbnail_width))
        self.flow_box.set_max_children_per_line(max_per_line)
        
        self.flow_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.flow_box.set_activate_on_single_click(True)  # Single click activation
        self.flow_box.connect("child-activated", self.on_item_activated)
        
        # Connect signals for keyboard navigation
        self.flow_box.set_can_focus(True)
        self.flow_box.connect("keynav-failed", self.on_keynav_failed)
        
        scrolled.set_child(self.flow_box)
        self.append(scrolled)
        
        # Message for empty folders
        self.empty_label = Gtk.Label(label="No images found in this folder")
        self.empty_label.add_css_class("dim-label")
        self.empty_label.add_css_class("title-3")
        self.empty_label.set_margin_top(50)
        self.empty_label.set_visible(False)
        self.append(self.empty_label)
        
        # Connect to scrolled window adjustment for lazy loading
        vadj = scrolled.get_vadjustment()
        vadj.connect("value-changed", self.on_scroll_value_changed)

    def load_folder(self, folder_path):
        """Load images from the specified folder."""
        # Update current folder
        self.current_folder = folder_path
        self.path_label.set_text(self.current_folder)
        
        # Save current folder to config
        self.parent_window.config.set('last_folder', folder_path)
        self.parent_window.config.save()
        
        # Clear current items
        while self.flow_box.get_first_child():
            self.flow_box.remove(self.flow_box.get_first_child())
        
        # Show loading indicator
        self.empty_label.set_text("Loading...")
        self.empty_label.set_visible(True)
        
        # Start a thread to scan the directory
        threading.Thread(
            target=self._scan_directory_thread,
            args=(folder_path,),
            daemon=True
        ).start()
    
    def _scan_directory_thread(self, folder_path):
        """Thread function to scan directory contents."""
        image_files = []
        dir_items = []
        
        try:
            # Scan directory
            for entry in os.scandir(folder_path):
                if entry.is_file():
                    ext = os.path.splitext(entry.name)[1].lower()
                    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.tga']:
                        image_files.append(entry.path)
                elif entry.is_dir():
                    dir_items.append(entry.path)
            
            # Sort files
            image_files.sort()
            dir_items.sort()
            
            # Update UI in the main thread
            GLib.idle_add(self._finish_load_folder, folder_path, image_files, dir_items)
        except (PermissionError, FileNotFoundError):
            GLib.idle_add(self._show_folder_error, "Could not access folder")
    
    def _finish_load_folder(self, folder_path, image_files, dir_items):
        """Finish loading folder in the main thread."""
        # Store the current files
        self.current_files = image_files
        
        # Add directory items first
        for dir_path in dir_items:
            dir_item = self.create_directory_item(dir_path)
            self.flow_box.append(dir_item)
        
        # Load first batch of images
        self.load_next_batch(force_first_batch=True)
        
        # Show empty message if no images found
        if not self.current_files and not dir_items:
            self.empty_label.set_text("No images found in this folder")
            self.empty_label.set_visible(True)
        else:
            self.empty_label.set_visible(False)
        
        return False  # Remove from idle queue
    
    def _show_folder_error(self, message):
        """Show folder error message."""
        self.show_error(message)
        self.empty_label.set_text("Error loading folder")
        self.empty_label.set_visible(True)
        return False  # Remove from idle queue

    def load_next_batch(self, force_first_batch=False):
        """Load the next batch of thumbnail items."""
        if self.loading_batch and not force_first_batch:
            return
            
        self.loading_batch = True
        
        # Get the count of already loaded image items (non-directory items)
        loaded_count = 0
        child = self.flow_box.get_first_child()
        while child:
            if hasattr(child, 'file_path'):  # Skip directory items
                loaded_count += 1
            child = child.get_next_sibling()
        
        # Check if we've loaded all files
        if loaded_count >= len(self.current_files) and not force_first_batch:
            self.loading_batch = False
            return
            
        # Calculate the range for this batch
        start_idx = 0 if force_first_batch else loaded_count
        end_idx = min(start_idx + self.batch_size, len(self.current_files))
        
        # Add image files to grid for this batch
        for i in range(start_idx, end_idx):
            file_path = self.current_files[i]
            item = ImageItem(file_path, self)
            self.flow_box.append(item)
        
        self.loading_batch = False

    def on_scroll_value_changed(self, adjustment):
        """Handle scroll event for lazy loading."""
        # Load more items when user scrolls near the bottom
        upper = adjustment.get_upper()
        page_size = adjustment.get_page_size()
        value = adjustment.get_value()
        
        # If scrolled to 80% of the way down, load more items
        if value > (upper - page_size) * 0.8:
            self.load_next_batch()

    def create_directory_item(self, dir_path):
        """Create an item for a directory."""
        child = Gtk.FlowBoxChild()
        child.dir_path = dir_path
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_top(6)
        box.set_margin_bottom(6)
        box.set_margin_start(6)
        box.set_margin_end(6)
        
        # Directory icon
        image = Gtk.Image.new_from_icon_name("folder-symbolic")
        image.set_pixel_size(48)
        image.add_css_class("dim-label")
        image.set_margin_top(12)
        image.set_margin_bottom(12)
        box.append(image)
        
        # Directory name
        dirname = os.path.basename(dir_path)
        if len(dirname) > 15:
            dirname = dirname[:12] + "..."
        label = Gtk.Label(label=dirname)
        label.set_ellipsize(True)
        label.set_tooltip_text(os.path.basename(dir_path))
        box.append(label)
        
        child.set_child(box)
        return child

    def on_item_activated(self, flow_box, child):
        """Handle item activation (click)."""
        # Store reference to the selected item for keyboard navigation
        self.selected_item = child
        
        if hasattr(child, 'dir_path'):
            # If it's a directory, navigate to it
            self.load_folder(child.dir_path)
        else:
            # If it's an image, load it in the preview - use the cached image if available
            file_path = child.file_path
            
            # For better performance, directly mark the image as selected without loading
            # to provide immediate feedback while the image loads in background
            self.parent_window.title_label.set_title(os.path.basename(file_path))
            
            # Start loading the image asynchronously
            self.parent_window.image_view.load_image(file_path)

    def on_keynav_failed(self, flowbox, direction):
        """Handle keyboard navigation failures."""
        # For up navigation at the top, focus on the back button
        if direction == Gtk.DirectionType.UP and self.selected_item:
            self.back_button.grab_focus()
            return True
        return False

    def on_back_clicked(self, button):
        """Navigate to parent directory."""
        parent_dir = os.path.dirname(self.current_folder)
        if parent_dir and parent_dir != self.current_folder:
            self.load_folder(parent_dir)

    def on_open_folder_clicked(self, button):
        """Open folder chooser dialog."""
        dialog = Gtk.FileChooserDialog(
            title="Select Folder",
            transient_for=self.parent_window,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Open", Gtk.ResponseType.ACCEPT)
        
        # Set current folder
        dialog.set_current_folder(Gio.File.new_for_path(self.current_folder))
        
        dialog.connect("response", self.on_folder_dialog_response)
        dialog.show()

    def on_folder_dialog_response(self, dialog, response):
        """Handle folder chooser dialog response."""
        if response == Gtk.ResponseType.ACCEPT:
            folder_path = dialog.get_file().get_path()
            self.load_folder(folder_path)
            # Save to recent folders
            self.parent_window.config.set('startup_folder', folder_path)
        dialog.destroy()

    def filter_files(self, search_text):
        """Filter files by search text."""
        search_text = search_text.lower()
        
        # Show all items if search text is empty
        if not search_text:
            child = self.flow_box.get_first_child()
            while child:
                child.set_visible(True)
                child = child.get_next_sibling()
            return
        
        # Filter items by filename
        child = self.flow_box.get_first_child()
        while child:
            visible = False
            if hasattr(child, 'dir_path'):
                # For directories, check directory name
                dirname = os.path.basename(child.dir_path).lower()
                visible = search_text in dirname
            elif hasattr(child, 'file_path'):
                # For images, check filename
                filename = os.path.basename(child.file_path).lower()
                visible = search_text in filename
            
            child.set_visible(visible)
            child = child.get_next_sibling()

    def show_error(self, message):
        """Show error toast."""
        toast = Adw.Toast.new(message)
        self.parent_window.add_toast(toast)
