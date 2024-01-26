import sys
import pymongo

class DBAccess():
    def __init__(self):
        self.mongodb_connection_string = "mongodb://localhost:27017/"
        self.mongo_client = pymongo.MongoClient(self.mongodb_connection_string)

    def create_database(self, database_name):
        existing_databases = self.mongo_client.list_database_names()
        if "database_name" not in existing_databases:
            db = self.mongo_client[database_name]

    def save_preprocessed_metrics_data(self, database_name, metrics_df):
        db = self.mongo_client[database_name]

        for i, row in metrics_df.iterrows():
            db.metrics.insert_one(row.to_dict())

    def get_all_metrics(self, database_name):
        db = self.mongo_client[database_name]
        return db.metrics.find()
    