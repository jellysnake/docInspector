from typing import List, Tuple, Optional

from DocInspector import DocStats
from DocInspector.Collectors import *

FOLDER_MIME = "application/vnd.google-apps.folder"
FILE__MIME = "application/vnd.google-apps.document"


def collectFromFile(fileId, service, incrementSize, unsafeLevel):
    # Build docstats
    docStats = DocStats(incrementSize)
    docStats.general.id = fileId

    # Get general stats
    collectGeneralStats(docStats, service)

    # Get individual stats
    collectIndividualStats(docStats, service)

    #  Get timeline stats
    collectTimelineStats(docStats, service)

    if unsafeLevel > 0:
        # Get unsafe Stats
        collectUnsafeStats(docStats, service, unsafeLevel > 1)
    return docStats


def getFilesInFolder(service, id) -> Optional[List]:
    """
    Lists all the id's of the files in a folder

    :param service: The service to request with
    :param id: The id of the folder
    :return: The ids of the child files
    """
    children = service.children().list(folderId=id).execute()
    children = [child['id'] for child in children['items']]
    children = [child for child in children if getMimeType(service, child) == FILE__MIME]
    return children


def getMimeType(service, id) -> str:
    """
    Gets the mime type of a given id

    :param service: The service to use for requesting
    :param id: The ID of the item to check
    :return: True if it's a folder. False if it's a file. None if it's neither
    """
    data = service.files().get(fileId=id).execute()
    return data['mimeType'] or ""


def collectFromFolder(folderId, service, incrementSize, unsafeLevel) -> Tuple[DocStats, List[DocStats]]:
    print("Processing folder")
    fileIds = getFilesInFolder(service, folderId)
    fileStats = []

    # Do stats for all files
    globalStats = DocStats(incrementSize)
    globalStats.general.id = folderId
    collectGeneralStats(globalStats, service)

    for fileId in fileIds:
        print(f"Processing file: {fileId}")
        fileStats.append(collectFromFile(fileId, service, incrementSize, unsafeLevel))
        globalStats.mergeIn(fileStats[-1])
    globalStats.general.creationDate = fileStats[0].general.creationDate

    return globalStats, fileStats


def tryCollectFromId(fileId, service, incrementSize, unsafeLevel):
    itemType = getMimeType(service, fileId)
    if itemType == FOLDER_MIME:
        return collectFromFolder(fileId, service, incrementSize, unsafeLevel)
    elif itemType == FILE__MIME:
        print("Processing file")
        docStats = collectFromFile(fileId, service, incrementSize, unsafeLevel)
        return docStats, None
    else:
        print(f"Unknown file type. '{itemType}'")
