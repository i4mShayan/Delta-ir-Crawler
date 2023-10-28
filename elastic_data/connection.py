from elasticsearch import Elasticsearch
import pandas as pd

def connect():
    es = Elasticsearch(
        ['localhost'],
        port=9200
    )

    es.ping()

    return es

def get_json_by_index(index_name):
    es = connect()

    search_query = {
        "query": {
            "match_all": {}
        }
    }

    result = es.search(index=index_name, body=search_query, size=1000, )

    return result

def get_df_by_index(index_name):
    result = get_json_by_index(index_name)
    df = pd.DataFrame([hit['_source'] for hit in result['hits']['hits']])
    return df

