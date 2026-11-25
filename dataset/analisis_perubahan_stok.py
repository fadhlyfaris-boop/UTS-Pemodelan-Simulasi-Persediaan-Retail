import os
import pandas as pd
import numpy as np

# =====================================================
# 1. MEMBACA DATASET
# =====================================================

base_dir = os.path.dirname(__file__)

file_path = os.path.join(
    base_dir,
    "retail_store_inventory.csv"
)

df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values(
    ["Store ID", "Product ID", "Date"]
)

print("=" * 65)
print("       ANALISIS PERUBAHAN PERSEDIAAN HARIAN")
print("=" * 65)

# =====================================================
# 2. MENGHITUNG PERUBAHAN INVENTORY
# =====================================================

df["Previous Inventory"] = (
    df.groupby(["Store ID", "Product ID"])["Inventory Level"]
    .shift(1)
)

df["Inventory Change"] = (
    df["Inventory Level"] - df["Previous Inventory"]
)

df["Net Transaction"] = (
    df["Units Ordered"] - df["Units Sold"]
)

# =====================================================
# 3. MENGHAPUS BARIS PERTAMA SETIAP PRODUK-TOKO
# =====================================================

analysis = df.dropna(
    subset=["Previous Inventory", "Inventory Change"]
).copy()

# =====================================================
# 4. ANALISIS STATISTIK
# =====================================================

print("\n[1] STATISTIK PERUBAHAN PERSEDIAAN")
print("-" * 65)

print(
    analysis[
        [
            "Inventory Change",
            "Units Ordered",
            "Units Sold",
            "Net Transaction"
        ]
    ].describe().round(2)
)

# =====================================================
# 5. KORELASI PERUBAHAN PERSEDIAAN
# =====================================================

print("\n[2] KORELASI PERUBAHAN PERSEDIAAN")
print("-" * 65)

correlation = analysis[
    [
        "Inventory Change",
        "Units Ordered",
        "Units Sold",
        "Net Transaction"
    ]
].corr()

print(correlation.round(4))

# =====================================================
# 6. MEMBANDINGKAN PERUBAHAN STOK DAN TRANSAKSI
# =====================================================

analysis["Difference"] = (
    analysis["Inventory Change"]
    - analysis["Net Transaction"]
)

print("\n[3] PERBANDINGAN PERUBAHAN STOK DAN TRANSAKSI")
print("-" * 65)

print(
    analysis["Difference"].describe().round(2)
)

print(
    "\nRata-rata perubahan persediaan:",
    round(analysis["Inventory Change"].mean(), 2)
)

print(
    "Rata-rata selisih pemesanan dan penjualan:",
    round(analysis["Net Transaction"].mean(), 2)
)

print(
    "Korelasi perubahan stok dengan transaksi bersih:",
    round(
        analysis["Inventory Change"].corr(
            analysis["Net Transaction"]
        ),
        4
    )
)

# =====================================================
# 7. MENYIMPAN HASIL
# =====================================================

output_path = os.path.join(
    base_dir,
    "analisis_perubahan_stok.csv"
)

analysis.to_csv(output_path, index=False)

print("\nHasil analisis disimpan di:")
print(output_path)

print("\n" + "=" * 65)
print("       ANALISIS PERUBAHAN STOK SELESAI")
print("=" * 65)