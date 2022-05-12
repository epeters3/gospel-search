import os
from elasticsearch import Elasticsearch

client = Elasticsearch(os.environ["ES_HOST"])
