import streamlit as st
import pandas as pd
from utils import *

st.write("# Overview Page")

st.write("Welcome to the Overview page of the GM Credit Fund Risk Model application.")

df = load_data('./data/companies.csv')
clean_df = load_data('./processed_data/companies_cleaned_data.csv')

st.write(df)
st.write(clean_df)

