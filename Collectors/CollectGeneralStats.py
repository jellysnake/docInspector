from DocStats import DocStats


def collectGeneralStats(stats: DocStats, service):
    # Print file name
    file_meta = service.files().get(fileId=stats.general.id).execute()
    print(file_meta.get('title'))

    # Print link to google doc file
    print('Link ', file.meta.get('selfLink'))

    # Print date of creation
    creationDate = file_meta.get('createdDate')
    creationDate = creationDate[:9]
    print('Creation Date: ', creationDate)
        


