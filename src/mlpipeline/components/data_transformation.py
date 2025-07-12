import os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.mlpipeline.entity.config_entity import DataTransformationConfig
from src.mlpipeline.logging import logger
from src.mlpipeline.utils.stats_test import feature_engineering, perform_statistical_tests


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def train_test_split_data(self):
        # Load data
        data = pd.read_csv(self.config.data_path)
        logger.info(f"Original data loaded: {data.shape}")
        
        # Apply feature engineering
        data = feature_engineering(data)
        logger.info(f"Feature engineering completed: {data.shape}")
        
        # Split data
        train, test = train_test_split(data, test_size=0.2, random_state=42, stratify=data['Sex'])
        
        # Perform statistical tests on train data and save results
        stats_file = os.path.join(self.config.root_dir, "statstestresults.txt")
        perform_statistical_tests(train, stats_file)
        
        # Save only train.csv and test.csv
        train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)

        logger.info("Train and test data split completed.")
        logger.info(f"Train data shape: {train.shape}")
        logger.info(f"Test data shape: {test.shape}")
        
        print(train.shape)
        print(test.shape)
        