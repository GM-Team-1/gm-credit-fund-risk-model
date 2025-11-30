from utils import sample_or_head
import streamlit as st

def run(st, data_store, ctx):
    st.title("Overview")
    st.markdown("Welcome to the GM Credit Fund Risk Model dashboard — Overview page.")

    dataset_names = sorted(list(data_store.keys()))
    sel = st.selectbox("Select dataset to preview", ["-- select --"] + dataset_names)

    if sel and sel != "-- select --":
        df = data_store.get(sel)
        if df is None or df.empty:
            st.error(f"No data loaded for {sel}.")
            return

        st.subheader(f"Preview — `{sel}` ({df.shape[0]} rows × {df.shape[1]} cols)")
        st.dataframe(sample_or_head(df, n=10))

        with st.expander("Show full columns"):
            st.write(list(df.columns))

        st.markdown("### Basic summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        col3.metric("Numeric cols", len(numeric_cols))

        if numeric_cols:
            st.markdown("#### Numeric column sample statistics")
            st.dataframe(df[numeric_cols].describe().T.style.format("{:.3f}"))
    else:
        st.info("Select a dataset from the dropdown to preview it.")
