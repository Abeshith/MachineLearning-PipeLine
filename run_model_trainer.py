#!/usr/bin/env python3
"""
Run Model Trainer Pipeline
"""
import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.mlpipeline.pipeline.model_trainer_pipeline import ModelTrainerTrainingPipeline
from src.mlpipeline.logging import logger

def main():
    """Main function to run the model trainer pipeline"""
    STAGE_NAME = "Model Trainer Stage"
    
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        # Run model trainer pipeline
        model_trainer_pipeline = ModelTrainerTrainingPipeline()
        model_trainer_pipeline.initiate_model_trainer()
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<")
        
        # Display success message
        print(f"\n🎉 {STAGE_NAME} completed successfully!")
        print("🤖 Model has been trained and saved.")
        print("📁 Check artifacts/model_trainer/ for the trained model.")
        
    except Exception as e:
        logger.exception(e)
        print(f"❌ Error in {STAGE_NAME}: {str(e)}")
        raise e

if __name__ == "__main__":
    main()
