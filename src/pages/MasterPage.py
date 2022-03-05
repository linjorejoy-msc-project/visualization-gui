from tkinter import Frame, LabelFrame
from tkinter import N

import visualization_gui_main
from widgetclasses.MyLabelFrame import MyLabelFrame


class StartPage(Frame):
    def __init__(self, parent, controller: visualization_gui_main.VisualizationGui):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.header_label_frame = MyLabelFrame(
            self, self.controller, text="Preferences", height="80", expand=N
        )

        self.body_label_frame = MyLabelFrame(
            self, self.controller, text="Options", height="500", expand=True
        )

        self.footer_label_frame = MyLabelFrame(
            self, self.controller, text="Options", height="50", expand=N
        )

    def set_ui(self):
        pass
