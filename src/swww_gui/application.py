import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib

from swww_gui.window import SwwwGuiWindow
from swww_gui.config import SwwwGuiConfig
from swww_gui.localization import Translator


class SwwwGuiApplication(Adw.Application):
    """Main application class for SwwwGui."""

    def __init__(self):
        super().__init__(application_id="io.github.swwwgui",
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.config = SwwwGuiConfig()
        self.translator = Translator(self.config)
        self.create_action("quit", self.on_quit_action)
        self.create_action("about", self.on_about_action)
        
    def do_activate(self):
        """Called when the application is activated."""
        window = self.props.active_window
        if not window:
            window = SwwwGuiWindow(application=self)
        window.present()

    def create_action(self, name, callback):
        """Add an application action."""
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)

    def on_quit_action(self, action, param):
        """Callback for the app.quit action."""
        self.quit()

    def on_about_action(self, action, param):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="SwwwGui",
            application_icon="io.github.swwwgui",
            developer_name="SwwwGui Contributors",
            version="0.1.0",
            developers=["SwwwGui Contributors"],
            copyright="© 2025 SwwwGui Contributors",
            license_type=Gtk.License.GPL_3_0,
            website="https://github.com/LGFae/swww",
            issue_url="https://github.com/LGFae/swww/issues",
        )
        about.present()


def main():
    """Run the application."""
    app = SwwwGuiApplication()
    try:
        return app.run(sys.argv)
    except KeyboardInterrupt:
        # Корректно обрабатываем Ctrl+C
        print("Shutting down gracefully...")
        app.quit()
        return 0
    except Exception as e:
        print(f"Error running application: {e}")
        return 1


if __name__ == "__main__":
    main()
