# pages/1_📈_Market_Overview.py
# ---------------------------------
# This script creates the "Market Overview" page of the Streamlit dashboard.
# It displays our key exploratory data analysis (EDA) visualizations.
# ---------------------------------

import os
import pandas as pd
import streamlit as st
import plotly.express as px

# Data Loading
# Re-using the same data loading function from the main dashboard page
# Streamlit's caching ensures the data is loaded only once.
PROCESSED_DATA_PATH = os.path.join('data', 'processed', 'jobs.parquet')

@st.cache_data
def load_data():
    """Loads the cleaned job data from the Parquet file."""
    if not os.path.exists(PROCESSED_DATA_PATH):
        st.error(f"Error: Processed data file not found at {PROCESSED_DATA_PATH}")
        return pd.DataFrame()
    return pd.read_parquet(PROCESSED_DATA_PATH)

df = load_data()

# Page Content

st.title("📈 Market Overview")
st.markdown("""
This page provides a high-level overview of the locum tenens job market based on our dataset.
Use the interactive charts below to explore trends in pay rates by specialty and location.
""")

if df.empty:
    st.warning("Could not load data. Please ensure the data pipeline has been run successfully.")
else:
    # Overall Metrics
    st.header("Overall Market Metrics")
    df_with_rates = df.dropna(subset=['rate_hourly'])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Job Postings Analyzed", f"{len(df):,}")
    col2.metric("Postings with Pay Data", f"{len(df_with_rates):,}")
    col3.metric("Median Hourly Rate (Overall)", f"${df_with_rates['rate_hourly'].median():.2f}")
    
    st.markdown("---")
    
    # Visualization Section
    st.header("Visualizations")
    
    # Treemap for Specialties
    st.subheader("Pay Rate Analysis by Specialty")
    st.markdown("""
    The treemap below visualizes all medical specialties in the dataset.
    - **Size of the rectangle** corresponds to the number of job postings.
    - **Color** corresponds to the median hourly pay rate (darker is higher).
    """)
    
    specialty_pay = df_with_rates.groupby('specialty').agg(
        median_hourly_rate=('rate_hourly', 'median'),
        job_count=('job_id', 'count')
    ).reset_index()

    # Prepare data for a robust treemap by defining a parent column to avoid Plotly bugs
    treemap_data = specialty_pay.copy()
    treemap_data['parent'] = 'All Specialties' # Assign a common parent

    fig_treemap = px.treemap(
        treemap_data,
        names='specialty',
        parents='parent',
        values='job_count',
        color='median_hourly_rate',
        color_continuous_scale='YlGnBu',
        title='Treemap of Specialties by Job Count and Median Pay Rate'
    )
    fig_treemap.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig_treemap, use_container_width=True)
    
    # Choropleth Map for Location
    st.subheader("Pay Rate Analysis by Location")
    st.markdown("The map below shows the median hourly pay rate for each state in our dataset.")
    
    state_pay = df_with_rates.groupby(['state', 'state_id']).agg(
        median_hourly_rate=('rate_hourly', 'median'),
        job_count=('job_id', 'count')
    ).reset_index()

    fig_map = px.choropleth(
        state_pay,
        locations='state_id',
        locationmode="USA-states",
        color='median_hourly_rate',
        scope="usa",
        hover_name='state',
        color_continuous_scale=px.colors.sequential.Blues,
        title='Median Hourly Pay Rate Across the United States'
    )
    fig_map.update_layout(title_x=0.5)
    st.plotly_chart(fig_map, use_container_width=True)
