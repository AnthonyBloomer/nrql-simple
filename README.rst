nrql-simple
===========

nrql-simple provides a dead-simple way to interact with the New Relic
Insights query API. You can interact with this library programmatically
or via the Command Line.

Installation
------------

nrql-simple is available on the `Python Package Index
(PyPI) <https://pypi.org/project/nrql-simple/>`__. You can install
nrql-simple using pip.

::

   virtualenv env
   source env/bin/activate
   pip install nrql-simple

To install the development version, run:

::

   pip install https://github.com/AnthonyBloomer/nrql-simple/archive/master.zip

About
-----

The New Relic Insights query API is a REST API for querying Insights
event data. After you supply a standard NRQL query via HTTPS request,
the query API returns a JSON response for parsing.

To use the API, you need a query key. You can have multiple query keys,
and any query key can be used to initiate any Insights API query. If you
have multiple systems querying Insights or different data destinations,
New Relic recommends you use multiple query keys to enhance data
security.

To create a new query key:

1. Go to `insights.newrelic.com <https://insights.newrelic.com>`__ >
   Manage data > API keys.
2. Select the plus icon next to the Query keys heading.
3. Enter a short description of the key.
4. Select Save your notes.

You will also need make note of your New Relic Account ID. To find the
account ID for your New Relic account:

1. Sign in to `rpm.newrelic.com <https://rpm.newrelic.com>`__.
2. In the URL bar, copy the number after the /accounts/ portion of the
   URL: ``https://rpm.newrelic.com/accounts/ACCOUNT_ID/``

Usage
-----

The first step is to initialize a NRQL object and set your API Key and
Account ID.

.. code:: python

   from nrql.api import NRQL
   nrql = NRQL()
   nrql.api_key = 'YOUR_API_KEY'
   nrql.account_id = 'YOUR_ACCOUNT_ID'

Alternatively, you can export your API key and Account ID as environment
variables.

::

   $ export NR_API_KEY='YOUR_API_KEY'
   $ export NR_ACCOUNT_ID='YOUR_ACCOUNT_ID'

Then simply pass your NRQL statement into the ``query`` function. NRQL
is a query language similar to SQL that you use to make calls against
the New Relic Insights Events database. Refer to the `NRQL
documentation <https://docs.newrelic.com/docs/insights/nrql-new-relic-query-language/nrql-resources/nrql-syntax-components-functions>`__
for examples and usage information.

Consider the following example that gets the unique number of container
IDs for each application since this quarter.

.. code:: python

   req = nrql.query("select uniqueCount(containerId) from NrDailyUsage facet apmAppName since this quarter")
   for k in req['facets']:
       print("%s : %s" % (k['name'], k['results'][0]['uniqueCount']))

To use the CLI, you must first export your API key and Account ID as
environment variables. Then, simply call the ``nrql`` command with your
NRQL statement as an argument.

::

   nrql "select uniqueCount(containerId) from nrdailyusage where apmAppName = 'SinatraApp' since this quarter"

The above command will output JSON formatted like this:

.. code:: json

   {
       "metadata": {
           "beginTime": "2018-10-01T00:00:00Z", 
           "beginTimeMillis": 1538352000000, 
           "contents": [
               {
                   "attribute": "containerId", 
                   "function": "uniquecount", 
                   "simple": true
               }
           ], 
           "endTime": "2018-12-28T19:46:49Z", 
           "endTimeMillis": 1546026409529, 
           "eventType": "NrDailyUsage", 
           "eventTypes": [
               "NrDailyUsage"
           ], 
           "guid": "40507b80-9084-b36e-0de4-ceb3e617c7fa", 
           "messages": [], 
           "openEnded": true, 
           "rawCompareWith": "", 
           "rawSince": "THIS QUARTER", 
           "rawUntil": "NOW", 
           "routerGuid": "790fecc4-a57d-4f35-88c9-6acc8f5a413c"
       }, 
       "performanceStats": {
           "cacheMisses": 1, 
           "cacheSkipped": 2, 
           "decompressedBytes": 72593, 
           "decompressionCacheEnabledCount": 0, 
           "decompressionCacheGetTime": 0, 
           "decompressionCachePutTime": 0, 
           "decompressionCount": 0, 
           "decompressionOutputBytes": 0, 
           "decompressionTime": 0, 
           "fileProcessingTime": 69, 
           "fileReadCount": 179, 
           "fullCacheHits": 176, 
           "ignoredFiles": 0, 
           "inspectedCount": 11470, 
           "ioBytes": 0, 
           "ioTime": 0, 
           "matchCount": 264, 
           "maxInspectedCount": 243, 
           "mergeTime": 0, 
           "minInspectedCount": 1, 
           "omittedCount": 0, 
           "partialCacheHits": 0, 
           "processCount": 174, 
           "rawBytes": 31159, 
           "responseBodyBytes": 29601, 
           "runningQueriesTotal": 2113, 
           "slowLaneFileProcessingTime": 0, 
           "slowLaneFiles": 0, 
           "slowLaneWaitTime": 0, 
           "subqueryWeightUpdates": 0, 
           "sumFileProcessingTimePercentile": 0.0, 
           "sumSubqueryWeight": 174.0, 
           "sumSubqueryWeightStartFileProcessingTime": 189149, 
           "wallClockTime": 71
       }, 
       "results": [
           {
               "uniqueCount": 175
           }
       ]
   }

Contributing
------------

-  Fork the project and clone locally.
-  Create a new branch for what you’re going to work on.
-  Push to your origin repository.
-  Create a new pull request in GitHub.
