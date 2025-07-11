import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Import aman: coba dari utils, kalau gagal langsung
try:
    from utils import data_handler
except Exception:
    import sys
    sys.path.append("utils")
    import data_handler

st.set_page_config(page_title="Mas D Farm Egg", layout="wide")
st.title("🥚 Mas D Farm Egg - Sistem Pencatatan & Analisis")

menu = st.sidebar.radio("📌 Navigasi", ["Input Data", "Analisis & Laporan"])

if not os.path.exists("data"):
    os.makedirs("data")

if menu == "Input Data":
    tab1, tab2, tab3, tab4 = st.tabs([
        "📥 Ayam Masuk", "🍽️ Pakan", "🥚 Produksi Telur", "💰 Penjualan Telur"
    ])

    with tab1:
        st.subheader("📥 Input Ayam Masuk")
        tanggal = st.date_input("Tanggal Masuk", value=datetime.today())
        jumlah_ayam = st.number_input("Jumlah Ayam", min_value=1, step=1)
        umur = st.number_input("Umur Ayam (minggu)", min_value=1, step=1)
        if st.button("✅ Simpan Data Ayam"):
            data = {"Tanggal": tanggal, "Jumlah Ayam": jumlah_ayam, "Umur (minggu)": umur}
            data_handler.save_data("data/ayam.csv", data)
            st.success("✅ Data ayam berhasil disimpan.")

    with tab2:
        st.subheader("🍽️ Input Pakan")
        tanggal = st.date_input("Tanggal Pakan", value=datetime.today())
        jumlah = st.number_input("Jumlah Sak", min_value=1, step=1)
        harga = st.number_input("Harga per Sak (Rp)", min_value=0.0, step=500.0)
        if st.button("✅ Simpan Data Pakan"):
            data = {"Tanggal": tanggal, "Jumlah Sak": jumlah, "Harga per Sak": harga}
            data_handler.save_data("data/pakan.csv", data)
            st.success("✅ Data pakan berhasil disimpan.")

    with tab3:
        st.subheader("🥚 Input Produksi Telur")
        tanggal = st.date_input("Tanggal Produksi", value=datetime.today())
        jumlah = st.number_input("Jumlah Telur", min_value=1, step=1)
        kualitas = st.selectbox("Kualitas", ["Baik", "Retak", "Kecil"])
        if st.button("✅ Simpan Data Produksi"):
            data = {"Tanggal": tanggal, "Jumlah Telur": jumlah, "Kualitas": kualitas}
            data_handler.save_data("data/produksi.csv", data)
            st.success("✅ Data produksi telur berhasil disimpan.")

    with tab4:
        st.subheader("💰 Input Penjualan Telur")
        tanggal = st.date_input("Tanggal Jual", value=datetime.today())
        jumlah = st.number_input("Jumlah Terjual", min_value=1, step=1)
        harga = st.number_input("Harga Jual per Butir (Rp)", min_value=0.0, step=100.0)
        metode = st.selectbox("Metode Penjualan", ["Pasar", "Tengkulak", "Online"])
        if st.button("✅ Simpan Data Penjualan"):
            data = {"Tanggal": tanggal, "Jumlah Terjual": jumlah, "Harga Jual": harga, "Metode": metode}
            data_handler.save_data("data/penjualan.csv", data)
            st.success("✅ Data penjualan berhasil disimpan.")

elif menu == "Analisis & Laporan":
    st.subheader("📊 Analisis & Laporan Keuangan")
    st.info("Fitur ini akan menampilkan ringkasan produksi, penggunaan pakan, pendapatan, serta estimasi Break Even Point (BEP).")
