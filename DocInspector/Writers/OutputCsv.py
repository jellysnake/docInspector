from typing import List

from DocInspector.DocStats import DocStats


def outputGenerals(stats: DocStats) -> List[str]:
    return ["General Stats",
            f"Name, {stats.general.name}",
            f"Creation Date, {stats.general.creationDate}",
            f"Link, https://docs.google.com/document/d/{stats.general.id}/view",
            ""]


def outputIndividuals(stats: DocStats) -> List[str]:
    return []


def outputTimeline(stats: DocStats) -> List[str]:
    return []


def outputCsv(stats: DocStats) -> str:
    output = []

    output.extend(outputGenerals(stats))
    output.extend(outputIndividuals(stats))
    output.extend(outputTimeline(stats))

    return "\n".join(output)
