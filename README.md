# Locum Tenens Pay Rate Analysis & Forecasting

## Research Question
**How do locum tenens pay rates vary by specialty, location, and season, and can we predict future rate spikes?**

---

## Introduction
The locum tenens industry connects healthcare providers with hospitals and clinics on a temporary basis. 
Rates for locum work can fluctuate significantly depending on factors such as medical specialty, geographic location, 
urgency of the position, and time of year. Despite the abundance of job postings, there is no widely available, 
public-facing tool that analyzes these trends or predicts rate changes.

This project aims to fill that gap by collecting locum job posting data, analyzing patterns in pay rates, and 
building a simple forecasting model to anticipate future spikes. The end result could serve as a valuable 
resource for both providers seeking optimal opportunities and staffing organizations aiming to set competitive rates.

---

## Objectives
1. **Data Collection** – Gather locum job postings containing pay rates, specialty, location, and start date.
2. **Exploratory Analysis** – Identify trends in pay rates by specialty, state/city, and seasonality.
3. **Visualization** – Build interactive charts and dashboards to display insights.
4. **Prediction Model** – Train a model to forecast short-term pay rate changes by specialty and location.
5. **Public Insights** – Provide a clear, accessible tool or report that others can use to explore trends.

---

## Recommended Steps
1. **Select a Data Source**
   - Use a public job boards with accessible locum postings.
   - Starting point: [ProLocums](https://www.prolocums.com/job-search) (no login required).

2. **Data Gathering**
   - Use Python libraries such as `requests` + `BeautifulSoup` for HTML parsing.
   - Alternatively, check if JSON endpoints are available in the network tab for direct structured data pulls.
   - Store data in CSV or a database (e.g., SQLite, PostgreSQL).

3. **Data Cleaning & Preparation**
   - Standardize column names and formats.
   - Convert pay ranges into numeric values (hourly/daily).
   - Extract temporal features (month, season) from start dates.

4. **Exploratory Data Analysis (EDA)**
   - Average pay rate by specialty.
   - Highest-paying states/cities.
   - Seasonal trends in rates and demand.
   - Identify specialties with the largest fluctuations.

5. **Prediction**
   - Create a time series model (e.g., ARIMA, Prophet) or regression model to forecast pay rates.
   - Test accuracy using historical data splits.

6. **Visualization**
   - Use `Plotly`, `Dash`, or `Streamlit` for an interactive dashboard.
   - Include filters for specialty, location, and date range.

7. **Documentation & Sharing**
   - Publish code and documentation on GitHub.
   - Share visualizations publicly or deploy dashboard to platforms like Streamlit Cloud or Heroku.

---

## Recommended Public Data Source
**ProLocums Job Board**  
- URL: [https://www.prolocums.com/job-search](https://www.prolocums.com/job-search)  
- Publicly accessible without login.  
- Lists specialty, location, start date, and sometimes pay rates.  
- Filterable by specialty and location, making targeted data collection easier.

---

## Data Gathering Techniques
- **Direct HTML Scraping**:  
  - Use `requests` to fetch HTML and `BeautifulSoup` to parse listings.
- **Network Sniffing for JSON**:  
  - Check the browser developer tools “Network” tab to see if job listings load via a JSON API endpoint.
- **Scheduled Data Collection**:  
  - Run scraper daily with `cron` (Linux/macOS) or Task Scheduler (Windows) to build a time series dataset.
- **Ethical Considerations**:  
  - Only scrape publicly visible data.
  - Respect site `robots.txt`.
  - Implement request delays to avoid overloading servers.

---

## Expected Outcomes
- An interactive dashboard showing:
  - Highest-paying specialties.
  - Regional pay comparisons.
  - Seasonal demand and pay rate spikes.
- Predictive insights for upcoming months.

---

## Tech Stack
- **Languages:** Python
- **Libraries:** requests, BeautifulSoup4, pandas, numpy, plotly, dash/streamlit, scikit-learn, prophet
- **Database (optional):** SQLite / PostgreSQL
- **Hosting (optional):** Streamlit Cloud, Heroku, Vercel

---
