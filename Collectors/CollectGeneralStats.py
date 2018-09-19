from DocStats import DocStats


def collectGeneralStats(stats: DocStats, service):
    # Print file name
    file_meta = service.files().get(fileId=stats.general.id).execute()
    stats.general.name = file_meta.get('title')

    # Print link to google doc file
    stats.general.link = file_meta.get('selfLink')
    
    # Print date of creation
    creationDate = file_meta.get('createdDate')
    creationDate = creationDate[:9]
    stats.general.creationDate = creationDate
    
        


