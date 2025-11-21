import streamlit as st
import pandas as pd

def load_data(url):
    df = pd.read_csv(url)
    return df

@st.cache_data
def load_and_cache_data(url):
    df = pd.read_csv(url)
    return df