from src.mlpipeline.entity.config_entity import (DataTransformationConfig)  
from src.mlpipeline.config.configuration import ConfigurationManager
from src.mlpipeline.components.data_transformation import DataTransformation
from src.mlpipeline.logging import logger
from pathlib import Path

STAGE_NAME = "Data Transformation Stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"), "r") as file:
                status_content = file.read().strip()
            
            # Parse the validation status more robustly
            if "Validation status: True" in status_content:
                status = "True"
            elif "Validation status: False" in status_content:
                status = "False"
            else:
                # Fallback to original parsing
                status = status_content.split(" ")[-1].strip()
            
            logger.info(f"Validation status: {status}")
            
            if status == "True":
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.train_test_split_data()
            else:
                raise Exception("Data Validation failed. Cannot proceed with Data Transformation.")
        except Exception as e:
            logger.exception(e)
            raise e