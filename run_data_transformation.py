#!/usr/bin/env python3
"""
Run Data Transformation Pipeline with Statistical Tests
"""
import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.mlpipeline.pipeline.data_transformation_pipeline import DataTransformationTrainingPipeline
from src.mlpipeline.logging import logger

def main():
    """Main function to run the data transformation pipeline"""
    STAGE_NAME = "Data Transformation Stage"
    
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        # Run data transformation pipeline
        data_transformation_pipeline = DataTransformationTrainingPipeline()
        data_transformation_pipeline.initiate_data_transformation()
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<")
        
        # Display success message
        print(f"\n🎉 {STAGE_NAME} completed successfully!")
        print("📊 Statistical analysis results are available in the logs and artifacts.")
        print("📁 Check artifacts/data_transformation/ for all generated files.")
        
    except Exception as e:
        logger.exception(e)
        print(f"❌ Error in {STAGE_NAME}: {str(e)}")
        raise e

if __name__ == "__main__":
    main()
