import pandas as pd
from pathlib import Path
import streamlit as st
import glob
from typing import Dict

@st.cache_data
def load_csv_safe(path: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.warning(f"Failed to load {path}: {e}")
        return pd.DataFrame()

def list_csv_files(base_dir: Path):
    pattern = str(base_dir / "*.csv")
    return sorted(glob.glob(pattern))

@st.cache_data
def load_all_processed_data(base_dir: Path) -> Dict[str, pd.DataFrame]:
    base_dir = Path(base_dir)
    data = {}
    for p in list_csv_files(base_dir):
        key = Path(p).stem
        data[key] = load_csv_safe(p)
    return data

def sample_or_head(df, n=5):
    if df is None or df.empty:
        return df
    if df.shape[0] <= n:
        return df
    return df.sample(n) if df.shape[0] >= 50 else df.head(n)
