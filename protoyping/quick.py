import json

from httplib2 import Http
from oauth2client import file, client, tools


class RevisionData:
    def __init__(self, data):
        self.startID = data['start']
        self.endID = data['end']
        self.endTime = data['endMillis']
        self.users = data['users']
        self.revisionKey = data['revisionMac']
        self.hasSubRevisions = data['expandable']


class User:
    def __init__(self, userId, data):
        self.id = userId
        self.name = data['name']
        self.photo = data['photo']
        self.color = data['color']
        self.anonymous = data['anonymous']


class RevisionList:
    def __init__(self, data):
        self.startRevision = data['firstRev']
        self.revisions = []
        for revision in data['tileInfo']:
            self.revisions.append(RevisionData(revision))


class Document:
    def __init__(self, http, docId):
        self.http = http
        self.docId = docId
        self.revisions = None

    def listRevisions(self):
        if not self.revisions:
            (_, content) = self.http.request(f"https://docs.google.com/document/d/{self.docId}/revisions/"
                                             f"tiles?id={self.docId}&"
                                             f"start=1&"
                                             f"showDetailedRevisions=false&filterNamed=false&"
                                             f"ouid=107477822689043550957&includes_info_params=true")
            content = json.loads(content[5:])
            self.revisions = RevisionList(content)
        return self.revisions


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', "https://www.googleapis.com/auth/drive")
        creds = tools.run_flow(flow, store)

    http = creds.authorize(Http())
    document = Document(http, "1DN4LxL8nSd9ZUbqhpXIfasmm8PQykJonOw7nUpKXpoo")
    document.listRevisions()

if __name__ == '__main__':
    main()
