from argparse import ArgumentParser


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
