# This example shows how to switch between environments i.e. production, staging, etc.
# This method involves first exporting all account id, api key as environment variables.
# By default, the program looks for the environment variables NR_API_KEY and NR_ACCOUNT_KEY.
# If the argument property is not none, then the program appends the environment string to NR_API_KEY. For example:
# NR_API_KEY_PROD
# When naming your environment variables, ensure to follow this naming convention.

from nrql.api import NRQL
from pprint import pprint

nrql = NRQL()
nrql.environment = 'PROD'

req = nrql.query("select uniqueCount(containerId) from NrDailyUsage facet apmAppName since this quarter")

pprint(req)
