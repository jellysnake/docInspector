from typing import Iterable, List

from DocInspector.DocStats import DocStats


def outputGenerals(stats: DocStats):
    return ["--- General Stats ---",
            f"Name:           {stats.general.name}",
            f"Creation Date:  {stats.general.creationDate}",
            f"Link:           https://docs.google.com/document/d/{stats.general.id}/view",
            ""]


def findMaxWidth(array: Iterable[str]) -> int:
    return len(max(array, key=len))


def getEditorStat(stats: DocStats, attribute: str) -> List[str]:
    editors = map(lambda editor: str(editor.__dict__[attribute]) or "N/A", stats.individuals.editors.values())
    return list(editors)


def outputIndividual(stats: DocStats):
    editors = getEditorStat(stats, "name")
    editorWidth = findMaxWidth(editors + ["Name"])
    additions = getEditorStat(stats, "additions")
    additionWidth = findMaxWidth(additions + ["Additions"])
    removals = getEditorStat(stats, "removals")
    removalWidth = findMaxWidth(removals + ["Removals"])
    changes = getEditorStat(stats, "changes")
    changesWidth = findMaxWidth(changes + ["Changes"])
    percent = getEditorStat(stats, "percent")
    percentWidth = findMaxWidth(percent + ["Percent"])

    output = [
        "--- Individual Stats ---",
        f"┌─{'─'*editorWidth}─┬─{'─'*additionWidth}─"
        f"┬─{'─'*removalWidth}─┬─{'─'*changesWidth}─┬─{'─'*percentWidth}─┐",

        "│ {0: ^{1}} │ {2: ^{3}} │ {4: ^{5}} │ {6: ^{7}} │ {8: ^{9}} │"
            .format("Name", editorWidth, "Additions", additionWidth,
                    "Removals", removalWidth, "Changes", changesWidth, "Percent", percentWidth),

        f"├─{'─'*editorWidth}─┼─{'─'*additionWidth}─"
        f"┼─{'─'*removalWidth}─┼─{'─'*changesWidth}─┼─{'─'*percentWidth}─┤",
    ]

    for i in range(len(editors)):
        output.append("│ {0: <{1}} ".format(editors[i], editorWidth)
                      + "│ {0: <{1}} ".format(additions[i], additionWidth)
                      + "│ {0: <{1}} ".format(removals[i], removalWidth)
                      + "│ {0: <{1}} ".format(changes[i], changesWidth)
                      + "│ {0: <{1}} │".format(percent[i], percentWidth))

    output.append(
        f"└─{'─'*editorWidth}─┴─{'─'*additionWidth}─"
        f"┴─{'─'*removalWidth}─┴─{'─'*changesWidth}─┴─{'─'*percentWidth}─┘", )
    return output + [""]


def outputTimeline(stats: DocStats):
    output = []

    return output


def outputPlain(stats: DocStats):
    output = []

    output.extend(outputGenerals(stats))
    output.extend(outputIndividual(stats))
    output.extend(outputTimeline(stats))

    return "\n".join(output)
