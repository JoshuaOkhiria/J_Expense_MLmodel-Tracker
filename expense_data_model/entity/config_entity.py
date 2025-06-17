from datetime import datetime
import os
import sys
from expense_data_model.constants import training_pipeline
from expense_data_model.logging.logger import logging

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)


class TrainingPipeline_configuration:
    def __init__(self,timestamp =  datetime.now()):
        timestamp = timestamp.now().strftime("%m_%d_%y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifacts_name = training_pipeline.ARTIFACT_DIR
        self.artifacts_dir = os.path.join(self.artifacts_name, timestamp)
        self.model_dir = os.path.join("final_model") #I can choose to hardcode this value in the cconstants file as well 
        self.timestamp:str = timestamp
        

class DataIngestion_configuration:
    def __init__(self, training_pipeline_config:TrainingPipeline_configuration):
        
        self.data_ingstion_dir:str = os.path.join(
            training_pipeline_config.artifacts_dir, training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path = os.path.join(self.data_ingstion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, 
                                                    training_pipeline.FILE_NAME)
        self.trainig_file_path = os.path.join(self.data_ingstion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                              training_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path = os.path.join(self.data_ingstion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                              training_pipeline.TEST_FILE_NAME)

        self.train_test_split_ratio:float = training_pipeline.DATA_INGESTIONN_TRAIN_TEST_SPLIT_RATIO
        self.database_name:str = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collections_name:str = training_pipeline.DATA_INGESTION_COLLECTION_NAME

        self.colums_names_file_path = os.path.join(self.data_ingstion_dir, training_pipeline.DATA_INGESTION_COLUMNS_NAMES_FILE_PATH,training_pipeline.DATA_INGESTION_COLUMNS_NAMES_FILE_NAME)
        


class Data_validation_configuration:
    def __init__(self, training_pipeline_config:TrainingPipeline_configuration):
        logging.info(f"initiating data validation config")
        self.data_validation_dir = os.path.join( training_pipeline_config.artifacts_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path = os.path.join(self.valid_data, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path = os.path.join(self.valid_data, training_pipeline.TEST_FILE_NAME)
        
        self.invalid_train_file_path = os.path.join(self.valid_data, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path = os.path.join(self.valid_data, training_pipeline.TEST_FILE_NAME)

        self.drift_report_file_path = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        logging.info(f"initiating data validation config completed successfully")


class Data_transformation_configuration:
    def __init__(self, training_pipeline_config:TrainingPipeline_configuration):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifacts_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"))
        self.transformed_test_file_path = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TEST_FILE_NAME.replace("csv","npy"))
        self.transformed_object_file_path = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)

        
class Machine_learning_model_configuration:
    def __init__(self, training_pipeline_config:TrainingPipeline_configuration):
        self.ml_model_dir = os.path.join(training_pipeline_config.artifacts_dir, training_pipeline.ML_MODEL_DIR_NAME)
        self.trained_model_file_path = os.path.join(self.ml_model_dir,training_pipeline.TRAINED_ML_MODEL_FILE_DIR, training_pipeline.TRAINED_ML_MODEL_NAME)
        self.expected_accuracy = training_pipeline.ML_MODEL_EXPECTED_SCORE

        


