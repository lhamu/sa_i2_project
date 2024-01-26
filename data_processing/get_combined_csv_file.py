import os
import json
import pandas as pd
from combine_files import get_combined_csv

def create_csv_file(file_name):
    with open(os.path.join("data", "cluster2", "json_data", f"{file_name}.json")) as f:
        json_data = json.load(f)

    # result_data = json_data["record"]["data"]["result"]
    result_data = json_data["data"]["result"]

    complete_data = []
    for datum in result_data:
        data_item = datum["metric"]
        data_item["value"] = datum["value"][1]

        complete_data.append(data_item)

    df = pd.DataFrame(complete_data)
    return df

def create_csv_files(file_path):
    data_files = [
        "container_cpu_usage", 
        "container_memory_usage", 
        "machine_cpu_cores", 
        "node_labels", 
        "node_status_allocatable", 
        "node_status_capacity", 
        "pod_container_resource_limits",
        "pod_container_resource_requests",
        "pod_info"
    ]

    for file_name in data_files:
        df = create_csv_file(file_name)
        df.to_csv(os.path.join(file_path, f"{file_name}.csv"), index=False)

if __name__ == "__main__":
    file_path = r"data\cluster2\csv_files"
    create_csv_files(file_path)
    combined_csv_path = r"data\cluster2"
    combined_df = get_combined_csv(file_path)
    combined_df.to_csv(os.path.join(combined_csv_path, "complete_data.csv"), index=False)
    