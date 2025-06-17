import os
import sys
import json
from sklearn.preprocessing import LabelEncoder
from datetime import datetime


from dotenv import load_dotenv
load_dotenv()

#getting the environment variable
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi 
ca = certifi.where() #retrives the path to the bundle of ca (certificate certificates provided by certifi) and stores it in the variable "ca"


import pandas as pd
import numpy as np
import pymongo
from expense_data_model.logging.logger import logging
from expense_data_model.exception.exception import ExpenseDataModelException


class ExpenseDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        
    def preprocessing(self, file_path):
        try:
            df = pd.read_excel(file_path)
            
            df['seconds'] = df.Timestamp.dt.second
            df['minutes'] = df.Timestamp.dt.minute
            df['hour'] = df.Timestamp.dt.hour
            df['month'] = df.Timestamp.dt.month
            df['day'] = df.Timestamp.dt.day

            df.drop(columns = "SN", inplace=True)
            df.columns = df.columns.str.replace(' ','_').str.lower()

            #rearranging columns names and also excuding the time stamp column
            df = df[['expense_type', 'seconds','minutes', 'hour', 'month','day', 'costs']]
            df['expense_type'] = LabelEncoder().fit_transform(df['expense_type'])

            return df
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        

    def csv_to_json_converter(self, df):
        try:
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        

    def push_data_to_mongodb(self, records, database, collections):
        try:
            self.records = records
            self.database = database
            self.collections = collections

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]

            self.collections = self.database[self.collections]
            self.collections.insert_many(self.records)
            return len(self.records)

        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        
if __name__ == "__main__":
    FILE_PATH = "Expense Data/Tracker_ (Responses).xlsx"
    DATABASE = "Josh_okhiria"
    COLLECTION = "ExpenseData"

    expense_class = ExpenseDataExtract()
    df1 = expense_class.preprocessing(file_path=FILE_PATH)
    RECORDS = expense_class.csv_to_json_converter(df=df1)
    print(RECORDS)

    no_of_records = expense_class.push_data_to_mongodb(records=RECORDS, database=DATABASE, collections=COLLECTION)
    print(no_of_records)

