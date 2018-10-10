from datetime import datetime
from math import floor


def timeToMilli(time):
    """
    Converts from a google revision timestamp into milliseconds since the Epoch

    :param time: The timestamp to convert
    :return: The timestamp in milliseconds
    """
    return datetime.strptime(time,
                             "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()


def calculateTimelineStart(start, incrementSize):
    """
    Calculates the time to start the first revision at
    :param start: The current start time
    :param incrementSize: The size of the increments
    :return: start, rounded down to the nearest increment
    """
    return floor(start / incrementSize) * incrementSize
