from typing import List


class TimelineStats:
    class IncrementStats:
        def __init__(self):
            self.additions = {}
            self.removals = {}
            self.changes = {}

        def isEmpty(self):
            return self.changes

        def addAddition(self, editor, size):
            if editor not in self.additions:
                self.additions[editor] = 0
                self.changes[editor] = 0

            self.additions[editor] = size
            self.changes[editor] += 1

        def addRemoval(self, editor, size):
            if editor not in self.additions:
                self.removals[editor] = 0
                self.changes[editor] = 0

            self.removals[editor] = size
            self.changes[editor] += 1

    def __init__(self, size):
        self.increments = []
        self.incrementSize = size

    def getIncrement(self, id) -> IncrementStats:
        return self.increments[id]

    def makeIncrement(self) -> IncrementStats:
        self.increments.append(self.IncrementStats())
        return self.increments[-1]

    def removeIncrement(self, id):
        self.increments.pop(id)

    def getIncrementSize(self):
        return self.incrementSize

    def setIncrementSize(self, size):
        self.incrementSize = size

    def getNumIncrements(self):
        return len(self.increments)


class IndividualStats:
    class EditorStats:
        def __init__(self):
            self.additions = 0
            self.removals = 0
            self.changes = 0
            self.name = "anonymous"
            self.percent = 0

        def addAddition(self, size):
            self.additions = size
            self.changes += 1

        def addRemoval(self, size):
            self.removals = size
            self.changes += 1

    def __init__(self):
        self.editors = {}

    def getEditor(self, id) -> EditorStats:
        return self.editors[id]

    def removeEditor(self, id):
        del self.editors[id]

    def makeEditor(self, id) -> EditorStats:
        self.editors[id] = self.EditorStats()
        return self.editors[id]

    def getEditors(self) -> List[str]:
        return list(self.editors.keys())


class DocStats:
    individuals: IndividualStats
    timeline: TimelineStats

    def __init__(self):
        self.editors = []
        self.timeline = TimelineStats()
        self.individuals = IndividualStats()
