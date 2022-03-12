# Tkinter modules
from tkinter import Tk, Frame, Menu
from tkinter import TOP, BOTH, NSEW

# Pages
import pages.StartPage as StartPage
import pages.TestPage as TestPage
import pages.StartServer as StartServer

# Helpermodules
from helpermodules.constants import CURRENT_VERSION, settings_dict


class VisualizationGui(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Global Vars and Constants
        self.server_socket = None

        # Storing Frames
        self.frames = {}
        self.pages_navigation_history = []

        # Setting UI
        # Tk.iconbitmap(self, default=ICON)
        Tk.wm_title(self, f"Visualization {CURRENT_VERSION}")

        # Global Variables
        SCREEN_RATIO = settings_dict["screenRatio"]
        if not (0.7 < SCREEN_RATIO < 1):
            SCREEN_RATIO = 0.85
        Tk.geometry(self, self.get_screen_dimentions(SCREEN_RATIO))

        # Global Container
        self.global_container = Frame(self)
        self.global_container.pack(side=TOP, fill=BOTH, expand=True)

        self.global_container.grid_rowconfigure(0, weight=1)
        self.global_container.columnconfigure(0, weight=1)

        FRAMES = [StartPage.StartPage, StartServer.StartServer, TestPage.TestPage]

        for FRAME in FRAMES:
            frame = FRAME(self.global_container, self)
            self.frames[FRAME] = frame
            frame.grid(row=0, column=0, sticky=NSEW)

        # Add Menu
        self.add_menu()
        self.show_frame(StartServer.StartServer)

    def get_screen_dimentions(self, ratio: float = 0.8):

        ScreenSizeX = self.winfo_screenwidth()
        ScreenSizeY = self.winfo_screenheight()
        ScreenRatio = ratio
        FrameSizeX = int(ScreenSizeX * ScreenRatio)
        FrameSizeY = int(ScreenSizeY * ScreenRatio)
        FramePosX = int((ScreenSizeX - FrameSizeX) / 10)
        FramePosY = int((ScreenSizeY - FrameSizeY) / 10)

        return f"{FrameSizeX}x{FrameSizeY}+{FramePosX}+{FramePosY}"

    def add_menu(self):
        menu = Menu(self)
        self.config(menu=menu)

        # File Menu
        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Quit", command=self.quit)

    def show_frame(self, FrameName):
        frame = self.frames[FrameName]
        self.pages_navigation_history.append(frame)
        frame.tkraise()
        frame.set_ui()

    def go_back(self):
        self.pages_navigation_history.pop()
        prev_frame = self.pages_navigation_history[
            len(self.pages_navigation_history) - 1
        ]
        prev_frame.tkraise()


if __name__ == "__main__":

    app = VisualizationGui()
    app.mainloop()
