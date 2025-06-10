
import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    url = "Data_2025.xlsx"
    return pd.read_excel(url, sheet_name="data")

df = load_data()

# Resolve potential column naming issues
def get_column_safe(df, name_options):
    for name in name_options:
        if name in df.columns:
            return name
    return None

unit_name_col = get_column_safe(df, ["Unit name"])
region_col = get_column_safe(df, ["Region"])
year_col = get_column_safe(df, ["Year"])
quarter_col = get_column_safe(df, ["Quarter"])
recovery_col = get_column_safe(df, ["Recovery type", "Recovery Type", "Recovery_type"])
size_col = get_column_safe(df, ["Unit size", "Unit Size"])
brand_col = get_column_safe(df, ["Brand name", "Brand"])

# Main layout filters
st.title("Technical Data Comparison")

col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    selected_unit = st.selectbox("Unit name", sorted(df[unit_name_col].dropna().unique()))
    selected_region = st.selectbox("Region", sorted(df[region_col].dropna().unique()))
    selected_year = st.selectbox("Year", sorted(df[year_col].dropna().unique()))

with col_filter2:
    selected_quarter = st.selectbox("Quarter", sorted(df[quarter_col].dropna().unique()))
    selected_recovery = st.selectbox("Recovery type", sorted(df[recovery_col].dropna().unique()))
    selected_size = st.selectbox("Unit size", sorted(df[size_col].dropna().unique()))

# Filter data
filtered_df = df[
    (df[unit_name_col] == selected_unit) &
    (df[region_col] == selected_region) &
    (df[year_col] == selected_year) &
    (df[quarter_col] == selected_quarter) &
    (df[recovery_col] == selected_recovery) &
    (df[size_col] == selected_size)
]

# Brand selection
brands = filtered_df[brand_col].dropna().unique()
if len(brands) < 2:
    st.warning("Not enough brands to compare. Adjust filters.")
else:
    brand1 = st.selectbox("Select Brand 1", brands, index=0)
    brand2 = st.selectbox("Select Brand 2", brands, index=1 if len(brands) > 1 else 0)

    df1 = filtered_df[filtered_df[brand_col] == brand1].reset_index(drop=True)
    df2 = filtered_df[filtered_df[brand_col] == brand2].reset_index(drop=True)

    if not df1.empty and not df2.empty:
        st.subheader("Comparison Table")
        col1, col2, col3 = st.columns([2, 3, 3])
        with col1:
            st.markdown("**Parameter**")
        with col2:
            st.markdown(f"**{brand1}**")
        with col3:
            st.markdown(f"**{brand2}**")

        for col in filtered_df.columns:
            if col not in [brand_col]:
                val1 = df1.at[0, col] if col in df1.columns else "-"
                val2 = df2.at[0, col] if col in df2.columns else "-"
                col1, col2, col3 = st.columns([2, 3, 3])
                with col1:
                    st.write(col)
                with col2:
                    st.write(val1)
                with col3:
                    st.write(val2)
    else:
        st.warning("One of the selected brands has no data.")
