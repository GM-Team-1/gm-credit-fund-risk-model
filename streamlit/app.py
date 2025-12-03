# streamlit/app.py
import streamlit as st
from utils import load_all_processed_data

# Load all CSVs
data_store = load_all_processed_data("processed_data")

from overview import run as overview_run
from geographic import run as geographic_run
from risk_profiles import run as risk_profiles_run
from recommendations import run as recommendations_run

# Wrap pages for Streamlit Navigation
pages = [
    st.Page(
        page=lambda: overview_run(st, data_store, st.runtime.scriptrunner.get_script_run_ctx()),
        url_path="overview",
        title="Overview"
    ),
    st.Page(
        page=lambda: geographic_run(st, data_store, st.runtime.scriptrunner.get_script_run_ctx()),
        url_path="geographic",
        title="Geographic"
    ),
    st.Page(
        page=lambda: risk_profiles_run(st, data_store, st.runtime.scriptrunner.get_script_run_ctx()),
        url_path="risk_profiles",
        title="Risk Profiles"
    ),
    st.Page(
        page=lambda: recommendations_run(st, data_store, st.runtime.scriptrunner.get_script_run_ctx()),
        url_path="recommendations",
        title="Recommendations"
    ),
]

pg = st.navigation(pages)
pg.run()
