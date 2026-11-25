import os
import pandas as pd
import numpy as np

# =====================================================
# ANALISIS HUBUNGAN PERSEDIAAN RETAIL
# =====================================================

print("=" * 65)
print("       ANALISIS HUBUNGAN PERSEDIAAN RETAIL")
print("=" * 65)

# 1. MEMBACA DATASET

base_dir = os.path.dirname(__file__)

file_path = os.path.join(
    base_dir,
    "retail_store_inventory.csv"
)

df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"])

# 2. STATISTIK VARIABEL UTAMA

print("\n[1] STATISTIK VARIABEL UTAMA")
print("-" * 65)

variabel = [
    "Inventory Level",
    "Units Sold",
    "Units Ordered",
    "Demand Forecast"
]

print(df[variabel].describe().round(2).to_string())

# 3. KORELASI ANTARVARIABEL

print("\n[2] MATRIKS KORELASI")
print("-" * 65)

korelasi = df[variabel].corr()

print(korelasi.round(4).to_string())

# 4. SELISIH PEMESANAN DAN PENJUALAN

print("\n[3] ANALISIS SELISIH PEMESANAN DAN PENJUALAN")
print("-" * 65)

df["Net Order"] = (
    df["Units Ordered"] - df["Units Sold"]
)

print(
    df["Net Order"].describe().round(2).to_string()
)

print(
    f"\nTotal Units Sold    : {df['Units Sold'].sum():,}"
)

print(
    f"Total Units Ordered : {df['Units Ordered'].sum():,}"
)

print(
    f"Selisih total       : {df['Net Order'].sum():,}"
)

# 5. POLA BERDASARKAN TOKO

print("\n[4] ANALISIS BERDASARKAN TOKO")
print("-" * 65)

per_toko = df.groupby("Store ID").agg({
    "Inventory Level": "mean",
    "Units Sold": "mean",
    "Units Ordered": "mean"
}).round(2)

print(per_toko.to_string())

# 6. POLA BERDASARKAN PRODUK

print("\n[5] ANALISIS BERDASARKAN PRODUK")
print("-" * 65)

per_produk = df.groupby("Product ID").agg({
    "Inventory Level": "mean",
    "Units Sold": "mean",
    "Units Ordered": "mean"
}).round(2)

print(per_produk.to_string())

# 7. PERBANDINGAN PENJUALAN DAN FORECAST

print("\n[6] PERBANDINGAN PENJUALAN DAN FORECAST")
print("-" * 65)

df["Forecast Error"] = (
    df["Demand Forecast"] - df["Units Sold"]
)

print(
    df["Forecast Error"].describe().round(2).to_string()
)

mae = np.abs(df["Forecast Error"]).mean()

print(f"\nMean Absolute Error: {mae:.2f}")

# 8. PENYIMPANAN HASIL

output_path = os.path.join(
    base_dir,
    "analisis_hubungan.csv"
)

per_toko.to_csv(
    os.path.join(base_dir, "analisis_per_toko.csv")
)

per_produk.to_csv(
    os.path.join(base_dir, "analisis_per_produk.csv")
)

print("\nHasil analisis berhasil disimpan.")

print("\n" + "=" * 65)
print("          ANALISIS HUBUNGAN SELESAI")
print("=" * 65)