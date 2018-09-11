from DocStats import DocStats
from DocumentEditors import findAndPrintEditors
from ModifyDateRange import getDatesModifiedWithin


def collectIndividualStats(stats: DocStats, service, args):
    # Print Document Editors
    rev_meta = service.revisions().list(fileId=stats.general.id).execute()
    findAndPrintEditors(rev_meta)

    if args.dates:
        # Print Modified dates
        getDatesModifiedWithin(args.dates, rev_meta)
