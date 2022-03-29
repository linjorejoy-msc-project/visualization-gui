import socket
import threading
import json
from typing import List

from helpermodules.RequiredObjects import ConfigData, DDSInfo, Participant
from helpermodules.constants import HEADERSIZE

from helperfunctions.serverfunctions2 import (
    start_server,
    format_msg_with_header,
    recv_msg,
)
from helperfunctions.ddsfunctions import instantiate_dds

# DDS
server_socket: socket.socket = start_server()
dds_info_object: DDSInfo = DDSInfo()

# Constants
CONSTANTS = {}

# Variables
constants_set = False

# Required Lists
participant_list: List[Participant] = []


def save_data_of_participant(
    participant_socket: socket.socket, participant_address, config_str: str
):
    config_json = json.loads(config_str)
    config_data_obj = ConfigData(config_json=config_json)
    this_participant_obj = Participant(
        participant_socket=participant_socket,
        address=participant_address,
        config_data=config_data_obj,
    )
    dds_info_object.add_subscribed_participant(this_participant_obj)
    return this_participant_obj


def send_info_to_subscribers(info, from_participant: Participant):
    for each_participant in dds_info_object.get_participant_list():
        if from_participant is not each_participant:
            each_participant.participant_socket.send(format_msg_with_header(info))


def set_constants(fields_participant_obj: Participant):
    global constants_set
    global CONSTANTS
    fields_participant_obj.participant_socket.send(format_msg_with_header("CONSTANTS"))
    constants_str = recv_msg(fields_participant_obj.participant_socket)
    print(f"Received constants str \n{constants_str=}")
    CONSTANTS = json.loads(constants_str)
    constants_set = True


def send_constants(participant_obj: Participant):
    while True:
        msg = recv_msg(participant_obj.get_participant_socket())
        if msg == "CONSTANTS":
            constants_dict = {}
            for each_constant in participant_obj.config_data.constants_required:
                # TODO
                constants_dict[each_constant] = CONSTANTS[each_constant]
            participant_obj.get_participant_socket().send(
                format_msg_with_header(json.dumps(constants_dict))
            )
            break


def handle_participant(participant_obj: Participant):
    print(f"Thread started for {participant_obj.participant_socket}")

    if participant_obj.config_data.name == "fields":
        set_constants(participant_obj)

    if constants_set:
        send_constants(participant_obj)

    while True:
        new_info = recv_msg(participant_obj.participant_socket)
        send_info_to_subscribers(new_info, participant_obj.participant_socket)


def instantiate_participant(
    participant_socket: socket.socket, participant_address, config_str: str
):
    global constants_set
    this_participant_obj = save_data_of_participant(
        participant_socket, participant_address, config_str
    )

    this_participant_thread = threading.Thread(
        target=handle_participant, args=(this_participant_obj,)
    )
    this_participant_thread.start()


def start_server_listening():
    global server_socket
    while True:
        new_participant, new_participant_address = server_socket.accept()

        # Request Config Data
        new_participant.send(format_msg_with_header("CONFIG"))

        # Receiving Config data
        config_str = recv_msg(new_participant)
        print(f"{config_str=}")
        if config_str:
            instantiate_participant(
                new_participant, new_participant_address, config_str
            )
        else:
            print(f"Config Not Received {config_str=}")


def main():
    global dds_info_object
    instantiate_dds(dds_info_object)
    # Threads
    listening_thread = threading.Thread(target=start_server_listening)

    # Starting threads
    listening_thread.start()


if __name__ == "__main__":
    main()
