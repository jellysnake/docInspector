import json


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
