import os
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
                        help='The document id to scrape')

    parser.add_argument('-d, --dates', dest='dates', action='store', required=False,
                        help='The start and date to load from. Format of "dd-mm-yyyy/dd-mm-yyyy"')

    parser.add_argument('-t, --time', dest='timeIncrement', type=str, default='1:0:0',
                        required=False, help="The time increment to display changes in. Format of 'd:h:m'")

    parser.add_argument('-u, --unsafe', dest='isUnsafe', action='store_true', default=False,
                        required=False, help='Use the unsafe API to gain more data')

    parser.add_argument('-f, --fine', dest='useFine', action='store_true', default=False,
                        required=False, help='Use a finer level of detail with the unsafe API')

    parser.add_argument('-c, --cache', dest='cache', action='store_true', default=False,
                        required=False, help='Caches login details to prevent re-authentication.')

    return parser.parse_args()


def authenticate(scope, args):
    """
    Performs the authentication flow.
    Handles the credential management

    :param scope: The scope to authenticate with
    :param args: The arguments passed in to the program.
    :return: (The drive api service, The http requests object)
    """
    if args.cache:
        store = file.Storage('token.json')
    else:
        store = client.Storage()
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', scope)
        creds = tools.run_flow(flow, store, args)
    http = creds.authorize(Http())
    service = build('drive', 'v2', http=http)

    if not args.cache and os.path.exists('token.json'):
        os.remove('token.json')

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
