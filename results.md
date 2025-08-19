# Project Results: Locum Tenens Pay Rate Analysis

This analysis helps locum tenens businesses make smarter, data-driven decisions by revealing the key factors—specialty, location, and specific job requirements—that most influence physician pay rates, enabling more competitive recruitment and better market understanding.

This document summarizes the key findings from our analysis of the locum tenens job market data. Our primary research question was:

> How do locum tenens pay rates vary by specialty, location, and season?

---

## 1. Pay Rate Variation by Specialty

**Finding:** Pay rates are heavily influenced by medical specialty. Highly specialized and procedural fields command significantly higher rates than generalist or primary care fields.

**Supporting Visualization:** A comprehensive treemap was created to visualize all 64 specialties at once. In this chart, the size of each rectangle represents the number of job postings, and the color represents the median hourly pay rate.

*   **Location:** `notebooks/02_eda.ipynb` (Cell 4: "Pay Rate Analysis by Specialty")

### Summary Tables

The tables below show the top 10 highest and lowest paying specialties based on the median hourly rate from our dataset.

**Top 10 Highest-Paying Specialties**

| Specialty               | Median Hourly Rate |
|:------------------------|:-------------------|
| Gastroenterology        | $450.00            |
| Hematology Oncology     | $450.00            |
| Anesthesiology          | $400.00            |
| Urology                 | $400.00            |
| Surgery - General       | $375.00            |
| Cardiology - General    | $350.00            |
| Neurological Surgery    | $350.00            |
| Psychiatry              | $350.00            |
| Radiology               | $325.00            |
| Neurology               | $300.00            |

**Top 10 Lowest-Paying Specialties**
*(Note: This includes specialties with fewer data points)*

| Specialty               | Median Hourly Rate |
|:------------------------|:-------------------|
| Wound Care              | $125.00            |
| Geriatrics              | $150.00            |
| Family Practice         | $175.00            |
| Internal Medicine       | $187.50            |
| Pediatrics              | $200.00            |
| Hospitalist             | $225.00            |
| Emergency Medicine      | $250.00            |
| Obstetrics/Gynecology   | $250.00            |
| Urgent Care             | $250.00            |
| Otolaryngology          | $275.00            |

---

## 2. Pay Rate Variation by Location

**Finding:** Geographical location is a significant driver of pay rates. There is considerable variance between states and regions, likely due to local market demand, cost of living, and the number of available physicians.

**Supporting Visualizations:**
Two primary visualizations were created to explore these geographical trends:

1.  **Regional Bar Chart:** A horizontal bar chart displaying the median hourly rate for every state, colored by one of six geographical regions (New England, Mid-Atlantic, South, Midwest, Southwest, West).
2.  **Choropleth Map:** A map of the United States where each state is colored based on its median hourly pay rate, providing an intuitive geographical overview.

*   **Location:** `notebooks/02_eda.ipynb` (Cell 6: "Pay Rate Analysis by Location")

### Median Hourly Rate by State (Full Data)

The table below provides a comprehensive breakdown of the median hourly pay rate for each state, based on the available job postings in our dataset.

| State(s)                                                                                                                  | Median Hourly Rate |
|:--------------------------------------------------------------------------------------------------------------------------|:-------------------|
| Florida                                                                                                                   | $400.00            |
| Alabama                                                                                                                   | $350.00            |
| Maryland                                                                                                                  | $325.00            |
| Minnesota                                                                                                                 | $312.50            |
| Colorado, Arizona, Ohio, Missouri, Nebraska, North Dakota, Michigan, Arkansas                                            | $300.00            |
| Idaho                                                                                                                     | $287.50            |
| Wisconsin                                                                                                                 | $275.00            |
| Indiana                                                                                                                   | $262.50            |
| Massachusetts, Maine, New Hampshire, Washington, Alaska, Oklahoma, Texas, Iowa, Illinois, New York, Pennsylvania, Virginia, Kentucky, West Virginia | $250.00            |
| New Mexico, South Carolina                                                                                                | $237.50            |
| California, Wyoming, Utah, Kansas                                                                                         | $220.00            |
| Vermont                                                                                                                   | $210.00            |
| Nevada                                                                                                                    | $205.00            |
| Montana, Oregon, Mississippi, Tennessee, North Carolina                                                                   | $200.00            |
| Georgia                                                                                                                   | $155.00            |
| Connecticut                                                                                                               | $144.00            |
| New Jersey                                                                                                                | $120.00            |

---

## 3. Pay Rate Variation by Season

**Finding:** **This question cannot be answered with the current data.**

**Reasoning:** The analysis is based on a single data snapshot collected on a specific date. To accurately analyze seasonality, we would need to collect data periodically (e.g., weekly or monthly) over an extended period, ideally 12 months or more. This would allow us to identify and quantify any seasonal trends, such as increased demand for certain specialties during winter.

The data collection pipeline (`src/data_collection.py`) is designed to be re-run, which makes this a feasible and highly recommended next step for future analysis.

---

## 4. Business Applications & Value

This project provides direct, actionable value to a locum tenens business in three key areas:

**1. Faster, More Competitive Bidding:**
Instead of relying on manual research, the predictive model can be used as an internal tool to generate instant, data-driven market rate estimates for new job orders. This allows for faster, more confident bidding on hospital contracts, ensuring offers are competitive enough to attract physicians without sacrificing margins.

**2. Strategic Business Development:**
The analysis of high-value markets is no longer a guessing game. The dashboard and results clearly identify which specialties and geographical locations offer the highest pay rates. This enables the business to strategically focus its recruitment and marketing efforts on the most profitable opportunities, maximizing the return on investment.

**3. Data-Driven Negotiations:**
This analysis provides objective data that can be used as leverage in negotiations.
*   **With Hospitals:** If a hospital's proposed rate is below market for a job with specific requirements (e.g., trauma coverage, on-call duty), this data can be used to justify a higher rate.
*   **With Physicians:** It allows the business to build trust by demonstrating that their pay offers are fair and aligned with current market data.

In essence, this project transforms business decisions from being based on intuition into being driven by **fast, accurate, and defensible data.**
