from src.mlpipeline.entity.config_entity import (ModelTrainerConfig)  
from src.mlpipeline.config.configuration import ConfigurationManager
from src.mlpipeline.components.model_trainer import ModelTrainer
from src.mlpipeline.logging import logger
from pathlib import Path

STAGE_NAME = "Model Training Stage"

class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def initiate_model_trainer(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.train_model()


if __name__ == "__main__":
    try:
        logger.info(f"Starting the {STAGE_NAME}...")
        model_trainer_pipeline = ModelTrainerTrainingPipeline()
        model_trainer_pipeline.initiate_model_trainer()
        logger.info(f"Completed the {STAGE_NAME}...")
    except Exception as e:
        logger.exception(e)
        raise e