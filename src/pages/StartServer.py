import json
import socket
import threading
import time

from tkinter import SW, NSEW
from tkinter import scrolledtext
from turtle import width

# from helperfunctions.logger import add_log
from helpermodules.RequiredObjects import Participant, ConfigData

import pages.MasterPage as MasterPage

from widgetclasses.MyButton import MyButton
from widgetclasses.MyLabelFrame import MyLabelFrame

from helperfunctions.serverfunctions import on_new_participant, start_server


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

        self.logs_scrolled_text = None

        self.listening = True
        self.server_started = False
        self.listening_cycle_continue = True
        self.listen_max_times = 5

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

    def set_ui_sublabelframe3(self):
        # self.logs_scrolled_text = scrolledtext.ScrolledText(self.body_sublabelframe3)
        self.logs_scrolled_text = scrolledtext.ScrolledText(
            self.body_sublabelframe3, width=100, height=40, font=("courier", 8)
        )
        self.logs_scrolled_text.pack()
        self.logs_scrolled_text.config(state="disabled")

    def set_ui(self):
        self.set_subframes_bodyframe()
        self.set_ui_sublabelframe1()
        self.set_ui_sublabelframe3()
        self.column_configure_body_frame()
        self.starting_server()
        self.listening_thread = threading.Thread(target=self.listening_function)
        self.listening_thread.start()
        return super().set_ui()

    def starting_server(self):
        self.controller.server_socket = start_server(
            addressFamily=socket.AF_INET,
            socketKind=socket.SOCK_STREAM,
            hostName=socket.gethostname(),
            port=1234,
        )
        self.server_started = True
        for i in range(20):
            self.controller.add_log("INFO", str(self.controller.server_socket))

    def listening_function(self):
        while self.listening:
            # try:
            # if not self.server_started:
            #     self.starting_server()
            participant_socket, address = self.controller.server_socket.accept()
            print(participant_socket)
            config_data = on_new_participant(
                participant_socket=participant_socket, addr=address
            )
            print(f"{config_data=}")
            config_data_obj: ConfigData = ConfigData(
                config_json=json.loads(config_data)
            )

            participantObj: Participant = Participant(
                participant_socket=participant_socket,
                address=address,
                config_data=config_data_obj,
            )

            self.controller.ddsInfoObj.add_subscribed_participant(participantObj)

            participant_handle_thread = threading.Thread(
                target=self.handle_participant, args=(participant_socket,)
            )
            participant_handle_thread.start()
        # except Exception as e:
        #     print(e)

    def handle_participant(self, participant: socket.socket):
        while True:
            print(
                f"Thread for {str(participant)} has started and is listening for msgs"
            )
            break

    def start_listening(self):
        self.listening = True

    def stop_listening(self):
        self.listening = False

    def add_log_to_textarea(self, message: str):

        self.logs_scrolled_text.config(state="normal")
        self.logs_scrolled_text.insert("end", message)
        self.logs_scrolled_text.yview("end")
        self.logs_scrolled_text.config(state="disabled")
