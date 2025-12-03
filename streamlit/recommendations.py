# streamlit/recommendations.py
import streamlit as st
import pandas as pd

def run(st, data_store, ctx):
    st.markdown("<h1 style='text-align:center; color:#1f77b4;'>Recommendations</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#555;'>Suggested investments, industry undercap analysis, and sector opportunities</h3>", unsafe_allow_html=True)
    st.markdown("---")

    candidates = data_store.get("investment_candidates_analysis", pd.DataFrame())
    undercap = data_store.get("industry_undercap_analysis", pd.DataFrame())
    sector_matrix = data_store.get("sector_opportunity_matrix", pd.DataFrame())

    st.subheader("Investment Candidates")
    if not candidates.empty:
        st.dataframe(candidates.head(50))
    else:
        st.info("No investment candidate data available.")

    st.subheader("Undercap / Opportunity Summaries")
    if not undercap.empty:
        st.dataframe(undercap.head())
    else:
        st.info("No undercap data available.")

    st.subheader("Sector Opportunity Matrix")
    if not sector_matrix.empty:
        st.dataframe(sector_matrix.head())
    else:
        st.info("No sector opportunity data available.")
