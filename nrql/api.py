import requests
import os
from .utils import export_as_csv
import colorful

INSIGHTS_URL = "https://insights-api.newrelic.com/v1/accounts/%s/query"
INSIGHTS_EU_REGION_URL = "https://insights-api.eu.newrelic.com/v1/accounts/%s/query"


class NRQL(object):
    def __init__(self, api_key=None, account_id=None):
        self.api_key = api_key
        self.account_id = account_id
        self._url = INSIGHTS_URL
        self._eu_url = INSIGHTS_EU_REGION_URL
        self._region = "US"
        self._verbose = False
        self._csv = False
        self._environment = None
        self._stmt = []
        self._filename = "events.csv"

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, region):
        self._region = region

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    @property
    def csv(self):
        return self._csv

    @csv.setter
    def csv(self, csv):
        self._csv = csv

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, verbose):
        self._verbose = verbose

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, environment):
        self._environment = environment

    @staticmethod
    def _print_messages(response):
        if "metadata" in response and "messages" in response["metadata"]:
            for message in response["metadata"]["messages"]:
                print(colorful.bold(message))

    def _multiple_account_handler(self):
        if self.environment is None:
            nr_api_key = os.environ.get("NR_API_KEY")
            nr_account_id = os.environ.get("NR_ACCOUNT_ID")
        else:
            nr_api_key = os.environ.get("NR_API_KEY_%s" % self.environment.upper())
            nr_account_id = os.environ.get(
                "NR_ACCOUNT_ID_%s" % self.environment.upper()
            )
            if not nr_account_id or not nr_api_key:
                print(colorful.bold("%s account environment variables not set." % self.environment))
        return nr_api_key, nr_account_id

    def _make_request(self, query_stmt):
        payload = {"nrql": query_stmt}
        req = requests.get(
            self._url % self.account_id,
            headers={"X-Query-Key": self.api_key},
            params=payload,
        )
        if self.verbose:
            print(colorful.bold("Request URL: %s" % req.url))
            print(colorful.bold("Status Code: %s" % req.status_code))
        response = req.json()
        self._print_messages(response)
        if not self.verbose:
            response.pop("metadata", None)
            response.pop("performanceStats", None)

        return response

    def query(self, stmt):
        nr_api_key, nr_account_id = self._multiple_account_handler()
        if not self.api_key or not self.account_id:
            if nr_api_key and nr_account_id:
                self._api_key = nr_api_key
                self._account_id = nr_account_id
            else:
                raise Exception("An api key and account id is required.")

        if not self.region == "US":
            self._url = self._eu_url

        resp = self._make_request(stmt)
        if self.csv:
            export_as_csv(resp, self.filename)
        else:
            return resp
