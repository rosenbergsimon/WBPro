from homepage import Homepage
import customtkinter as tk
from threading import Thread
import time
import ctypes
import pyautogui

# bg = #353535, buttons = #3EA216, highlight buttons = #74BD57


# class MainApp holds two variables for storage, the current base tk window open, and the root (hidden) window. It is
# a collection of methods referenced later in the program, passed through class initializers.
# Also has class MouseInactivityWatcher, which listens for mouse movement, and terminates program if none detected.

class MouseInactivityWatcher:
    def __init__(self, root, timeout_seconds, main):
        self.root = root
        self.timeout = timeout_seconds
        self.main = main
        self.last_position = None
        self.main.watcher_stop = self.stop
        self.running = True

        # Start background thread
        self.thread = Thread(target=self.watch_inactivity, daemon=True)
        self.thread.start()

    def get_mouse_position(self):
        return pyautogui.position()

    def watch_inactivity(self):
        while self.running:
            self.last_position = self.get_mouse_position()
            time.sleep(self.timeout)
            current_pos = self.get_mouse_position()
            if current_pos != self.last_position:
                pass
            else:
                self.main.quit_application()

    def stop(self):
        print("stopped")
        self.running = False


class MainApp:
    def __init__(self, root):
        self.root = root
        self.current_window = None  # set to None so nothing to destroy in below function
        self.show_homepage()        # starts the application by launching Homepage
        self.watcher_stop = None  # temporary object that will become a ref to MouseInactivityWatcher.stop

    # allows for a new toplevel window to be launched while destroying the previously open one
    def switch_window(self, window_class):
        if self.current_window:
            self.current_window.destroy()
        # passes all the needed functions of this file into each instantiated class
        # root is passed down for a couple uses later. Homepage is used in "Go Back" buttons in ui
        self.current_window = window_class(self.switch_window, self.quit_application, self.root, self.show_homepage)

    # launches the initial homepage
    def show_homepage(self):
        if self.current_window:
            self.current_window.destroy()
        self.switch_window(Homepage)

    # will shut down the python process
    def quit_application(self):
        self.watcher_stop()
        self.current_window.quit()
        self.current_window.destroy()
        self.root.quit()
        self.root.destroy()


def set_scale():
    user32 = ctypes.windll.user32
    user32.SetProcessDpiAwarenessContext(-1)
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    height_ratio = height / 1050
    width_ratio = width / 1680
    scale_to_use = min(height_ratio, width_ratio)

    tk.set_window_scaling(scale_to_use)
    tk.set_widget_scaling(scale_to_use)


# run is withdraw from the taskbar/user access, is only for mainloop. The run instance is actually the base root, but
# nothing happens on it. The whole program is run from toplevel windows.
if __name__ == "__main__":
    set_scale()
    run = tk.CTk()
    run.withdraw()

    app = MainApp(run)
    watcher = MouseInactivityWatcher(run, 30, app)

    run.mainloop()
