from nrql.api import NRQL
from pprint import pprint

nrql = NRQL()
nrql.verbose = True
req = nrql.query("select uniqueCount(containerId) from NrDailyUsage facet apmAppName since this quarter")
pprint(req)
