# Project Assumptions

This document outlines the key assumptions made during the development of my Locum Tenens Pay Rate Analysis project. Documenting these assumptions is crucial for transparency and reproducibility.

---

## 1. Data Cleaning and Normalization

### 1.1. Pay Rate Extraction

- **Priority of Data Sources:** We prioritize structured data over unstructured text. The `RegularHR` column is considered the primary source for pay rates. If this value is missing or zero, we fall back to a regular expression search on the HTML `Description` of the job posting.
- **Handling of Missing Rates:** If a pay rate cannot be found in either the structured column or the description, it is treated as a true missing value (`NaN`). We do not attempt to impute or guess these values.

### 1.2. Normalization to Daily Rate

- **Assumption of 8-Hour Workday:** The `rate_daily` column is calculated by multiplying the `rate_hourly` by 8. This assumes a standard 8-hour workday for locum tenens physicians. We acknowledge that this is a simplification, as actual shift lengths can vary. The primary metric for analysis in the EDA notebook is `rate_hourly` to avoid this assumption where possible.

### 1.3. Aggregation Metric

- **Use of Median:** When aggregating pay rates (e.g., by specialty, state, or week), we use the **median** instead of the mean. The median is less sensitive to extreme outliers, providing a more robust measure of the central tendency for pay rates, which can often be skewed.

## 2. Modeling

### 2.1. Model Type

- **Cross-Sectional Model:** Due to the initial dataset being a single snapshot in time, we have built a cross-sectional model to predict current pay rates based on job features. The time-series forecasting model outlined in the original project plan can be implemented once several weeks of data have been collected.

### 2.2. Feature Selection

- **Initial Feature Set:** Our baseline model uses `specialty` and `state` as the primary predictors. We acknowledge that other factors (e.g., job duration, specific skills required) could influence pay rates, but these were chosen for their high availability and impact, as observed during the EDA.

## 3. Data Source

### 3.1. Single Source

- **ProLocums as the Single Source:** This analysis is based exclusively on data from the ProLocums job board. The trends and predictions reflect the job market as represented on this specific platform and may not be generalizable to the entire locum tenens industry.

### 3.2. Data Freshness

- **Snapshot in Time:** The analysis and models are based on the data as it was collected on a specific date. The job market is dynamic, and rates can change. The data pipeline is designed to be re-run regularly to capture these changes.
