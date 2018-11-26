from datetime import datetime, timezone
from typing import Iterable, List

from DocInspector.DocStats import DocStats


def outputGenerals(stats: DocStats):
    """
    Create the general file section of the stats
    :param stats: The stats to use to build the general section
    :return: A list containing each line of the output
    """
    return ["--- General Stats ---",
            f"Name:           {stats.general.name}",
            f"Creation Date:  {stats.general.creationDate}",
            f"Link:           https://docs.google.com/document/d/{stats.general.id}/view",
            ""]


def findMaxWidth(array: Iterable[str]) -> int:
    """
    Find the longest string in a given list
    :param array: The list to search through
    :return: The length of the longest string in the list
    """
    return len(max(array, key=len))


def getEditorStat(stats: DocStats, attribute: str) -> List[str]:
    """
    Get a given stat from all the editors
    :param stats: The stats object containing the editors to seach through
    :param attribute: The attribute to collate
    :return: A list of that attribute for each editor
    """
    editors = map(lambda editor: str(editor.__dict__[attribute] or "N/A"), stats.individuals.editors.values())
    return list(editors)


def outputIndividual(stats: DocStats):
    """
    Create the individual section of the stats
    :param stats: The stats to use to build the individual table
    :return: A list containing each line of the output
    """
    editors = getEditorStat(stats, "name")
    editorWidth = findMaxWidth(editors + ["Name"])
    additions = getEditorStat(stats, "additions")
    additionWidth = findMaxWidth(additions + ["Additions"])
    removals = getEditorStat(stats, "removals")
    removalWidth = findMaxWidth(removals + ["Removals"])
    changes = getEditorStat(stats, "changes")
    changesWidth = findMaxWidth(changes + ["Changes"])
    percent = getEditorStat(stats, "percent")
    percentWidth = findMaxWidth(percent + ["Percent"])

    output = [
        "--- Individual Stats ---",
        f"┌─{'─'*editorWidth}─┬─{'─'*additionWidth}─"
        f"┬─{'─'*removalWidth}─┬─{'─'*changesWidth}─┬─{'─'*percentWidth}─┐",

        "│ {0: ^{1}} │ {2: ^{3}} │ {4: ^{5}} │ {6: ^{7}} │ {8: ^{9}} │"
            .format("Name", editorWidth, "Additions", additionWidth,
                    "Removals", removalWidth, "Changes", changesWidth, "Percent", percentWidth),

        f"├─{'─'*editorWidth}─┼─{'─'*additionWidth}─"
        f"┼─{'─'*removalWidth}─┼─{'─'*changesWidth}─┼─{'─'*percentWidth}─┤",
    ]

    for i in range(len(editors)):
        output.append("│ {0: <{1}} ".format(editors[i], editorWidth)
                      + "│ {0: <{1}} ".format(additions[i], additionWidth)
                      + "│ {0: <{1}} ".format(removals[i], removalWidth)
                      + "│ {0: <{1}} ".format(changes[i], changesWidth)
                      + "│ {0: <{1}} │".format(percent[i], percentWidth))

    output.append(
        f"└─{'─'*editorWidth}─┴─{'─'*additionWidth}─"
        f"┴─{'─'*removalWidth}─┴─{'─'*changesWidth}─┴─{'─'*percentWidth}─┘", )
    return output + [""]


def buildEntry(i, dates, editorIds, editorAdditions, editorRemovals, dateWidth, editorWidths):
    """
    Build a row entry for an increment
    :param i: The increment number
    :param dates: All the dates of increments
    :param editorIds: The id's of each editor
    :param editorAdditions: The number of additions, per editor, per increment
    :param editorRemovals: The number of removals, per editor, per increment
    :param dateWidth: The width of the date column
    :param editorWidths: The width of each editors column
    :return: The two lines that make up this increment's row
    """
    # Add the additions
    date, time = dates[i].split('\n')
    additions = "│ {0: ^{1}} ".format(date, dateWidth)
    for editor in editorIds:
        additions += "│ {0: ^{1}} ".format(editorAdditions[editor][i], editorWidths[editor])
    additions += "│"

    # Then the removals
    removals = "│ {0: ^{1}} ".format(time, dateWidth)
    for editor in editorIds:
        removals += "│ {0: ^{1}} ".format(editorRemovals[editor][i], editorWidths[editor])
    removals += "│"

    if i < len(dates) - 1 and dates[i + 1]:
        # Then the row seperator if the next entry isn't blank
        last = f"├─{'─'*dateWidth}─"
        for editor in editorIds:
            last += f"┼─{'─'*editorWidths[editor]}─"
        last += "┤"
        return [additions, removals, last]
    else:
        return additions, removals


def buildRowBorder(start, middle, end, spacer, dateWidth, editorWidths, editorIds):
    """
    Create a row border line.
    :param start: The character to use at the start
    :param middle: The character to use for each middle column
    :param end: The character to use at the end
    :param spacer: The character to use for each cell ceiling/floor
    :param dateWidth: The width of the date column
    :param editorWidths: The width of each editors column
    :param editorIds: The ids of each editor
    :return:
    """
    line = start + spacer * (dateWidth + 2)
    for editor in editorIds:
        line += middle + spacer * (editorWidths[editor] + 2)
    return line + end


def loadFromIncrements(stats: DocStats):
    """
    Converts the stats from the DocStats format into something more suited for being turned into a timeline

    :param stats: The stats to use to build the timeline
    :return: Multiple lists containing collated data for each column
    """
    editorIds = stats.individuals.editors.keys()
    dates = []
    editorAdditions = {id: [] for id in editorIds}
    editorRemovals = {id: [] for id in editorIds}
    editorNames = {id: stats.individuals.editors[id].name for id in editorIds}

    # Collect the data from increments
    time = stats.timeline.timelineStart
    for increment in stats.timeline.increments:
        if len(increment.editors):
            # Append the date
            dates.append(datetime.fromtimestamp(time / 1000)
                         .replace(tzinfo=timezone.utc)
                         .astimezone(tz=None)
                         .strftime('%d/%m/%Y\n%I:%M:%S %p'))

            for editor in editorIds:
                if editor in increment.editors:
                    # Append the data or N/A if it's None
                    editorAdditions[editor].append(
                        ("+" + str(increment.editors[editor].additions) or "N/A"))
                    editorRemovals[editor].append(
                        ("-" + str(increment.editors[editor].removals) or "N/A"))
                else:
                    # Editor did nothing, so make them blank
                    editorAdditions[editor].append("")
                    editorRemovals[editor].append("")
        else:
            # Nothing happened so make them blank
            dates.append("")
            for editor in editorIds:
                editorAdditions[editor].append("")
                editorRemovals[editor].append("")
        time += stats.timeline.incrementSize
    return dates, editorIds, editorAdditions, editorRemovals, editorNames


def calculateWidths(dates, editorIds, editorAdditions, editorRemovals, editorNames):
    """
    Calculate the width of the columns based on the data they will contain
    :param dates: All the dates of increments
    :param editorIds: The id's of each editor
    :param editorAdditions: The number of additions, per editor, per increment
    :param editorRemovals: The number of removals, per editor, per increment
    :param editorNames: The names of each editor
    :return: The width of the dates column and the width of each editor's column
    """
    dateWidth = findMaxWidth(
        [date.split('\n')[0] for date in dates if date]
        + [date.split('\n')[1] for date in dates if date]
        + ['Date']
    )
    editorWidths = {}
    for editor in editorIds:
        editorWidths[editor] = findMaxWidth(
            editorRemovals[editor]
            + editorAdditions[editor]
            + [editorNames[editor]])
    return dateWidth, editorWidths


def buildTimelineTable(dates, editorIds, editorAdditions, editorRemovals, editorNames, dateWidth, editorWidths):
    """
    Build the visual timeline given the stats to include
    :param dates: All the dates of increments
    :param editorIds: The id's of each editor
    :param editorAdditions: The number of additions, per editor, per increment
    :param editorRemovals: The number of removals, per editor, per increment
    :param editorNames: The names of each editor
    :param dateWidth: The width of the dates column, in characters
    :param editorWidths:  THe width of each editor's column, in characters
    :return:
    """
    output = ["--- Timeline Stats ---",
              buildRowBorder("┌", "┬", "┐", "─", dateWidth, editorWidths, editorIds)]

    header = "│ {0: ^{1}} ".format("Date", dateWidth)
    for editor in editorIds:
        header += "│ {0: ^{1}} ".format(editorNames[editor], editorWidths[editor])
    output.append(header + "│")

    if dates[0]:
        output.append(buildRowBorder("╞", "╪", "╡", "═", dateWidth, editorWidths, editorIds))
    else:
        output.append(buildRowBorder("/", "/", "/", "═", dateWidth, editorWidths, editorIds))

    # Build the entries
    blankAdded = False
    for i in range(len(dates)):
        if dates[i]:
            # Add the additions
            output.extend(
                buildEntry(i, dates, editorIds, editorAdditions, editorRemovals, dateWidth, editorWidths))

            # Reset the blank counter
            blankAdded = False

        elif not blankAdded:
            # Insert a blank entry marker
            blankAdded = True
            if i != 0:
                output.append(buildRowBorder("/", "/", "/", "─", dateWidth, editorWidths, editorIds))
            output.append(buildRowBorder("┆", "┆", "┆", " ", dateWidth, editorWidths, editorIds))
            if i < len(dates) - 1:
                output.append(buildRowBorder("/", "/", "/", "─", dateWidth, editorWidths, editorIds))

    # Add in the final row
    output.append(buildRowBorder("└", "┴", "┘", "─", dateWidth, editorWidths, editorIds))
    return output


def outputTimeline(stats: DocStats):
    """
    Create the timeline section of the stats
    :param stats: The stats to use to build the timeline
    :return: A list containing each line of the output
    """
    incrementStats = list(loadFromIncrements(stats))
    return buildTimelineTable(*(
            incrementStats
            + list(calculateWidths(*incrementStats))))


def outputPlain(stats: DocStats):
    """
    Convert the stats collected into a plain visual format.
    :param stats: The stats to output
    :return: A string that contains the data in plain format
    """
    output = []

    output.extend(outputGenerals(stats))
    output.extend(outputIndividual(stats))
    output.extend(outputTimeline(stats))

    return "\n".join(output)
