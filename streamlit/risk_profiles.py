import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import streamlit as st

def run(st, data_store, ctx):
    st.title("Risk Profiles & Personas")
    st.markdown("Visualizing risk clusters and personas.")

    cluster_df = data_store.get("cluster_validation_dataset", pd.DataFrame())
    st.write(f"Rows in cluster dataset: {len(cluster_df)}")

    if cluster_df.empty or "cluster_label" not in cluster_df.columns:
        st.info("Using demo data because cluster dataset is empty or missing 'cluster_label'.")
        np.random.seed(42)
        cluster_df = pd.DataFrame({
            "cluster_label": np.random.choice([0,1,2], size=20),
            "feature1": np.random.rand(20)*10,
            "feature2": np.random.rand(20)*5
        })

    counts = cluster_df["cluster_label"].value_counts().reset_index()
    counts.columns = ["cluster", "count"]
    st.subheader("Cluster distribution")
    st.plotly_chart(px.bar(counts, x="cluster", y="count", title="Cluster sizes"))

    numeric_cols = cluster_df.select_dtypes(include="number").columns.tolist()
    numeric_cols = [c for c in numeric_cols if c != "cluster_label"]
    if len(numeric_cols) >= 2:
        scaler = StandardScaler()
        scaled = scaler.fit_transform(cluster_df[numeric_cols])
        pca = PCA(n_components=2)
        proj = pca.fit_transform(scaled)
        proj_df = pd.DataFrame(proj, columns=["PCA1","PCA2"])
        proj_df["cluster_label"] = cluster_df["cluster_label"].values
        st.subheader("PCA projection")
        st.plotly_chart(px.scatter(proj_df, x="PCA1", y="PCA2", color="cluster_label"))
    else:
        st.info("Not enough numeric columns for PCA visualization.")
