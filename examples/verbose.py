# This example shows how to enable verbose mode.
# By default the output will not include the performanceStats or metadata objects from the response.
# To output the entire JSON response, set verbose = True.


from nrql.api import NRQL
from pprint import pprint

nrql = NRQL()
nrql.verbose = True
req = nrql.query("select uniqueCount(containerId) from NrDailyUsage facet apmAppName since this quarter")
pprint(req)
