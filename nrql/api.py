import requests
import os


class NRQL(object):

    def __init__(self, api_key=None, account_id=None):
        self._api_key = api_key
        self._account_id = account_id
        self._url = "https://insights-api.newrelic.com/v1/accounts/%s/query?nrql=%s"
        self._eu_url = "https://insights-api.eu.newrelic.com/v1/accounts/%s/query?nrql=%s"
        self._region = 'US'
        self._verbose = False
        self._environment = None

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

    def query(self, stmt):

        if not self.api_key or not self.account_id:
            if os.environ.get('NR_API_KEY') and os.environ.get('NR_ACCOUNT_ID'):
                self._api_key = os.environ.get('NR_API_KEY')
                self._account_id = os.environ.get('NR_ACCOUNT_ID')
            else:
                raise Exception("An api key and account id is required.")

        if not self.region == 'US':
            self._url = self._eu_url

        req = requests.get(self._url % (self.account_id, stmt), headers={"X-Query-Key": self.api_key})

        response = req.json()

        if not self.verbose:
            response.pop('metadata', None)
            response.pop('performanceStats', None)

        return response
