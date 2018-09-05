from argparse import ArgumentParser

from oauth2client import tools


def parseArguments():
    parser = ArgumentParser(description='Runs statistical analysis on the contributions to google doc files',
                            parents=[tools.argparser])
    parser.add_argument('fileId', metavar='docId', type=str,
                        help='The document id to scrape')

    parser.add_argument('-d, --dates', dest='dates', action='store', required=False,
                        help='The start and date to load from. Format of "dd-mm-yyyy/"dd-mm-yyyy"')

    parser.add_argument('-u, --unsafe', dest='isUnsafe', action='store_true', default=False,
                        required=False, help='Use the unsafe API to gain more data')

    parser.add_argument('-f, --fine', dest='useFine', action='store_true', default=False,
                        required=False, help='Use a finer level of detail with the unsafe API')

    return parser.parse_args()


if __name__ == '__main__':
    args = parseArguments()