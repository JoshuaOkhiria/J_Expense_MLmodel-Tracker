import pandas as pd
import numpy as np
import os
import sys
import pymongo
from sklearn.model_selection import train_test_split
from typing import List

from dotenv import load_dotenv
load_dotenv()

from expense_data_model.exception.exception import ExpenseDataModelException
from expense_data_model.logging.logger import logging

from expense_data_model.entity.config_entity import DataIngestion_configuration

from expense_data_model.entity.artifact_entity import DataIngestionArtifact
from expense_data_model.constants import training_pipeline

mongodb_url = os.getenv("MONGO_DB_URL")



class Dataingestion:
    def __init__(self, data_ingestion_config:DataIngestion_configuration):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ExpenseDataModelException(e, sys)

    def export_collection_as_dataframe(self):
        """Read data from mongo db"""

        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collections_name

            mongo_client = pymongo.MongoClient(mongodb_url)
            collections = mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collections.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns = "_id", axis = 1)
            
            df.replace({"na":np.nan}, inplace=True)
            return df
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        
    
    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        """ This is basically saving the data into a directory if choice"""
        try:
            feature_store_filepath = self.data_ingestion_config.feature_store_file_path
            #create a folder
            dir_name = os.path.dirname(feature_store_filepath)
            os.makedirs(dir_name, exist_ok= True)
            dataframe.to_csv(feature_store_filepath, index = False, header = True)
            return dataframe
        except Exception as e:
            raise ExpenseDataModelException(e, sys)

    def save_columns_names(self, dataframe:pd.DataFrame):
        try:
            cols_names = dataframe.columns            
            columns_dir_name = os.path.dirname(self.data_ingestion_config.colums_names_file_path)
            os.makedirs(columns_dir_name, exist_ok=True)
            with open(self.data_ingestion_config.colums_names_file_path, 'w') as file:
                for values in cols_names:
                    file.write(values + '\n')
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        
    def split_data_into_train_test(self, dataframe: pd.DataFrame):
        try:
            df = dataframe
            logging.info("successfully read in data")

            # partition data into training and testing portions
            train_set, test_set = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio)

            logging.info("splited data into traning and test partitions")
            # defining training  file path
            dir_path = os.path.dirname(self.data_ingestion_config.trainig_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info("successfully created directoty to save train data")
            
            # defining test file path
            dir_path = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info("successfully created directoty to save test data")

            # saving files into training file path
            train_set.to_csv(self.data_ingestion_config.trainig_file_path, index = False, header = True)
            logging.info("successfully saved train data")

            # saving files into test file path
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index = False, header = True)
            logging.info("successfully saved test data")
            # save data into the appropriate file directory
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.save_columns_names(dataframe)
            self.split_data_into_train_test(dataframe)

            dataIngestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.trainig_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path)
            
            return dataIngestion_artifact
        except Exception as e:
            raise ExpenseDataModelException(e, sys)

