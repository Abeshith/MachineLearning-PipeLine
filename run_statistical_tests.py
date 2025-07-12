#!/usr/bin/env python3
"""
Run Statistical Tests on Transformed Data
"""
import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.mlpipeline.config.configuration import ConfigurationManager
from src.mlpipeline.components.data_transformation import DataTransformation
from src.mlpipeline.logging import logger
import json

def main():
    """Main function to run statistical tests"""
    
    try:
        logger.info("Running statistical tests on transformed data")
        
        # Initialize configuration and data transformation
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        
        # Run statistical tests
        correlations, anova_results = data_transformation.run_statistical_tests()
        
        # Load and display transformation report
        with open("artifacts/data_transformation/transformation_report.json", "r") as f:
            report = json.load(f)
        
        print("\n" + "="*60)
        print("TRANSFORMATION SUMMARY REPORT")
        print("="*60)
        
        print(f"Original data shape: {report['original_shape']}")
        print(f"Transformed data shape: {report['transformed_shape']}")
        print(f"Outliers removed: {report['outliers_removed']} ({report['outliers_percentage']:.2f}%)")
        print(f"New features added: {report['new_features']}")
        print(f"High correlation features (>0.5): {report['high_correlation_features']}")
        print(f"Low correlation features (<0.1): {report['low_correlation_features']}")
        
        print("\n" + "="*60)
        print("✅ Statistical analysis completed successfully!")
        print("📊 Check the logs for detailed analysis results.")
        
    except Exception as e:
        logger.exception(e)
        print(f"❌ Error running statistical tests: {str(e)}")
        raise e

if __name__ == "__main__":
    main()
