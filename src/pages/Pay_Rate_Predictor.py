# pages/2_🤖_Pay_Rate_Predictor.py
# ------------------------------------
# This script creates the "Pay Rate Predictor" page of the dashboard.
# It allows users to input job characteristics and get a live prediction
# from our trained Random Forest model.
# ------------------------------------

import os
import pandas as pd
import streamlit as st
import joblib

# Load Model and Artifacts
MODEL_PATH = os.path.join('models', 'random_forest_model.joblib')
DATA_PATH = os.path.join('data', 'processed', 'jobs.parquet')

@st.cache_resource
def load_model():
    """Loads the trained machine learning model."""
    if not os.path.exists(MODEL_PATH):
        st.error(f"Error: Model file not found at {MODEL_PATH}")
        return None
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_unique_values():
    """Loads the processed data to get unique values for dropdowns."""
    if not os.path.exists(DATA_PATH):
        st.error(f"Error: Data file not found at {DATA_PATH}")
        return {}
    df = pd.read_parquet(DATA_PATH)
    
    # Create a dictionary to map states to their cities for cascading dropdowns
    state_city_map = df.groupby('state')['city'].apply(lambda x: sorted(list(x.dropna().unique()))).to_dict()
    
    return {
        'specialty': sorted(df['specialty'].dropna().unique()),
        'state': sorted(df['state'].dropna().unique()),
        'state_city_map': state_city_map,
    }

model = load_model()
unique_values = load_unique_values()

# Page Content

st.title("🤖 Pay Rate Predictor")

st.markdown("""
This tool uses our trained machine learning model to predict the hourly pay rate for a locum tenens position based on its characteristics.

**Instructions:**
1.  Fill out the details for the job posting in the sidebar on the left.
2.  The model's prediction will be displayed below.
""")

if not model or not unique_values:
    st.warning("Model or data artifacts could not be loaded. Please ensure the pipeline has been run successfully.")
else:
    # Sidebar Inputs
    st.sidebar.header("Job Details")

    specialty = st.sidebar.selectbox("Medical Specialty", unique_values['specialty'])
    state = st.sidebar.selectbox("State", unique_values['state'])
    
    # The city dropdown is now dependent on the selected state
    available_cities = unique_values['state_city_map'].get(state, [])
    city = st.sidebar.selectbox("City", available_cities)
    
    job_duration_days = st.sidebar.number_input("Job Duration (Days)", min_value=1, max_value=365, value=30)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Job Requirements (from Description)")
    
    is_board_certified = st.sidebar.checkbox("Board Certified/Eligible Required", value=True)
    has_weekend_shift = st.sidebar.checkbox("Includes Weekend Shifts", value=False)
    is_trauma_center = st.sidebar.checkbox("Is a Trauma Center", value=False)
    requires_acls = st.sidebar.checkbox("Requires ACLS Certification", value=False)
    uses_epic_emr = st.sidebar.checkbox("Uses Epic EMR System", value=False)

    # Prediction Logic
    
    # Get the column names from the model's training data
    # The model expects the input in the exact same format
    model_features = model.feature_names_in_
    
    # Create an empty DataFrame with the correct feature columns
    input_df = pd.DataFrame(columns=model_features)
    input_df.loc[0] = 0 # Initialize a row with zeros
    
    # Prepare the input for the model
    # 1. Set the numerical features
    input_df['job_duration_days'] = job_duration_days
    input_df['is_board_certified'] = 1 if is_board_certified else 0
    input_df['has_weekend_shift'] = 1 if has_weekend_shift else 0
    input_df['is_trauma_center'] = 1 if is_trauma_center else 0
    input_df['requires_acls'] = 1 if requires_acls else 0
    input_df['uses_epic_emr'] = 1 if uses_epic_emr else 0
    
    # Set the one-hot encoded categorical features
    # The feature name is in the format 'category_value' (e.g., 'state_CA')
    spec_col = f'specialty_{specialty}'
    if spec_col in model_features:
        input_df[spec_col] = 1
        
    state_col = f'state_{state}'
    if state_col in model_features:
        input_df[state_col] = 1

    city_col = f'city_{city}'
    if city_col in model_features:
        input_df[city_col] = 1

    # Make Prediction
    prediction = model.predict(input_df)[0]
    
    # Display Prediction
    st.header("Prediction")
    st.metric("Predicted Hourly Rate", f"${prediction:,.2f}")

    st.markdown("---")
    st.subheader("Inputs Used for This Prediction")
    st.write(input_df.T.rename(columns={0: 'Value'}))
