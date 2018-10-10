from DocStats import DocStats


def collectGeneralStats(stats: DocStats, service):
    """
    Collects a bunch of general stats about the document
    At present this includes the creation date, self link and title

    :param stats: The object to store the stats in
    :param service: The service to use to make api calls
    """
    # Call the data from the api.
    file_meta = service.files().get(fileId=stats.general.id).execute()
    # Load in file stats
    stats.general.name = file_meta.get('title')
    stats.general.link = file_meta.get('selfLink')
    stats.general.creationDate = file_meta.get('createdDate')

    stats.timeline.setTimelineStart(stats.general.creationDate)
