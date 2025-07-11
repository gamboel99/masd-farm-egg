import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Import aman untuk data_handler
try:
    from utils import data_handler
except:
    import sys
    sys.path.append("utils")
    import data_handler

st.set_page_config(page_title="Mas D Farm Egg", layout="wide")
st.title("🥚 Mas D Farm Egg - Sistem Pencatatan & Analisis")

menu = st.sidebar.radio("📌 Navigasi", ["Input Data", "Analisis & Laporan"])

if not os.path.exists("data"):
    os.makedirs("data")

# ==================== INPUT ====================
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
        if os.path.exists("data/ayam.csv"):
            st.subheader("📊 Riwayat Ayam Masuk")
            st.dataframe(pd.read_csv("data/ayam.csv"))

    with tab2:
        st.subheader("🍽️ Input Pakan")
        tanggal = st.date_input("Tanggal Pakan", value=datetime.today())
        jumlah = st.number_input("Jumlah Sak", min_value=1, step=1)
        harga = st.number_input("Harga per Sak (Rp)", min_value=0.0, step=500.0)
        if st.button("✅ Simpan Data Pakan"):
            data = {"Tanggal": tanggal, "Jumlah Sak": jumlah, "Harga per Sak": harga}
            data_handler.save_data("data/pakan.csv", data)
            st.success("✅ Data pakan berhasil disimpan.")
        if os.path.exists("data/pakan.csv"):
            st.subheader("📊 Riwayat Pakan")
            st.dataframe(pd.read_csv("data/pakan.csv"))

    with tab3:
        st.subheader("🥚 Input Produksi Telur")
        tanggal = st.date_input("Tanggal Produksi", value=datetime.today())
        jumlah = st.number_input("Jumlah Telur", min_value=1, step=1)
        kualitas = st.selectbox("Kualitas", ["Baik", "Retak", "Kecil"])
        if st.button("✅ Simpan Data Produksi"):
            data = {"Tanggal": tanggal, "Jumlah Telur": jumlah, "Kualitas": kualitas}
            data_handler.save_data("data/produksi.csv", data)
            st.success("✅ Data produksi telur berhasil disimpan.")
        if os.path.exists("data/produksi.csv"):
            st.subheader("📊 Riwayat Produksi Telur")
            st.dataframe(pd.read_csv("data/produksi.csv"))

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
        if os.path.exists("data/penjualan.csv"):
            st.subheader("📊 Riwayat Penjualan")
            st.dataframe(pd.read_csv("data/penjualan.csv"))

# ==================== ANALISIS ====================
elif menu == "Analisis & Laporan":
    st.subheader("📊 Analisis & Laporan Keuangan")

    df_ayam = pd.read_csv("data/ayam.csv") if os.path.exists("data/ayam.csv") else pd.DataFrame()
    df_pakan = pd.read_csv("data/pakan.csv") if os.path.exists("data/pakan.csv") else pd.DataFrame()
    df_produksi = pd.read_csv("data/produksi.csv") if os.path.exists("data/produksi.csv") else pd.DataFrame()
    df_jual = pd.read_csv("data/penjualan.csv") if os.path.exists("data/penjualan.csv") else pd.DataFrame()

    total_ayam = df_ayam["Jumlah Ayam"].sum() if not df_ayam.empty else 0
    total_pakan = df_pakan["Jumlah Sak"].sum() if not df_pakan.empty else 0
    biaya_pakan = (df_pakan["Jumlah Sak"] * df_pakan["Harga per Sak"]).sum() if not df_pakan.empty else 0
    total_telur = df_produksi["Jumlah Telur"].sum() if not df_produksi.empty else 0
    pendapatan = (df_jual["Jumlah Terjual"] * df_jual["Harga Jual"]).sum() if not df_jual.empty else 0

    try:
        harga_jual_rata = df_jual["Harga Jual"].mean()
        bep_butir = biaya_pakan / harga_jual_rata if harga_jual_rata > 0 else 0
    except:
        bep_butir = 0

    st.metric("🐔 Total Ayam Masuk", f"{total_ayam} ekor")
    st.metric("🍽️ Total Pakan Digunakan", f"{total_pakan} sak")
    st.metric("🥚 Total Produksi Telur", f"{total_telur} butir")
    st.metric("💰 Total Pendapatan", f"Rp {pendapatan:,.0f}")
    st.metric("💸 Total Biaya Pakan", f"Rp {biaya_pakan:,.0f}")
    st.metric("⚖️ Estimasi BEP (Butir Telur)", f"{bep_butir:.0f} butir" if bep_butir > 0 else "Belum cukup data")
    st.caption("⚠️ Perhitungan BEP hanya berdasarkan biaya pakan untuk saat ini.")
