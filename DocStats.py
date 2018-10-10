from typing import List


class GeneralStats:
    """
    Collates stats about the document itself
    """

    def __init__(self):
        self.name = ""
        self.id = ""
        self.link = ""
        self.creationDate = ""


class TimelineStats:
    """
    Collates stats calculated for the timeline
    """

    class IncrementStats:
        """
        Represents a single increment of time
        """

        def __init__(self):
            self.additions = {}
            self.removals = {}
            self.changes = {}
            self.editors = set()
            self.time = None

        def isEmpty(self):
            """
            :return: True if the increment contained no changes. False otherwise
            """
            return self.changes

        def addAddition(self, editor, size):
            """
            Adds an addition to the increment.
            Automatically updates the edit counter.

            :param editor: The id of the editor that made the addition
            :param size: The size of the edit in characters
            """
            if editor not in self.additions:
                self.additions[editor] = 0
                self.changes[editor] = 0

            self.additions[editor] = size
            self.changes[editor] += 1

        def addRemoval(self, editor, size):
            """
            Adds a removal to the increment.
            Automatically updates the edit counter.

            :param editor: The editor that made the removal
            :param size: The size of the edit in characters
            """
            if editor not in self.additions:
                self.removals[editor] = 0
                self.changes[editor] = 0

            self.removals[editor] = size
            self.changes[editor] += 1

    def __init__(self, size):
        self.increments = []
        self.incrementSize = size

    def getIncrement(self, id) -> IncrementStats:
        """
        Get the given increment.

        :param id: The id of the increment to get
        :return: The increment, if it exists.
        """
        return self.increments[id]

    def makeIncrement(self) -> IncrementStats:
        """
        Appends a new increment and adds it to the list

        :return: THe newly created increment
        """
        self.increments.append(self.IncrementStats())
        return self.increments[-1]

    def removeIncrement(self, id):
        """
        Removes the given increment from the list

        :param id: The increment to remove
        """
        self.increments.pop(id)

    def getIncrementSize(self):
        """
        :return: The size of each increment
        """
        return self.incrementSize

    def setIncrementSize(self, size):
        """
        :param size:  the size of each increment
        """
        self.incrementSize = size

    def getNumIncrements(self):
        """
        :return: how many increments are stored
        """
        return len(self.increments)


class IndividualStats:
    """
    Collates all the stats for the individual data section
    """

    class EditorStats:
        """
        Represents stats made by an individual editor
        """

        def __init__(self):
            self.additions = None
            self.removals = None
            self.changes = None
            self.name = None
            self.percent = None

        def addAddition(self, size):
            """
            Adds an addition to the editor.
            Automatically increases the edit counter

            :param size: The size of the addition in characters
            """
            self.additions = size
            self.changes += 1

        def addRemoval(self, size):
            """
            Adds an removal to the editor.
            Automatically increases the edit counter

            :param size: The size of the removal in characters
            """
            self.removals = size
            self.changes += 1

    def __init__(self):
        self.editors = {}
        self.total = self.EditorStats()

    def getEditor(self, id) -> EditorStats:
        """
        Gets an editor's contributions
        :param id: The id of the editor to get
        :return: An EditorStats of the edits they made
        """
        return self.editors[id]

    def removeEditor(self, id):
        """
        Removes an editor from the list

        :param id: The id of the editor to remove
        """
        del self.editors[id]

    def makeEditor(self, id) -> EditorStats:
        """
        Makes a new editor and adds it to the list.
        Returns the newly made editor

        :param id: The id of the editor just made
        """
        self.editors[id] = self.EditorStats()
        return self.editors[id]

    def getEditors(self) -> List[str]:
        """
        :return: The id's of all the editors stored
        """
        return list(self.editors.keys())


class DocStats:
    """
    Class to collate all the stats from each of the calculation phases
    """
    individuals: IndividualStats
    timeline: TimelineStats
    general: GeneralStats

    def __init__(self, incrementSize):
        self.timeline = TimelineStats(incrementSize)
        self.individuals = IndividualStats()
        self.general = GeneralStats()
