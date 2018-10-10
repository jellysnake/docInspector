from argparse import ArgumentParser

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
                        help='A valid google document ID from which revision data will be retrieved')

    parser.add_argument('-d, --dates', dest='dates', action='store', required=False,
                        help='The start and end date range from which statistics will be extracted in the format "dd-mm-yyyy/dd-mm-yyyy". Ensure that start and end date are within the range of the documents lifespan')

    parser.add_argument('-t, --time', dest='timeIncrement', type=str, default='1:0:0',
                        required=False, help="Time increment in which changes will be displayed in the format 'd:h:m'. Only increments with recognised changes will be displayed")

    parser.add_argument('-u, --unsafe', dest='isUnsafe', action='store_true', default=False,
                        required=False, help='Unsafe API which will gather a larger amount of date from the same date range. Use this to gather more data for each increment of time')

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

    store.delete()
    return service, http


if __name__ == '__main__':
    args = parseArguments()
    service, http = authenticate('https://www.googleapis.com/auth/drive'
                                 if args.isUnsafe else
                                 'https://www.googleapis.com/auth/drive.metadata.readonly',
                                 args)

    docStats = DocStats(args.timeIncrement)
    docStats.general.id = args.fileId

    # Get general stats
    collectGeneralStats(docStats, service)

    # Get individual stats
    collectIndividualStats(docStats, service, args)

    #  Get timeline stats
    collectTimelineStats(docStats, service, args)

    if args.isUnsafe:
        # Get unsafe Stats
        collectUnsafeStats(docStats, http, args)

    outputStats(docStats, args)
