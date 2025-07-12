import os
import subprocess
import zipfile
from pathlib import Path
from src.mlpipeline.entity.config_entity import DataValidationConfig
from src.mlpipeline.logging import logger
import pandas as pd


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
        
    def validate_all_columns(self) -> bool:
        try:
            validation_status = None
            
            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)
            
            all_schema = self.config.all_schema.keys()
            
            logger.info(f"Data columns: {all_cols}")
            logger.info(f"Schema columns: {list(all_schema)}")
            
            missing_cols = []
            extra_cols = []
            
            # Check for missing columns
            for schema_col in all_schema:
                if schema_col not in all_cols:
                    missing_cols.append(schema_col)
            
            # Check for extra columns
            for data_col in all_cols:
                if data_col not in all_schema:
                    extra_cols.append(data_col)
            
            if missing_cols or extra_cols:
                validation_status = False
                status_msg = f"Validation status: {validation_status}\n"
                if missing_cols:
                    status_msg += f"Missing columns: {missing_cols}\n"
                if extra_cols:
                    status_msg += f"Extra columns: {extra_cols}\n"
                    
                logger.error(f"Validation failed. Missing: {missing_cols}, Extra: {extra_cols}")
            else:
                validation_status = True
                status_msg = f"Validation status: {validation_status}\nAll columns match the schema.\n"
                logger.info("All columns validation passed!")
            
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(status_msg)

            return validation_status
        except Exception as e:
            logger.exception(e)
            raise e