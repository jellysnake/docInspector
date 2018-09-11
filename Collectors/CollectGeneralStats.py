from DocStats import DocStats


def collectGeneralStats(stats: DocStats, service):
    # Print file name
    file_meta = service.files().get(fileId=stats.general.id).execute()
    print(file_meta.get('title'))
