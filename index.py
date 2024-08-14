import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

def read_csv_data(file_path):
  """Reads the CSV data into a pandas DataFrame and performs basic exploration.

  Args:
    file_path: Path to the CSV file.

  Returns:
    pandas.DataFrame: The loaded DataFrame.
  """

  df = pd.read_csv(file_path)

  # Basic exploration:
#   print(df.head())
#   print(df.info())
#   print(df.describe())

  # Handle missing values (e.g., fillna, dropna)
  # Handle outliers (e.g., z-score, IQR)
  # Feature engineering (if necessary)

  return df

from elasticsearch_dsl import Index, Text, Keyword, Integer, Float, Date, Boolean, GeoPoint

def create_elasticsearch_index(es_client, index_name, df):
  """Creates an Elasticsearch index with inferred mappings based on DataFrame schema.

  Args:
    es_client: Elasticsearch client instance.
    index_name: Name of the index to create.
    df: Pandas DataFrame containing the data.
  """

  index = Index(index_name)
  index.doc_type = 'house_data'  # Set document type (optional)

  mappings = {}
  for col in df.columns:
      if pd.api.types.is_numeric_dtype(df[col]):
          mappings[col] = Integer() if df[col].dtype == np.int64 else Float()
      elif pd.api.types.is_datetime64_dtype(df[col]):
          mappings[col] = Date()
      elif df[col].dtype == bool:
          mappings[col] = Boolean()
      else:
          mappings[col] = Text(analyzer='keyword')

  index.mapping = {'properties': mappings}

  index.create(index=index_name, body=index.to_dict())


def ingest_data(es_client, index_name, data):
  """Ingests data into Elasticsearch.

  Args:
    es_client: Elasticsearch client instance.
    index_name: Name of the index to ingest data into.
    data: Data to be ingested (pandas DataFrame).
  """

  def data_generator(data):
    for index, row in data.iterrows():
      yield {
          '_index': index_name,
          '_id': index,
          '_source': row.to_dict()
      }

  actions = data_generator(data)
  successes, failures = bulk(es_client, actions=actions, chunk_size=1000)

def main():
  # Replace with your file path
  # Read data
  df = read_csv_data("train.csv")

  # Connect to Elasticsearch
  es_client = Elasticsearch(url="http://username:password@localhost:9200")  # Replace with your credentials and hostname

  # Define index mappings (simplified for ETL focus)
  mappings = {
      'properties': {
          'Id': Integer(),
          'MSSubClass': Integer(),
          'MSZoning': Keyword(),
          # ... Define mappings for all fields
      }
  }

  # Create Elasticsearch index
  create_elasticsearch_index(es_client, 'house_index', mappings)

  # Ingest data into Elasticsearch
  ingest_data(es_client, 'house_index', df)

  print("Data ingestion completed!")

if __name__ == "__main__":
  main()
