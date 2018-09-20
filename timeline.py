from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime
from os import mkdir, path
from webbrowser import open_new


# If modifying these scopes, delete the file token.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
OUTPUT_DIR = "output"


"""
Prints timeline of given doc to the console

:param rev_meta : revision metadata from google docs API
:return file_path : the path to the generated html file
"""
def create_timeline(f_name, rev_meta):
    revisions = rev_meta.get('items', [])

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
                            <th>Date</th>
                            <th>Time</th>
                            <th>Editors</th>
                        </tr>
    """)

    for revision in revisions:
        date = datetime.strptime(revision['modifiedDate'][2:10], "%y-%m-%d").strftime("%d %B %Y")
        time = datetime.strptime(revision['modifiedDate'][11:18], "%H:%M:%S").strftime("%I:%M:%S %p")
        editors = revision['lastModifyingUserName']
        file.write(f"""
                        <tr>
                            <td>{date}</td>
                            <td>{time}</td>
                            <td>{editors}</td>
                        </tr>
        """)

    file.write("""
                    </table>
                </div>
            </body>
        </html>
    """)

    file.close()
    return file_path



if __name__ == '__main__':
    # Authentication
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v2', http=creds.authorize(Http()))

    # Get file name and revision info
    doc_id = '1_oa9owQzzM5NPEVS36pWtzFpswjx4FZH33ALwCr1cTs'
    f_name = service.files().get(fileId=doc_id).execute().get('title')
    rev_meta = service.revisions().list(fileId=doc_id).execute()

    # Create timeline file
    file_path = create_timeline(f_name, rev_meta)

    # Open generated file
    open_new(file_path)
