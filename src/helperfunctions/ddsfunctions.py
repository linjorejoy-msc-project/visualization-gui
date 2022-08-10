import socket
import json
from typing import List

from helpermodules.RequiredObjects import DDSInfo

# Constants
topics = [
    {"name": "fuel_flow", "regex": ""},
    {"name": "thrust", "regex": ""},
    {"name": "drag", "regex": ""},
    {"name": "motion", "regex": ""},
    {"name": "field", "regex": ""},
    {"name": "field_update", "regex": ""},
    {"name": "atmosphere", "regex": ""},
    {"name": "motion_update", "regex": ""},
]


# DDS Enabling Functions
def print_initial_info():
    print("Server is going to start")


# Topics func
def set_topics(dds_info_object: DDSInfo):
    dds_info_object.add_topic_info_from_list(topic_list=topics)


def instantiate_dds(dds_info_object):
    print_initial_info()
    set_topics(dds_info_object)
