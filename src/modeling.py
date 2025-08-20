# src/modeling.py
# --------------------------
# This script is responsible for building a predictive model to forecast
# locum tenens pay rates. It uses a cross-sectional approach to predict
# hourly rates based on job characteristics.
# --------------------------

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
import joblib
import numpy as np

# Define the path to the processed data
PROCESSED_DATA_PATH = os.path.join('data', 'processed', 'jobs.parquet')
MODEL_OUTPUT_PATH = os.path.join('models')

def load_data() -> pd.DataFrame:
    """Loads the cleaned job data from the Parquet file."""
    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(f"Processed data file not found at {PROCESSED_DATA_PATH}")
    
    df = pd.read_parquet(PROCESSED_DATA_PATH)
    print(f"Successfully loaded data with shape: {df.shape}")
    return df

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares the data for modeling by selecting features and encoding categorical variables.
    """
    # Select features and target
    categorical_features = ['specialty', 'state', 'city']
    numerical_features = [
        'job_duration_days',
        'is_board_certified',
        'has_weekend_shift',
        'is_trauma_center',
        'requires_acls',
        'uses_epic_emr'
    ]
    target = 'rate_hourly'
    features = categorical_features + numerical_features
    
    # --- Data Cleaning & Preprocessing ---
    # Log transform the job duration to handle skewness
    df['job_duration_days'] = np.log1p(df['job_duration_days'])
    
    # Drop rows where the target is missing, as we can't train on them
    df_model = df[features + [target]].dropna(subset=[target])
    
    # Handle Missing Values for Features
    # For job duration, fill missing values with the median. This is a robust way
    # to handle missing data without discarding the entire row.
    median_duration = df_model['job_duration_days'].median()
    df_model['job_duration_days'].fillna(median_duration, inplace=True)
    
    # For city and coverage_type, fill missing values with a placeholder string.
    df_model['city'].fillna('Unknown', inplace=True)
    
    # One-hot encode categorical features
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    encoded_cats = encoder.fit_transform(df_model[categorical_features])
    
    # Create a new DataFrame with the encoded features
    df_encoded_cats = pd.DataFrame(encoded_cats, columns=encoder.get_feature_names_out(categorical_features))
    
    # Reset index to ensure proper alignment
    df_model.reset_index(drop=True, inplace=True)
    
    # Combine encoded categorical features with numerical features
    df_processed = pd.concat([df_model[numerical_features], df_encoded_cats], axis=1)
    
    print(f"Feature engineering complete. Modeling with {len(df_processed.columns)} features.")
    
    return df_model, df_processed, target


def main():
    """Main function to run the modeling pipeline."""
    print("Starting modeling pipeline...")
    
    # Load and preprocess data
    df = load_data()
    
    df_model, df_encoded, target = feature_engineering(df)
    
    if df_model.empty:
        print("No data available for modeling after feature engineering. Aborting.")
        return
        
    # Train and Evaluate Model
    X = df_encoded
    y = df_model[target]
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"\nTraining model on {len(X_train)} samples, testing on {len(X_test)} samples.")
    
    # Initialize and train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("\n--- Model Evaluation ---")
    print(f"  - R-squared (R²): {r2:.2f}")
    print(f"  - Mean Absolute Error (MAE): ${mae:.2f}")
    print("------------------------")

    # --- Feature Importance ---
    print("\n--- Top 15 Feature Importances ---")
    importances = model.feature_importances_
    feature_names = X_train.columns
    importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    print(importance_df.head(15))
    print("------------------------------------")
    
    # Display a few sample predictions
    print("\n--- Sample Predictions ---")
    predictions_df = pd.DataFrame({'Actual Rate': y_test, 'Predicted Rate': y_pred}).reset_index(drop=True)
    print(predictions_df.head())
    print("--------------------------")
    
    # Save Model and Test Data
    # Save the trained model and the test set for further analysis and visualization
    print("\nSaving model and test data artifacts...")
    os.makedirs(MODEL_OUTPUT_PATH, exist_ok=True)
    
    joblib.dump(model, os.path.join(MODEL_OUTPUT_PATH, 'random_forest_model.joblib'))
    X_test.to_parquet(os.path.join(MODEL_OUTPUT_PATH, 'X_test.parquet'))
    y_test.to_frame().to_parquet(os.path.join(MODEL_OUTPUT_PATH, 'y_test.parquet'))
    importance_df.to_csv(os.path.join(MODEL_OUTPUT_PATH, 'feature_importances.csv'), index=False)
    
    print("Artifacts saved successfully.")


if __name__ == "__main__":
    main()
