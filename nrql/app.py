from .api import NRQL
from .utils import prettyjson, export_as_csv
from .args_parser import arg_parser


def main():
    nrql = NRQL()
    args = arg_parser()
    nrql.region = args.region
    nrql.verbose = args.verbose
    nrql.environment = args.env
    req = nrql.query(args.stmt)
    if args.output_csv:
        export_as_csv(req, args.filename)
    else:
        print(prettyjson(req))


if __name__ == '__main__':
    main()
