from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score
from expense_data_model.exception.exception import ExpenseDataModelException
import os, sys
from expense_data_model.entity.artifact_entity import LinearRegression_Artifatcs

def get_regresion_score(y_true, y_pred)->LinearRegression_Artifatcs:
    try:
        model_r2 = r2_score(y_true, y_pred)
        model_mae = mean_absolute_error(y_true, y_pred)
        model_mse = mean_squared_error(y_true, y_pred)
        model_rmse = root_mean_squared_error(y_true, y_pred) 

        regression_metric = LinearRegression_Artifatcs(
            root_mean_square_error = model_rmse,
            mean_square_error = model_mse,
            mean_absolute_error = model_mae,
            r2 = model_r2
                )
        return regression_metric
    
    except Exception as e:
        raise ExpenseDataModelException(e, sys)
    
    