from src.mlpipeline.entity.config_entity import (DataValidationConfig)  
from src.mlpipeline.config.configuration import ConfigurationManager
from src.mlpipeline.components.data_validation import DataValidation
from src.mlpipeline.logging import logger

STAGE_NAME = "Data Validation Stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass 

    def initiate_data_validation(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()
