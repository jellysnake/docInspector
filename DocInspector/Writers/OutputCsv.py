from datetime import datetime, timezone
from typing import List

from DocInspector.DocStats import DocStats


def outputGenerals(stats: DocStats) -> List[str]:
    """
    Create the general stats in a csv format
    :param stats: The stats to convert
    :return: The general stats in a csv format
    """
    return ["General Stats",
            f"Name, {stats.general.name}",
            f"Creation Date, {stats.general.creationDate}",
            f"Link, https://docs.google.com/document/d/{stats.general.id}/view",
            ""]


def outputIndividuals(stats: DocStats) -> List[str]:
    """
    Create the individual stats table
    :param stats: The source of the stats to use
    :return: The individual stats ina  csv format
    """
    # Create the header rows
    output = ["Individual Stats"
              "Name, Additions, Removals, Changes, Percent"]

    # Create a row for each editor
    for editorId in stats.individuals.getEditors():
        editor = stats.individuals.getEditor(editorId)
        output.append(f"{editor.name}, {editor.additions}, {editor.removals}, {editor.changes}, {editor.percent}")
    return output + [""]


def outputTimeline(stats: DocStats) -> List[str]:
    """
    Creates the timeline for all increments.
    This does not cull increments where nothing happened.

    :param stats: The stats to use for the timeline
    :return: The timeline in csv format
    """
    editorIds = stats.individuals.getEditors()

    # Create the header rows
    output = ["Timeline Stats"
              f"Additions,{','*len(editorIds)},Removals"]
    additionLine = "Date, "
    removalLine = "Date, "
    for editor in editorIds:
        additionLine += stats.individuals.editors[editor].name + ","
        removalLine += stats.individuals.editors[editor].name + ","
    output.append(additionLine + "," + removalLine)

    # Create the timeline rows
    time = stats.timeline.timelineStart
    for increment in stats.timeline.increments:
        # Add the increment date
        additionLine = datetime.fromtimestamp(time / 1000) \
                           .replace(tzinfo=timezone.utc) \
                           .astimezone(tz=None) \
                           .strftime('%d/%m/%Y - %I:%M:%S %p') \
                       + ","
        removalLine = str(additionLine)  # We want a copy not the same
        # Add each editor's additions
        for editor in editorIds:
            if editor in increment.editors:
                additionLine += str(increment.editors[editor].additions or "") + ","
                removalLine += str(increment.editors[editor].removals or "") + ","
            else:
                additionLine += ","
                removalLine += ","
        output.append(removalLine + "," + removalLine)
        time += stats.timeline.incrementSize

    return output


def outputCsv(stats: DocStats) -> str:
    """
    Convert the stats provided into a csv representation of them.
    :param stats: The stats to convert
    :return: A string of all the stats in CSV format
    """
    output = []

    output.extend(outputGenerals(stats))
    output.extend(outputIndividuals(stats))
    output.extend(outputTimeline(stats))

    return "\n".join(output)
