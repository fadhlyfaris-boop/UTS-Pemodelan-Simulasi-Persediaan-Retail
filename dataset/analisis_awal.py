import os
import pandas as pd

# =====================================================
# ANALISIS AWAL DATASET RETAIL STORE INVENTORY
# =====================================================

print("=" * 65)
print("       ANALISIS AWAL RETAIL STORE INVENTORY DATASET")
print("=" * 65)

# 1. MEMBACA DATASET
print("\n[1] MEMBACA DATASET")
print("-" * 65)

file_path = os.path.join(
    os.path.dirname(__file__),
    "retail_store_inventory.csv"
)

df = pd.read_csv(file_path)

print("Dataset berhasil dibaca!")
print(f"Jumlah baris  : {df.shape[0]:,}")
print(f"Jumlah kolom  : {df.shape[1]}")

# 2. MENAMPILKAN NAMA KOLOM
print("\n[2] DAFTAR KOLOM DATASET")
print("-" * 65)

for nomor, kolom in enumerate(df.columns, start=1):
    print(f"{nomor}. {kolom}")

# 3. MENAMPILKAN LIMA DATA PERTAMA
print("\n[3] LIMA DATA PERTAMA")
print("-" * 65)

print(df.head().to_string(index=False))

# 4. INFORMASI DATASET
print("\n[4] INFORMASI DATASET")
print("-" * 65)

df.info()

# 5. MEMERIKSA DATA KOSONG
print("\n[5] PEMERIKSAAN DATA KOSONG")
print("-" * 65)

missing = df.isnull().sum()

print(missing.to_string())

print(f"\nTotal data kosong: {missing.sum():,}")

# 6. MEMERIKSA DATA DUPLIKAT
print("\n[6] PEMERIKSAAN DATA DUPLIKAT")
print("-" * 65)

duplicate_count = df.duplicated().sum()

print(f"Jumlah data duplikat: {duplicate_count:,}")

# 7. STATISTIK DESKRIPTIF
print("\n[7] STATISTIK DESKRIPTIF")
print("-" * 65)

print(df.describe(include="all").to_string())

# 8. PEMERIKSAAN IDENTITAS DATA
print("\n[8] IDENTITAS DATASET")
print("-" * 65)

if "Date" in df.columns:
    dates = pd.to_datetime(df["Date"], errors="coerce")

    print(f"Tanggal awal : {dates.min()}")
    print(f"Tanggal akhir: {dates.max()}")

if "Store ID" in df.columns:
    print(f"Jumlah toko  : {df['Store ID'].nunique()}")

if "Product ID" in df.columns:
    print(f"Jumlah produk: {df['Product ID'].nunique()}")

# 9. SELESAI
print("\n" + "=" * 65)
print("             ANALISIS AWAL SELESAI")
print("=" * 65)