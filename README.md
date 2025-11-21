# gm-credit-fund-risk-model
CFRM to evaluate under-capitalized startups for G&M

## Description
The G&M Credit Fund Risk Model (CFRM) is a machine learning project designed to evaluate early-stage, under-capitalized startups in the U.S., which currently receive less than 2% of venture capital. Investors face high uncertainty when funding these teams, as returns are not guaranteed within a given timeframe. This project seeks to address two core questions: can we estimate the risk of investment in a startup, and can we design a set of risk profiles.

## Dependencies
pip install -r requirements.txt

## Data Handling/Storage
### data folder
The raw data should be kept in the data folder underneath the name 'companies.csv'

Download [https://www.kaggle.com/datasets/amirataha/startups]

### processed_data folder
All notebooks are set to save and retrive any processed data from this directory.

## Pipeline
1. CFRM.ipynb - Initial exploration of the data
    > File Inputs: companies.csv
2. data_cleaning.ipynb - Target variables and data cleaning
    > File Inputs: companies.csv
    > File Outputs: companies_optimized_targets.csv, companies_cleaned_data.csv
3. feature_engineering.ipynb - Creates and alters features
    > File Input: companies_cleaned_data.csv
    > File Output: companies_feature_engineering.csv
4. eda.ipynb - Analyzes and explores new features
    > File Input: companies_feature_engineering.csv
4. EDA_visualizations.ipynb - Creates visualizations and reports
    > File Input: companies_feature_engineering.csv

## Streamlit Dashboard
To run the dashboard locally, from the project root run the following:
    streamlit run streamlit/app.py

## Contributors
Aanya Bhandari, Emily Jiang, Fikreab Mezgebu, Casey Chin
