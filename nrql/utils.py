import json

import pandas as pd
from pygments import highlight, lexers, formatters


def export_as_csv(data, filename):
    if not (
        "results" in data
        and "events" in data["results"][0]
        and len(data["results"][0]["events"]) > 0
    ):
        print(prettyjson(data))
        return
    data.pop("metadata", None)
    data.pop("performanceStats", None)
    df = pd.DataFrame(data["results"][0]["events"])
    df.to_csv(filename, index=False, header=True)
    print("Exported to csv: %s" % filename)


def prettyjson(req):
    formatted_json = json.dumps(req, sort_keys=True, indent=4)
    return highlight(
        str(formatted_json).encode("utf-8"),
        lexers.JsonLexer(),
        formatters.TerminalFormatter(),
    )
