from DocInspector.DocStats import DocStats
from DocInspector.Helpers import calculateTimelineStart, timeToMilli


def collectTimelineStats(stats: DocStats, service):
    """
    Collects stats for the timeline from the official api.
    At present this is limited to just the last editor in each major revision in each increment

    :param stats: The stat object to fill up
    :param service: The service to use to make any calls to the api
    :param args: The arguments passed into the program
    """

    rev_meta = service.revisions().list(fileId=stats.general.id).execute()
    currentTime = calculateTimelineStart(timeToMilli(stats.general.creationDate), stats.timeline.incrementSize)
    revisionList = rev_meta['items']

    i = 0
    # Iterate until we run out of revisions
    while i < len(rev_meta['items']):
        increment = stats.timeline.makeIncrement()
        # Iterate whilst we are in the current increment
        # Check to make sure we don't run out of revisions
        while i < len(revisionList) and timeToMilli(revisionList[i]['modifiedDate']) <= currentTime:
            # Add the data from this revision
            if "lastModifyingUserName" in revisionList[i]:
                name = revisionList[i]['lastModifyingUserName']
                increment.makeEditor(name).name = name
            i += 1
        currentTime += stats.timeline.incrementSize
