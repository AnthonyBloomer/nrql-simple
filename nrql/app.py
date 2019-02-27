from .api import NRQL
import json
import csv
from argparse import ArgumentParser

from pygments import highlight, lexers, formatters


def arg_parser():
    parser = ArgumentParser(prog='nrql-simple')
    parser.add_argument('stmt',
                        help="The NRQL statement.")
    parser.add_argument('--region', '--r',
                        default='US',
                        help="Pass this flag to set your region (EU or US) By default the region is set to US.")
    parser.add_argument('--env', '--e',
                        help="Environment handler.")
    parser.add_argument('--filename', '--f',
                        default='events.csv',
                        help="The output CSV filename. Default is events.csv")
    parser.add_argument('--csv', '--c',
                        dest='output_csv',
                        action='store_true',
                        default=False,
                        help="Pass this flag to output the Event data to CSV.")
    parser.add_argument('--verbose', '--v',
                        dest='verbose',
                        action='store_true',
                        default=False,
                        help="Pass this flag if you want the whole response.")
    args = parser.parse_args()
    return args


def export_as_csv(data, filename):
    with open(filename, 'wb') as f:
        w = csv.writer(f)
        w.writerow([k for k in data[0].keys()])
        for ele in data:
            w.writerow([d for d in ele.itervalues()])


def prettyjson(req):
    formatted_json = json.dumps(req, sort_keys=True, indent=4)
    return highlight(str(formatted_json).encode('utf-8'),
                     lexers.JsonLexer(),
                     formatters.TerminalFormatter())


def main():
    nrql = NRQL()
    args = arg_parser()
    nrql.region = args.region
    nrql.verbose = args.verbose
    nrql.environment = args.env
    req = nrql.query(args.stmt)
    if args.output_csv:
        if 'results' in req and 'events' in req['results'][0] and len(req['results'][0]['events']) > 0:
            req.pop('metadata', None)
            req.pop('performanceStats', None)
            export_as_csv(req['results'][0]['events'], args.filename)
            print("Exported to csv: %s" % args.filename)
        else:
            print(prettyjson(req))
    else:
        print(prettyjson(req))


if __name__ == '__main__':
    main()
