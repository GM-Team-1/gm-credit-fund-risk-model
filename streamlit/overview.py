# streamlit/overview.py
import streamlit as st
from utils import sample_or_head

def run(st, data_store, ctx):
    # Page title
    st.markdown("<h1 style='text-align:center; color:#1f77b4;'>GM Credit Fund Risk Model Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#555;'>Overview: Explore datasets and key metrics at a glance</h3>", unsafe_allow_html=True)
    st.markdown("---")

    dataset_names = sorted(list(data_store.keys()))
    sel = st.selectbox("Select dataset to preview", ["-- select --"] + dataset_names)

    if sel and sel != "-- select --":
        df = data_store.get(sel)
        if df is None or df.empty:
            st.error(f"No data loaded for `{sel}`.")
            return

        st.subheader(f"Preview — `{sel}` ({df.shape[0]} rows × {df.shape[1]} columns)")
        st.dataframe(sample_or_head(df, n=10))

        with st.expander("Show full columns"):
            st.write(list(df.columns))

        st.markdown("### Dataset Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        col3.metric("Numeric Columns", len(numeric_cols))

        if numeric_cols:
            st.markdown("#### Sample Statistics (Numeric Columns)")
            st.dataframe(df[numeric_cols].describe().T.style.format("{:.3f}"))
    else:
        st.info("Select a dataset from the dropdown to preview it.")
