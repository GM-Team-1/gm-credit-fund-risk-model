# utils.py
import pandas as pd
from pathlib import Path
import streamlit as st
import glob
from typing import Dict, List

@st.cache_data
def load_csv_safe(path: Path) -> pd.DataFrame:
    """Safely load a CSV file into a DataFrame. Returns empty DataFrame on failure."""
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.warning(f"Failed to load {path}: {e}")
        return pd.DataFrame()

def list_csv_files(base_dir: Path) -> List[str]:
    """Return a sorted list of all CSV files in the given directory."""
    pattern = str(base_dir / "*.csv")
    return sorted(glob.glob(pattern))

@st.cache_data
def load_all_processed_data(base_dir: Path) -> Dict[str, pd.DataFrame]:
    """Load all CSVs in a directory into a dictionary keyed by filename stem."""
    base_dir = Path(base_dir)
    data: Dict[str, pd.DataFrame] = {}
    for csv_path in list_csv_files(base_dir):
        key = Path(csv_path).stem
        data[key] = load_csv_safe(csv_path)
    return data

def sample_or_head(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Return a sample of n rows if the DataFrame is large, otherwise return head."""
    if df is None or df.empty:
        return df
    if df.shape[0] <= n:
        return df
    return df.sample(n) if df.shape[0] >= 50 else df.head(n)
