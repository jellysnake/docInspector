from DocStats import DocStats
from Helpers import timeToMilli, calculateTimelineStart


def collectTimelineStats(stats: DocStats, service, args):
    """
    Collects stats for the timeline from the official api.
    At present this is limited to just the last editor in each major revision in each increment

    :param stats: The stat object to fill up
    :param service: The service to use to make any calls to the api
    :param args: The arguments passed into the program
    """

    rev_meta = service.revisions().list(fileId=stats.general.id).execute()
    currentTime = calculateTimelineStart(timeToMilli(stats.general.creationDate), stats.timeline.incrementSize)

    i = 0
    # Iterate until we run out of revisions
    while i < len(rev_meta['items']):
        increment = stats.timeline.makeIncrement()
        # Iterate whilst we are in the current increment
        # Check to make sure we don't run out of revisions
        while i < len(rev_meta['items']) and timeToMilli(rev_meta['items'][i]['modifiedDate']) <= currentTime:
            # Add the data from this revision
            increment.makeEditor(rev_meta['items'][i]['lastModifyingUserName'])
            i += 1
        currentTime += stats.timeline.incrementSize
