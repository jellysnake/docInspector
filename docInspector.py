from argparse import ArgumentParser
from typing import List, Optional

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from Collectors import *
from DocStats import DocStats
from OutputStats import outputStats


def parseArguments():
    """
    Builds the argument parser, and then calls it to parse the arguments
    Also correctly inherits from the oauth2client arguments.

    :return: The argument object of the parsed arguments
    """
    parser = ArgumentParser(description='Runs statistical analysis on the contributions to google doc files',
                            parents=[tools.argparser])
    parser.add_argument('fileId', metavar='docId', type=str,
                        help='The document id to scrape')

    parser.add_argument('-d, --dates', dest='dates', action='store', required=False,
                        help='The start and date to load from. Format of "dd-mm-yyyy/dd-mm-yyyy"')

    parser.add_argument('-t, --time', dest='timeIncrement', type=str, default='1:0:0',
                        required=False, help="The time increment to display changes in. Format of 'd:h:m'")

    parser.add_argument('-u, --unsafe', dest='isUnsafe', action='store_true', default=False,
                        required=False, help='Use the unsafe API to gain more data')

    parser.add_argument('-f, --fine', dest='useFine', action='store_true', default=False,
                        required=False, help='Use a finer level of detail with the unsafe API')

    return parser.parse_args()


def authenticate(scope, args):
    """
    Performs the authentication flow.
    Handles the credential management

    :param scope: The scope to authenticate with
    :param args: The arguments passed in to the program.
    :return: (The drive api service, The http requests object)
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', scope)
        creds = tools.run_flow(flow, store, args)
    http = creds.authorize(Http())
    service = build('drive', 'v2', http=http)

    # TODO: Re-add
    # store.delete()
    return service, http


def getStatsForFile(service, http, args, id) -> DocStats:
    """
    Calls subfunctions to load in stats for the given file.

    :param service: The service to use for the API requests
    :param http: The Requests object to use for the other requests
    :param args: The arguments passed to the program
    :param id: The ID of the file
    :return: The DocStats object containing the file's stats
    """
    # Build docstats
    docStats = DocStats(args.timeIncrement)
    docStats.general.id = id

    # Get general stats
    collectGeneralStats(docStats, service)

    # Get individual stats
    collectIndividualStats(docStats, service, args)

    #  Get timeline stats
    collectTimelineStats(docStats, service, args)

    if args.isUnsafe:
        # Get unsafe Stats
        collectUnsafeStats(docStats, http, args)
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


def main():
    args = parseArguments()
    service, http = authenticate('https://www.googleapis.com/auth/drive'
                                 if args.isUnsafe else
                                 'https://www.googleapis.com/auth/drive.metadata.readonly',
                                 args)
    itemType = getMimeType(service, args.fileId)
    if itemType == FOLDER_MIME:
        print("Processing folder")
        fileIds = getFilesInFolder(service, args.fileId)
        fileStats = []

        # Do stats for all files
        globalStats = DocStats(args.timeIncrement)
        for fileId in fileIds:
            print(f"Processing file: {fileId}")
            fileStats.append(getStatsForFile(service, http, args, fileId))
            globalStats.mergeIn(fileStats[-1])
        globalStats.general.creationDate = fileStats[0].general.creationDate
        # Output stats
        print("Outputting data")
        outputStats(globalStats, args)
        for fileStat in fileStats:
            outputStats(fileStat, args)

    elif itemType == FILE__MIME:
        print("Processing file")
        docStats = getStatsForFile(service, http, args, args.fileId)
        outputStats(docStats, args)
    else:
        print(f"Unknown file type. '{itemType}'")


FOLDER_MIME = "application/vnd.google-apps.folder"
FILE__MIME = "application/vnd.google-apps.document"
if __name__ == '__main__':
    main()
