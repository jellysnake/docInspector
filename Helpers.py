from datetime import datetime


def timeToMilli(time):
    """
    Converts from a google revision timestamp into milliseconds since the Epoch

    :param time: The timestamp to convert
    :return: The timestamp in milliseconds
    """
    return datetime.strptime(time,
                             "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
