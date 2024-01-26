import os
import numpy as np
import pandas as pd

def get_combined_csv(file_path):
    cpu_usage_df = pd.read_csv(os.path.join(file_path, "container_cpu_usage.csv"))
    mem_usage_df = pd.read_csv(os.path.join(file_path, "container_memory_usage.csv"))
    cpu_cores_df = pd.read_csv(os.path.join(file_path, "machine_cpu_cores.csv"))
    node_labels_df = pd.read_csv(os.path.join(file_path, "node_labels.csv"))
    node_status_allocatable_df = pd.read_csv(os.path.join(file_path, "node_status_allocatable.csv"))
    node_status_capacity_df = pd.read_csv(os.path.join(file_path, "node_status_capacity.csv"))
    pod_container_resource_limits_df = pd.read_csv(os.path.join(file_path, "pod_container_resource_limits.csv"))
    pod_container_resource_requests_df = pd.read_csv(os.path.join(file_path, "pod_container_resource_requests.csv"))
    pod_info_df = pd.read_csv(os.path.join(file_path, "pod_info.csv"))

    cpu_usage_df["cpu_cores"] = np.nan
    cpu_usage_df["boot_id"] = np.nan
    cpu_usage_df["system_uuid"] = np.nan
    cpu_usage_df["machine_id"] = np.nan

    nodes = list(set(node_status_allocatable_df["node"].tolist()))
    node_resources = list(set(node_status_allocatable_df["resource"].tolist()))

    cpu_usage_df["node_label"] = np.nan
    # from node_status_allocatable
    for resource in node_resources:
        cpu_usage_df[f"{resource}_resource"] = np.nan
        cpu_usage_df[f"{resource}_unit"] = np.nan
        cpu_usage_df[f"{resource}_node_status_allocatable"] = np.nan

        #from node_status_capacity
        cpu_usage_df[f"{resource}_node_status_capacity"] = np.nan

    # from pod_container_resource_limits
    container_resources = list(set(pod_container_resource_limits_df["resource"].tolist()))
    for resource in container_resources:
        cpu_usage_df[f"{resource}_pod_container_resource"] = np.nan
        cpu_usage_df[f"{resource}_pod_container_resource_uid"] = np.nan
        cpu_usage_df[f"{resource}_pod_container_resource_unit"] = np.nan
        cpu_usage_df[f"{resource}_pod_container_resource_limit"] = np.nan

        # from pod_container_resource_requests
        cpu_usage_df[f"{resource}_pod_container_resource_requests"] = np.nan

    # from pod_info
    cpu_usage_df["pod_info"] = np.nan
    cpu_usage_df["pod_created_by_kind"] = np.nan
    cpu_usage_df["pod_created_by_name"] = np.nan
    cpu_usage_df["host_ip"] = np.nan
    cpu_usage_df["host_network"] = np.nan
    cpu_usage_df["pod_ip"] = np.nan
    cpu_usage_df["pod_priority_class"] = np.nan
    cpu_usage_df["memory_usage"] = np.nan

    for i, _row in cpu_cores_df.iterrows():
        cpu_cores = _row["value"]
        namespace = _row["namespace"]
        node = _row["node"]
        boot_id = _row["boot_id"]
        system_uuid = _row["system_uuid"]
        machine_id = _row["machine_id"]

        # Add the number of CPU cores to the pod information data frame.
        cpu_usage_df.loc[((cpu_usage_df["node"]==node)), ["cpu_cores", "boot_id", "system_uuid", "machine_id"]] = [cpu_cores, boot_id, system_uuid, machine_id]

    for i, _row in node_labels_df.iterrows():
        node = _row["node"]
        pod = _row["pod"]
        node_label = _row["value"]

        cpu_usage_df.loc[((cpu_usage_df["node"]==node)), "node_label"] = node_label

    for node in nodes:
        for resource in node_resources:
            _row = node_status_allocatable_df[((node_status_allocatable_df["node"]==node) & (node_status_allocatable_df["resource"]==resource))].iloc[0]
            resource_value = _row["value"]
            resource_unit = _row["unit"]

            cpu_usage_df.loc[(cpu_usage_df["node"]==node), [f"{resource}_resource", f"{resource}_node_status_allocatable", f"{resource}_unit"]] = [resource, resource_value, resource_unit]

    for node in nodes:
        for resource in node_resources:
            _row = node_status_capacity_df[((node_status_capacity_df["node"]==node) & (node_status_capacity_df["resource"]==resource))].iloc[0]
            resource_value = _row["value"]

            cpu_usage_df.loc[(cpu_usage_df["node"]==node), [f"{resource}_node_status_capacity"]] = [resource_value]


    completed_data = []
    for i, row in cpu_usage_df.iterrows():
        row["cpu_usage"] = row["value"]
        container_name = row["container"]
        node = row["node"]
        pod = row["pod"]
        namespace = row["namespace"]

        # get the memory usage for this pod
        corresponding_memory_row = mem_usage_df[((mem_usage_df["node"]==node) & \
                                                (mem_usage_df["container"]==container_name) & \
                                                (mem_usage_df["pod"]==pod))]
        if not corresponding_memory_row.empty:
            corresponding_memory_row = corresponding_memory_row.iloc[0]
            row["memory_usage"] = corresponding_memory_row["value"]

        # get the resource limits for pod
        for resource in container_resources:
            # corresponding_container_resource_row = pod_container_resource_limits_df[(pod_container_resource_limits_df["node"]==node) & \
            #                                                                         (pod_container_resource_limits_df["container"]==container_name) & \
            #                                                                         (pod_container_resource_limits_df["pod"]==pod) & \
            #                                                                         (pod_container_resource_limits_df["namespace"]==namespace) & \
            #                                                                         (pod_container_resource_limits_df["resource"]==resource)]
            corresponding_container_resource_row = pod_container_resource_limits_df[(pod_container_resource_limits_df["node"]==node) & \
                                                                                    (pod_container_resource_limits_df["container"]==container_name) & \
                                                                                    (pod_container_resource_limits_df["pod"]==pod) & \
                                                                                    (pod_container_resource_limits_df["resource"]==resource)]
            if len(corresponding_container_resource_row) > 0:
                corresponding_container_resource_row = corresponding_container_resource_row.iloc[0]
                row[f"{resource}_pod_container_resource"] = resource
                row[f"{resource}_pod_container_resource_uid"] = corresponding_container_resource_row["uid"]
                row[f"{resource}_pod_container_resource_unit"] = corresponding_container_resource_row["unit"]
                row[f"{resource}_pod_container_resource_limit"] = corresponding_container_resource_row["value"]

        for resource in container_resources:
            # corresponding_container_resource_requests_row = pod_container_resource_requests_df[(pod_container_resource_requests_df["node"]==node) & \
            #                                                                           (pod_container_resource_requests_df["container"]==container_name) & \
            #                                                                           (pod_container_resource_requests_df["pod"]==pod) & \
            #                                                                           (pod_container_resource_requests_df["namespace"]==namespace) & \
            #                                                                           (pod_container_resource_requests_df["resource"]==resource)]
            corresponding_container_resource_requests_row = pod_container_resource_requests_df[(pod_container_resource_requests_df["node"]==node) & \
                                                                                    (pod_container_resource_requests_df["container"]==container_name) & \
                                                                                    (pod_container_resource_requests_df["pod"]==pod) & \
                                                                                    (pod_container_resource_requests_df["resource"]==resource)]
            if len(corresponding_container_resource_requests_row) > 0:
                corresponding_container_resource_requests_row = corresponding_container_resource_requests_row.iloc[0]
                row[f"{resource}_pod_container_resource_requests"] = corresponding_container_resource_requests_row["value"] 


        corresponding_pod_info_row = pod_info_df[(pod_info_df["node"]==node) & \
                                                    (pod_info_df["pod"]==pod) & \
                                                    (pod_info_df["namespace"]==namespace)]
        if len(corresponding_pod_info_row) > 0:
            corresponding_pod_info_row = corresponding_pod_info_row.iloc[0]
            
            row["pod_info"] = corresponding_pod_info_row["value"]
            row["pod_created_by_kind"] = corresponding_pod_info_row["created_by_kind"]
            row["pod_created_by_name"] = corresponding_pod_info_row["created_by_name"]
            row["host_ip"] = corresponding_pod_info_row["host_ip"]
            row["host_network"] = corresponding_pod_info_row["host_network"]
            row["pod_ip"] = corresponding_pod_info_row["pod_ip"]
            row["pod_priority_class"] = corresponding_pod_info_row["priority_class"]

        completed_data.append(row)

    completed_df = pd.DataFrame(completed_data)

    return completed_df
