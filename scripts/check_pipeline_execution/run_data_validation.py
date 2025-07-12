#!/usr/bin/env python3
"""
Run Data Validation Pipeline Only
"""
import sys
from pathlib import Path

# Add src to Python path - go up 2 directories to reach project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.mlpipeline.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.mlpipeline.logging import logger

def main():
    """Main function to run the data validation pipeline"""
    STAGE_NAME = "Data Validation Stage"
    
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_validation_pipeline = DataValidationTrainingPipeline()
        data_validation_pipeline.initiate_data_validation()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<")
        
        # Read and display the validation result
        with open("artifacts/data_validation/status.txt", "r") as f:
            status = f.read().strip()
        
        print(f"\n{STAGE_NAME} completed successfully!")
        print(f"Validation Result: {status}")
        
    except Exception as e:
        logger.exception(e)
        raise e

if __name__ == "__main__":
    main()