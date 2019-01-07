import unittest
from subprocess import check_output

from nrql.api import NRQL


class NRQLTests(unittest.TestCase):

    def test_query(self):
        nrql = NRQL()
        req = nrql.query("select uniqueCount(containerId) from NrDailyUsage facet apmAppName since this quarter")
        self.assertIn('facets', req)
        self.assertTrue(len(req['facets']) > 0)
        for k in req['facets']:
            print("%s : %s" % (k['name'], k['results'][0]['uniqueCount']))

    def test_query_invalid_query(self):
        nrql = NRQL()
        req = nrql.query("from table select *")
        self.assertIn('results', req)
        self.assertTrue(len(req['results'][0]['events']) == 0)
