from api import NRQL
import json
from argparse import ArgumentParser

from pygments import highlight, lexers, formatters


def main():
    parser = ArgumentParser(prog='nrql-simple')
    parser.add_argument('stmt', help="The NRQL statement.")
    args = parser.parse_args()
    nrql = NRQL()
    req = nrql.query(args.stmt)
    formatted_json = json.dumps(req, sort_keys=True, indent=4)
    colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)


if __name__ == '__main__':
    main()
