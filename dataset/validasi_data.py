import os
import pandas as pd

# =====================================================
# VALIDASI DATASET RETAIL STORE INVENTORY
# =====================================================

print("=" * 65)
print("       VALIDASI DATASET RETAIL STORE INVENTORY")
print("=" * 65)

# 1. MEMBACA DATASET
base_dir = os.path.dirname(__file__)

file_path = os.path.join(
    base_dir,
    "retail_store_inventory.csv"
)

df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"])

# 2. VALIDASI RENTANG TANGGAL
print("\n[1] VALIDASI RENTANG TANGGAL")
print("-" * 65)

tanggal = pd.date_range(
    start=df["Date"].min(),
    end=df["Date"].max(),
    freq="D"
)

tanggal_aktual = df["Date"].drop_duplicates().sort_values()

tanggal_hilang = tanggal.difference(tanggal_aktual)

print(f"Jumlah hari seharusnya : {len(tanggal)}")
print(f"Jumlah hari tersedia   : {len(tanggal_aktual)}")
print(f"Tanggal hilang         : {len(tanggal_hilang)}")

# 3. VALIDASI JUMLAH OBSERVASI PER HARI
print("\n[2] JUMLAH OBSERVASI PER HARI")
print("-" * 65)

observasi_harian = df.groupby("Date").size()

print(f"Minimum observasi/hari : {observasi_harian.min()}")
print(f"Maksimum observasi/hari : {observasi_harian.max()}")
print(f"Rata-rata observasi/hari: {observasi_harian.mean():.2f}")

# 4. VALIDASI KOMBINASI TOKO DAN PRODUK
print("\n[3] VALIDASI KOMBINASI TOKO DAN PRODUK")
print("-" * 65)

kombinasi = df.groupby("Date").apply(
    lambda x: x[["Store ID", "Product ID"]].drop_duplicates().shape[0],
    include_groups=False
)

print(f"Kombinasi minimum: {kombinasi.min()}")
print(f"Kombinasi maksimum: {kombinasi.max()}")

# 5. VALIDASI DUPLIKAT KUNCI DATA
print("\n[4] PEMERIKSAAN DUPLIKAT KUNCI")
print("-" * 65)

duplikat_kunci = df.duplicated(
    subset=["Date", "Store ID", "Product ID"]
).sum()

print(f"Duplikat berdasarkan tanggal, toko, produk: {duplikat_kunci}")

# 6. PEMERIKSAAN NILAI NEGATIF
print("\n[5] PEMERIKSAAN NILAI NEGATIF")
print("-" * 65)

kolom_numerik = [
    "Inventory Level",
    "Units Sold",
    "Units Ordered",
    "Demand Forecast",
    "Price",
    "Discount",
    "Competitor Pricing"
]

for kolom in kolom_numerik:

    jumlah_negatif = (df[kolom] < 0).sum()

    print(f"{kolom:<25}: {jumlah_negatif}")

# 7. PEMERIKSAAN DEMAND FORECAST
print("\n[6] ANALISIS DEMAND FORECAST NEGATIF")
print("-" * 65)

forecast_negatif = df[df["Demand Forecast"] < 0]

print(f"Jumlah forecast negatif: {len(forecast_negatif)}")

if len(forecast_negatif) > 0:

    print("\nContoh data forecast negatif:")

    print(
        forecast_negatif[
            ["Date", "Store ID", "Product ID",
             "Units Sold", "Demand Forecast"]
        ].head(10).to_string(index=False)
    )

    output_path = os.path.join(
        base_dir,
        "data_forecast_negatif.csv"
    )

    forecast_negatif.to_csv(
        output_path,
        index=False
    )

    print("\nData forecast negatif disimpan:")
    print(output_path)

# 8. DISTRIBUSI KATEGORI
print("\n[7] DISTRIBUSI KATEGORI PRODUK")
print("-" * 65)

print(df["Category"].value_counts().to_string())

# 9. DISTRIBUSI TOKO
print("\n[8] DISTRIBUSI TOKO")
print("-" * 65)

print(df["Store ID"].value_counts().to_string())

# 10. KESIMPULAN
print("\n" + "=" * 65)
print("                 VALIDASI SELESAI")
print("=" * 65)