from datetime import datetime


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

        for editor in self.editors:
            self.total.mergeIn(self.editors[editor])

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
