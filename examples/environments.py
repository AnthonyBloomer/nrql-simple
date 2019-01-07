from nrql.api import NRQL
from pprint import pprint

nrql = NRQL()
nrql.environment = 'PROD'
req = nrql.query("select uniqueCount(containerId) from NrDailyUsage facet apmAppName since this quarter")
pprint(req)
