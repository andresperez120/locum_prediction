# Locum Tenens Pay Rate Analysis & Forecasting

## Research Question
**How do locum tenens pay rates vary by specialty, location, and season, and can we predict future rate spikes?**

---

## Introduction
The locum tenens industry connects healthcare providers with hospitals and clinics on a temporary basis. Rates for locum work can fluctuate significantly depending on factors such as medical specialty, geographic location, and urgency of the position. 

This project analyzes these trends by collecting job posting data from ProLocums. It cleans the data, extracts key features using NLP, and builds a predictive model to forecast hourly pay rates. The entire project is presented in an interactive Streamlit dashboard that allows users to explore market trends and predict pay rates for specific job criteria.

---

## Objectives
1. **Data Collection** – Gathers locum job postings from ProLocums, handling pagination to create a comprehensive raw dataset.
2. **Data Processing** – Cleans the raw data, normalizes pay rates, and engineers new features, including NLP-derived flags from job descriptions.
3. **Predictive Modeling** – Trains a Random Forest model to predict hourly pay rates based on job characteristics like specialty, location, duration, and specific requirements.
4. **Interactive Dashboard** – Presents the findings through a multi-page Streamlit application, featuring a market overview and a pay rate predictor tool.

---

## Project Structure
- **/data**: Contains raw and processed data. The final, cleaned dataset is stored in `data/processed/jobs.parquet`.
- **/docs**: Contains project documentation, including key assumptions.
- **/models**: Stores the trained machine learning model (`random_forest_model.joblib`) and test data splits.
- **/notebooks**: Jupyter notebooks used for exploratory data analysis (`eda.ipynb`) and model prediction analysis (`prediction_analysis.ipynb`).
- **/src**: All Python source code.
  - `data_collection.py`, `data_cleaning.py`, `nlp_feature_extraction.py`, `modeling.py`: The core data pipeline scripts.
  - `dashboard.py`: The main entry point for the Streamlit app.
  - `pages/`: Each `.py` file here represents a page in the Streamlit app.

---

## Natural Language Processing (NLP)
To enrich the dataset, key features were extracted from the HTML job descriptions. The process focused on parsing the text contained within bullet points (`<li>` tags), as these areas typically contain the most structured and valuable information.

A keyword-matching algorithm was used to search this extracted text for terms related to certifications (e.g., "board certified"), work conditions (e.g., "weekend shifts"), and specific skills or environments (e.g., "trauma center," "ACLS," "Epic EMR"). This created new binary features that significantly improved the predictive power of the model.

---

## Tech Stack
- **Language:** Python
- **Libraries:** Streamlit, Pandas, Scikit-learn, Plotly, NLTK, Joblib, Requests, BeautifulSoup4

---

## How to Run This Project

Follow these steps to set up and run the data pipeline and dashboard locally.

### 1. Setup and Installation

First, clone the repository and navigate into the project directory. It's recommended to use a virtual environment to manage dependencies.

```bash
# Create and activate a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt
```

### 2. Run the Data Pipeline (Optional)

The repository includes pre-processed data and a trained model. However, if you wish to refresh the data from the source, run the pipeline scripts in order.

```bash
# Step 1: Collect the raw job data from the web
python3 src/data_collection.py

# Step 2: Clean and process the raw data
python3 src/data_cleaning.py

# Step 3: Train the predictive model on the new data
python3 src/modeling.py
```

### 3. Launch the Dashboard

To explore the data and use the prediction tool, launch the Streamlit dashboard.

```bash
# Run the Streamlit application
streamlit run src/dashboard.py
```

Your web browser should open a new tab with the interactive dashboard.
