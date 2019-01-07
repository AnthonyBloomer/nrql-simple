# nrql-simple

[![Build Status](https://travis-ci.org/AnthonyBloomer/nrql-simple.svg?branch=master)](https://travis-ci.org/AnthonyBloomer/nrql-simple)
[![codecov](https://codecov.io/gh/AnthonyBloomer/nrql-simple/branch/master/graph/badge.svg)](https://codecov.io/gh/AnthonyBloomer/nrql-simple)

nrql-simple is a small Python library that provides a convenient way to interact with the [New Relic Insights query API](https://docs.newrelic.com/docs/insights/insights-api/get-data/query-insights-event-data-api). You can interact with this library programmatically or via the Command Line.

## Installation


nrql-simple is available on the [Python Package Index (PyPI)](https://pypi.org/project/nrql-simple/). You can install nrql-simple using pip.

```
virtualenv env
source env/bin/activate
pip install nrql-simple
```

To install the development version, run:

```
pip install https://github.com/AnthonyBloomer/nrql-simple/archive/master.zip
```

## About

The New Relic Insights query API is a REST API for querying Insights event data. After you supply a standard NRQL query via HTTPS request, the query API returns a JSON response for parsing.

To use the API, you need a query key. You can have multiple query keys, and any query key can be used to initiate any Insights API query. If you have multiple systems querying Insights or different data destinations, New Relic recommends you use multiple query keys to enhance data security.

To create a new query key:

1. Go to [insights.newrelic.com](https://insights.newrelic.com) > Manage data > API keys.
2. Select the plus icon next to the Query keys heading.
3. Enter a short description of the key.
4. Select Save your notes.

You will also need make note of your New Relic Account ID. To find the account ID for your New Relic account:

1. Sign in to [rpm.newrelic.com](https://rpm.newrelic.com).
2. In the URL bar, copy the number after the /accounts/ portion of the URL: `https://rpm.newrelic.com/accounts/ACCOUNT_ID/`

## Usage

The first step is to initialize a NRQL object and set your API Key and Account ID.

``` python
from nrql.api import NRQL
nrql = NRQL()
nrql.api_key = 'YOUR_API_KEY'
nrql.account_id = 'YOUR_ACCOUNT_ID'
```

Alternatively, you can export your API key and Account ID as environment variables.

```
$ export NR_API_KEY='YOUR_API_KEY'
$ export NR_ACCOUNT_ID='YOUR_ACCOUNT_ID'
```

Then simply pass your NRQL statement into the `query` function. NRQL is a query language similar to SQL that you use to make calls against the New Relic Insights Events database. Refer to the [NRQL documentation](https://docs.newrelic.com/docs/insights/nrql-new-relic-query-language/nrql-resources/nrql-syntax-components-functions) for examples and usage information.

Consider the following example that gets the unique number of container IDs for each application since this quarter.

``` python
req = nrql.query("select uniqueCount(containerId) from NrDailyUsage facet apmAppName since this quarter")
for k in req['facets']:
    print("%s : %s" % (k['name'], k['results'][0]['uniqueCount']))
```

### Command Line Usage

```

usage: nrql-simple [-h] [--verbose] stmt [region]

positional arguments:
  stmt            The NRQL statement.
  region          Pass this flag to set your region (EU or US) By default the
                  region is set to US.

optional arguments:
  -h, --help      show this help message and exit
  --verbose, --v  Pass this flag if you want the whole response.

```

To use the CLI, you must first export your API key and Account ID as environment variables. 


```
$ export NR_API_KEY='YOUR_API_KEY'
$ export NR_ACCOUNT_ID='YOUR_ACCOUNT_ID'
```


Then, simply call the `nrql` command with your NRQL statement as an argument.

```
nrql "select uniqueCount(containerId) from nrdailyusage where apmAppName = 'SinatraApp' since this quarter"
```

The above command will output JSON formatted like this:

``` json
{
    "results": [
        {
            "uniqueCount": 175
        }
    ]
}
```

By default the output will not include the `performanceStats` or `metadata` objects from the response. 
To output the entire JSON response, pass the `--verbose` flag.

```
nrql "select uniqueCount(containerId) from NrDailyUsage facet apmAppName since this quarter" --verbose
```

## Managing multiple accounts

If you wish to easily switch between accounts, you can use the `environment` class method.
If you are using the command line tool use the `environment` command line argument. For example:

```python
from nrql.api import NRQL
nrql = NRQL()
nrql.environment = "PROD"
```

Or via the command line:

``` bash
nrql "select uniqueCount(containerId) from NrDailyUsage facet apmAppName since this quarter" environment='PROD'
```

By default, the program looks for the environment variables `NR_API_KEY` and `NR_ACCOUNT_KEY`. 

If the `environment` argument is not none, then the program appends the environment string to `NR_API_KEY`. For example:

```
NR_API_KEY_PROD
```

When naming your environment variables, ensure to follow this naming convention.

## Tests

The Python `unittest` module contains its own test discovery function, which you can run from the command line:

```
 python -m unittest discover tests/
```


## Contributing

- Fork the project and clone locally.
- Create a new branch for what you're going to work on.
- Push to your origin repository.
- Create a new pull request in GitHub.

