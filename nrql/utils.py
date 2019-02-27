import csv
import json
from pygments import highlight, lexers, formatters


def export_as_csv(data, filename):
    if 'results' in data and 'events' in data['results'][0] and len(data['results'][0]['events']) > 0:
        data.pop('metadata', None)
        data.pop('performanceStats', None)
    else:
        print(prettyjson(data))
        return
    res = data['results'][0]['events']
    with open(filename, 'wb') as f:
        w = csv.writer(f)
        w.writerow([str(k).encode('utf-8') for k in res[0].keys()])
        for ele in res:
            w.writerow([str(d).encode('utf-8') for d in ele.itervalues()])
    print("Exported to csv: %s" % filename)


def prettyjson(req):
    formatted_json = json.dumps(req, sort_keys=True, indent=4)
    return highlight(str(formatted_json).encode('utf-8'),
                     lexers.JsonLexer(),
                     formatters.TerminalFormatter())
