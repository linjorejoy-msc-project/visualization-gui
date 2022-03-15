import json
import socket
import threading
import time
from tkinter import SW, NSEW
from helperfunctions.logger import add_log
from helpermodules.RequiredObjects import Client, ConfigData

import pages.MasterPage as MasterPage

from widgetclasses.MyButton import MyButton
from widgetclasses.MyLabelFrame import MyLabelFrame

from helperfunctions.serverfunctions import on_new_client, start_server


class StartServer(MasterPage.MasterPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.body_sublabelframe1 = None
        self.body_sublabelframe2 = None
        self.body_sublabelframe3 = None

        self.start_server_button = None

        self.start_listening_button = None
        self.stop_listening_button = None
        self.start_listening_cycle_button = None
        self.stop_listening_cycle_button = None

        self.listening = True
        self.listening_cycle_continue = True
        self.listen_max_times = 5

        self.listening_thread = threading.Thread(target=self.listening_function)
        self.listening_thread.start()

        # self.bg_func_thread = threading.Thread(target=self.bg_functions)
        # self.bg_func_thread.start()

        # self.bg_functions()

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

    def column_configure_body_frame(self):
        self.body_label_frame.columnconfigure(0, weight=1)
        self.body_label_frame.columnconfigure(1, weight=1)
        self.body_label_frame.columnconfigure(2, weight=3)

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
            grid=(0, 0),
            anchor=SW,
        )

        self.start_listening_button = MyButton(
            parent=self.body_sublabelframe1,
            controller=self.controller,
            text="Start Listening",
            command=self.start_listening,
            rely=1,
            relx=0,
            x=5,
            y=-5,
            grid=(1, 0),
            anchor=SW,
        )

        self.stop_listening_button = MyButton(
            parent=self.body_sublabelframe1,
            controller=self.controller,
            text="Stop Listening",
            command=self.stop_listening,
            rely=1,
            relx=0,
            x=5,
            y=-5,
            grid=(2, 0),
            anchor=SW,
        )

        self.start_listening_cycle_button = MyButton(
            parent=self.body_sublabelframe1,
            controller=self.controller,
            text="Start Listening For More",
            command=self.start_listening_cycle,
            rely=1,
            relx=0,
            x=5,
            y=-5,
            grid=(3, 0),
            anchor=SW,
        )

        self.stop_listening_cycle_button = MyButton(
            parent=self.body_sublabelframe1,
            controller=self.controller,
            text="Stop Listening For More",
            command=self.stop_listening_cycle,
            rely=1,
            relx=0,
            x=5,
            y=-5,
            grid=(4, 0),
            anchor=SW,
        )

    def set_ui(self):
        self.set_subframes_bodyframe()
        self.set_ui_sublabelframe1()
        self.column_configure_body_frame()
        return super().set_ui()

    def listening_function(self):
        while self.listening:
            client_socket, address = self.controller.server_socket.accept()
            config_data = on_new_client(client_socket=client_socket, addr=address)
            config_data_obj: ConfigData = ConfigData(
                config_json=json.loads(config_data)
            )

            ClientObj: Client = Client(
                client_socket=client_socket,
                address=address,
                config_data=config_data_obj,
            )

            self.controller.clients.add_client(ClientObj)
