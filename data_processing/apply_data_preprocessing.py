import os, sys
import pandas as pd
from db_access import DBAccess

parent_dir = os.path.dirname(os.getcwd())
sys.path.append(parent_dir)

from data_analytics.compute_carbon_emission import main

def apply_preprocessing(data):
    """
    Applies preprocessing to the data.
    """
    cleaned_data = data.copy()
    cleaned_data.dropna(subset=['memory_usage', 'cpu_usage'], inplace=True)

    return cleaned_data

def prepare_and_save_data(database_name, metrics_df):
    db_access = DBAccess()

    db_access.save_preprocessed_metrics_data(database_name, metrics_df)
    print("Data saved to MongoDB")

if __name__ == "__main__":
    cluster = "cluster2"
    database_name = "i2_energy_efficiency_cluster2"
    file_name = r"data\{0}\complete_data_with_power_consumed.csv".format(cluster)

    complete_data_df = pd.read_csv(file_name)
    complete_data_df = main(complete_data_df)
    preprocessed_df = apply_preprocessing(complete_data_df)
    prepare_and_save_data(database_name, preprocessed_df)
    