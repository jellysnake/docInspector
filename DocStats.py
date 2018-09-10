from typing import Dict, List


class TimelineStats:
    class IncrementStats:
        def __init__(self):
            ...

        def getAdditions(self) -> Dict[str, int]:
            ...

        def getRemovals(self) -> Dict[str, int]:
            ...

        def getChanges(self) -> Dict[str, int]:
            ...

    def __init__(self):
        ...

    def getIncrement(self, id):
        ...

    def getIncrementSize(self):
        ...

    def getNumIncrements(self):
        ...


class IndividualStats:
    class EditorStats:
        def __init__(self):
            ...

        def getAdditions(self):
            ...

        def getRemovals(self):
            ...

        def getChanges(self):
            ...

        def getName(self):
            ...

    def __init__(self):
        ...

    def getEditor(self, id) -> EditorStats:
        ...

    def removeEditor(self, id):
        ...

    def makeEditor(self, id) -> EditorStats:
        ...

    def getEditors(self) -> List[str]:
        ...


class DocStats:
    individuals: IndividualStats
    timeline: TimelineStats

    def __init__(self):
        self.editors = []
        self.timeline = TimelineStats()
        self.individuals = IndividualStats()
