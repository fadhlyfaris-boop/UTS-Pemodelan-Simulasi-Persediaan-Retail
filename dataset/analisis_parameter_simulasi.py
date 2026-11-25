import os
import pandas as pd

# =====================================================
# 1. MEMBACA DATASET
# =====================================================

base_dir = os.path.dirname(__file__)

df = pd.read_csv(
    os.path.join(base_dir, "retail_store_inventory.csv")
)

df["Date"] = pd.to_datetime(df["Date"])

print("=" * 65)
print("       ANALISIS PARAMETER MODEL SIMULASI")
print("=" * 65)

# =====================================================
# 2. STATISTIK PERMINTAAN
# =====================================================

print("\n[1] STATISTIK PERMINTAAN KESELURUHAN")
print("-" * 65)

sales_mean = df["Units Sold"].mean()
sales_std = df["Units Sold"].std()

print(f"Rata-rata permintaan : {sales_mean:.2f}")
print(f"Simpangan baku       : {sales_std:.2f}")
print(f"Permintaan minimum  : {df['Units Sold'].min()}")
print(f"Permintaan maksimum : {df['Units Sold'].max()}")

# =====================================================
# 3. STATISTIK PER TOKO DAN PRODUK
# =====================================================

grouped = (
    df.groupby(["Store ID", "Product ID"])
    .agg(
        Average_Demand=("Units Sold", "mean"),
        Demand_Std=("Units Sold", "std"),
        Average_Inventory=("Inventory Level", "mean"),
        Average_Order=("Units Ordered", "mean"),
        Total_Sales=("Units Sold", "sum")
    )
    .reset_index()
)

print("\n[2] JUMLAH KOMBINASI TOKO DAN PRODUK")
print("-" * 65)

print("Jumlah kombinasi:", len(grouped))

# =====================================================
# 4. KOMBINASI DENGAN PENJUALAN TERTINGGI
# =====================================================

print("\n[3] LIMA KOMBINASI DENGAN RATA-RATA PENJUALAN TERTINGGI")
print("-" * 65)

print(
    grouped.sort_values(
        "Average_Demand",
        ascending=False
    ).head(5).round(2).to_string(index=False)
)

# =====================================================
# 5. KOMBINASI DENGAN PENJUALAN TERENDAH
# =====================================================

print("\n[4] LIMA KOMBINASI DENGAN RATA-RATA PENJUALAN TERENDAH")
print("-" * 65)

print(
    grouped.sort_values(
        "Average_Demand",
        ascending=True
    ).head(5).round(2).to_string(index=False)
)

# =====================================================
# 6. MENENTUKAN PARAMETER REFERENSI
# =====================================================

print("\n[5] PARAMETER REFERENSI SIMULASI")
print("-" * 65)

print("Persediaan awal referensi :", round(df["Inventory Level"].mean(), 2))
print("Permintaan rata-rata      :", round(sales_mean, 2))
print("Simpangan baku permintaan :", round(sales_std, 2))
print("Rata-rata pemesanan       :", round(df["Units Ordered"].mean(), 2))

# =====================================================
# 7. MENYIMPAN HASIL
# =====================================================

output_path = os.path.join(
    base_dir,
    "parameter_toko_produk.csv"
)

grouped.to_csv(output_path, index=False)

print("\nHasil disimpan di:")
print(output_path)

print("\n" + "=" * 65)
print("       ANALISIS PARAMETER SELESAI")
print("=" * 65)