import streamlit as st
import pandas as pd
import plotly.express as px
st.title("Customer Analytics Dashboard")
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "customers.csv")

df = pd.read_csv(csv_path)
st.sidebar.header("Filter Data")
departments = st.sidebar.multiselect(
    "Pilih Departments",
    df["Department"].dropna().unique()
)
genders = st.sidebar.multiselect(
    "Pilih Gender",
    df["Gender"].dropna().unique()
)
st.sidebar.header("Filter Rentang Umur")
min_usia, max_usia = int(df["Age"].min()), int(df["Age"].max())
usia_range = st.sidebar.slider(
    "Usia",
    min_value=min_usia,
    max_value=max_usia,
    value=(min_usia, max_usia)
)
df_filtered = df[
    (df["Department"].isin(departments)) &
    (df["Gender"].isin(genders)) &
    (df["Age"].between(usia_range[0], usia_range[1]))
]
st.subheader("Data Tabel")
st.dataframe(df_filtered)
st.subheader("Visualisasi Statistik")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Distribusi Gender")
    pie_gender = px.pie(
        df_filtered,
        names="Gender",
        color="Gender",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(pie_gender)
with col2:
    st.subheader("Gaji Rata-rata per Department")

    salary_dept = (
        df_filtered
        .groupby("Department")["AnnualSalary"]
        .mean()
        .reset_index()
    )

    bar_salary = px.bar(
        salary_dept,
        x="Department",
        y="AnnualSalary",
        color="Department",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(bar_salary)

st.subheader("Rata-rata Gaji Berdasarkan Usia")
salary_age = (
    df_filtered
    .groupby("Age")["AnnualSalary"]
    .mean()
    .reset_index()
    .sort_values("Age")
)

line_age = px.line(
    salary_age,
    x="Age",
    y="AnnualSalary",
    markers=True
)

st.plotly_chart(line_age)

st.subheader("Tambahakn Chart Lainnya Versi Anda Sendiri!")
st.write("Untuk menambahkan chart lihat dan pahami struktur tabel data set file customers.csv")

st.subheader("Distribusi Jumlah Karyawan per Department")

count_dept = (
    df_filtered
    .groupby("Department")
    .size()
    .reset_index(name="Jumlah Karyawan")
)

bar_count = px.bar(
    count_dept,
    x="Department",
    y="Jumlah Karyawan",
    color="Department"
)

st.plotly_chart(bar_count, use_container_width=True)