import pandas as pd
import numpy as np
import os, sys
import yaml
import pickle

from expense_data_model.exception.exception import ExpenseDataModelException
from expense_data_model.logging.logger import logging

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


def read_yaml_file(filepath):
    try:
        with open(filepath, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise ExpenseDataModelException(e, sys)
    
    
def write_yaml_file(filepath:str, content:object, replace:bool = False)->None:
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise ExpenseDataModelException(e, sys)
    

def save_numpy_array(file_path:str, array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file:
            np.save(file, array)    
    except Exception as e:
        raise ExpenseDataModelException(e, sys)


def save_object(file_path:str, obj:object):
    try:
        logging.info(f"initiating saving object ")
        os.makedirs(os.path.dirname(file_path), exist_ok= True)
        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)
        logging.info(f"object has been saved successfully")
    except Exception as e:
        raise ExpenseDataModelException(e, sys)
    
    
def load_object(file_path:str) -> object:
    try:
        logging.info(f"about to sve load object ")
        if not os.path.exists(file_path):
            raise Exception(f"This file {file_path} does not exists")
        with open(file_path, 'rb') as file:
            val =  pickle.load(file)
            logging.info(f"object loaded successfully ")
            return val
    except Exception as e:
        raise ExpenseDataModelException(e, sys)
    

def load_numpy_array(file_path:str):
    try:
        with open(file_path, 'rb') as file:
            return np.load(file)
    except Exception as e:
        raise ExpenseDataModelException(e, sys)


def evaluate_models(x_train, y_train, x_test, y_test, modelss, params):
    try:
        logging.info(f"Initiating model evaluation ")
        report = {}

        for i in range(len(list(modelss))):
            model = list(modelss.values())[i]
            param = params[list(params.keys())[i]]

            gs = GridSearchCV(model, param, cv = 3)
            gs.fit(x_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            pred_y_train = model.predict(x_train)
            pred_y_test = model.predict(x_test)

            train_model_score = r2_score(y_train, pred_y_train)
            test_model_score = r2_score(y_test, pred_y_test)

            report[list(modelss.keys())[i]] = test_model_score
        logging.info(f"model evaluation completed successfully")
        return report
    except Exception as e:
        raise ExpenseDataModelException(e, sys)