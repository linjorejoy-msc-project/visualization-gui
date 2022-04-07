import socket
import threading
import json
from typing import List
from inputimeout import inputimeout, TimeoutOccurred
import logging

from helpermodules.RequiredObjects import ConfigData, DDSInfo, Participant
from helpermodules.constants import HEADERSIZE

from helperfunctions.serverfunctions2 import (
    start_server,
    format_msg_with_header,
    recv_msg,
)
from helperfunctions.ddsfunctions import instantiate_dds

# Logging

FORMAT = "%(levelname)-10s %(asctime)s: %(message)s"
logging.basicConfig(
    filename="src/LOGS/logs.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format=FORMAT,
    filemode="w",
)

# DDS
server_socket: socket.socket = start_server()
dds_info_object: DDSInfo = DDSInfo()

# Constants
CONSTANTS = {}

# Variables
constants_set = False
analysis_started = False

# Required Lists
participant_list: List[Participant] = []


def broadcast_message(msg: str):
    for each_participant in dds_info_object.get_participant_list():
        each_participant.get_participant_socket().send(format_msg_with_header(msg))


def send_info_to_subscribers(info: str, from_participant: Participant):
    topic = info[:25].strip()
    # logging.info(
    #     f"{from_participant.config_data.name} send {info} and its topic recognized as {topic=}"
    # )
    topic_obj = dds_info_object.get_topic_by_name(topic)
    # if topic_obj:
    #     logging.info(f"For {topic=} found topic_obj: {topic_obj.topic_name=}")
    # else:
    #     logging.error(f"Received {topic=} from ")
    # TODO: check if asked for a variable

    if topic_obj:
        logging.info(f"{format_msg_with_header(info)=}\nsent to subscribers")
        for each_participant in topic_obj.get_subscribed_participants():
            # logging.debug(
            #     f"{format_msg_with_header(info)=}\nsent to {each_participant.config_data.name}"
            # )
            each_participant.get_participant_socket().send(format_msg_with_header(info))
    else:
        logging.error(f"The topic: {topic} does not have an object")


def set_constants(fields_participant_obj: Participant):
    global constants_set
    global CONSTANTS
    # logging.info(
    #     f"Sending to {fields_participant_obj.config_data.name} the literal 'CONSTANTS' as :{format_msg_with_header('CONSTANTS')}"
    # )
    fields_participant_obj.participant_socket.send(format_msg_with_header("CONSTANTS"))
    constants_str = recv_msg(fields_participant_obj.participant_socket)
    # logging.info(f"Constants should be received {constants_str=}")
    CONSTANTS = json.loads(constants_str)
    constants_set = True


def send_constants(participant_obj: Participant):
    while True:
        msg = recv_msg(participant_obj.get_participant_socket())
        # logging.info(f"Waiting for requesting constants and received {msg=}")
        if msg == "CONSTANTS":
            constants_dict = {}
            for each_constant in participant_obj.config_data.constants_required:
                constants_dict[each_constant] = CONSTANTS[each_constant]
            # logging.info(
            #     f"Sending to {participant_obj.config_data.name} the constants dictionary\n{format_msg_with_header(json.dumps(constants_dict))}"
            # )
            participant_obj.get_participant_socket().send(
                format_msg_with_header(json.dumps(constants_dict))
            )
            break


def handle_participant(participant_obj: Participant):
    global analysis_started
    global constants_set

    # logging.info(f"Inside handle Participant with {analysis_started=}")
    if participant_obj.config_data.name == "field":
        # logging.info(
        #     f"Participant Field should be Received {participant_obj.config_data.name=}"
        # )
        set_constants(participant_obj)
        constants_set = True

    # Setting Constants
    # logging.info(f"{participant_obj.config_data.name=} ran and {constants_set=}")
    if constants_set and participant_obj.config_data.name != "field":
        # logging.info(f"Send constants to : {participant_obj.config_data.name}")
        send_constants(participant_obj)

    # Start Analysis
    """ if analysis_started start the while loop which send "START" to all participants
    then start listening and for each info run send_info_to_subscribers()
    """
    # Start analysis msg send
    while True:
        # time.sleep(1)
        if analysis_started:
            # logging.info(
            #     f"Analysis started and the message :\n{format_msg_with_header('START')}\nwas sent to {participant_obj.config_data.name}"
            # )
            participant_obj.get_participant_socket().send(
                format_msg_with_header("START")
            )
            break
        # logging.info(f"{participant_obj.config_data.name} waiting to start analysis")

    # Start Analysis
    # logging.info("#" * 20)
    # logging.info("\n" * 10)
    # logging.info("#" * 20)
    logging.info(f"Analysis while loop started for {participant_obj.config_data.name}")
    while True:
        info = recv_msg(participant_obj.get_participant_socket())
        # logging.info(f"{participant_obj.config_data.name}:-{info=}")
        send_info_to_subscribers(info, participant_obj)


def request_analysis_start(new_participant_address):
    global analysis_started
    try:
        # logging.info(f"{new_participant_address} waiting for reply to start Analysis")
        answer = inputimeout(prompt="To start Analysis, type'y': ", timeout=5)
    except TimeoutOccurred:
        # logging.info(f"{new_participant_address} stopped requesting")
        answer = "n"
    if answer == "y" or answer == "Y":
        analysis_started = True
    else:
        return


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


def instantiate_participant(
    participant_socket: socket.socket, participant_address, config_str: str
):
    this_participant_obj = save_data_of_participant(
        participant_socket, participant_address, config_str
    )

    this_participant_thread = threading.Thread(
        target=handle_participant, args=(this_participant_obj,)
    )
    this_participant_thread.start()


def start_server_listening():
    global server_socket

    logging.info("start_server_listening while loop started")
    while not analysis_started:
        # New Participant
        new_participant, new_participant_address = server_socket.accept()
        logging.info(f"Found {new_participant_address}: {new_participant}")

        # Config
        new_participant.send(format_msg_with_header("CONFIG"))
        config_str = recv_msg(new_participant)

        if config_str:
            instantiate_participant(
                new_participant, new_participant_address, config_str
            )
        else:
            logging.error(f"Expected Config but receied {config_str=}")

        request_analysis_start(new_participant_address)


def main():
    global dds_info_object

    instantiate_dds(dds_info_object)

    listening_thread = threading.Thread(target=start_server_listening)
    listening_thread.start()


if __name__ == "__main__":
    main()
