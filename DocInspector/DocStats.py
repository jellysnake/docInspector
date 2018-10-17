from typing import List, Dict, Optional
from weakref import ref

from DocInspector.Helpers import timeToMilli, calculateTimelineStart


class GeneralStats:
    """
    Collates stats about the document itself
    """

    def __init__(self, parent):
        self.name = ""
        self.id = ""
        self.link = ""
        self.creationDate = ""
        self.parent = ref(parent)


class IndividualStats:
    """
    Collates all the stats for the individual data section
    """
    editors: Dict[str, 'IndividualStats.EditorStats']
    total: 'IndividualStats.EditorStats'

    class EditorStats:
        """
        Represents stats made by an individual editor
        """

        def __init__(self):
            self.additions = None
            self.removals = None
            self.changes = None
            self.name = None
            self.unsafeId = None
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

        def mergeIn(self, other: 'IndividualStats.EditorStats'):
            self.name = self.name or other.name
            self.additions = (other.additions or 0) + (self.additions or 0)
            self.removals = (other.removals or 0) + (self.removals or 0)
            self.changes = (other.changes or 0) + (self.changes or 0)

    def __init__(self, parent):
        self.editors = {}
        self.total = self.EditorStats()
        self.parent = ref(parent)

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

    def findEditorByUnsafe(self, id) -> Optional[str]:
        for editor in self.editors:
            if self.editors[editor].unsafeId and self.editors[editor].unsafeId == id:
                return editor
        return None

    def mergeIn(self, other: 'IndividualStats'):
        for editor in other.getEditors():
            # Find the id of the editor
            # We try and match by unsafe ID, falling back to general ID.
            id = editor
            if other.editors[editor].unsafeId:
                id = self.findEditorByUnsafe(other.editors[editor].unsafeId)
            # If the id exists, we merge it. Else we make a new editor and merge that.
            if id in self.editors:
                self.editors[editor].mergeIn(other.editors[editor])
            else:
                self.makeEditor(editor).mergeIn(other.editors[editor])
        # Merge total changes
        self.total.mergeIn(other.total)
        # Re-calculate percentages
        for editor in self.editors:
            if self.total.additions + self.total.removals != 0:
                self.editors[editor].percent = (self.editors[editor].removals + self.editors[editor].additions) \
                                               / (self.total.additions + self.total.removals)
            else:
                self.editors[editor].percent = 0


class TimelineStats:
    """
    Collates stats calculated for the timeline
    """
    parent: 'DocStats'

    def __init__(self, size, parent):
        days, hours, mins = map(int, size.split(':'))
        timeSize = (((days * 24) + hours) * 60 + mins) * 60 * 1000
        self.incrementSize = timeSize
        self.increments = []
        self.timelineStart = 0
        self.parent = ref(parent)

    def getIncrement(self, id) -> IndividualStats:
        """
        Get the given increment.

        :param id: The id of the increment to get
        :return: The increment, if it exists.
        """
        return self.increments[id]

    def makeIncrement(self) -> IndividualStats:
        """
        Appends a new increment and adds it to the list

        :return: THe newly created increment
        """
        self.increments.append(IndividualStats(self))
        return self.increments[-1]

    def removeIncrement(self, id):
        """
        Removes the given increment from the list

        :param id: The increment to remove
        """
        self.increments.pop(id)

    def getIncrementSize(self) -> int:
        """
        :return: The size of each increment
        """
        return self.incrementSize

    def setIncrementSize(self, size):
        """
        :param size:  the size of each increment
        """
        self.incrementSize = size

    def getNumIncrements(self) -> int:
        """
        :return: how many increments are stored
        """
        return len(self.increments)

    def mergeIn(self, other: 'TimelineStats'):
        """
        Merges together two timelines.
        Takes into account different starting dates.
        Assumes they have the same increment size

        :param other: The other timeline to merge in
        """
        incSize = self.incrementSize
        selfIncs = list(self.increments)
        otherIncs = list(other.increments)

        selfStart = self.timelineStart
        otherStart = other.timelineStart
        selfEnd = selfStart + len(selfIncs) * incSize
        otherEnd = otherStart + len(otherIncs) * incSize

        self.increments = []

        isOverlap = selfStart <= otherEnd + incSize / 3 and otherStart <= selfEnd + incSize / 3
        if isOverlap:
            # This is the earlier starter
            if selfStart <= otherStart:
                currentTime = selfStart
                while currentTime <= otherStart:
                    self.increments.append(selfIncs.pop(0))
                    currentTime += self.incrementSize

            # Other is the earlier starter
            elif otherStart <= selfStart:
                currentTime = otherStart
                while currentTime <= selfStart:
                    self.increments.append(otherIncs.pop(0))
                    currentTime += self.incrementSize
            # Add them all in for the duration of the overlap
            while otherIncs and selfIncs:
                inc = otherIncs.pop(0)
                inc.mergeIn(selfIncs.pop(0))
                self.increments.append(inc)
            # One of the two is empty so we add both sequentially
            while otherIncs:
                self.increments.append(otherIncs.pop(0))
            while selfIncs:
                self.increments.append(selfIncs.pop(0))

        else:
            if selfStart < otherStart:
                # Self is the lower one
                self.increments.extend(selfIncs)
                diff = round((otherStart - selfEnd) / incSize)
                self.increments.extend([IndividualStats(self) for _ in range(diff)])
                self.increments.extend(otherIncs)
            else:
                # Other is the lower one
                self.increments.extend(otherIncs)
                diff = round((selfStart - otherEnd) / incSize)
                self.increments.extend([IndividualStats(self) for _ in range(diff)])
                self.increments.extend(selfIncs)

    def setTimelineStart(self, start):
        self.timelineStart = calculateTimelineStart(timeToMilli(start), self.incrementSize)


class DocStats:
    """
    Class to collate all the stats from each of the calculation phases
    """
    individuals: IndividualStats
    timeline: TimelineStats
    general: GeneralStats

    def __init__(self, incrementSize):
        self.timeline = TimelineStats(incrementSize, self)
        self.individuals = IndividualStats(self)
        self.general = GeneralStats(self)

    def mergeIn(self, other: 'DocStats'):
        self.individuals.mergeIn(other.individuals)
        self.timeline.mergeIn(other.timeline)
