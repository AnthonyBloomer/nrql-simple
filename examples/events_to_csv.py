# Export Event data to CSV.

from nrql.api import NRQL

nrql = NRQL()
nrql.csv = True
nrql.filename = 'events.csv'

nrql.query("select * from Transaction where appName = 'RabbitMQ' since this quarter")
