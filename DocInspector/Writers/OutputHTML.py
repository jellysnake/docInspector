from datetime import datetime, timezone
from math import ceil
from os import path
from webbrowser import open_new

from DocInspector.DocStats import DocStats

folder = path.dirname(__file__)


def replace_line(old_line, new_line, lines):
    """
    Replace single line in the html file

    :param old_line:    the line to be replaced
    :param new_line:    the line that will replace old_line
    :param lines:       current contents of html file
    :return:            new contents of html file
    """

    edit_index = lines.index(old_line)
    lines[edit_index] = new_line

    return lines


def create_general_stats(stats: DocStats, lines):
    """
    Prints the General Stats of the doc

    :param stats:   data of the given doc
    :param lines:   holds the contents of output html file
    :return:        new contents of output html file
    """

    g_s = stats.general  # general info

    # print title
    lines = replace_line("<!-- GENERAL STATS TITLE -->", "\t\t<title>%s</title>" % g_s.name, lines)

    # print doc name
    lines = replace_line("<!-- GENERAL STATS NAME -->", '\t\t\t\t\t<h1>%s</h1>' % g_s.name, lines)

    # print id
    lines = replace_line("<!-- GENERAL STATS ID -->", '\t\t\t\t\t<td>%s</td>' % g_s.id, lines)

    # print creation date
    creation_date = datetime.strptime(g_s.creationDate, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
        tzinfo=timezone.utc).astimezone(tz=None).strftime(
        '%d/%m/%Y - %I:%M:%S %p')
    lines = replace_line("<!-- GENERAL STATS DATE -->", '\t\t\t\t\t<td>%s</td>' % creation_date, lines)

    # print link
    lines = replace_line("<!-- GENERAL STATS LINK -->", '\t\t\t\t\t<td><a href="%s">%s</a></td>' % (g_s.link, g_s.link),
                         lines)

    return lines


def write_lines(new_lines, lines, edit_index):
    """
    Inserts new lines where specified

    :param new_lines:   the new lines to be added
    :param lines:       holds all the current lines of output html file
    :param edit_index:  the index to insert new lines
    :return:            new contents of output html file
    """

    lines[edit_index:edit_index] = new_lines
    edit_index += len(new_lines)

    return lines, edit_index


def create_timeline(stats: DocStats, lines):
    """
    Print the timeline of revisions

    :param stats:   DocStats object of doc data
    :param lines:   current contents of output html file
    :return:        new contents of html file
    """

    t_s = stats.timeline
    num_increments = t_s.getNumIncrements()

    start_time = t_s.timelineStart

    # find where to fill timeline
    edit_index = lines.index("<!-- TIMELINE CONTENTS -->")
    lines.pop(edit_index)

    # fill timeline
    for i in range(num_increments):
        new_index = edit_index
        inc = t_s.getIncrement(i)

        # skip iteration if no changes
        if len(inc.editors) == 0:
            continue

        dt = start_time + (i * t_s.incrementSize)

        sum_adds = inc.total.additions
        sum_rems = inc.total.removals

        # create container for timeline point
        lines, new_index = write_lines([
            '\t\t\t<div class="container">',
            '\t\t\t\t<div class="content">',
            '\t\t\t\t\t<h2>%s</h2>' % datetime.fromtimestamp(dt / 1000)
                .replace(tzinfo=timezone.utc)
                .astimezone(tz=None)
                .strftime('%d/%m/%Y - %I:%M:%S %p'),
            '\t\t\t\t\t<table width=100% cellpadding="0">'
        ], lines, new_index)

        # fill timeline point with addition/removal info
        for editor in inc.getEditors():
            edits = inc.getEditor(editor)
            adds_percent = ceil((edits.additions / sum_adds) * 100) if sum_adds else 0
            rems_percent = ceil((edits.removals / sum_rems) * 100) if sum_rems else 0
            lines, new_index = write_lines([
                '\t\t\t\t\t\t<tr>',
                '\t\t\t\t\t\t\t<td width=80%%>%s</td>' % inc.getEditor(editor).name,
                '\t\t\t\t\t\t\t<td align="right">%d</td>' % (edits.additions or 0),
                '\t\t\t\t\t\t\t<td width=10% align="right">',
                '\t\t\t\t\t\t\t\t<span class="add_span" style="width:%d%%;">&nbsp</span>' % adds_percent,
                '\t\t\t\t\t\t\t</td>',
                '\t\t\t\t\t\t\t<td width=10% align="left">',
                '\t\t\t\t\t\t\t\t<span class="rem_span" style="width:%d%%;">&nbsp</span>' % rems_percent,
                '\t\t\t\t\t\t\t</td>',
                '\t\t\t\t\t\t\t<td align="right">%d</td>' % (edits.removals or 0),
                '\t\t\t\t\t\t</tr>',
            ], lines, new_index)

        # close container
        lines, new_index = write_lines([
            '\t\t\t\t\t</table>',
            '\t\t\t\t</div>',
            '\t\t\t</div>',
        ], lines, new_index)

    return lines


def create_individual_stats(stats: DocStats, lines):
    i_s = stats.individuals
    editors = i_s.getEditors()

    # create additions graph
    edit_index = lines.index("<!-- ADDITIONS CHART CONTENTS -->")
    lines.pop(edit_index)
    for i in editors:
        editor = i_s.getEditor(i)
        lines, edit_index = write_lines([
            "\t\t\t\t\t\t\t\t['%s', %03d]," % (editor.name, editor.additions or 0),
        ], lines, edit_index)

    # create removals graph
    edit_index = lines.index("<!-- REMOVALS CHART CONTENTS -->")
    lines.pop(edit_index)
    for i in editors:
        editor = i_s.getEditor(i)
        lines, edit_index = write_lines([
            "\t\t\t\t\t\t\t\t['%s', %03d]," % (editor.name, editor.removals or 0),
        ], lines, edit_index)

    # create percentage graph
    edit_index = lines.index("<!-- PERCENTAGE CHART CONTENTS -->")
    lines.pop(edit_index)
    for i in editors:
        editor = i_s.getEditor(i)
        lines, edit_index = write_lines([
            "\t\t\t\t\t\t\t\t['%s', %03d]," % (editor.name, editor.percent or 0),
        ], lines, edit_index)

    return lines


def outputHTML(stats: DocStats):
    # get contents from template
    file_path = path.abspath(folder + "/templates/doc_template.html")
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
    # create general stats, individual stats and timeline
    lines = create_general_stats(stats, lines)
    lines = create_individual_stats(stats, lines)
    lines = create_timeline(stats, lines)

    return "\n".join(lines)
