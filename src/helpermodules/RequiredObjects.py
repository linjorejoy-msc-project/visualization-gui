import socket
import logging

from typing import List, Dict

FORMAT = "%(levelname)-10s %(asctime)s: %(message)s"
logging.basicConfig(
    handlers=[
        logging.FileHandler(filename="src/LOGS/logs.log", encoding="utf-8", mode="w")
    ],
    level=logging.DEBUG,
    format=FORMAT,
)


class MessageData:
    def __init__(self) -> None:
        self.from_participant
        self.topic
        self.msg


class ConfigData:
    def __init__(
        self,
        config_json: dict = {},
        id: str = "",
        name: str = "",
        subscribed_topics: List[str] = [],
        published_topics: List[str] = [],
        constants_required: List[str] = [],
        variables_subscribed: List[str] = [],
    ) -> None:
        if config_json:
            self.id = config_json["id"]
            self.name = config_json["name"]
            self.subscribed_topics = config_json["subscribed_topics"]
            self.published_topics = config_json["published_topics"]
            self.constants_required = config_json["constants_required"]
            self.variables_subscribed = config_json["variables_subscribed"]
        else:
            self.id = id
            self.name = name
            self.subscribed_topics = subscribed_topics
            self.published_topics = published_topics
            self.constants_required = constants_required
            self.variables_subscribed = variables_subscribed


class Participant:
    def __init__(
        self,
        participant_socket: socket.socket,
        address,
        config_data: ConfigData,
    ) -> None:
        self.participant_socket = participant_socket
        self.address = address
        self.config_data = config_data

    def get_participant_socket(self):
        return self.participant_socket

    def is_subscribed_to_topic(self, topic: str):
        return topic in self.config_data.subscribed_topics


class Topic:
    def __init__(self, topic_name: str) -> None:
        self.topic_name = topic_name
        self.regex_format = ""
        self.subscribed_participants: List[Participant] = []
        self.messages: List[MessageData] = []

    def add_subscribed_participant(self, participant: Participant):
        # TODO
        self.subscribed_participants.append(participant)

    def get_subscribed_participants(self):
        return self.subscribed_participants


class DDSInfo:
    def __init__(self) -> None:
        self.topics: List[Topic] = []
        self.participants: List[Participant] = []

    def get_participant_list(self):
        return self.participants

    def get_participant_by_socket(self):
        pass

    def add_subscribed_participant(self, participant: Participant):
        self.participants.append(participant)
        self.add_participant_info_to_topics(participant)

    def remove_subscribed_participant(self, participant: Participant):
        self.participants.remove(participant)

    def add_topic_info_from_list(self, topic_list: List[Dict[str, str]]):
        for topic_dict in topic_list:
            logging.info(f"{topic_dict} conveted to object")
            this_topic_obj = Topic(topic_dict["name"])
            this_topic_obj.regex_format = topic_dict["regex"]
            self.topics.append(this_topic_obj)

    def get_topic_by_name(self, name: str):
        for topic in self.topics:
            if topic.topic_name == name:
                return topic
        return

    def add_participant_info_to_topics(self, participant: Participant):
        for topic_name in participant.config_data.subscribed_topics:
            this_topic_obj = self.get_topic_by_name(topic_name)
            if this_topic_obj:
                this_topic_obj.add_subscribed_participant(participant)
            else:
                print(f"{topic_name} does not have a topic object")
