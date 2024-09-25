import pandas as pd
from elasticsearch import Elasticsearch, helpers
# Read CSV File

def read_csv_data(csv_file):

    return pd.read_csv(csv_file)



# Create Elasticsearch Index (if not exists)

def create_elasticsearch_index(es_client, index_name):

    if not es_client.indices.exists(index=index_name):

        es_client.indices.create(

            index=index_name,

            body={

                "mappings": {

                    "properties": {

                        "Id": {"type": "integer"},

                        "MSSubClass": {"type": "integer"},

                        "MSZoning": {"type": "keyword"},

                        "LotFrontage": {"type": "integer"},

                        "LotArea": {"type": "integer"},

                        "Street": {"type": "keyword"},

                        "Alley": {"type": "keyword"},

                        "LotShape": {"type": "keyword"},

                        "LandContour": {"type": "keyword"},

                        "Utilities": {"type": "keyword"},

                        "LotConfig": {"type": "keyword"}

                    }

                }

            }

        )

        print(f"Created index {index_name}")



# Bulk Ingest Data to Elasticsearch

def ingest_data(es_client, df, index_name):

    actions = [

        {

            "_index": index_name,

            "_source": {

                "Id": row["Id"],

                "MSSubClass": row["MSSubClass"],

                "MSZoning": row["MSZoning"],

                "LotFrontage": row["LotFrontage"],

                "LotArea": row["LotArea"],

                "Street": row["Street"],

                "Alley": row["Alley"],

                "LotShape": row["LotShape"],

                "LandContour": row["LandContour"],

                "Utilities": row["Utilities"],

                "LotConfig": row["LotConfig"]

            }

        }

        for _, row in df.iterrows()

    ]

    helpers.bulk(es_client, actions)

    print(f"Data ingested to index {index_name}")



# Main Execution

if __name__ == "__main__":

    # Set Elasticsearch connection

    es_client = Elasticsearch("http://localhost:9200")

    index_name = "house_data"



    #Read CSV

    csv_file = "train.csv"  # Replace with the path to your actual CSV file

    df = read_csv_data(csv_file)

    es_client.info()



    #Create Index

    create_elasticsearch_index(es_client, index_name)



    #Ingest Data

    ingest_data(es_client, df, index_name)