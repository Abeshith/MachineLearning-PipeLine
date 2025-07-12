from pathlib import Path
from src.mlpipeline.constants import *
from src.mlpipeline.utils.common import read_yaml, create_directories
from src.mlpipeline.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig

class ConfigurationManager:
    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])

    ### Data Ingestion Configuration
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        return DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source_url=config.source_URL,
            load_data_file=Path(config.load_data_file),
            unzip_dir=Path(config.unzip_dir)
        )
    

    ### Data Validation Configuration
    def get_data_validation_config(self) -> DataValidationConfig:
        """ Get the data validation configuration
        This method creates the directories for data validation and returns the configuration object.

        Returns:
            DataValidationConfig: _config object for data validation
        """
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        # Create directories for data validation
        create_directories([config.root_dir])
        
        data_validation_config = DataValidationConfig(
            root_dir = config.root_dir,
            STATUS_FILE = config.STATUS_FILE,
            unzip_data_dir = config.unzip_data_dir,
            all_schema = schema
        )
        
        return data_validation_config
    
     ### Data Transformation Configuration
    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Get the data transformation configuration

        Returns:
            DataTransformationConfig: _description_
        """
        config = self.config.data_transformation
        
        create_directories([config.root_dir])
         
        data_transformation_config = DataTransformationConfig(
            root_dir = Path(config.root_dir),
            data_path = Path(config.data_path)
        )
        return data_transformation_config
    
    
    ### Model Trainer Configuration
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.XGB
        schema = self.schema.TARGET_COLUMN

        # Create the directories for the artifacts
        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir = Path(config.root_dir),
            train_data_path = Path(config.train_data_path),
            test_data_path = Path(config.test_data_path),
            model_name = config.model_name,
            max_depth = params.max_depth,
            colsample_bytree = params.colsample_bytree,
            subsample = params.subsample,
            n_estimators = params.n_estimators,
            learning_rate = params.learning_rate,
            eval_metric = params.eval_metric,
            target = schema.name
        )
        return model_trainer_config
    
    ### Model Evaluation Configuration
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        schema = self.schema.TARGET_COLUMN
        params = self.params.XGB

        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir = Path(config.root_dir),
            model_path = Path(config.model_path),
            test_data_path = Path(config.test_data_path),
            all_params = params,
            metrics_file_name = Path(config.metrics_file_name),
            target_column = schema.name,
            mlflow_uri =  "https://dagshub.com/abheshith7/MachineLearning_PipeLine.mlflow"
        )
        return model_evaluation_config