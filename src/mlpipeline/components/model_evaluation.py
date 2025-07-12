from src.mlpipeline.entity.config_entity import (ModelEvaluationConfig)
from src.mlpipeline.logging import logger
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from mlflow.models import infer_signature
import joblib
import os
from urllib.parse import urlparse
from src.mlpipeline.utils.common import save_json
from pathlib import Path
import dagshub
dagshub.init(repo_owner='abheshith7', repo_name='WineQuality-Prediction-Pipeline', mlflow=True)

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2
    
    def log_into_mlflow(self):

        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        X_test = test_data.drop(self.config.target_column, axis=1)
        y_test = test_data[self.config.target_column]

        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():

            predictions = model.predict(X_test)

            (rmse, mae, r2) = self.eval_metrics(y_test, predictions)

            mlflow.log_params(self.config.all_params)

            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("r2", r2)

            # Save metrics as a local JSON file
            metrics = {
                "rmse": rmse,
                "mae": mae,
                "r2": r2
            }
            save_json(Path(self.config.metrics_file_name), metrics)

            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(model, "model", registered_model_name="ElasticNetModel")
            else:
                mlflow.sklearn.log_model(model, "model")