import os, sys

import  certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv('MONGO_DB_URL')
print(mongo_db_url)

from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import pandas as pd

from expense_data_model.exception.exception import ExpenseDataModelException
from expense_data_model.logging.logger import logging
from expense_data_model.pipeline.training_pipeline import TrainingPipeline_
from expense_data_model.utils.ml_utils.metric.Regression_metric import get_regresion_score
from expense_data_model.utils.main_utils.utils import load_object
import pymongo

from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, Request, FastAPI, File
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory = "./templates")
from uvicorn import run as app_run
from starlette.responses import RedirectResponse

app = FastAPI()
origins = ["*"]

# This basically allows us to access the internet
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)



import pandas as pd
from expense_data_model.utils.ml_utils.models.estimator import ExpenseData_Model

client = pymongo.MongoClient(mongo_db_url, tlscafile=ca)

from expense_data_model.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from expense_data_model.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collections = database[DATA_INGESTION_COLLECTION_NAME]


import mlflow
import dagshub
from urllib.parse import urlparse



@app.get("/", tags = ['authentication'])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train():
    try:
        trian___pipeline = TrainingPipeline_()
        trian___pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise ExpenseDataModelException(e, sys)
    

@app.post("/prep test data")    
async def preping_data_for_test(request: Request, file: UploadFile = File(...)):
        try:
            logging.info("Initiate data preparation for test")
            
            df = pd.read_csv(file.file)

            # logging.info("data has been successfully read into pandas")

            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
            
            df['seconds'] = df.Timestamp.dt.second
            df['minutes'] = df.Timestamp.dt.minute
            df['hour'] = df.Timestamp.dt.hour
            df['month'] = df.Timestamp.dt.month
            df['day'] = df.Timestamp.dt.day

            if "SN" in df.columns:
                df.drop(columns = "SN", inplace=True)

            df.columns = df.columns.str.replace(' ','_').str.lower()

            #rearranging columns names and also excuding the time stamp column
            df = df[['expense_type', 'seconds','minutes', 'hour', 'month','day']]
            df['expense_type'] = LabelEncoder().fit_transform(df['expense_type'])
            df.to_csv("Test/test_data_1.csv", index = False)
            return "Test data successfully preped for Predictions"
        
        except Exception as e:
            raise ExpenseDataModelException(e, sys)
        

@app.post("/predict")
async def predict_(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor_ = load_object("final_model/preproccessor.pkl")
        model_ = load_object("final_model/model.pkl")

        f1_model = ExpenseData_Model(preprocessor=preprocessor_, model = model_)
        predictions = f1_model.predict(df)

        df['predicted_values'] = predictions
        df.to_csv('Predictions/output.csv')

        return "Predictions completed"
    
    except Exception as e:
        raise ExpenseDataModelException(e, sys)



if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)
    # The host parameter can also be "local", setting this to "0.0.0.0" allows you to be able to run the docker file.