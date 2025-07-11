def export_to_excel(df_pakan, df_jual, biaya_pakan, pendapatan, laba):
    import xlsxwriter
    from io import BytesIO

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    df_pakan.to_excel(writer, sheet_name="Pakan", index=False)
    df_jual.to_excel(writer, sheet_name="Penjualan", index=False)

    df_summary = pd.DataFrame({
        "Keterangan": ["Pendapatan", "Biaya Pakan", "Laba Bersih"],
        "Nilai (Rp)": [pendapatan, biaya_pakan, laba]
    })
    df_summary.to_excel(writer, sheet_name="Laba Rugi", index=False)

    writer.close()
    output.seek(0)
    return output.getvalue()
