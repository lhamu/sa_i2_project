import os
import json
import requests

base_url = "https://prom-stg.mediass.it/api/v1"

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

def get_metric_data(metric, start, end):
    url = "{}/query?query={}&start={}&end={}&step=15".format(base_url, metric, start, end)
    print(url)
    response = requests.get(url)
    return response.json()

def get_metrics_data(start, end, output_path):
    data = {}
    for metric in metrics:
        data[metric] = get_metric_data(metric, start, end)
        json.dump(data[metric], fp=os.path.join(output_path, "{}.json".format(metric)), indent=4)
    return data

if __name__ == "__main__":
    start = "2023-12-01T00:00:00Z"
    end = "2023-12-31T23:59:59Z"
    data = get_metrics_data(start, end)
    print(json.dumps(data, indent=4))
