import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. TITLE
st.title("Dashboard Analisis Data Penjualan 2024")

# 2. HEADER
st.header("Selamat Datang di Dashboard Interaktif")

# 3. SUBHEADER
st.subheader("Visualisasi Data dan Statistik Penjualan")

# 4. CAPTION
st.caption("Dashboard ini menampilkan data penjualan produk selama tahun 2024")

# 5. TEXT > Paragraf penjelasan
st.text("""
Dashboard ini dirancang untuk membantu tim sales dan manajemen
dalam memantau performa penjualan secara real-time.
Data diperbarui setiap hari untuk memberikan insight terkini.
""")

# Menambahkan paragraf dengan markdown untuk formatting lebih baik
st.markdown("""
### Tentang Dashboard
Dashboard ini menyediakan berbagai fitur analisis termasuk:
- Tabel data penjualan detail
- Visualisasi chart interaktif
- Statistik dan metrik penting
""")

# 6. CODE > Menampilkan potongan kode
st.subheader("Contoh Kode Python untuk Analisis Data")
code = '''
# Membaca data dari CSV
df = pd.read_csv('data_penjualan.csv')

# Menghitung total penjualan
total = df['Jumlah'].sum()

# Membuat visualisasi
df.plot(kind='bar', x='Produk', y='Jumlah')
'''
st.code(code, language='python')

# Membuat data sample untuk demonstrasi
st.header("Data Display")

# 7.1 TABEL / DATAFRAME
st.subheader("A. Tabel Data Penjualan")

# Membuat sample data
data = {
    'Produk': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headset'],
    'Kategori': ['Elektronik', 'Aksesoris', 'Aksesoris', 'Elektronik', 'Aksesoris'],
    'Jumlah Terjual': [150, 450, 380, 200, 290],
    'Harga (Rp)': [8500000, 150000, 350000, 2500000, 450000],
    'Revenue (Rp)': [1275000000, 67500000, 133000000, 500000000, 130500000]
}

df = pd.DataFrame(data)

# Menampilkan dataframe dengan styling
st.dataframe(df, use_container_width=True)

# Menampilkan metrik
col1, col2, col3 = st.columns(3)
col1.metric("Total Produk Terjual", f"{df['Jumlah Terjual'].sum():,}", "↑ 12%")
col2.metric("Total Revenue", f"Rp {df['Revenue (Rp)'].sum():,.0f}", "↑ 8%")
col3.metric("Rata-rata Harga", f"Rp {df['Harga (Rp)'].mean():,.0f}", "↓ 2%")

# 7.2 CHART
st.subheader("B. Visualisasi Data dengan Chart")

# Chart 1: Bar Chart
st.write("**1. Grafik Jumlah Penjualan per Produk**")
st.bar_chart(df.set_index('Produk')['Jumlah Terjual'])

# Chart 2: Line Chart - Data time series
st.write("**2. Trend Penjualan Bulanan**")
date_range = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')
trend_data = pd.DataFrame({
    'Bulan': date_range,
    'Penjualan': np.random.randint(800, 1500, size=len(date_range))
})
st.line_chart(trend_data.set_index('Bulan'))

# Chart 3: Area Chart
st.write("**3. Area Chart - Perbandingan Kategori**")
category_data = pd.DataFrame({
    'Elektronik': np.random.randint(100, 300, size=10),
    'Aksesoris': np.random.randint(200, 400, size=10)
})
st.area_chart(category_data)

# Footer
st.markdown("---")
st.caption("© 2024 Dashboard Analytics | Data diperbarui terakhir: 29 Desember 2024")