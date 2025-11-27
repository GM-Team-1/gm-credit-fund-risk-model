import streamlit as st
from utils import *
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.title("Risk Score Visualizations")

st.divider()

# Create interactive risk score displays by startup
st.write("## Individual Startup Risk Profiles")
risk_cols = ['failure_risk', 'risk_tier', 'risk_tier_label', 
             'country_risk_mean', 'country_risk_confidence', 
             'industry_risk_mean', 'industry_risk_confidence',
             'stage_risk_mean', 'geo_industry_risk', 
             'experience_risk_score', 
             'risk_vs_country_peers', 'risk_vs_industry_peers',
             'risk_vs_stage_peers', 'progression_risk_score']

numerical_risk_cols = ['failure_risk', 'risk_tier','country_risk_mean', 
                       'industry_risk_mean', 'stage_risk_mean', 'geo_industry_risk', 
                       'experience_risk_score', 'risk_vs_country_peers', 
                       'risk_vs_industry_peers', 'risk_vs_stage_peers', 'progression_risk_score']

df = load_and_cache_data('./processed_data/companies_feature_engineering.csv')

startups = df['name'].unique()
selected_startup = st.selectbox("Select a Company", startups)
startup_data = df[df['name'] == selected_startup]
st.write(f"Risk Profile for {selected_startup}")
st.dataframe(startup_data[['name'] + risk_cols])
fig, ax = plt.subplots()
ax.bar(numerical_risk_cols, startup_data[numerical_risk_cols].iloc[0])
ax.set_ylabel('Risk Score')
ax.set_title(f'Numerical Risk Scores for {selected_startup}')
ax.set_xticklabels(numerical_risk_cols, rotation=45, ha='right')
st.pyplot(fig)

st.divider()


# Implement risk distribution visualizations across portfolios

st.write("## Risk Score Distributions Across All Startups")

industries = df['category_code_clean'].unique()
    
selected_industry = st.selectbox("Select Industry for Distribution",industries)
selected_risk_score = st.selectbox("Select Risk Score to Display", numerical_risk_cols)
industry_data = df[df['category_code_clean'] == selected_industry]

# Create hover data based on selected risk score
hover_column = None
if 'stage' in selected_risk_score.lower():
    hover_column = 'funding_stage_clean'
elif 'country' in selected_risk_score.lower():
    hover_column = 'country_code'
elif 'industry' in selected_risk_score.lower():
    hover_column = 'category_code_clean'
else:
    hover_column = 'name'

# Create tabs for different visualization types
tab1, tab2 = st.tabs(["Histogram View", "Individual Points View"])

with tab1:
    # Traditional histogram
    fig2 = px.histogram(industry_data, x=selected_risk_score, 
                       nbins=20, 
                       title=f'{selected_risk_score.replace("_", " ").title()} Distribution for {selected_industry} Industry',
                       labels={selected_risk_score: selected_risk_score.replace('_', ' ').title()})
    fig2.update_layout(xaxis_title=selected_risk_score.replace('_', ' ').title(), 
                       yaxis_title='Number of Startups')
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    # Scatter plot with jitter to show individual points
    import numpy as np
    
    # Add jitter to y-axis for better visibility
    np.random.seed(42)  # For reproducible results
    jitter_y = np.random.normal(0, 0.1, len(industry_data))
    
    fig3 = px.scatter(industry_data, 
                     x=selected_risk_score, 
                     y=jitter_y,
                     hover_data=[hover_column, 'name'],
                     title=f'Individual {selected_risk_score.replace("_", " ").title()} Values for {selected_industry} Industry',
                     labels={selected_risk_score: selected_risk_score.replace('_', ' ').title()})
    
    # Customize the scatter plot
    fig3.update_traces(marker=dict(size=8, opacity=0.7))
    fig3.update_layout(
        xaxis_title=selected_risk_score.replace('_', ' ').title(), 
        yaxis_title='Individual Data Points (jittered for visibility)',
        yaxis=dict(showticklabels=False),  # Hide y-axis labels since jitter is artificial
        height=400
    )
    st.plotly_chart(fig3, use_container_width=True)

st.divider()


# Build risk factor contribution analysis charts
st.write("## Risk Factor Contribution Analysis")

risk_factors = ['country_risk_mean', 'industry_risk_mean', 'stage_risk_mean', 'experience_risk_score', 
                'risk_vs_country_peers', 'risk_vs_industry_peers', 'risk_vs_stage_peers', 'progression_risk_score']
selected_risk_factor = st.selectbox("Select Risk Factor for Contribution Analysis", risk_factors)
fig3, ax3 = plt.subplots()
ax3.boxplot([df[selected_risk_factor][df['risk_tier'] == i] for i in range(1,6)], labels=[1,2,3,4,5])
ax3.set_xlabel('Risk Tier')
ax3.set_ylabel(f'{selected_risk_factor} Score')
ax3.set_title(f'{selected_risk_factor} Contribution by Risk Tier')
st.pyplot(fig3)

st.divider()


# Add real-time risk assessment tools for individual companies

st.write("## Real-Time Risk Assessment Tool")

selected_company = st.selectbox("Select a Company:", df['name'].unique())


st.write(f"### Risk Profile for {selected_company}")

