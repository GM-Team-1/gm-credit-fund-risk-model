# recommendations.py
import streamlit as st
import pandas as pd  # <- add this line

def run(st, data_store, ctx):
    st.title("Recommendations")
    st.markdown("Investment candidates, undercap analysis, and sector opportunities.")

    candidates = data_store.get("investment_candidates_analysis", pd.DataFrame())
    undercap = data_store.get("industry_undercap_analysis", pd.DataFrame())
    sector_matrix = data_store.get("sector_opportunity_matrix", pd.DataFrame())

    st.subheader("Investment candidates")
    if not candidates.empty:
        st.dataframe(candidates.head(50))
    else:
        st.info("No investment candidate data available.")

    st.subheader("Undercap / Opportunity summaries")
    if not undercap.empty:
        st.dataframe(undercap.head())
    else:
        st.info("No undercap data available.")

    st.subheader("Sector opportunity matrix")
    if not sector_matrix.empty:
        st.dataframe(sector_matrix.head())
    else:
        st.info("No sector opportunity data available.")
