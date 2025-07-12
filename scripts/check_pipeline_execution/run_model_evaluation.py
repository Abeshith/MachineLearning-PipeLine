#!/usr/bin/env python3
"""
Run Model Evaluation Pipeline
"""
import sys
from pathlib import Path

# Add src to Python path - go up 2 directories to reach project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.mlpipeline.pipeline.model_evaluation_pipeline import ModelEvaluationTrainingPipeline
from src.mlpipeline.logging import logger

def main():
    """Main function to run the model evaluation pipeline"""
    STAGE_NAME = "Model Evaluation Stage"
    
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        # Run model evaluation pipeline
        model_evaluation_pipeline = ModelEvaluationTrainingPipeline()
        model_evaluation_pipeline.initiate_model_evaluation()
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<")
        
        print(f"\n🎉 {STAGE_NAME} completed successfully!")
        print("📊 Model evaluation results logged to MLFlow!")
        print("📁 Check artifacts/model_evaluation/ for metrics file.")
        
    except Exception as e:
        logger.exception(e)
        print(f"❌ Error in {STAGE_NAME}: {str(e)}")
        raise e

if __name__ == "__main__":
    main()