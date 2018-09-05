from typing import List

from .Helpers import UnsafeRequester, User
from .Revisions import RevisionMetadata, ChangeData


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
