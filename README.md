# GM Credit Fund Risk Model (CFRM)
A machine learning model to evaluate investment risk in under-capitalized early-stage startups for G&M.

## Description
The G&M Credit Fund Risk Model (CFRM) is a machine learning project designed to evaluate early-stage, under-capitalized startups in the U.S., which currently receive less than 2% of venture capital. Investors face high uncertainty when funding these teams, as returns are not guaranteed within a given timeframe. This project seeks to address two core questions: can we estimate the risk of investment in a startup, and can we design a set of risk profiles.

This project addresses two core questions:
1. Can we estimate the risk of investing in a startup?
2. Can we design a set of predictive risk profiles for these startups?

CRFM aims to:
1. Quantitatively estimate the risk associated with investing in a startup.
2. Generate predictive risk profiles to guide investment decisions for early-stage companies.

## Dependencies
Install the required Python packages:

```pip install -r requirements.txt```

## Data Handling
Raw data should be stored in the ```data``` folder under the filename ```companies.csv```.

## Storage
All notebooks save and retrieve processed data from the ```processed_data``` folder.

## Data Source
You can download the dataset here: 

https://www.kaggle.com/datasets/amirataha/startups

## Pipeline
1. CFRM.ipynb - Performs initial exploration and analysis of the raw dataset.
    > File Inputs: companies.csv
2. data_cleaning.ipynb - Defines target variables, handles missing values, and cleans the dataset.
    > File Inputs: companies.csv
    > 
    > File Outputs: companies_optimized_targets.csv, companies_cleaned_data.csv
3. feature_engineering.ipynb - Creates and transforms features for modeling.
    > File Input: companies_cleaned_data.csv
    > 
    > File Output: companies_feature_engineering.csv
4. eda.ipynb - Performs exploratory data analysis on the engineered features to identify patterns and insights.
    > File Input: companies_feature_engineering.csv
4. EDA_visualizations.ipynb - Generates visualizations and summary reports for the engineered dataset.
    > File Input: companies_feature_engineering.csv

## Dashboard
To launch the interactive dashboard locally, navigate to the project root and run:

```streamlit run streamlit/app.py```

## Contributors
Aanya Bhandari
Casey Chin
Emily Jiang
Fikreab Mezgebu
