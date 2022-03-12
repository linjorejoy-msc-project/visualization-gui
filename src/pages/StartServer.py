from tkinter import SW, NSEW

import pages.MasterPage as MasterPage

from widgetclasses.MyButton import MyButton
from widgetclasses.MyLabelFrame import MyLabelFrame

from helperfunctions.serverfunctions import start_server


class StartServer(MasterPage.MasterPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.body_sublabelframe1 = None

        self.body_sublabelframe2 = None

        self.body_sublabelframe3 = None

        self.start_server_button = None

    def set_subframes_bodyframe(self):
        self.body_sublabelframe1 = MyLabelFrame(
            parent=self.body_label_frame,
            controller=self.controller,
            text="Menu",
            height="600",
            grid=(0, 0),
            sticky=NSEW,
        )

        self.body_sublabelframe2 = MyLabelFrame(
            parent=self.body_label_frame,
            controller=self.controller,
            text="Info",
            height="600",
            grid=(0, 1),
            sticky=NSEW,
        )

        self.body_sublabelframe3 = MyLabelFrame(
            parent=self.body_label_frame,
            controller=self.controller,
            text="Logs",
            height="600",
            grid=(0, 2),
            sticky=NSEW,
        )

    def set_ui_sublabelframe1(self):
        self.start_server_button = MyButton(
            parent=self.body_sublabelframe1,
            controller=self.controller,
            text="Start Server",
            command=self.starting_server,
            rely=1,
            relx=0,
            x=5,
            y=-5,
            anchor=SW,
        )

    def column_configure_body_frame(self):
        self.body_label_frame.columnconfigure(0, weight=1)
        self.body_label_frame.columnconfigure(1, weight=1)
        self.body_label_frame.columnconfigure(2, weight=3)

    def set_ui(self):
        self.set_subframes_bodyframe()
        self.set_ui_sublabelframe1()
        self.column_configure_body_frame()
        return super().set_ui()

    def starting_server(self):
        self.controller.server_socket = start_server()
        print(self.controller.server_socket)
