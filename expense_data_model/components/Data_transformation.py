import pandas as pd
import os, sys
import numpy as np 

from expense_data_model.exception.exception import ExpenseDataModelException
from expense_data_model.logging.logger import logging
from expense_data_model.constants import training_pipeline
from expense_data_model.constants.training_pipeline import DATA_TRANSFORMATION_INPUTER_PARAMETERS, TARGET_COLUMN

from expense_data_model.entity.config_entity import Data_transformation_configuration
from expense_data_model.entity.artifact_entity import DataValidationArtifacts, DataTransformationArtifacts
from expense_data_model.utils.main_utils.utils import save_numpy_array, save_object

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline



class DataTransformation:
    def __init__(self,
                 data_validation_artifacts:DataValidationArtifacts,
                 data_transformation_config:Data_transformation_configuration
                 ):
        try:
            self.data_validation_artifact = data_validation_artifacts
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        
    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        

    def get_data_transformation_object(self):
        try:
            
            inputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_INPUTER_PARAMETERS)
            logging.info("initializing KNN imputer with {DATA_TRANSFORMATION_INPUTER_PARAMETERS}")
            processor:Pipeline = Pipeline([("inputer",inputer)])
            logging.info("KNN initialization completed")

            return processor
        except Exception as e:
            raise ExpenseDataModelException(e, sys)

    
    def initiate_data_transformation(self):
        try:
            # read in data
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_data_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_data_test_file_path)

            # training dataframe
            train_df_input_data = train_df.drop(columns = [TARGET_COLUMN], axis = 1)
            train_df_target_data = train_df[TARGET_COLUMN]

            #Testing dataframe
            test_df_input_data = test_df.drop(columns = [TARGET_COLUMN], axis = 1)
            test_df_target_data = test_df[TARGET_COLUMN]


            preprocessor = self.get_data_transformation_object()
            preprocessor_object = preprocessor.fit(train_df_input_data)

            transformed_train_df_input_data = preprocessor_object.transform(train_df_input_data)
            transformed_test_df_input_data = preprocessor_object.transform(test_df_input_data)

            train_arr = np.c_[transformed_train_df_input_data, np.array(train_df_target_data)]
            test_arr = np.c_[transformed_test_df_input_data ,np.array(test_df_target_data)]

            # save the numpy array
            save_numpy_array(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)
            
            # model pusher
            save_object("final_model/preproccessor.pkl"  ,preprocessor_object)

            data_transformation_artifacts = DataTransformationArtifacts(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifacts


        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        
