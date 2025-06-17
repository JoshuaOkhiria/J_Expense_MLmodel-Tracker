
import pandas as pd
import numpy as np
import os, sys
from scipy.stats import ks_2samp

from expense_data_model.exception.exception import ExpenseDataModelException
from expense_data_model.logging.logger import logging
from expense_data_model.utils.main_utils.utils import read_yaml_file, write_yaml_file

from expense_data_model.entity.config_entity import Data_validation_configuration
from expense_data_model.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifacts
from expense_data_model.constants import training_pipeline


class DataValidation:
    def __init__(self, 
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:Data_validation_configuration):
        try:
            self.data_validation_configutation = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema = read_yaml_file(training_pipeline.SCHEMA_FILE_PATH)
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path) # engine='openpyxl'
            return df
        except Exception as e:
            raise ExpenseDataModelException(e, sys) 
        
        
    def validate_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self.schema)
            logging.info(f"required number of columns: {number_of_columns}")
            logging.info(f"dataframe has :{len(dataframe.columns)}")

            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
             raise ExpenseDataModelException(e, sys)


    def detect_datadrift(self, base_df, current_df, threshold = 0.05):
        try:
            logging.info(f"checking for data drift")
            report = {}
            status =  True
            for values in base_df.columns:
                logging.info(f'commenced iteration for data drift')
                d1 = base_df[values]
                d2 = current_df[values]
                is_same_distrubution = ks_2samp(d1,d2)
                logging.info(f'data drift value {is_same_distrubution}')
                
                if threshold<= is_same_distrubution.pvalue:
                    is_found = False
                else:
                    is_found =  True
                    status = False
                report.update({values:
                                {'p_value':float(is_same_distrubution.pvalue),
                                   'drift_status':is_found
                                }})  
            logging.info(f'data drift completed')
            # creating file directory
            drift_report_filepath = self.data_validation_configutation.drift_report_file_path
            drift_dir = os.path.dirname(drift_report_filepath)
            os.makedirs(drift_dir, exist_ok=True)

            write_yaml_file(filepath = drift_report_filepath, content = report)
        except Exception as e:
            raise ExpenseDataModelException(e, sys)



    def initiate_data_validation(self) -> DataValidationArtifacts:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # read train and test data
            train_data = DataValidation.read_data(train_file_path)
            test_data = DataValidation.read_data(test_file_path)

            # validating number of columns
            status = self.validate_columns(train_data)
            if not status:
                error = f"Train dataframe does not contain all columns"
            status = self.validate_columns(test_data)
            if not status:
                error = f"Test dataframe does not contain all columns"

            # checking data drift
            status = self.detect_datadrift(base_df=train_data, current_df=test_data)
            train_dir_path = os.path.dirname(self.data_validation_configutation.valid_train_file_path)
            os.makedirs(train_dir_path, exist_ok=True)

            test_dir_path = os.path.dirname(self.data_validation_configutation.valid_test_file_path)
            os.makedirs(test_dir_path, exist_ok=True)

            train_data.to_csv(self.data_validation_configutation.valid_train_file_path, index=False, header=True)
            test_data.to_csv(self.data_validation_configutation.valid_test_file_path, index=False, header=True)

            data_validation_artifacts = DataValidationArtifacts(
                valid_data_train_file_path = self.data_ingestion_artifact.trained_file_path,
                valid_data_test_file_path = self.data_ingestion_artifact.test_file_path,
                invalid_data_train_file_path = None,
                invalid_data_test_file_path = None,
                validation_status = status,
                drift_report_file_path = self.data_validation_configutation.drift_report_file_path
            )

            return data_validation_artifacts
           
        except Exception as e:
            raise ExpenseDataModelException(e, sys)


