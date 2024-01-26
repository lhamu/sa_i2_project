# Example script (carbon_calculator.py)

import requests
import json
import config

prometheus_url = config[""]

def query_prometheus(query):
    response = requests.get(f"{prometheus_url}/api/v1/query", params={"query": query})
    return response.json()

def calculate_carbon_consumption(cpu_usage, memory_usage):
    # Your carbon consumption calculation logic here
    return cpu_usage + memory_usage

def main():
    cpu_query = 'sum(rate(node_cpu_seconds_total{mode="idle"}[1m])) by (node)'
    memory_query = 'sum(node_memory_MemFree_bytes) by (node)'

    cpu_data = query_prometheus(cpu_query)
    memory_data = query_prometheus(memory_query)

    for result in cpu_data['data']['result']:
        node = result['metric']['node']
        cpu_usage = float(result['value'][1])

        memory_result = next((r for r in memory_data['data']['result'] if r['metric']['node'] == node), None)
        memory_usage = float(memory_result['value'][1])

        carbon_consumption = calculate_carbon_consumption(cpu_usage, memory_usage)
        print(f"Node: {node}, Carbon Consumption: {carbon_consumption} kgCO2")

if __name__ == "__main__":
    main()