import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# /C:/Users/emily/OneDrive/Documents/GitHub/gm-credit-fund-risk-model/notebooks/app.py
import plotly.express as px

st.set_page_config(page_title="Startup Risk Dashboard", layout="wide")

# --- Helpers -----------------------------------------------------------------
@st.cache_data
def generate_sample_data(n=100):
    rng = np.random.default_rng(42)
    sectors = ["Fintech", "Health", "SaaS", "Marketplace", "AI", "Climate"]
    stages = ["Pre-seed", "Seed", "Series A", "Series B", "Growth"]
    countries = ["US", "UK", "DE", "FR", "IN", "CN"]

    df = pd.DataFrame({
        "company": [f"Startup {i+1}" for i in range(n)],
        "sector": rng.choice(sectors, n),
        "stage": rng.choice(stages, n),
        "country": rng.choice(countries, n),
        "employees": rng.integers(1, 800, n),
        "revenue_musd": np.round(10 ** rng.uniform(-1, 2.5, n), 2),  # 0.1M - ~316M
        "founders": rng.integers(1, 5, n),
        "last_funding_musd": np.round(10 ** rng.uniform(-2, 2, n), 2)
    })
    return df

def compute_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    # Create a risk score 0-100 where higher = higher risk.
    # Use simple heuristics: low revenue, few employees, low founders, small funding => higher risk
    df = df.copy()
    for col in ["revenue_musd", "employees", "founders", "last_funding_musd"]:
        if col not in df.columns:
            df[col] = np.nan

    # transform and invert where needed
    rev = np.log1p(df["revenue_musd"])
    emp = np.log1p(df["employees"])
    fund = np.log1p(df["last_funding_musd"])
    founders = df["founders"].fillna(1)

    # Normalize each to 0-1
    def norm(x):
        if x.isna().all():
            return pd.Series(0.5, index=x.index)
        return (x - x.min()) / (x.max() - x.min() + 1e-9)

    rev_n = norm(rev)
    emp_n = norm(emp)
    fund_n = norm(fund)
    founders_n = norm(founders)

    # Combine: higher normalized values reduce risk
    score = 1.0 - (0.4 * rev_n + 0.35 * emp_n + 0.15 * fund_n + 0.1 * founders_n)
    df["risk_score"] = (score * 100).clip(0, 100).round(1)
    return df

def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

# --- UI ----------------------------------------------------------------------
st.title("Startup Risk Scores — Interactive Dashboard")

with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader("Upload CSV with startup metrics", type=["csv"])
    use_sample = st.button("Load sample dataset")

    st.markdown("---")
    st.header("Filters")

# Load data
if uploaded:
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        st.stop()
elif use_sample or uploaded is None:
    df = generate_sample_data(120)

# Ensure risk_score exists
if "risk_score" not in df.columns or df["risk_score"].isna().all():
    df = compute_risk_score(df)

# Sidebar filters (continued)
with st.sidebar:
    sectors = df["sector"].dropna().unique().tolist()
    stages = df["stage"].dropna().unique().tolist()
    countries = df["country"].dropna().unique().tolist()

    sel_sectors = st.multiselect("Sector", options=sorted(sectors), default=sorted(sectors))
    sel_stages = st.multiselect("Stage", options=sorted(stages), default=sorted(stages))
    sel_countries = st.multiselect("Country", options=sorted(countries), default=sorted(countries))

    min_risk, max_risk = float(df["risk_score"].min()), float(df["risk_score"].max())
    risk_range = st.slider("Risk score range", min_value=0.0, max_value=100.0,
                           value=(min_risk, max_risk), step=0.1)

    st.markdown("---")
    st.markdown("Export")
    st.download_button("Download filtered CSV", to_csv_bytes(df), file_name="startups.csv", mime="text/csv")

# Apply filters
filtered = df[
    df["sector"].isin(sel_sectors) &
    df["stage"].isin(sel_stages) &
    df["country"].isin(sel_countries) &
    df["risk_score"].between(risk_range[0], risk_range[1])
].copy()

# Layout: KPIs + charts + table
kpi1, kpi2, kpi3 = st.columns([1.5, 1, 1])

avg_risk = filtered["risk_score"].mean() if not filtered.empty else np.nan
count_startups = len(filtered)
median_rev = filtered["revenue_musd"].median() if "revenue_musd" in filtered.columns else np.nan

kpi1.metric("Average risk", f"{avg_risk:.1f}" if not np.isnan(avg_risk) else "N/A")
kpi2.metric("Startups shown", f"{count_startups}")
kpi3.metric("Median revenue (M USD)", f"{median_rev:.2f}" if not np.isnan(median_rev) else "N/A")

st.markdown("### Risk distribution")
col1, col2 = st.columns(2)

with col1:
    if not filtered.empty:
        fig_hist = px.histogram(filtered, x="risk_score", nbins=25, title="Risk score distribution",
                                labels={"risk_score": "Risk score"})
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("No data for histogram with current filters.")

with col2:
    if "sector" in filtered.columns and not filtered.empty:
        agg = filtered.groupby("sector")["risk_score"].mean().reset_index().sort_values("risk_score", ascending=False)
        fig_bar = px.bar(agg, x="risk_score", y="sector", orientation="h",
                         title="Average risk by sector", labels={"risk_score": "Avg risk", "sector": "Sector"},
                         color="risk_score", color_continuous_scale="RdYlGn_r")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No sector data to show.")

st.markdown("### Explore startups")
# Table with color by risk
if filtered.empty:
    st.warning("No startups match the selected filters.")
else:
    st.dataframe(filtered.sort_values("risk_score", ascending=False).reset_index(drop=True), use_container_width=True)

    # Select a company for details
    company_list = filtered["company"].tolist()
    sel_company = st.selectbox("Select a company to inspect", options=["None"] + company_list)
    if sel_company and sel_company != "None":
        row = filtered[filtered["company"] == sel_company].iloc[0]
        st.subheader(f"{row['company']}")
        cols = st.columns(2)
        with cols[0]:
            st.write("Sector:", row.get("sector", ""))
            st.write("Stage:", row.get("stage", ""))
            st.write("Country:", row.get("country", ""))
            st.write("Employees:", int(row.get("employees", 0)))
        with cols[1]:
            st.write("Revenue (M USD):", row.get("revenue_musd", ""))
            st.write("Last funding (M USD):", row.get("last_funding_musd", ""))
            st.write("Founders:", int(row.get("founders", 0)))
            st.write("Risk score:", row.get("risk_score", ""))

    # Scatter plot revenue vs risk
    if "revenue_musd" in filtered.columns:
        fig_scat = px.scatter(filtered, x="revenue_musd", y="risk_score", color="sector",
                              size="employees" if "employees" in filtered.columns else None,
                              hover_data=["company", "stage", "country"],
                              title="Revenue vs Risk (size = employees)", labels={"revenue_musd": "Revenue (M USD)"})
        st.plotly_chart(fig_scat, use_container_width=True)