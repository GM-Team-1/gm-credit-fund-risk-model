import streamlit as st
from pathlib import Path
from utils import load_all_processed_data
import overview
import geographic
import risk_profiles
import recommendations

st.set_page_config(page_title="GM Credit Fund Risk Dashboard", layout="wide")

# Load CSVs from processed_data
BASE_DATA_DIR = Path(__file__).resolve().parents[1] / "processed_data"
data_store = load_all_processed_data(BASE_DATA_DIR)

PAGES = {
    "Overview": overview,
    "Geographic": geographic,
    "Risk Profiles": risk_profiles,
    "Recommendations": recommendations,
}

# Sidebar navigation
st.sidebar.title("GM Credit Fund")
st.sidebar.markdown("### Navigation")
page = st.sidebar.selectbox("Go to", list(PAGES.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("### Global controls")
year = st.sidebar.selectbox("Data year (if available)", ["All", "2023", "2024", "2025"], index=0)
st.sidebar.caption("Dataset-specific filters live in each page.")

# Run selected page
PAGES[page].run(st=st, data_store=data_store, ctx={"year": year})
