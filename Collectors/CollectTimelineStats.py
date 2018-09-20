from datetime import datetime

from DocStats import DocStats
from OutputStats import outputStats


def collectTimelineStats(stats: DocStats, service, args):
    days, hours, mins = map(int, args.timeIncrement.split(':'))
    timeSize = (((days * 24) + hours) * 60 + mins) * 60 * 1000
    rev_meta = service.revisions().list(fileId=stats.general.id).execute()
    currentTime = timeToMilli(stats.general.creationDate)

    i = 0
    while i < len(rev_meta['items']):
        increment = stats.timeline.makeIncrement()
        while i < len(rev_meta['items']) and timeToMilli(rev_meta['items'][i]['modifiedDate']) <= currentTime:
            increment.editors.add(rev_meta['items'][i]['lastModifyingUserName'])
            i += 1
        currentTime += timeSize


def timeToMilli(time):
    return datetime.strptime(time,
                            "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
