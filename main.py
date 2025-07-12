import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.mlpipeline.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.mlpipeline.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.mlpipeline.pipeline.data_transformation_pipeline import DataTransformationTrainingPipeline
from src.mlpipeline.pipeline.model_trainer_pipeline import ModelTrainerTrainingPipeline
from src.mlpipeline.pipeline.model_evaluation_pipeline import ModelEvaluationTrainingPipeline
from src.mlpipeline.logging import logger

def main():
    """Main function to run the pipeline"""
    
    # Stage 1: Data Ingestion
    STAGE_NAME = "Data Ingestion Stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_ingestion_pipeline = DataIngestionTrainingPipeline()
        data_ingestion_pipeline.initiate_data_ingestion()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e

    # Stage 2: Data Validation
    STAGE_NAME = "Data Validation Stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_validation_pipeline = DataValidationTrainingPipeline()
        data_validation_pipeline.initiate_data_validation()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e

    # Stage 3: Data Transformation
    STAGE_NAME = "Data Transformation Stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_transformation_pipeline = DataTransformationTrainingPipeline()
        data_transformation_pipeline.initiate_data_transformation()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e

    # Stage 4: Model Training
    STAGE_NAME = "Model Training Stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        model_trainer_pipeline = ModelTrainerTrainingPipeline()
        model_trainer_pipeline.initiate_model_trainer()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e

    # Stage 5: Model Evaluation
    STAGE_NAME = "Model Evaluation Stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        model_evaluation_pipeline = ModelEvaluationTrainingPipeline()
        model_evaluation_pipeline.initiate_model_evaluation()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e

if __name__ == "__main__":
    main()
