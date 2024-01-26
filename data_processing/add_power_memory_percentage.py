import os
import json
import pandas as pd

cluster = "cluster2"
complete_data_df = pd.read_csv(r"data\{0}\complete_data.csv".format(cluster))

with open(r"data\{0}\{0}_cpu_computing_power.json".format(cluster)) as f:
    cpu_computing_power = json.load(f)
    computing_power_data = cpu_computing_power["data"]["result"]

cpu_usage_data = []
for datum in computing_power_data:
    row = {}
    row["pod"] = datum["metric"]["pod"]
    row["power_consumed"] = datum["value"][1]

    cpu_usage_data.append(row)

cpu_usage_df = pd.DataFrame(cpu_usage_data)

with open(r"data\{0}\{0}_memory_percentage.json".format(cluster)) as f:
    memory_usage_percentage = json.load(f)
    memory_usage_percentage_data = memory_usage_percentage["data"]["result"]

for datum in memory_usage_percentage_data:
    pod = datum["metric"]["pod"]
    memory_usage = datum["value"][1]
    cpu_usage_df.loc[(cpu_usage_df["pod"]==pod), "memory_percentage"] = memory_usage

for i, row in cpu_usage_df.iterrows():
    complete_data_df.loc[(complete_data_df["pod"]==row["pod"]), ["power_consumed", "memory_percentage"]] = [row["power_consumed"], row["memory_percentage"]]

complete_data_df.to_csv("{0}_complete_data_with_power_consumed.csv".format(cluster), index=False)