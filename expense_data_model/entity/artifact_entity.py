from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str


@dataclass
class DataValidationArtifacts:
    valid_data_train_file_path:str
    valid_data_test_file_path:str
    invalid_data_train_file_path:str
    invalid_data_test_file_path:str
    validation_status:bool
    drift_report_file_path:str


@dataclass
class DataTransformationArtifacts:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str


@dataclass
class LinearRegression_Artifatcs:
    root_mean_square_error: float
    mean_square_error:float
    mean_absolute_error:float
    r2:float


@dataclass
class machine_learning_model_Artifacts:
    trained_model_file_path:str
    train_metric_Artifacts:LinearRegression_Artifatcs
    test_metric_artifacts:LinearRegression_Artifatcs
