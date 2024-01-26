import os, glob
import json
import pymongo

mongodb_connection_string = "mongodb://localhost:27017/"
mongo_client = pymongo.MongoClient(mongodb_connection_string)

folder_path = r"data\cluster1\json_data"

def get_metrics(file_name):
    print(file_name)
    prometheus_endpoint = "https://prom-stg.mediass.it/api/v1/query"
    with open(os.path.join("data", "cluster2", "json_data", f"{file_name}")) as f:
        json_data = json.load(f)

    result_data = json_data["data"]["result"]

    complete_data = []
    for datum in result_data:
        data_item = datum["metric"]
        data_item["value"] = datum["value"][1]
        data_item["prometheus_endpoint"] = prometheus_endpoint

        complete_data.append(data_item)

    return complete_data

def insert_data(collection, data):
    collection.insert_many(data)

for filename in glob.glob(os.path.join(folder_path, '*.json')):
    print(filename)
    metric = filename.split("\\")[-1].split('.json')[0]
    metrics = get_metrics(filename)
    collection = mongo_client["i2_energy_efficiency"][metric]
    data = get_metrics(filename)
    insert_data(collection, data)
