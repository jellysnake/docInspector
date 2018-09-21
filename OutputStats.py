from datetime import datetime, timedelta
from os import mkdir, path
from webbrowser import open_new
from DocStats import DocStats


OUTPUT_DIR = "output"


def outputStats(stats: DocStats, args):
    f_name = stats.general.name
    timeline_stats = stats.timeline

    # time increment
    ti = datetime.strptime(args.timeIncrement, "%H:%M:%S")
    ti = timedelta(hours=ti.hour, minutes=ti.minute, seconds=ti.second)

    # start date/time to display (either date/time of first increment or creation date)
    if args.dates:      # define start date/time
        temp_dates = args.dates.split('/')
        dt = datetime.strptime(temp_dates[0], '%Y-%m-%d')
        end_dt = datetime.strptime(temp_dates[1], '%Y-%m-%d')
    else:           # if start date/time not given then start from creation date
        dt = datetime.strptime(stats.general.creationDate, '%Y-%m-%dT%H:%M:%S.%fZ')

    # create the 'output' directory
    try:
        mkdir(OUTPUT_DIR)
    except Exception:
        pass

    # create file and open for editing
    file_path = path.join(OUTPUT_DIR, f_name + "_timeline.html")
    file = open(file_path, 'w')
    file.write(f"""
        <html>
            <head>
                <title>{f_name} Timeline</title>
                <style>
                    html {{
                        font-family: sans-serif;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 50%;
                    }}
                    th {{
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                    }}
                    td {{
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                    }}
                    tr:nth-child(even){{background-color: #f2f2f2}}
                </style>
            </head>
            <body>
                <div style="overflow-x:auto;">
                    <h1><i>{f_name}</i> Timeline</h1>
                    <table>
                        <tr>
                            <th>Date</th>
                            <th>Time</th>
                            <th>Change Type</th>
                            <th>Editors</th>
                            <th>Change Amount</th>
                        </tr>
    """)

    num_increments = timeline_stats.getNumIncrements()

    prev_date = ""

    for i in range(num_increments):
        increment = timeline_stats.getIncrement(i)
        adds = increment.additions
        rems = increment.removals

        if len(adds) == len(rems) == 0:     # make sure that None is displayed if there were no changes
            editors = ["None"]
            amounts = [0]
            types = ["None"]
        else:
            editors = list(adds.keys()) + list(rems.keys())
            amounts = list(adds.values()) + list(rems.values())
            types = ["Addition" for _ in range(len(adds))] + ["Removals" for _ in range(len(rems))]

        if dt.strftime('%d/%m/%Y') != prev_date:        # don't repeat dates
            date_to_display = dt.strftime('%d/%m/%Y')
            prev_date = dt.strftime('%d/%m/%Y')
        else:
            date_to_display = ""

        prev_time = ""

        for editor, amount, type in zip(editors, amounts, types):
            if dt.strftime('%d/%m/%Y') != prev_time:        # don't repeat times
                prev_time = dt.strftime('%d/%m/%Y')
                time_to_display = dt.strftime('%I:%M:%S %p')
            else:
                time_to_display = ""

            file.write(f"""
                    <tr>
                        <td>{date_to_display}</td>
                        <td>{time_to_display}</td>
                        <td>{type}</td>
                        <td>{editor}</td>
                        <td>{amount}</td>
                    </tr>
            """)

        dt += ti

    # close file and open in browser
    file.write("""
                    </table>
                </div>
            </body>
        </html>
    """)
    file.close()
    open_new(file_path)