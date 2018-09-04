from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

def main():
    # Authentication
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v2', http=creds.authorize(Http()))

    # Print file name
    doc_id = '1lt2SmAjRs14EqwlKyix8VsypZE0mBSfRztkjzma0BjI'
    file_meta = service.files().get(fileId=doc_id).execute()
    print(file_meta.get('title'))

    # Print revision dates and last modified user
    rev_meta = service.revisions().list(fileId=doc_id).execute()
    revisions = rev_meta.get('items', [])
    for revision in revisions:
        # print('\t' + revision['modifiedDate'] + " - " + revision['lastModifyingUserName'])
        print('\t {0}/{1}/{2} {3} - {4}'.format(revision['modifiedDate'][8:10], revision['modifiedDate'][5:7],
            revision['modifiedDate'][2:4], revision['modifiedDate'][11:16], revision['lastModifyingUserName']))

if __name__ == '__main__':
    main()
