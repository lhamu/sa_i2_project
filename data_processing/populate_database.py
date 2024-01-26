import os
import sys
import json
import pymongo

mongodb_connection_string = "mongodb://localhost:27017/"
mongo_client = pymongo.MongoClient(mongodb_connection_string)

metrics = [
    "machine_cpu_cores",
    "container_memory_usage_bytes",
    "container_cpu_usage_seconds_total",
    "kube_node_status_allocatable",
    "kube_pod_info",
    "kube_node_labels"
    "kube_pod_status_phase",
    "kube_pod_container_resource_requests",
    "kube_pod_container_resource_limits",
]

metric_file_mappings = {
    "machine_cpu_cores": "machine_cpu_cores.json",
    "container_memory_usage_bytes": "container_memory_usage.json",
    "container_cpu_usage_seconds_total": "container_cpu_usage.json",
    "kube_node_status_allocatable": "node_status_allocatable.json",
    "kube_pod_info": "pod_info.json",
    "kube_node_labels": "node_labels.json",
    "kube_pod_status_phase": "node_status_capacity.json",
    "kube_pod_container_resource_requests": "pod_container_resource_requests.json",
    "kube_pod_container_resource_limits": "pod_container_resource_limits.json"
}

# def get_metrics(file_name):
#     print(file_name)
#     prometheus_endpoint = "https://prom-stg.mediass.it/api/v1/query"
#     with open(os.path.join("data", "cluster2", "json_data", f"{file_name}")) as f:
#         json_data = json.load(f)

#     result_data = json_data["record"]["data"]["result"]
#     created_at = json_data["metadata"]["createdAt"]

#     complete_data = []
#     for datum in result_data:
#         data_item = datum["metric"]
#         data_item["value"] = datum["value"][1]
#         data_item["created_at"] = created_at
#         data_item["prometheus_endpoint"] = prometheus_endpoint

#         complete_data.append(data_item)

#     return complete_data

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

def main():
    for metric in metric_file_mappings:
        metric_filename = metric_file_mappings[metric]
        collection = mongo_client["i2_energy_efficiency_cluster2"][metric]
        data = get_metrics(metric_filename)
        insert_data(collection, data)

if __name__ == "__main__":
    main()