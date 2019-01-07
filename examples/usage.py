# This example gets the unique number of container IDs for each application since this quarter.

from nrql.api import NRQL

nrql = NRQL()

req = nrql.query("select uniqueCount(containerId) from NrDailyUsage facet apmAppName since this quarter")

for k in req['facets']:
    print("%s : %s" % (k['name'], k['results'][0]['uniqueCount']))
