from .api import NRQL
import json
from argparse import ArgumentParser

from pygments import highlight, lexers, formatters


def main():
    parser = ArgumentParser(prog='nrql-simple')
    parser.add_argument('stmt',
                        help="The NRQL statement.")
    parser.add_argument('--verbose', '--v',
                        dest='verbose',
                        action='store_true',
                        default=False,
                        help="Pass this flag if you want the whole response.")
    parser.add_argument('region',
                        nargs='?',
                        default='US',
                        help="Pass this flag to set your region (EU or US) By default the region is set to US.")
    parser.add_argument('env',
                        nargs='?',
                        help="Environment handler.")
    args = parser.parse_args()

    nrql = NRQL()

    nrql.region = args.region
    nrql.verbose = args.verbose
    nrql.environment = args.env

    req = nrql.query(args.stmt)

    formatted_json = json.dumps(req, sort_keys=True, indent=4)
    colorful_json = highlight(str(formatted_json).encode('utf-8'), lexers.JsonLexer(), formatters.TerminalFormatter())

    print(colorful_json)


if __name__ == '__main__':
    main()
