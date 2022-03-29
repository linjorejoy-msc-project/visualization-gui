# Tkinter modules
from tkinter import Tk, Frame, Menu
from tkinter import TOP, BOTH, NSEW

import sys
import time
import socket
import logging
import threading
from typing import List

# Helper Functions
from helperfunctions.logger import write_log
from helpermodules.RequiredObjects import DDSInfo
from pages.MasterPage import MasterPage

# Pages
import pages.StartPage as StartPage
import pages.TestPage as TestPage
import pages.StartServer as StartServer

# Helpermodules
from helpermodules.constants import CURRENT_VERSION, settings_dict
from dds_definition.topics_format import topics


class VisualizationGui(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Global Vars and Constants
        self.server_socket: socket.socket = None
        self.ddsInfoObj: DDSInfo = DDSInfo()
        self.ddsInfoObj.add_topic_info_from_list(topic_list=topics)
        self.topic_info = {}

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

        self.FRAMES = [
            StartPage.StartPage,
            StartServer.StartServer,
            TestPage.TestPage,
        ]

        for FRAME in self.FRAMES:
            frame = FRAME(self.global_container, self)
            self.frames[FRAME] = frame
            frame.grid(row=0, column=0, sticky=NSEW)
        print("Here..")
        print(f"Top : {self.frames}")

        # Add Menu
        self.add_menu()
        self.show_frame(StartServer.StartServer)
        self.set_log_settings()

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

    def set_log_settings(self):
        FORMAT = "%(levelname)-10s %(asctime)s: %(message)s"
        logging.basicConfig(
            filename="src/LOGS/logs.log",
            encoding="utf-8",
            level=logging.DEBUG,
            format=FORMAT,
        )

    def add_log(self, log_type: str, msg: str):
        if log_type == "DEBUG":
            logging.debug(msg)
        elif log_type == "INFO":
            logging.info(msg)
        elif log_type == "WARNING":
            logging.warning(msg)
        elif log_type == "ERROR":
            logging.error(msg)
        elif log_type == "CRITICAL":
            logging.critical(msg)
        else:
            print("None of them")

        # print(self.frames)
        self.frames[StartServer.StartServer].add_log_to_textarea(
            f"{log_type:<10} {time.asctime()}: {msg}\n"
        )


def start_gui():

    app = VisualizationGui()

    def on_close():
        write_log()
        app.destroy()
        exit(0)

    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()


if __name__ == "__main__":
    start_gui()
    # gui_thread = threading.Thread(target=start_gui)
    # gui_thread.start()

    # app = VisualizationGui()

    # def on_close():
    #     write_log()
    #     app.destroy()

    # app.protocol("WM_DELETE_WINDOW", on_close)
    # app.mainloop()
