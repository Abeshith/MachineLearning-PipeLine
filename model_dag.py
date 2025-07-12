from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import sys
import os
from pathlib import Path

# Add project root to Python path
# Handle both local execution and Airflow execution
if 'airflow' in __file__:
    # Running from Airflow dags directory - adjust for WSL/Ubuntu
    project_root = Path.home() / "MachineLearning Pipeline"
else:
    # Running from project directory
    project_root = Path(__file__).parent

# Add both project root and src directory to Python path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# Change working directory to project root for relative paths to work
os.chdir(str(project_root))

# Import pipeline modules
try:
    from src.mlpipeline.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
    from src.mlpipeline.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
    from src.mlpipeline.pipeline.data_transformation_pipeline import DataTransformationTrainingPipeline
    from src.mlpipeline.pipeline.model_trainer_pipeline import ModelTrainerTrainingPipeline
    from src.mlpipeline.pipeline.model_evaluation_pipeline import ModelEvaluationTrainingPipeline
    from src.mlpipeline.logging import logger
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    raise

# Task 1: Data Ingestion
def data_ingestion():
    logger.info(">>>>>> Data Ingestion Stage started <<<<<<")
    data_ingestion_pipeline = DataIngestionTrainingPipeline()
    data_ingestion_pipeline.initiate_data_ingestion()
    logger.info(">>>>>> Data Ingestion Stage completed <<<<<<")
    return "Data ingestion completed successfully"

# Task 2: Data Validation
def data_validation():
    logger.info(">>>>>> Data Validation Stage started <<<<<<")
    data_validation_pipeline = DataValidationTrainingPipeline()
    data_validation_pipeline.initiate_data_validation()
    logger.info(">>>>>> Data Validation Stage completed <<<<<<")
    return "Data validation completed successfully"

# Task 3: Data Transformation
def data_transformation():
    logger.info(">>>>>> Data Transformation Stage started <<<<<<")
    data_transformation_pipeline = DataTransformationTrainingPipeline()
    data_transformation_pipeline.initiate_data_transformation()
    logger.info(">>>>>> Data Transformation Stage completed <<<<<<")
    return "Data transformation completed successfully"

# Task 4: Model Training
def model_training():
    logger.info(">>>>>> Model Training Stage started <<<<<<")
    model_trainer_pipeline = ModelTrainerTrainingPipeline()
    model_trainer_pipeline.initiate_model_trainer()
    logger.info(">>>>>> Model Training Stage completed <<<<<<")
    return "Model training completed successfully"

# Task 5: Model Evaluation
def model_evaluation():
    logger.info(">>>>>> Model Evaluation Stage started <<<<<<")
    model_evaluation_pipeline = ModelEvaluationTrainingPipeline()
    model_evaluation_pipeline.initiate_model_evaluation()
    logger.info(">>>>>> Model Evaluation Stage completed <<<<<<")
    return "Model evaluation completed successfully"

# Define the DAG
with DAG(
    dag_id='ml_pipeline_dag',
    start_date=datetime(2025, 7, 12),
    schedule=None,
    catchup=False
) as dag:
    data_ingestion_task = PythonOperator(
        task_id='data_ingestion',
        python_callable=data_ingestion
    )
    data_validation_task = PythonOperator(
        task_id='data_validation',
        python_callable=data_validation
    )
    data_transformation_task = PythonOperator(
        task_id='data_transformation',
        python_callable=data_transformation
    )
    model_training_task = PythonOperator(
        task_id='model_training',
        python_callable=model_training
    )
    model_evaluation_task = PythonOperator(
        task_id='model_evaluation',
        python_callable=model_evaluation
    )

    # Set task dependencies
    data_ingestion_task >> data_validation_task >> data_transformation_task >> model_training_task >> model_evaluation_task
