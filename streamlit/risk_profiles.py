# streamlit/risk_profiles.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def run(st, data_store, ctx):
    st.markdown("<h1 style='text-align:center; color:#1f77b4;'>Risk Profiles & Personas</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#555;'>Explore client risk clusters and visualize personas with PCA projections</h3>", unsafe_allow_html=True)
    st.markdown("---")

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
    counts.columns = ["cluster","count"]
    st.subheader("Cluster Distribution")
    st.plotly_chart(px.bar(counts, x="cluster", y="count", title="Cluster Sizes"))

    numeric_cols = [c for c in cluster_df.select_dtypes(include="number").columns if c != "cluster_label"]

    if len(numeric_cols) >= 2:
        scaler = StandardScaler()
        scaled = scaler.fit_transform(cluster_df[numeric_cols])
        pca = PCA(n_components=2)
        proj = pca.fit_transform(scaled)
        proj_df = pd.DataFrame(proj, columns=["PCA1","PCA2"])
        proj_df["cluster_label"] = cluster_df["cluster_label"].values
        st.subheader("PCA Projection")
        st.plotly_chart(px.scatter(proj_df, x="PCA1", y="PCA2", color="cluster_label"))
    else:
        st.info("Not enough numeric columns for PCA visualization.")
