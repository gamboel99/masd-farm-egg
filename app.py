import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils import data_handler  # Modul untuk simpan & load data

# Konfigurasi halaman
st.set_page_config(page_title="Mas D Farm Egg", layout="wide")
st.title("🥚 Mas D Farm Egg - Sistem Pencatatan & Analisis")

# Sidebar Navigasi
menu = st.sidebar.radio("📌 Navigasi", ["Input Data", "Analisis & Laporan"])

# Pastikan folder data ada
if not os.path.exists("data"):
    os.makedirs("data")

# ============================
# BAGIAN INPUT DATA
# ============================
if menu == "Input Data":
    tab1, tab2, tab3, tab4 = st.tabs([
        "📥 Ayam Masuk",
        "🍽️ Pakan",
        "🥚 Produksi Telur",
        "💰 Penjualan Telur"
    ])

    with tab1:
        st.subheader("📥 Input Ayam Masuk")
        tanggal = st.date_input("Tanggal Masuk", value=datetime.today())
        jumlah_ayam = st.number_input("Jumlah Ayam", min_value=1, step=1)
        umur = st.number_input("Umur Ayam Saat Masuk (minggu)", min_value=1, step=1)
        if st.button("✅ Simpan Data Ayam"):
            data = {
                "Tanggal": tanggal,
                "Jumlah Ayam": jumlah_ayam,
                "Umur (minggu)": umur
            }
            data_handler.save_data("data/ayam.csv", data)
            st.success("✅ Data ayam berhasil disimpan.")

    with tab2:
        st.subheader("🍽️ Input Pakan Harian")
        tanggal = st.date_input("Tanggal Pemberian Pakan", value=datetime.today())
        jumlah_sak = st.number_input("Jumlah Sak", min_value=1, step=1)
        harga_per_sak = st.number_input("Harga per Sak (Rp)", min_value=0.0, step=500.0)
        if st.button("✅ Simpan Data Pakan"):
            data = {
                "Tanggal": tanggal,
                "Jumlah Sak": jumlah_sak,
                "Harga per Sak": harga_per_sak
            }
            data_handler.save_data("data/pakan.csv", data)
            st.success("✅ Data pakan berhasil disimpan.")

    with tab3:
        st.subheader("🥚 Input Produksi Telur")
        tanggal = st.date_input("Tanggal Produksi", value=datetime.today())
        jumlah_telur = st.number_input("Jumlah Telur (butir)", min_value=1, step=1)
        kualitas = st.selectbox("Kualitas Telur", ["Baik", "Retak", "Kecil"])
        if st.button("✅ Simpan Data Produksi"):
            data = {
                "Tanggal": tanggal,
                "Jumlah Telur": jumlah_telur,
                "Kualitas": kualitas
            }
            data_handler.save_data("data/produksi.csv", data)
            st.success("✅ Data produksi telur berhasil disimpan.")

    with tab4:
        st.subheader("💰 Input Penjualan Telur")
        tanggal = st.date_input("Tanggal Penjualan", value=datetime.today())
        jumlah_terjual = st.number_input("Jumlah Terjual (butir)", min_value=1, step=1)
        harga_jual = st.number_input("Harga Jual per Butir (Rp)", min_value=0.0, step=100.0)
        metode = st.selectbox("Metode Penjualan", ["Pasar", "Tengkulak", "Online"])
        if st.button("✅ Simpan Data Penjualan"):
            data = {
                "Tanggal": tanggal,
                "Jumlah Terjual": jumlah_terjual,
                "Harga Jual": harga_jual,
                "Metode": metode
            }
            data_handler.save_data("data/penjualan.csv", data)
            st.success("✅ Data penjualan berhasil disimpan.")

# ============================
# BAGIAN ANALISIS & LAPORAN (Placeholder)
# ============================
elif menu == "Analisis & Laporan":
    st.subheader("📊 Analisis & Laporan Keuangan")
    st.info("Fitur ini akan menampilkan ringkasan produksi, penggunaan pakan, pendapatan, serta estimasi Break Even Point (BEP). Akan dibuat setelah input data selesai.")
