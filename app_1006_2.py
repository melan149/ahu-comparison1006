
import streamlit as st
import pandas as pd
from PIL import Image

# Load data
@st.cache_data
def load_data():
    url = "Data_2025.xlsx"
    return pd.read_excel(url, sheet_name="data", engine='openpyxl')

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
logo_col = get_column_safe(df, ["Brand logo", "Brand Logo"])

# Main layout filters
st.title("Technical Data Comparison")

col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    selected_year1 = st.selectbox("Year", sorted(df[year_col].dropna().unique()), key="year1")
    selected_quarter1 = st.selectbox("Quarter", sorted(df[quarter_col].dropna().unique()), key="quarter1")
    selected_region1 = st.selectbox("Region", sorted(df[region_col].dropna().unique()), key="region1")
    selected_brand1 = st.selectbox("Select Brand", sorted(df[brand_col].dropna().unique()), key="brand1")
    selected_unit1 = st.selectbox("Unit name", sorted(df[unit_name_col].dropna().unique()), key="unit1")
    selected_recovery1 = st.selectbox("Recovery type", sorted(df[recovery_col].dropna().unique()), key="recovery1")
    selected_size1 = st.selectbox("Unit size", sorted(df[size_col].dropna().unique()), key="size1")

with col_filter2:
    selected_year2 = st.selectbox("Year", sorted(df[year_col].dropna().unique()), key="year2")
    selected_quarter2 = st.selectbox("Quarter", sorted(df[quarter_col].dropna().unique()), key="quarter2")
    selected_region2 = st.selectbox("Region", sorted(df[region_col].dropna().unique()), key="region2")
    selected_brand2 = st.selectbox("Select Brand", sorted(df[brand_col].dropna().unique()), key="brand2")
    selected_unit2 = st.selectbox("Unit name", sorted(df[unit_name_col].dropna().unique()), key="unit2")
    selected_recovery2 = st.selectbox("Recovery type", sorted(df[recovery_col].dropna().unique()), key="recovery2")
    selected_size2 = st.selectbox("Unit size", sorted(df[size_col].dropna().unique()), key="size2")

# Filter data for both brands
filtered_df1 = df[
    (df[year_col] == selected_year1) &
    (df[quarter_col] == selected_quarter1) &
    (df[region_col] == selected_region1) &
    (df[brand_col] == selected_brand1) &
    (df[unit_name_col] == selected_unit1) &
    (df[recovery_col] == selected_recovery1) &
    (df[size_col] == selected_size1)
]

filtered_df2 = df[
    (df[year_col] == selected_year2) &
    (df[quarter_col] == selected_quarter2) &
    (df[region_col] == selected_region2) &
    (df[brand_col] == selected_brand2) &
    (df[unit_name_col] == selected_unit2) &
    (df[recovery_col] == selected_recovery2) &
    (df[size_col] == selected_size2)
]

# Display comparison
if not filtered_df1.empty and not filtered_df2.empty:
    st.subheader("Comparison Table")
    col1, col2, col3 = st.columns([2, 3, 3])
    with col1:
        st.markdown("**Parameter**")
    with col2:
        st.markdown(f"**{selected_brand1}**")
    with col3:
        st.markdown(f"**{selected_brand2}**")

    for col in df.columns:
        if col not in [brand_col, logo_col]:
            val1 = filtered_df1[col].values[0] if col in filtered_df1.columns else "-"
            val2 = filtered_df2[col].values[0] if col in filtered_df2.columns else "-"
            col1, col2, col3 = st.columns([2, 3, 3])
            with col1:
                st.write(col)
            with col2:
                st.write(val1)
            with col3:
                st.write(val2)

    # Display brand logos
    logo1 = filtered_df1[logo_col].values[0] if logo_col in filtered_df1.columns else None
    logo2 = filtered_df2[logo_col].values[0] if logo_col in filtered_df2.columns else None

    if logo1:
        image1 = Image.open(f"images/{logo1}")
        image1 = image1.resize((int(5 * 37.7952755906), int(image1.height * (5 * 37.7952755906) / image1.width)))
        col2.image(image1)

    if logo2:
        image2 = Image.open(f"images/{logo2}")
        image2 = image2.resize((int(5 * 37.7952755906), int(image2.height * (5 * 37.7952755906) / image2.width)))
        col3.image(image2)
else:
    st.warning("One of the selected brands has no data.")
