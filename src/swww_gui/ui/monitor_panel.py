import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MonitorPanel(Gtk.Box):
    """Panel for configuring monitor-specific settings."""
    
    def __init__(self, parent_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.parent_window = parent_window
        self.swww_manager = parent_window.swww_manager
        self.setup_ui()
        self.refresh_monitors()
        
    def setup_ui(self):
        """Set up the UI components."""
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(12)
        self.set_margin_end(12)
        
        # Monitor header
        header = Gtk.Label(label="Monitor Settings")
        header.add_css_class("heading")
        header.set_xalign(0)
        self.append(header)
        
        # Create the preferences group
        group = Adw.PreferencesGroup()
        
        # Monitor selection
        monitor_row = Adw.ComboRow()
        monitor_row.set_title("Target Monitor")
        monitor_row.set_subtitle("Select a specific monitor or leave empty for all")
        
        # Create string list for monitors
        string_list = Gtk.StringList()
        string_list.append("All Monitors")  # First option is for all monitors
        self.monitor_string_list = string_list
        
        monitor_row.set_model(string_list)
        monitor_row.set_selected(0)  # Default to 'All Monitors'
        self.monitor_row = monitor_row
        group.add(monitor_row)
        
        # Мониторы определяются автоматически при запуске
        
        # Add group to panel
        self.append(group)
        
    def refresh_monitors(self):
        """Refresh the list of available monitors."""
        # Save the currently selected monitor name if any
        selected_index = self.monitor_row.get_selected()
        selected_monitor = ""
        if selected_index > 0 and selected_index < self.monitor_string_list.get_n_items():
            selected_monitor = self.monitor_string_list.get_string(selected_index)
        
        # Clear current monitor list except "All Monitors"
        while self.monitor_string_list.get_n_items() > 1:
            self.monitor_string_list.remove(1)
        
        # Get available monitors
        monitors = self.swww_manager.get_monitors()
        
        # Add monitors to list
        for monitor in monitors:
            self.monitor_string_list.append(monitor)
        
        # Restore previously selected monitor if it still exists
        if selected_monitor:
            for i in range(self.monitor_string_list.get_n_items()):
                if i > 0 and self.monitor_string_list.get_string(i) == selected_monitor:
                    self.monitor_row.set_selected(i)
                    return
        
        # If not found, select "All Monitors"
        self.monitor_row.set_selected(0)
    
    def on_refresh_clicked(self, button):
        """Handle refresh button click."""
        self.refresh_monitors()
        
        # Show toast message
        toast = Adw.Toast.new("Monitor list refreshed")
        self.parent_window.add_toast(toast)
    
    def get_selected_monitor(self):
        """Get the selected monitor."""
        selected_index = self.monitor_row.get_selected()
        
        # Return empty string for "All Monitors" option
        if selected_index == 0:
            return ""
        
        # Return monitor name for specific monitor
        if selected_index < self.monitor_string_list.get_n_items():
            return self.monitor_string_list.get_string(selected_index)
        
        return ""
    
    def set_selected_monitor(self, monitor):
        """Set the selected monitor."""
        # If empty, select "All Monitors"
        if not monitor:
            self.monitor_row.set_selected(0)
            return
        
        # Look for the specified monitor
        for i in range(self.monitor_string_list.get_n_items()):
            if i > 0 and self.monitor_string_list.get_string(i) == monitor:
                self.monitor_row.set_selected(i)
                return
        
        # If not found, select "All Monitors"
        self.monitor_row.set_selected(0)
