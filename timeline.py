from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime


# If modifying these scopes, delete the file token.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'


''' 
Prints timeline of given doc to the console
:parameter rev_meta : revision metadata from google docs API
'''
def create_timeline(rev_meta):
    file = open('file_timeline.txt', 'w')
    revisions = rev_meta.get('items', [])

    for revision in revisions:
        date_time = datetime.strptime(revision['modifiedDate'][2:18], "%y-%m-%dT%H:%M:%S").strftime("%d/%m/%y %I:%M:%S %p")

        file.write('{0} - {1}\n'.format(
            date_time,
            revision['lastModifyingUserName']
        ))

    file.close()


if __name__ == '__main__':
    # Authentication
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v2', http=creds.authorize(Http()))

    # Print file name
    doc_id = '17kB9r4NG2akVqVE6-FmLP9xT6mKhoI5AKPkO4dhRAxo'
    # file_meta = service.files().get(fileId=doc_id).execute()
    # print(file_meta.get('title'))

    # Print revision dates and last modified user
    rev_meta = service.revisions().list(fileId=doc_id).execute()
    create_timeline(rev_meta)
