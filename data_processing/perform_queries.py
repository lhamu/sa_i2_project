import json
import requests

base_url_mappings = {
    "cluster1": "https://prom-staging.cerplus.it/api/v1/query",
    "cluster2": "https://prom-stg.mediass.it/api/v1/query"
}

def get_cpu_computing_power(base_url, cluster_name):
    # query = 'sum by (cpu)(rate(node_cpu_seconds_total{mode!="idle"}[5m]))*100'
    # query = 'sum(rate(container_cpu_usage_seconds_total{container!~"POD|"}[5m]))*100 by (namespace,pod)'
    query = '100 * max(rate(container_cpu_usage_seconds_total[5m])/ on (container, pod) kube_pod_container_resource_limits{resource="cpu"}) by (pod)'
    response = requests.get(base_url,
        params={'query': query})
    
    if response.status_code == 200:
        response_data = response.json()
        with open(f"{cluster_name}_cpu_computing_power.json", "w") as fp:
            json.dump(response_data, fp, indent=4)


def get_percentage_memory_used(base_url, cluster_name):
    # query = 'node_memory_Active_bytes/node_memory_MemTotal_bytes*100'
    # query = 'sum(rate(container_memory_usage_bytes{container!~"POD|"}[5m]))*100 by (namespace,pod)'
    query = '100 * max(container_memory_working_set_bytes/ on (container, pod) kube_pod_container_resource_limits{resource="memory"}) by (pod)'
    response = requests.get(base_url,
        params={'query': query})
    
    if response.status_code == 200:
        response_data = response.json()
        with open(f"{cluster_name}_memory_percentage.json", "w") as fp:
            json.dump(response_data, fp, indent=4)

def get_all_instances(base_url):
    query = 'label_values(up, instance)'
    params = {'query': query}

    try:
        response = requests.get(f'{base_url}', params=params)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'success':
            instances = data['data']['result']
            return [instance['metric']['instance'] for instance in instances]
        else:
            print(f"Prometheus query failed: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error making Prometheus API request: {e}")
        return None

def get_cpu_usage_per_pod(base_url, cluster_name):
    instances = get_all_instances(base_url)
    all_data = {}
    for instance in instances:
        query = '100 - rate(sum by (pod) (container_cpu_usage_seconds_total{job="kubelet", container!="POD", container!="", pod!="", namespace!="", instance="{}"}[5m])) * 100'.format(instance)
        response = requests.get(base_url,
            params={'query': query})
        
        if response.status_code == 200:
            all_data[instance] = response.json()
    
    with open(f"{cluster_name}_cpu_usage_per_pod.json", "w") as fp:
        json.dump(all_data, fp, indent=4)

if __name__ == "__main__":
    for key in base_url_mappings:
        get_cpu_computing_power(base_url_mappings[key], key)
        get_percentage_memory_used(base_url_mappings[key], key)
        get_cpu_usage_per_pod(base_url_mappings[key], key)