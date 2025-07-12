import numpy as np
from src.mlpipeline.logging import logger
from src.mlpipeline.entity.config_entity import (ModelTrainerConfig)
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNet
import os, joblib
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train_model(self):
        logger.info("Starting model training...")
        
        # Load the training and testing data
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)
        
        logger.info(f"Training data shape: {train_data.shape}")
        logger.info(f"Test data shape: {test_data.shape}")

        # Separate the features and target variable
        # Remove non-feature columns like 'id'
        feature_cols = [col for col in train_data.columns if col not in [self.config.target, 'id']]
        
        X_train = train_data[feature_cols]
        y_train = train_data[self.config.target]
        X_test = test_data[feature_cols]
        y_test = test_data[self.config.target]
        
        logger.info(f"Features used: {feature_cols}")
        logger.info(f"Target: {self.config.target}")

        # Initialize the RandomForest model (as backup for XGBoost)
        model = RandomForestRegressor(
            max_depth=self.config.max_depth,
            n_estimators=min(self.config.n_estimators, 100), 
            random_state=42,
            n_jobs=-1
        )

        logger.info("Training RandomForest model...")
        # Train the model
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        logger.info(f"Model training completed!")
        logger.info(f"Test RMSE: {rmse:.4f}")
        logger.info(f"Test R2 Score: {r2:.4f}")
        
        print(f"Model Training Results:")
        print(f"Test RMSE: {rmse:.4f}")
        print(f"Test R2 Score: {r2:.4f}")

        # Save the model
        model_path = os.path.join(self.config.root_dir, self.config.model_name)
        joblib.dump(model, model_path)
        logger.info(f"Model saved to: {model_path}")
        
        return model, rmse, r2