from datetime import datetime, timedelta
from os import mkdir, path
from webbrowser import open_new
from DocStats import DocStats


OUTPUT_DIR = "output"


def create_timeline(stats: DocStats, args):
    f_name = stats.general.name
    timeline_stats = stats.timeline

    # time increment size
    ti = list(map(int, args.timeIncrement.split(':')))
    ti = timedelta(days=ti[0], hours=ti[1], minutes=ti[2])

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
                    }}
                    th {{
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 12px;
                    }}
                    td {{
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 10px;
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
    prev_date = ""      # keeps track of whether the dates are repeated

    for i in range(num_increments):
        increment = timeline_stats.getIncrement(i)
        adds = increment.additions
        rems = increment.removals

        if len(adds) == len(rems) == 0:     # skip if there were no changes
            dt += ti
            pass

        for j, (editor, amount) in enumerate(adds.items()):
            display_date = ""
            display_time = ""
            display_type = ""

            if j == 0:
                if prev_date != dt.strftime('%d/%m/%Y'):        # don't repeat dates
                    display_date = dt.strftime('%d/%m/%Y')
                    prev_date = dt.strftime('%d/%m/%Y')
                display_time = dt.strftime('%I:%M:%S %p')
                display_type = "Additions"

            file.write(f"""
                    <tr>
                        <td>{display_date}</td>
                        <td>{display_time}</td>
                        <td>{display_type}</td>
                        <td>{editor}</td>
                        <td>{amount}</td>
                    </tr>
            """)

        for j, (editor, amount) in enumerate(rems.items()):
            display_type = ""
            if j == 0:
                display_type = "Removals"

            file.write(f"""
                    <tr>
                        <td></td>
                        <td></td>
                        <td>{display_type}</td>
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


def outputStats(stats: DocStats, args):
    create_timeline(stats, args)
