nrql-simple
===========

|Build Status| |codecov|

nrql-simple is a small Python library that provides a convenient way to
interact with the `New Relic Insights query
API <https://docs.newrelic.com/docs/insights/insights-api/get-data/query-insights-event-data-api>`__.
You can interact with this library programmatically or via the Command
Line.

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

Command Line Usage
~~~~~~~~~~~~~~~~~~

::

   usage: nrql [-h] [--region REGION] [--env ENV] [--filename FILENAME]
                      [--csv] [--verbose]
                      stmt

   positional arguments:
     stmt                  The NRQL statement.

   optional arguments:
     -h, --help            show this help message and exit
     --region REGION, --r REGION
                           Pass this flag to set your region (EU or US) By
                           default the region is set to US.
     --env ENV, --e ENV    Environment handler.
     --filename FILENAME, --f FILENAME
                           The output CSV filename. Default is events.csv
     --csv, --c            Pass this flag to output the Event data to CSV.
     --verbose, --v        Pass this flag if you want the whole response.

To use the CLI, you must first export your API key and Account ID as
environment variables.

::

   $ export NR_API_KEY='YOUR_API_KEY'
   $ export NR_ACCOUNT_ID='YOUR_ACCOUNT_ID'

Then, simply call the ``nrql`` command with your NRQL statement as an
argument.

::

   nrql "select uniqueCount(containerId) from nrdailyusage where apmAppName = 'SinatraApp' since this quarter"

The above command will output JSON formatted like this:

.. code:: json

   {
       "results": [
           {
               "uniqueCount": 175
           }
       ]
   }

By default the output will not include the ``performanceStats`` or
``metadata`` objects from the response. To output the entire JSON
response, pass the ``--verbose`` flag.

::

   nrql "select uniqueCount(containerId) from NrDailyUsage facet apmAppName since this quarter" --verbose

Managing multiple accounts
--------------------------

If you wish to easily switch between accounts, you can use the
``environment`` class method. If you are using the command line tool use
the ``env`` command line argument. For example:

.. code:: python

   from nrql.api import NRQL
   nrql = NRQL()
   nrql.environment = "PROD"

Or via the command line:

.. code:: bash

   nrql "select uniqueCount(containerId) from NrDailyUsage facet apmAppName since this quarter" --env='PROD'

By default, the program looks for the environment variables
``NR_API_KEY`` and ``NR_ACCOUNT_KEY``.

If the ``env`` argument is not none, then the program appends the
environment string to ``NR_API_KEY``. For example:

::

   NR_API_KEY_PROD

When naming your environment variables, ensure to follow this naming
convention.

Output as CSV
-------------

To export Event data to a csv file via the CLI, pass the ``--csv``
argument, for example:

::

   nrql "select * from Transaction where appName = 'RabbitMQ' since this quarter" --csv 

This will export a csv file (``events.csv``) to the current working
directory.

To change the output file, pass the ``--filename`` argument:

::

   nrql "select * from Transaction where appName = 'RabbitMQ' since this quarter" --csv --filename='rabbit.csv'

Tests
-----

The Python ``unittest`` module contains its own test discovery function,
which you can run from the command line:

::

    python -m unittest discover tests/

Contributing
------------

-  Fork the project and clone locally.
-  Create a new branch for what you’re going to work on.
-  Push to your origin repository.
-  Create a new pull request in GitHub.

.. |Build Status| image:: https://travis-ci.org/AnthonyBloomer/nrql-simple.svg?branch=master
   :target: https://travis-ci.org/AnthonyBloomer/nrql-simple
.. |codecov| image:: https://codecov.io/gh/AnthonyBloomer/nrql-simple/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/AnthonyBloomer/nrql-simple
