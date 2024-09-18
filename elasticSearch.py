from elasticsearch_dsl import Index, Text, Keyword, Integer, Float, Date, Boolean, GeoPoint
import json
import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from dotenv import load_dotenv
import os

load_dotenv()
elastic_path = os.getenv("ELASTIC_SEARCH_PATH")  
elastic_secret_key = os.getenv("ELASTIC_SEARCH_API_KEY")

def insertData(data):
  es = Elasticsearch(
      'https://localhost:9200',
      basic_auth=("elastic", elastic_secret_key),
      ca_certs='/Users/kang-eunhye/elasticsearch-8.15.0/certs.pem' 
      )
  print(es.ping())

  # Define the index name explicitly 
  index_name = "product_list"

  # schema in mapping.json 
  # with open('mapping.json', 'r') as f:
  #   mapping = json.load(f)
  #   es.indices.create(index=index_name, body=mapping)

  # Load data from a CSV or JSON file (example)
  # df = pd.read_csv("your_product_data.csv")
  # data = df.to_dict(orient="records")  # Assuming data is in a pandas DataFrame

  # Bulk insertion (replace with your actual data structure)
  bulk_actions = []
  for product in data:
    doc = {
      "neighborhood": product.get("neighborhood", None),  # Handle missing values
      "salePrice": product.get("salePrice", None),
      "lotArea": product.get("lotArea", None),
      "status": product.get("status", None),
    }
    action = {
        "_index": index_name,
        "_source": doc
    }
    bulk_actions.append(action)

  bulk(es, bulk_actions)
  print("Data ingestion completed!")

# Example usage
data = [
  {"neighborhood": "Sawyer2", "salePrice": 11400, "lotArea": 2000, "status": 1},
]

insertData(data)