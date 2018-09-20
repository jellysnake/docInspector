from datetime import datetime
from os import mkdir, path
from webbrowser import open_new

from DocStats import DocStats

OUTPUT_DIR = "output"


def outputStats(stats: DocStats, args):
    f_name = stats.general.name
    timeline_stats = stats.timeline
    # revisions = rev_meta.get('items', [])

    try:
        mkdir(OUTPUT_DIR)
    except Exception:
        pass

    file_path = path.join(OUTPUT_DIR, f_name + "_timeline.html")
    file = open(file_path, 'w')

    file.write(f"""
        <html>
            <head>
                <title>{f_name}_Timeline</title>
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
                        padding: 12px;
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
                    <h1>"{f_name}" Timeline</h1>
                    <table>
                        <tr>
                            <th>Date/Time</th>
                            <th>Change Type</th>
                            <th>Change Amount</th>
                            <th>Editors</th>
                        </tr>
    """)

    num_increments = timeline_stats.getNumIncrements()
    print(num_increments)

    for i in range(num_increments):
        increment = timeline_stats.getIncrement(i)

        additions = increment.additions
        removals = increment.removals
        for editor, amount in additions.items():
            file.write(f"""
                    <tr>
                        <td></td>
                        <td>Addition</td>
                        <td>{editor}</td>
                        <td>{amount}</td>
                    </tr>
            """)
        for editor, amount in removals.items():
            file.write(f"""
                    <tr>
                        <td></td>
                        <td>Removal</td>
                        <td>{editor}</td>
                        <td>{amount}</td>
                    </tr>
            """)
    file.write("""
                    </table>
                </div>
            </body>
        </html>
    """)

    file.close()
    open_new(file_path)


def timeToMilli(time):
    return datetime.strptime(time,
                             "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
