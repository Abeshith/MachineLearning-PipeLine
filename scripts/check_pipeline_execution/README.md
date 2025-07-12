# Pipeline Execution Scripts

This folder contains organized scripts for running different parts of the ML pipeline.

## 📁 Structure

```
scripts/
└── check_pipeline_execution/
    ├── run_complete_pipeline.py     # Run all 5 pipeline stages
    ├── run_data_validation.py       # Run only data validation
    ├── run_data_transformation.py   # Run only data transformation
    ├── run_model_trainer.py         # Run only model training
    ├── run_model_evaluation.py      # Run only model evaluation
    └── run_statistical_tests.py     # Run statistical analysis
```

## 🚀 Usage

### Run Complete Pipeline
```bash
python scripts/check_pipeline_execution/run_complete_pipeline.py
```

### Run Individual Stages
```bash
# Data Validation
python scripts/check_pipeline_execution/run_data_validation.py

# Data Transformation
python scripts/check_pipeline_execution/run_data_transformation.py

# Model Training
python scripts/check_pipeline_execution/run_model_trainer.py

# Model Evaluation
python scripts/check_pipeline_execution/run_model_evaluation.py

# Statistical Tests
python scripts/check_pipeline_execution/run_statistical_tests.py
```

## 📊 Pipeline Stages

1. **Data Ingestion**: Downloads data from Kaggle
2. **Data Validation**: Validates data schema and quality
3. **Data Transformation**: Performs feature engineering and statistical analysis
4. **Model Training**: Trains XGBoost model
5. **Model Evaluation**: Evaluates model and logs to MLflow

## 📁 Output

All artifacts are saved to the `artifacts/` folder:
- `artifacts/data_ingestion/` - Raw data
- `artifacts/data_validation/` - Validation status
- `artifacts/data_transformation/` - Transformed data and stats
- `artifacts/model_trainer/` - Trained model
- `artifacts/model_evaluation/` - Model metrics

## 🔧 Prerequisites

Make sure you have:
- Python environment activated
- All required packages installed
- Kaggle API configured (for data ingestion)
- MLflow and DagHub setup (for model tracking)