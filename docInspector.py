from argparse import ArgumentParser

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from DocumentEditors import findAndPrintEditors
from ModifyDateRange import getDatesModifiedWithin
from UnsafeApi import Document
from timeline import create_timeline


def parseArguments():
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
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', scope)
        creds = tools.run_flow(flow, store, args)
    http = creds.authorize(Http())
    service = build('drive', 'v2', http=http)
    store.delete()
    return service, http


def getTotalChanges(document):
    print("Loading all changes. (May take a while, especially if using --fine flag).")
    changes = document.getTotalChanges()
    totalSize = changes.totalAdditions() + changes.totalRemovals()
    users = changes.getUsers()
    for user in users:
        if user != "unknown":
            userSize = changes.userAdditions(user) + changes.userRemovals(user)
            print("%s made %2.2f%% of all changes" % (document.getUser(user).name, (userSize / totalSize) * 100))


def getIncrementData(doc: Document, increment):
    days, hours, mins = map(int, increment.split(':'))
    millis = (((days * 24) + hours) * 60 + mins) * 60 * 1000
    changes = doc.getChangesInIncrement(millis)
    i = 0
    print("Changes per student per increment:")
    for i in changes:
        print(f"{i}'th increment")
        for user in changes[i].getUsers():
            if user != 'unknown':
                print(f"\t{doc.getUser(user)} added {changes[i].userAdditions(user)} chars, "
                      f"and removed {changes[i].userRemovals(user)} "
                      f"in {changes[i].userChanges(user)} edits")
        print("")


if __name__ == '__main__':
    args = parseArguments()
    service, http = authenticate('https://www.googleapis.com/auth/drive'
                                 if args.isUnsafe else
                                 'https://www.googleapis.com/auth/drive.metadata.readonly',
                                 args)

    # Print file name
    file_meta = service.files().get(fileId=args.fileId).execute()
    print(file_meta.get('title'))

    # Print timeline code
    rev_meta = service.revisions().list(fileId=args.fileId).execute()
    file_name = service.files().get(fileId=args.fileId).execute().get('title')
    create_timeline(rev_meta)

    # Print Document Editors
    findAndPrintEditors(rev_meta)

    if args.dates:
        # Print Modified dates
        getDatesModifiedWithin(args.dates, rev_meta)

    # Print Unsafe API
    if args.isUnsafe:
        doc = Document(http, args.fileId, args.useFine)
        getTotalChanges(doc)
        getIncrementData(doc, args.timeIncrement)
