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
dagshub.init(repo_owner='abheshith7', repo_name='MachineLearning_PipeLine', mlflow=True)

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

        # Define features used during training (excluding 'id' and target)
        features_to_use = ['Sex', 'Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp',
                          'BMI', 'Calories_per_min', 'Age_Weight', 'Heart_Temp']
        
        # Use only the features that were used during training
        X_test = test_data[features_to_use]
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
            # Create the full path for the metrics file
            metrics_file_path = self.config.root_dir / self.config.metrics_file_name
            save_json(metrics_file_path, metrics)

            # Print evaluation results
            print(f"\n📊 MODEL EVALUATION RESULTS:")
            print(f"   RMSE: {rmse:.4f}")
            print(f"   MAE: {mae:.4f}")
            print(f"   R2 Score: {r2:.4f}")

            # Try to log the model
            try:
                if tracking_url_type_store != "file":
                    # Try to log model without registration first
                    mlflow.sklearn.log_model(model, "model")
                    logger.info("Model logged successfully to MLflow")
                else:
                    mlflow.sklearn.log_model(model, "model")
                    logger.info("Model logged successfully to local MLflow")
            except Exception as model_log_error:
                logger.warning(f"Failed to log model to MLflow: {str(model_log_error)}")
                # Continue without failing the pipeline
                print(f"⚠️  Warning: Could not log model to MLflow, but metrics were saved locally")
                
            logger.info("Model evaluation completed successfully")