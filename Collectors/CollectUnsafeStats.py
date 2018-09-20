from DocStats import DocStats
from UnsafeApi import Document


def collectUnsafeStats(stats: DocStats, http, args):
    doc = Document(http, stats.general.id, args.useFine)
    getTotalChanges(doc, stats)
    getIncrementData(doc, args.timeIncrement)


def getTotalChanges(document, stats: DocStats):
    # Clear official stats
    editors = stats.individuals.getEditors()
    for editor in editors:
        stats.individuals.removeEditor(editor)

    # Load in unsafe stats
    print("Loading all changes. (May take a while, especially if using --fine flag).")
    changes = document.getTotalChanges()
    stats.individuals.total.additions = changes.totalAdditions()
    stats.individuals.total.removals = changes.totalRemovals()
    stats.individuals.total.changes = changes.totalChanges()
    stats.individuals.total.percent = 100

    totalSize = changes.totalAdditions() + changes.totalRemovals()
    users = changes.getUsers()
    for user in users:
        if user != "unknown":
            editor = stats.individuals.makeEditor(user)
            editor.name = document.getUser(user).name
            editor.additions = changes.userAdditions(user)
            editor.removals = changes.userRemovals(user)
            editor.changes = changes.userChanges(user)
            userSize = editor.additions + editor.removals
            editor.percent = (userSize / totalSize) * 100


def getIncrementData(doc: Document, increment):
    days, hours, mins = map(int, increment.split(':'))
    millis = (((days * 24) + hours) * 60 + mins) * 60 * 1000
    changes = doc.getChangesInIncrement(millis)
    i = 0
    print("Changes per student per increment:")
    for i in changes:
        print(f"{i}'th increment")
        for user in changes[i].getUsers():
            if user != 'unknown':
                print(f"\t{doc.getUser(user)} added {changes[i].userAdditions(user)} chars, "
                      f"and removed {changes[i].userRemovals(user)} "
                      f"in {changes[i].userChanges(user)} edits")
        print("")
