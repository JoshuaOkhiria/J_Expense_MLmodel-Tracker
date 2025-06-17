import os, sys
from expense_data_model.components.Data_ingestion import Dataingestion
from expense_data_model.components.Data_validation import DataValidation
from expense_data_model.components.Data_transformation import DataTransformation
from expense_data_model.components.machine_trainer import model_training

from expense_data_model.entity.config_entity import (
    TrainingPipeline_configuration,
    DataIngestion_configuration,
    Data_validation_configuration,
    Data_transformation_configuration,
    Machine_learning_model_configuration
)

from expense_data_model.exception.exception import ExpenseDataModelException
from expense_data_model.logging.logger import logging

from expense_data_model.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifacts,
    DataTransformationArtifacts,
    machine_learning_model_Artifacts
)

from expense_data_model.constants.training_pipeline import TRAINING_BUCKET_NAME
from expense_data_model.cloud.s3_syncer import  s3_sync


class TrainingPipeline_:
    def __init__(self):
        self.training_pipeline_config = TrainingPipeline_configuration()
        self.s3_sync = s3_sync()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestion_configuration(self.training_pipeline_config)
            logging.info(f"initiating data injestion")
            data_ingestion = Dataingestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f'data ingestion completed and artifacts: {data_ingestion_artifact}')
            return data_ingestion_artifact
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = Data_validation_configuration(self.training_pipeline_config)
            logging.info(f"initiating data validation")
            data_validation = DataValidation(data_validation_config=self.data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f'data validation completed and artifacts: {data_validation_artifact}')
            return  data_validation_artifact
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifacts):
        try:
            self.data_transformation_config = Data_transformation_configuration(self.training_pipeline_config)
            logging.info(f"initiating data transformation")
            data_transformation = DataTransformation(data_validation_artifacts=data_validation_artifact, data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f'data transformation completed and artifacts: {data_transformation_artifact}')
            return  data_transformation_artifact
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifacts):
        try:
            self.model_trainer_config = Machine_learning_model_configuration(self.training_pipeline_config)
            logging.info(f"initiating ml model training")
            model_trainer = model_training(data_transformation_artifacts=data_transformation_artifact, machine_learning_model_config=self.model_trainer_config)
            model_trainer_artifact = model_trainer.initiate_model_training()
            logging.info(f'model training completed and artifacts: {model_trainer_artifact}')
            return model_trainer_artifact
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        

    def sync_artifactss_s3_bucket(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/Artifacts/{self.training_pipeline_config.timestamp}" 
            self.s3_sync.sync_folder_to_s3(self.training_pipeline_config.artifacts_dir, aws_bucket_url)
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        
    def sync_saved_model_to_s3_bucket(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(self.training_pipeline_config.model_dir, aws_bucket_url)
        except Exception as e:
            raise ExpenseDataModelException(e, sys)


    def run_pipeline(self):
        try:
            data_ingestion_artifact_ = self.start_data_ingestion()
            data_validation_artifacts_ = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact_)
            data_trasformation_artifact_ = self.start_data_transformation(data_validation_artifact=data_validation_artifacts_)
            model_trainer_artifact_ = self.start_model_trainer(data_transformation_artifact=data_trasformation_artifact_)

            # self.sync_artifactss_s3_bucket()
            # self.sync_saved_model_to_s3_bucket()

            return model_trainer_artifact_
        except Exception as e:
            raise ExpenseDataModelException(e, sys)