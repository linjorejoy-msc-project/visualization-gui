from tkinter import Frame

import visualization_gui_main


class ServerPage(Frame):
    def __init__(self, parent, controller: visualization_gui_main.VisualizationGui):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

    def set_ui(self):
        pass
