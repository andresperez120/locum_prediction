# src/dashboard.py
# --------------------------
# This script is the main entry point for the Streamlit dashboard.
# It serves as the welcome page for the multi-page application.
# --------------------------

import streamlit as st
import os
from datetime import datetime

def main():
    # --- Page Configuration ---
    st.set_page_config(
        page_title="Locum Tenens Pay Rate Analysis",
        page_icon="💸",
        layout="wide"
    )

    # --- Welcome Page Content ---
    st.title("Welcome to the Locum Tenens Pay Rate Dashboard")
    st.markdown("""
    ### Your Data-Driven Tool for the Locum Tenens Market
    
    This dashboard is designed to provide insights into the locum tenens job market, helping businesses and physicians make smarter, more informed decisions. Our analysis is powered by a comprehensive dataset scraped from public job boards and a predictive model trained to estimate pay rates.
    
    ---
    
    ### How to Use This Dashboard
    
    Use the navigation sidebar on the left to explore the different sections of this application:
    
    *   **📈 Market Overview:** Explore interactive charts and maps that break down pay rates by specialty and location. This is where you can identify high-value markets and understand broad trends.
    
    *   **🤖 Pay Rate Predictor:** Access our predictive model through a simple, interactive form. Input the details of a job to get an instant, data-driven estimate of its likely hourly pay rate.
    
    ---
    
    This project was built to demonstrate a complete data science workflow, from data collection and cleaning to predictive modeling and interactive visualization.
    """)
    st.sidebar.success("Select a page above to begin.")

    # Data Freshness
    DATA_PATH = "data/processed/jobs.parquet"
    if os.path.exists(DATA_PATH):
        last_updated_timestamp = os.path.getmtime(DATA_PATH)
        last_updated_date = datetime.fromtimestamp(last_updated_timestamp).strftime("%m/%d/%y")
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**Data Last Updated:**<br>{last_updated_date}", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
