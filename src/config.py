from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

def get_session():
    cloud_config = {
        'secure_connect_bundle': 'credentials/secure-connect-diabetes-bigdata.zip'
    }

    with open('credentials/diabetes-bigdata-token.json') as f:
        secrets = json.load(f)

    CLIENT_ID = secrets['clientId']
    CLIENT_SECRET = secrets['secret']

    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    return session
