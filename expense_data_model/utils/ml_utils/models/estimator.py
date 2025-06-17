import os, sys

from expense_data_model.exception.exception import ExpenseDataModelException
from expense_data_model.logging.logger import logging

from expense_data_model.constants.training_pipeline import TRAINED_ML_MODEL_NAME, TRAINED_ML_MODEL_FILE_DIR

class ExpenseData_Model:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise ExpenseDataModelException(e, sys)  


    def predict(self, x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e: 
            raise ExpenseDataModelException(e, sys) 