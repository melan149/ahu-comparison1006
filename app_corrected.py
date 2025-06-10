
import streamlit as st
import pandas as pd

# Load data from a file or GitHub URL
@st.cache_data
def load_data():
    # Replace with the raw GitHub link if hosted on GitHub
    # Example: url = "https://raw.githubusercontent.com/user/repo/branch/Data_2025.xlsx"
    url = "Data_2025.xlsx"
    df = pd.read_excel(url, sheet_name="data")
    return df

df = load_data()

# Debug: show all column names to identify issues
st.write("Available columns:", df.columns.tolist())

# Column fallback handling
def get_column_safe(df, name_options):
    for name in name_options:
        if name in df.columns:
            return name
    return None

# Resolve potential column naming issues
unit_name_col = get_column_safe(df, ["Unit name"])
region_col = get_column_safe(df, ["Region"])
year_col = get_column_safe(df, ["Year"])
quarter_col = get_column_safe(df, ["Quarter"])
recovery_col = get_column_safe(df, ["Recovery type", "Recovery Type", "Recovery_type"])
size_col = get_column_safe(df, ["Unit size", "Unit Size"])

# Sidebar Filters
st.sidebar.title("Filter Options")
unit_names = df[unit_name_col].dropna().unique()
regions = df[region_col].dropna().unique()
years = df[year_col].dropna().unique()
quarters = df[quarter_col].dropna().unique()
recovery_types = df[recovery_col].dropna().unique()
unit_sizes = df[size_col].dropna().unique()

selected_unit = st.sidebar.selectbox("Unit name", sorted(unit_names))
selected_region = st.sidebar.selectbox("Region", sorted(regions))
selected_year = st.sidebar.selectbox("Year", sorted(years))
selected_quarter = st.sidebar.selectbox("Quarter", sorted(quarters))
selected_recovery = st.sidebar.selectbox("Recovery type", sorted(recovery_types))
selected_size = st.sidebar.selectbox("Unit size", sorted(unit_sizes))

# Filter Data
filtered_df = df[
    (df[unit_name_col] == selected_unit) &
    (df[region_col] == selected_region) &
    (df[year_col] == selected_year) &
    (df[quarter_col] == selected_quarter) &
    (df[recovery_col] == selected_recovery) &
    (df[size_col] == selected_size)
]

# Display Comparison
st.title("Technical Data Comparison")
brand_col = get_column_safe(df, ["Brand name", "Brand"])
brands = filtered_df[brand_col].dropna().unique()

if len(brands) >= 2:
    brand1, brand2 = brands[:2]
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{brand1}")
        st.dataframe(filtered_df[filtered_df[brand_col] == brand1].reset_index(drop=True))

    with col2:
        st.subheader(f"{brand2}")
        st.dataframe(filtered_df[filtered_df[brand_col] == brand2].reset_index(drop=True))

elif len(brands) == 1:
    st.subheader(f"{brands[0]}")
    st.dataframe(filtered_df.reset_index(drop=True))
else:
    st.warning("No matching data found. Adjust filter criteria.")
