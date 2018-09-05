import json
from datetime import datetime
from typing import List

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
            size = data['ei'] - data['si'] + 1
            self.changes += 1
            if size != 0:
                editType = data['sm']['revdiff_dt'] if 'revdiff_dt' in data['sm'] else None
                if editType == 1:
                    self.additions += size
                elif editType == 2:
                    self.removals += size
                elif editType is None:
                    self.additions += size
                    print(f"Edit of size {size} had no edit type. Defaulting to addition")
                else:
                    print(f"ERROR: Ghost edit of size {size} found?")
                    self.changes -= 1  # Ensure it doesn't show up

        def hasUser(self) -> bool:
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

    def __init__(self, data=None):
        self.editors = {}
        self.total = self.EditorChanges()
        if data:
            self.initFromData(data)

    def initFromData(self, data):
        """
        Inits the class with the given data.
        This data should be in the raw JSON format returned by the web request

        :param data: The data to load in
        """
        changes = []
        # Pull the list of changes from the snapshot
        for chunk in data['chunkedSnapshot']:
            for entry in chunk:
                if entry['ty'] == 'as' and entry['st'] == "revision_diff":
                    changes.append(entry)

        # Load the changes into both the running total and the user totals
        users = {}
        for entry in changes:
            user = entry['sm']['revdiff_aid'] if "revdiff_aid" in entry['sm'] else ""
            if user not in users:
                users[user] = self.EditorChanges()
            users[user].addChange(entry)
            self.total.mergeIn(users[user])

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

    def mergeIn(self, other: 'ChangeData'):
        """
        Merges the changes in another revision into this revision.

        :param other: The other revision to merge in
        :return: None
        """
        self.total.mergeIn(other.total)
        for user in other.getUsers():
            if user in self.editors:
                self.editors[user].mergeIn(other.editors[user])
            else:
                self.editors[user] = other.editors[user]

    def totalAdditions(self) -> int:
        """
        :return: The total number of characters added in this revision
        """
        return self.total.additions

    def totalRemovals(self) -> int:
        """
        :return: The total number of characters removed in this revision
        """
        return self.total.removals

    def totalChanges(self) -> int:
        """
        :return: The total number of characters edits in this revision
        """
        return self.total.changes

    def getUsers(self) -> list:
        """
        :return: all the users that have edited this revision
        """
        return list(self.editors.keys())

    def userAdditions(self, user) -> int:
        """
        :param user: The user to look up
        :return: The number of additions by that user
        :raise KeyError: If the user did not edit the revision
        """
        if user in self.editors:
            return self.editors[user].additions
        else:
            raise KeyError(f"User {user} did not edit this revision")

    def userRemovals(self, user) -> int:
        """
        :param user: The user to look up
        :return: The number of removals by that user
        :raise KeyError: If the user did not edit the revision
        """
        if user in self.editors:
            return self.editors[user].removals
        else:
            raise KeyError(f"User {user} did not edit this revision")

    def userChanges(self, user) -> int:
        """
        :param user: The user to look up
        :return: The number of changes by that user
        :raise KeyError: If the user did not edit the revision
        """
        if user in self.editors:
            return self.editors[user].changes
        else:
            raise KeyError(f"User {user} did not edit this revision")


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

    def __repr__(self):
        """
        :return: This revision as a string format
        """
        return f"'{self.name}' revision @ {datetime.fromtimestamp(1347517370).strftime('%c')}"

    def getChanges(self) -> ChangeData:
        """
        Get the changes made in this revision.
        This method caches the changes after the first call.

        :return: The changes made in this revision
        """
        if not self.change:
            rawData = self.requester.requestRevision(self)
            self.change = ChangeData(rawData)

        return self.change


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

    def __repr__(self):
        return f"{self.name}({self.getId()})"


class Document:
    """
    Represents a single document.
    This is made up of multiple revisions.
    """

    def __init__(self, http, docId, useFine=False):
        """
        Creates a new document with the given id.

        :param http: The http object to make calls with
        :param docId: The ID of the document in question
        """
        self.requester = UnsafeRequester(http, docId, useFine)
        self.docId = docId
        self.revisions = None
        self.users = None
        self.totalChanges = None

    def _loadRevisions(self, data):
        """
        Internal Function.
        Loads the revisions from the revision data provided.

        :param data: The data to load from
        :return: None
        """
        self.revisions = []
        for revision in data['tileInfo']:
            self.revisions.append(RevisionMetadata(revision, self.requester))
        self.revisions.sort(key=lambda x: x.startId)

    def _loadUsers(self, data):
        """
        Internal Function
        Loads the users from the data provided.

        :param data: The data to load from
        :return: None
        """
        self.users = {}
        for userNumber in data['userMap']:
            userData = User(userNumber, data['userMap'][userNumber])
            self.users[userData.getId()] = userData

    def getRevisionList(self) -> List[RevisionMetadata]:
        """
        Returns a List of all 'major' revisions
        A major revision is one which is either:
            both expandable and unexpanded,
            or named.

        :return: A list of all major revisions
        """
        if self.revisions is None or self.users is None:
            rawData = self.requester.requestList()
            self._loadRevisions(rawData)
            self._loadUsers(rawData)
        return self.revisions

    def getIdRange(self) -> tuple:
        """
        Get the range of revision ids in this document.
        This is defined as the start id of the first revision and the end id of the last revision.
        Revisions are sorted by start id, so if there is an overlap the last id may not be the true last revision.

        :return: A tuple where the first element is the first id and the second is the last
        """
        revisions = self.getRevisionList()
        return revisions[0].startId, revisions[-1].endId

    def getTotalChanges(self) -> ChangeData:
        """
        Get an object representing the entirety of the changes made in this document.
        This is all the individual changes made.

        :return: A ChangeData for all the changes made
        """
        if self.totalChanges is None:
            revisionList = self.getRevisionList()
            self.totalChanges = revisionList[0].getChanges()
            for revision in revisionList[1:]:
                self.totalChanges.mergeIn(revision.getChanges())

        return self.totalChanges

    def getUser(self, user) -> User:
        """
        Gets information about a specific user
        :param user: The user to get
        :return: A User for that user
        :raise KeyError: If the user could not be found
        """
        if self.users is None:
            if self.revisions is None or self.users is None:
                rawData = self.requester.requestList()
                self._loadRevisions(rawData)
                self._loadUsers(rawData)
        if user in self.users:
            return self.users[user]
        else:
            raise KeyError(f"User {user} did not edit the document")

    def getForIdRange(self, startId, endId) -> ChangeData:
        """
        Get all the changes made in a given id range.
        This is an aggregate of all the changes made

        All revisions with a start >= to startId and an end <= endId will be included.
        This means that a revision may not be included if one of the two falls just outside the range.
        It also means that the endpoints may not be included if there is no revision that exactly matches them.

        :param startId: The starting id
        :param endId: The ending id
        :return: An aggregate of all the changes in that id range
        """
        revisions = self.getRevisionList()
        changes = ChangeData()
        for i in range(len(revisions)):
            if revisions[i].startId >= startId and revisions[i].endId <= endId:
                changes.mergeIn(revisions[i].getChanges())
        return changes


class UnsafeRequester:
    """
    Makes requests to the unsafe API
    """

    def __init__(self, http, docId, useFine=False):
        """

        :param http: The http object to make the direct calls with
        :param docId: The ID of the document to call against.
        """
        self.http = http
        self.docId = docId
        self.useFine = useFine
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
                                         f"showDetailedRevisions={'true' if self.useFine else 'false'}"
                                         f"&filterNamed=false")

        return json.loads(content[5:])


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
    # doc = Document(http, "1DN4LxL8nSd9ZUbqhpXIfasmm8PQykJonOw7nUpKXpoo") # Terasology Plan
    # doc = Document(http, "13zenM2HX9WDJr1tt2YxGZ3RPYhk5ktc_tcEG_ess--Q") # Mayoral Char SHeet
    doc = Document(http, "17kB9r4NG2akVqVE6-FmLP9xT6mKhoI5AKPkO4dhRAxo")  # FIT2101 Project Plan

    totalChanges = doc.getTotalChanges()
    print(f"In total there were {totalChanges.totalAdditions()} characters added"
          f" and {totalChanges.totalRemovals()} removed"
          f" by {len(totalChanges.getUsers())} users")
    totalSize = totalChanges.totalAdditions() + totalChanges.totalRemovals()

    for user in totalChanges.getUsers():
        userSize = totalChanges.userAdditions(user) + totalChanges.userRemovals(user)
        print(f"{doc.getUser(user) if user != 'unknown' else 'unknown'} made {(userSize/totalSize)*100}% of changes.")


if __name__ == '__main__':
    main()
