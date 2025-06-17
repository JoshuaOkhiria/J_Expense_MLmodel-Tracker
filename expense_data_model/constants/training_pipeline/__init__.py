import os
import sys
import pandas as pd
import numpy as np


"""COMMON CONSTANT VARIABLES FOR TRAINING PIPELINE"""
TARGET_COLUMN = "costs"
PIPELINE_NAME:str = "ExpenseData_Tracker"
ARTIFACT_DIR:str = "Artifacts"
FILE_NAME:str = "Expense_data.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")
SAVED_MODEL_DIR:str = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"


"""DATA INGESTION"""
DATA_INGESTION_COLLECTION_NAME = "ExpenseData"
DATA_INGESTION_DATABASE_NAME = "Josh_okhiria"
DATA_INGESTIONN_TRAIN_TEST_SPLIT_RATIO: float = 0.2
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_COLUMNS_NAMES_FILE_PATH = "columns_names"
DATA_INGESTION_COLUMNS_NAMES_FILE_NAME = "columns.txt"



""""DATA VALIDATION"""
DATA_VALIDATION_DIR_NAME = 'Data validation'
DATA_VALIDATION_VALID_DIR = "validated"
DATA_VALIDATION_INVALID_DIR = "Invalidated"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "drift.yaml"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"



"""DATA TRANSFORMATION"""
DATA_TRANSFORMATION_DIR_NAME = "Data transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "Transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "Transformed_object"
DATA_TRANSFORMATION_INPUTER_PARAMETERS = {
    'missing_values': np.nan,
    'n_neighbors':3,
    "weights":"uniform"
}



""" MODEL TRAINER/TRAINING """
ML_MODEL_DIR_NAME:str = 'ML_model'
TRAINED_ML_MODEL_FILE_DIR: str = 'Trained_model_dir'
TRAINED_ML_MODEL_NAME: str = 'Expense_data_model'
ML_MODEL_EXPECTED_SCORE:float = 0.6
ML_MODEL_UNDERFITTING_OVERFITTING_THRESHOLD:float = 0.05


TRAINING_BUCKET_NAME = "jexpensedata"