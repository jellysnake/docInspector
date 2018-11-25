from ..DocStats import DocStats
from ..UnsafeApi import Document


def collectUnsafeStats(stats: DocStats, service, useFine):
    """
    Uses the unsafe api to supplement the stats gathered from the official api
    This is only run if the `-u` flag is passed in

    :param stats: The stats object to store the data in
    :param http: The http object to make calls with
    :param useFine: Flag that controls if the finer revision level should be used.
    """
    http = service._http
    # Make a document (akin to a `service`) and pass it into the child methods
    doc = Document(http, stats.general.id, useFine)
    getTotalChanges(doc, stats)
    getIncrementData(doc, stats)


def getTotalChanges(document, stats: DocStats):
    """
    Gets the total changes made by each editor to the document
    This supplements the stats from `CollectIndividualStats.py`

    :param document: The document object that makes the calls
    :param stats: The stats object to store the results in
    """

    # Clear official stats
    editors = stats.individuals.getEditors()
    for editor in editors:
        stats.individuals.removeEditor(editor)

    # Obtain the total changes.
    print("Loading all changes. (May take a while, especially if using the --fine flag).")
    changes = document.getTotalChanges()

    # Load in the changes made by all users
    stats.individuals.total.additions = changes.totalAdditions()
    stats.individuals.total.removals = changes.totalRemovals()
    stats.individuals.total.changes = changes.totalChanges()
    stats.individuals.total.percent = 100

    # Load in the changes made by each user.
    totalSize = changes.totalAdditions() + changes.totalRemovals()
    users = changes.getUsers()
    for user in users:
        # TODO: This is a hack and we need to handle anonymous users.
        if user != "unknown":
            editor = stats.individuals.makeEditor(user)
            editor.name = document.getUser(user).name
            editor.additions = changes.userAdditions(user)
            editor.removals = changes.userRemovals(user)
            editor.changes = changes.userChanges(user)
            userSize = editor.additions + editor.removals
            editor.percent = (userSize / totalSize) * 100
            editor.unsafeId = document.getUser(user).id


def getIncrementData(doc: Document, stats):
    """
    Load in the data from each increment.
    This supplements the data from `CollectTimelineStats.py`

    :param doc: The document to make calls with
    :param stats: The stats object to store the data in
    """

    # Clear out the official data
    for i in range(stats.timeline.getNumIncrements() - 1, -1, -1):
        stats.timeline.removeIncrement(i)
    # Load in the changes from the api
    changes = doc.getChangesInIncrement(stats.timeline.incrementSize)

    # Add in the data from each increment
    for i in range(len(changes)):
        increment = stats.timeline.makeIncrement()
        totalAdd = 0
        totalRemove = 0
        totalChange = 0
        for user in changes[i].getUsers():
            # TODO: This is a hack and we need to handle anonymous users.
            if user != "unknown":
                editor = increment.makeEditor(user)
                editor.additions = changes[i].userAdditions(user)
                editor.removals = changes[i].userRemovals(user)
                editor.changes = changes[i].userChanges(user)
                editor.name = doc.getUser(user).name

                totalChange += editor.changes
                totalAdd += editor.additions
                totalRemove += editor.removals

        increment.total.additions = totalAdd or None
        increment.total.removals = totalRemove or None
        increment.total.changes = totalChange or None
