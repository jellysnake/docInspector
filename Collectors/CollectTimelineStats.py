from DocStats import DocStats
from OutputStats import outputStats


def collectTimelineStats(stats: DocStats, service):
    rev_meta = service.revisions().list(fileId=stats.general.id).execute()
    outputStats(stats, '')
