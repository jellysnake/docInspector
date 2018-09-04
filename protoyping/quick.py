import json
from datetime import datetime

from httplib2 import Http
from oauth2client import file, client, tools


class ChangeData:
    """
    Represents the collated changes made in a revision
    """

    class EditorChanges:
        """
        Class that stores the changes made by a single editor
        This is a nested class as it should not be publicly visible information.

        Used & exposed by methods in the outer Change Data class
        """

        def __init__(self):
            """
            Inits the class with all counters set to and a None id.
            """
            self.additions = 0
            self.changes = 0
            self.removals = 0
            self.userId = None

        def addChange(self, data):
            """
            Load the raw change data into this instance
            This converts the data into additions/removals in a robust manner

            :param data: The data to add. This should be in the raw JSON format
            :return: None
            :raise Exception: If the change type is invalid.
            """
            size = data['ei'] - data['si']
            if size != 0:
                editType = data['sm']['revdiff_dt'] if 'revdiff_dt' in data['sm'] else -1
                if editType == 1:
                    self.additions += size
                elif editType == 2:
                    self.removals += size
                else:
                    raise Exception(f"Unknown change type '{editType}'")

        def hasUser(self):
            """
            :return: True if this class has an ID set or not.
            """
            return self.userId is not None

        def setUserId(self, newId):
            """
            :param newId: The new user id to set for this instance
            """
            self.userId = newId

        def mergeIn(self, other):
            """
            Merges the contents of another EditorChanges instance into this one
            Retains the ID for this instance, even if it is None.

            :param other: The other instance to merge into this one
            :return: None
            """
            self.additions += other.additions
            self.removals += other.removals
            self.changes += other.changes

    def __init__(self, data):
        """
        Inits the class with the given data.
        This data should be in the raw JSON format returned by the web request

        :param data: The data to load in
        """
        # Pull the list of changes from the snapshot
        self.changes = []
        for chunk in data['chunkedSnapshot']:
            for entry in chunk:
                if entry['ty'] == 'as' and entry['st'] == "revision_diff":
                    self.changes.append(entry)

        # Load the changes into both the running total and the user totals
        users = {}
        self.total = self.EditorChanges()
        for entry in self.changes:
            user = entry['sm']['revdiff_aid'] if "revdiff_aid" in data['sm'] else ""
            if user not in users:
                users[user] = self.EditorChanges()
            users[user].addChange(data)
            self.total.addChange(data)

        self.editors = {}
        # Update the user Id to the standard
        for user in users:
            if user in data['userInfo']:  # We have userdata, so we copy the user into the store
                newId = data['userInfo'][user]['color']
                self.editors[newId] = users[user]
                self.editors[newId].setUserId(newId)
            else:  # We don't have data, so we merge into the unknown case
                if 'unknown' not in self.editors:
                    self.editors['unknown'] = users[user]
                    self.editors["unknown"].setUserId("unknown")
                else:
                    self.editors['unknown'].mergeIn(users[user])


class RevisionMetadata:
    """
    A single revision.
    This is the metadata for the revision. The actual revision data is contained with the ChangeData instance
    """

    def __init__(self, data, requester):
        """
        Inits the class from the given data.
        This should be the raw JSON data returned from the call to get the list of revisions.

        :param data: The raw JSON data
        :param requester: The requester with which to make future calls.
        """
        self.change = None
        self.requester = requester

        self.name = data['name'] if 'name' in data else "unnamed"
        self.startId = data['start']
        self.endId = data['end']
        self.endTime = data['endMillis']
        self.users = data['users']
        self.revisionKey = data['revisionMac']
        self.hasSubRevisions = data['expandable']

    def __str__(self):
        """
        :return: This revision as a string format
        """
        return f"'{self.name}' revision @ {datetime.fromtimestamp(1347517370).strftime('%c')}"

    def getChanges(self):
        """
        Get the changes made in this revision.
        This method caches the changes after the first call.

        :param data: The data to use to load the changes from, Optional
        :return: The changes made in this revision
        """
        if not self.change:
            rawData = self.requester.requestRevision(self)
            self.change = ChangeData(rawData)

        return self.change


class UnsafeRequester:
    """
    Makes requests to the unsafe API
    """

    def __init__(self, http, docId):
        """

        :param http: The http object to make the direct calls with
        :param docId: The ID of the document to call against.
        """
        self.http = http
        self.docId = docId
        self.baseUrl = f"https://docs.google.com/document/d/{self.docId}/"

    def requestRevision(self, revision):
        """
        Requests the detailed revision data for a revision

        :param revision: The revision to request for
        :return: The raw json of that revision
        """
        return self.requestRevisionRange(revision.startId, revision.endId)

    def requestRevisionRange(self, startId, endId):
        """
        Requests the detailed revision data for a given revision range.

        :param startId: The start id of the range
        :param endId: The end id of the range
        :return: The raw json for that range, as a single revision object.
        """
        (_, content) = self.http.request(
            self.baseUrl +
            f"showrevision?id={self.docId}&"
            f"end={endId}&start={startId}")
        return json.loads(content[5:])

    def requestList(self):
        """
        Request a list of all revisions on this document

        :return: The raw json of the list of revisions
        """
        (_, content) = self.http.request(self.baseUrl +
                                         f"revisions/tiles?id={self.docId}&"
                                         f"start=1&"
                                         f"showDetailedRevisions=false&filterNamed=false")

        return json.loads(content[5:])


class User:
    """
    Represents a single user.
    """

    def __init__(self, userId, data):
        """
        Creates a new user from the raw data

        :param userId: The ID of the user
        :param data: The raw json data
        """
        self.id = userId
        self.name = data['name']
        self.photo = data['photo']
        self.color = data['color']
        self.anonymous = data['anonymous']

    def getId(self):
        return self.color


class Document:
    """
    Represents a single document.
    This is made up of multiple revisions.
    """

    def __init__(self, http, docId):
        """
        Creates a new document with the given id.

        :param http: The http object to make calls with
        :param docId: The ID of the document in question
        """
        self.requester = UnsafeRequester(http, docId)
        self.docId = docId
        self.revisions = None
        self.users = None
        self.totalRevision = None

    def _loadRevisions(self, data):
        self.revisions = []
        for revision in data['tileInfo']:
            self.revisions.append(RevisionMetadata(revision, self.requester))

    def _loadUsers(self, data):
        self.users = {}
        for userNumber in data['userMap']:
            userData = User(userNumber, data['userMap'][userNumber])
            self.users[userData.getId()] = userData

    def getRevisionList(self):
        if self.revisions is None or self.users is None:
            rawData = self.requester.requestList()
            self._loadRevisions(rawData)
            self._loadUsers(rawData)
        return self.revisions


def main():
    # Basic authentication
    # This will be replaced with more thorough code
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', "https://www.googleapis.com/auth/drive")
        creds = tools.run_flow(flow, store)
    http = creds.authorize(Http())

    # Create the main document object
    document = Document(http, "1DN4LxL8nSd9ZUbqhpXIfasmm8PQykJonOw7nUpKXpoo")

    # Get the total revision data

    print(f"Revisions: {document.getRevisionList()}")

    # print(f"There are {len(revisions)} revisions in this document")
    # for revision in revisions:
    #     print(f"\t{str(revision)}:")
    #     users = {}
    #     changes = revision.getChanges()
    #     for change in changes:
    #         if change.user not in users:
    #             users[change.user] = [change.user, 0, 0, 0]
    #         users[change.user][1] += 1
    #         if change.editType == 1:
    #             users[change.user][2] += change.getSize()
    #         elif change.editType == 2:
    #             users[change.user][3] += change.getSize()
    #     print(f"\t\tThere were {len(users)} users:")
    #     for editor in users.values():
    #         print(f"\t\t{editor[0]} made {editor[1]} edits, totaling {editor[2]} additions and {editor[3]} deletions")


if __name__ == '__main__':
    main()
