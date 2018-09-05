from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Print file name
    # doc_id = input('Enter id> ')
    doc_id = '1lt2SmAjRs14EqwlKyix8VsypZE0mBSfRztkjzma0BjI'
    file_meta = service.files().get(fileId=doc_id).execute()
    print('name: ' + file_meta.get('name'))

    # Print revision dates
    rev_meta = service.revisions().list(fileId=doc_id).execute()
    revisions = rev_meta.get('revisions', [])
    print(service.revisions().get(fileId=doc_id, revisionId='1').execute()) # print revision data for first revision
    print('revisions: ')
    for revision in revisions:
        print('\t' + revision['modifiedTime'])

if __name__ == '__main__':
    main()
