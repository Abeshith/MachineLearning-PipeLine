import numpy as np
import pandas as pd
from scipy import stats
from src.mlpipeline.logging import logger


def feature_engineering(df):
    """Apply feature engineering transformations"""
    df = df.copy()
    
    # BMI - Added to train data
    if 'Weight' in df.columns and 'Height' in df.columns:
        df['BMI'] = df['Weight'] / ((df['Height'] / 100) ** 2)
    
    # Calories per minute - Added to train data
    if 'Calories' in df.columns and 'Duration' in df.columns:
        df['Calories_per_min'] = df['Calories'] / df['Duration'].replace(0, 1)
    
    # Sex as numeric
    df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
    
    # Interaction features
    if 'Age' in df.columns and 'Weight' in df.columns:
        df['Age_Weight'] = df['Age'] * df['Weight']
    
    if 'Heart_Rate' in df.columns and 'Body_Temp' in df.columns:
        df['Heart_Temp'] = df['Heart_Rate'] * df['Body_Temp']

    return df


def perform_statistical_tests(train_df, output_file):
    """Perform statistical tests and save results to file"""
    logger.info("Starting statistical tests...")
    
    # Remove outliers using Z-score
    numeric_cols = ['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp', 'Calories']
    z_scores = np.abs(stats.zscore(train_df[numeric_cols]))
    train_clean = train_df[(z_scores < 3).all(axis=1)]
    
    # Calculate correlations
    correlation_features = ['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp',
                           'Calories_per_min', 'Age_Weight', 'Heart_Temp']
    
    correlations = {}
    correlation_results = []
    
    for col in correlation_features:
        if col in train_clean.columns:
            corr = np.corrcoef(train_clean[col], train_clean['Calories'])[0, 1]
            correlations[col] = corr
            correlation_results.append(f"{col} correlation with Calories: {corr:.3f}")
    
    # ANOVA test for Sex
    anova = stats.f_oneway(train_clean[train_clean['Sex'] == 0]['Calories'],
                          train_clean[train_clean['Sex'] == 1]['Calories'])
    
    # Write results to file
    with open(output_file, 'w') as f:
        f.write("STATISTICAL TEST RESULTS\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("OUTLIER REMOVAL:\n")
        f.write(f"Original training data shape: {train_df.shape}\n")
        f.write(f"Clean training data shape: {train_clean.shape}\n")
        f.write(f"Outliers removed: {len(train_df) - len(train_clean)} ({((len(train_df) - len(train_clean))/len(train_df)*100):.2f}%)\n\n")
        
        f.write("FEATURE CORRELATIONS WITH CALORIES:\n")
        f.write("-" * 40 + "\n")
        for result in correlation_results:
            f.write(result + "\n")
        
        f.write(f"\nANOVA TEST FOR SEX:\n")
        f.write("-" * 40 + "\n")
        f.write(f"F-statistic: {anova.statistic:.3f}\n")
        f.write(f"p-value: {anova.pvalue:.3f}\n")
        
        if anova.pvalue < 0.05:
            f.write("Result: Significant difference between groups\n")
        else:
            f.write("Result: No significant difference between groups\n")
    
    logger.info(f"Statistical test results saved to {output_file}")
    
    # Print results to console
    print("\nSTATISTICAL TEST RESULTS:")
    print("=" * 50)
    for result in correlation_results:
        print(result)
    print(f"\nANOVA test for Sex: F={anova.statistic:.3f}, p={anova.pvalue:.3f}")
    
    return train_clean
