from datetime import datetime, timedelta
from os import mkdir, path
from webbrowser import open_new
from math import ceil

from DocStats import DocStats


OUTPUT_DIR = "output/"
TEMPLATE_FILE = "templates/doc_template.html"


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

    gi = stats.general  # general info

    # print title
    lines = replace_line("<!-- GENERAL STATS TITLE -->", "\t\t<title>%s</title>" % gi.name, lines)

    # print doc name
    lines = replace_line("<!-- GENERAL STATS NAME -->", '       <h1>%s</h1>' % gi.name, lines)

    # print id
    lines = replace_line("<!-- GENERAL STATS ID -->", '               <td class="gs_td">%s</td>' % gi.id, lines)

    # print creation date
    creation_date = datetime.strptime(gi.creationDate, "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%d/%m/%Y - %I:%M:%S %p')
    lines = replace_line("<!-- GENERAL STATS DATE -->", '               <td class="gs_td">%s</td>' % creation_date, lines)

    # print link
    lines = replace_line("<!-- GENERAL STATS LINK -->", '               <td class="gs_td"><a href="%s">%s</a></td>' % (gi.link, gi.link), lines)

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


def create_timeline(stats: DocStats, args, lines):
    """
    Print the timeline of revisions

    :param stats:   DocStats object of doc data
    :param args:    arguments from commandline
    :param lines:   current contents of output html file
    :return:        new contents of html file
    """

    timeline_stats = stats.timeline
    num_increments = timeline_stats.getNumIncrements()

    # time increment size
    ti = list(map(int, args.timeIncrement.split(':')))
    ti = timedelta(days=ti[0], hours=ti[1], minutes=ti[2])

    # start date/time to display (either date/time of last increment or now)
    if args.dates:      # define start date/time
        temp_dates = args.dates.split('/')
        dt = datetime.strptime(temp_dates[1], '%Y-%m-%d')
    else:               # if start date/time not given then start from now
        dt = datetime.now()

    # find where to fill timeline
    edit_index = lines.index("<!-- TIMELINE CONTENTS -->")
    lines.pop(edit_index)

    # fill timeline
    for i in reversed(range(num_increments)):
        adds = timeline_stats.getIncrement(i).additions
        rems = timeline_stats.getIncrement(i).removals

        # skip iteration if no changes
        if len(adds) == 0 and len(rems) == 0:
            dt -= ti
            continue

        # convert into more suitable format
        changes = {}
        for k, v in adds.items():
            if k in rems:
                changes.update({k: [v, rems[k]]})
            else:
                changes.update({k: [v, 0]})
        for k, v in rems.items():
            if k not in rems:
                changes.update({k: [0, v]})
        sum_adds = sum(adds.values())
        sum_rems = sum(rems.values())

        # create container for timeline point
        lines, edit_index = write_lines([
            '           <div class="container">',
            '               <div class="content">',
            '                   <h2>%s</h2>' % dt.strftime('%d/%m/%Y - %I:%M:%S %p'),
            '                   <table width=100% cellpadding="0">'
        ], lines, edit_index)

        # fill timeline point with addition/removal info
        for editor, amount in changes.items():
            adds_percent = ceil((amount[0]/sum_adds)*100) if sum_adds != 0 else 100
            rems_percent = ceil((amount[0]/sum_adds)*100) if sum_rems != 0 else 100
            lines, edit_index = write_lines([
                "                       <tr>",
                "                           <td width=80%%>%s</td>" % editor,
                '                           <td width=10% align="right">',
                '                               <span class="add_span" style="width:%d%%;">&nbsp</span>' % adds_percent,
                "                           </td>",
                '                           <td width=10% align="left">',
                '                               <span class="rem_span" style="width:%d%%;">&nbsp</span>' % rems_percent,
                "                           </td>",
                "                       </tr>",
            ], lines, edit_index)

        # close container
        lines, edit_index = write_lines([
            '                   </table>',
            '               </div>',
            '           </div>',
        ], lines, edit_index)

        dt -= ti

    return lines


def outputStats(stats: DocStats, args):
    f_name = stats.general.name

    # create the 'output' directory if it doesn't already exist
    try:
        mkdir(OUTPUT_DIR)
    except Exception:
        pass

    # get contents from template
    file_path = path.abspath(TEMPLATE_FILE)
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()

    # create general stats, timeline
    lines = create_general_stats(stats, lines)
    lines = create_timeline(stats, args, lines)

    # create file and write contents
    file_path = path.abspath(OUTPUT_DIR + f_name + ".html")
    with open(file_path, 'w') as f:
        for line in lines:
            f.write("%s\n" % line)

    # open in browser
    open_new(file_path)
