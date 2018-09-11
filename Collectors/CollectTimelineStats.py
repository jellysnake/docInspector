from DocStats import DocStats
from timeline import create_timeline


def collectTimelineStats(stats:DocStats, service):
    rev_meta = service.revisions().list(fileId=stats.general.id).execute()
    create_timeline(rev_meta)
