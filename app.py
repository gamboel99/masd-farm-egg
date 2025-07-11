import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO
from utils import data_handler

BERAT_KONVERSI = 1 / 16  # 1 butir = 0.0625 kg

st.set_page_config(page_title="Mas D Farm Egg", layout="wide")
st.title("🥚 Mas D Farm Egg - Sistem Pencatatan & Analisis")

menu = st.sidebar.radio("📌 Navigasi", ["Input Data", "Analisis & Laporan"])

if not os.path.exists("data"):
    os.makedirs("data")

# ======================= INPUT =======================
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
        st.subheader("💰 Input Penjualan Telur (Butir)")
        tanggal = st.date_input("Tanggal Jual", value=datetime.today())
        jumlah = st.number_input("Jumlah Terjual (butir)", min_value=1, step=1)
        harga = st.number_input("Harga Jual per Kg (Rp)", min_value=0.0, step=100.0)
        metode = st.selectbox("Metode Penjualan", ["Pasar", "Tengkulak", "Online"])
        if st.button("✅ Simpan Data Penjualan"):
            data = {
                "Tanggal": tanggal,
                "Jumlah Terjual (butir)": jumlah,
                "Harga per Kg": harga,
                "Metode": metode
            }
            data_handler.save_data("data/penjualan.csv", data)
            st.success("✅ Data penjualan berhasil disimpan.")
        if os.path.exists("data/penjualan.csv"):
            st.subheader("📊 Riwayat Penjualan")
            st.dataframe(pd.read_csv("data/penjualan.csv"))

# ======================= ANALISIS =======================
elif menu == "Analisis & Laporan":
    st.subheader("📊 Analisis Laba Rugi & BEP")

    df_pakan = pd.read_csv("data/pakan.csv") if os.path.exists("data/pakan.csv") else pd.DataFrame()
    df_jual = pd.read_csv("data/penjualan.csv") if os.path.exists("data/penjualan.csv") else pd.DataFrame()

    # Hitung total biaya pakan
    biaya_pakan = (df_pakan["Jumlah Sak"] * df_pakan["Harga per Sak"]).sum() if not df_pakan.empty else 0

    # Konversi penjualan ke kg
    if not df_jual.empty:
        df_jual["Berat Terjual (kg)"] = df_jual["Jumlah Terjual (butir)"] * BERAT_KONVERSI
        df_jual["Pendapatan"] = df_jual["Berat Terjual (kg)"] * df_jual["Harga per Kg"]
        total_kg = df_jual["Berat Terjual (kg)"].sum()
        total_pendapatan = df_jual["Pendapatan"].sum()
    else:
        total_kg = 0
        total_pendapatan = 0

    # Hitung laba
    laba = total_pendapatan - biaya_pakan
    st.metric("💰 Total Pendapatan", f"Rp {total_pendapatan:,.0f}")
    st.metric("💸 Total Biaya Pakan", f"Rp {biaya_pakan:,.0f}")
    st.metric("📈 Laba Bersih", f"Rp {laba:,.0f}")
    st.metric("⚖️ Total Telur Terjual", f"{total_kg:.2f} kg")

    # Tombol unduh laporan
    if st.button("⬇️ Download Laporan Excel"):
        file_bytes = data_handler.export_to_excel(df_pakan, df_jual, biaya_pakan, total_pendapatan, laba)
        st.download_button(
            label="📥 Download Laporan Laba Rugi",
            data=file_bytes,
            file_name="laporan_keuangan_masd_farm.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
