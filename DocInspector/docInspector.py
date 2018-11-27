import os
from argparse import ArgumentParser
from os import path
from typing import Dict, Callable

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.contrib import dictionary_storage

from DocInspector import tryCollectFromId, DocStats, outputPlain, outputHTML, outputCsv

FOLDER_MIME = "application/vnd.google-apps.folder"
FILE__MIME = "application/vnd.google-apps.document"
folder = os.path.dirname(__file__)
outputLookup: Dict[str, Callable[[DocStats], str]] = {
    "html": outputHTML,
    "csv": outputCsv,
    "plain": outputPlain
}


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
                        help='The start and end date range from which statistics will be extracted in the format '
                             '"dd-mm-yyyy/dd-mm-yyyy". Value will default to lifespan of the document if left blank '
                             'or value entered is outside of document lifespan')

    parser.add_argument('-t, --time', dest='timeIncrement', type=str, default='1:0:0',
                        required=False,
                        help="Time increment in which changes will be displayed in the format 'd:h:m'. Only "
                             "increments with recognised changes will be displayed")

    parser.add_argument('-u, --unsafe', dest='isUnsafe', action='store_true', default=False,
                        required=False,
                        help='Unsafe API which will gather a larger amount of date from the same date range. Use this '
                             'to gather more data for each increment of time')

    parser.add_argument('-f, --fine', dest='useFine', action='store_true', default=False,
                        required=False,
                        help='Use a finer level of detail with the unsafe API. This may take a while as large amounts '
                             'of data are being retrieved')

    parser.add_argument('-c, --cache', dest='cache', action='store_true', default=False,
                        required=False,
                        help='Caches login details to prevent re-authentication. Use this to store credentials so '
                             'that authentication is only prompted once')

    parser.add_argument('-p --path', dest='path', type=str, required=False, default=None,
                        help='The file path to write the data to. A new file will be created if none exists. If none '
                             'is provided defaults to writing it to stdout')

    parser.add_argument('-o --output', dest='output', type=str, choices=outputLookup.keys(), required=False,
                        default='plain',
                        help='The format to output the data in. Defaults to plain output. Valid output formats are '
                             '"html" - A html visual output')
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
        store = file.Storage(folder + '/token.json')
    else:
        store = dictionary_storage.DictionaryStorage({}, 'token')

    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(folder + '/credentials.json', scope)
        creds = tools.run_flow(flow, store, args)
    service = build('drive', 'v2', http=creds.authorize(Http()))

    if not args.cache and os.path.exists(folder + '/token.json'):
        os.remove(folder + '/token.json')
    return service


def writeToFile(data, file_path=None):
    """
    Attempts to write the data to the given file.
    Creates a new file if none-exists.

    If no path is provided then the data is simply written to stdout
    :param data:
    :param path:
    :return:
    """
    if file_path:
        # create file and write contents
        file_path = path.abspath(file_path)
        with open(file_path, 'w', encoding='utf8') as f:
            f.write(data)
    else:
        # print data
        print(data)


def main():
    print("Authenticating")
    args = parseArguments()
    service = authenticate('https://www.googleapis.com/auth/drive'
                           if args.isUnsafe else
                           'https://www.googleapis.com/auth/drive.metadata.readonly',
                           args)
    print("Collecting stats")
    unsafeLevel = (2 if args.useFine else 1) if args.isUnsafe else 0
    globalStats, fileStats = tryCollectFromId(args.fileId, service, args.timeIncrement, unsafeLevel)
    # Output stats
    print("Outputting data")
    writeToFile(outputLookup[args.output](globalStats), args.path)
    if fileStats:
        for fileStat in fileStats:
            writeToFile(outputLookup[args.output](fileStat), args.path)


if __name__ == '__main__':
    main()
