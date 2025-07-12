from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    load_data_file: Path
    unzip_dir: Path

@dataclass
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict

@dataclass
class DataTransformationConfig:
    root_dir: Path
    data_path: Path

@dataclass
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    max_depth: int
    colsample_bytree: float
    subsample: float
    n_estimators: int
    learning_rate: float
    eval_metric: str
    target: str

@dataclass
class ModelEvaluationConfig:
    root_dir: Path
    model_path: Path
    test_data_path: Path
    all_params: dict
    metrics_file_name: Path
    target_column: str
    mlflow_uri: str