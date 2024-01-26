import os
import requests
import pandas as pd

from data_analytics import config

def get_electricity_consumed(cpu_usage, processor_info):
    """
    This function calculates the electricity consumed by the CPU
    :param cpu_usage: CPU usage in percentage
    :param processor_info: dictionary with processor watt information
    :return: Electricity consumed by the CPU in kilowatt
    """
    if str(cpu_usage) not in ["nan", ""]:
        electricity_consumed = cpu_usage * processor_info["average_watts"]
        return electricity_consumed/ 1000 # to convert unit into kiloWatt.
    return 0

def get_co2_emissions(electricity_consumed, region):
    """
    This function calculates the CO2 emissions based on the electricity consumed by the CPU
    :param electricity_consumed:  Electricity consumed by the CPU in kilowatt
    :param region: region where the Kubernetes cluster is hosted
    :return: CO2 emissions
    """
    electricity_api = config.API_ENDPOINT + f"?zone={region}"
    carbon_intensity_data = requests.get(electricity_api, headers={'auth-token': config.API_KEY})
    # response will have carbonIntensity measured in gCO2eq/kWh
    carbon_intensity = carbon_intensity_data.json()["carbonIntensity"]

    co2_emissions = electricity_consumed * carbon_intensity

    return co2_emissions

def main(metrics_data):
    processor_file = config.PROCESSOR_FILE
    processor_df = pd.read_excel(processor_file)
    processor_type = config.PROCESSOR_TYPE
    region = config.REGION
    specific_processor_info = processor_df[processor_df["architecture"]==processor_type].iloc[0]

    metrics_data["electricity_consumed"] = metrics_data["power_consumed"].apply(lambda x: get_electricity_consumed(x, specific_processor_info))
    metrics_data["co2_emissions"] = metrics_data.apply(lambda x: get_co2_emissions(x["electricity_consumed"], region), axis=1)
    output_file_path = "cluster2_preprocessed_file_with_co2_emissions.csv"
    metrics_data.to_csv(output_file_path, index=False)

    return metrics_data

if __name__ == "__main__":
    metrics_file_path = r"data\cluster1\preprocessed_data.csv"
    metrics_data = pd.read_csv(metrics_file_path)
    main(metrics_data)