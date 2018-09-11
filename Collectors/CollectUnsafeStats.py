from DocStats import DocStats
from UnsafeApi import Document


def collectUnsafeStats(stats: DocStats, http, args):
    doc = Document(http, stats.general.id, args.useFine)
    getTotalChanges(doc)
    getIncrementData(doc, args.timeIncrement)


def getTotalChanges(document):
    print("Loading all changes. (May take a while, especially if using --fine flag).")
    changes = document.getTotalChanges()
    totalSize = changes.totalAdditions() + changes.totalRemovals()
    users = changes.getUsers()
    for user in users:
        if user != "unknown":
            userSize = changes.userAdditions(user) + changes.userRemovals(user)
            print("%s made %2.2f%% of all changes" % (document.getUser(user).name, (userSize / totalSize) * 100))


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
