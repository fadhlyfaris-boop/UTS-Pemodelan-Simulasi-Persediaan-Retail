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
print("           ANALISIS POLA PERMINTAAN RETAIL")
print("=" * 65)

# =====================================================
# 2. AGREGASI PENJUALAN HARIAN
# =====================================================

daily = (
    df.groupby("Date")
    .agg(
        Total_Sales=("Units Sold", "sum"),
        Average_Sales=("Units Sold", "mean"),
        Total_Forecast=("Demand Forecast", "sum")
    )
    .reset_index()
)

print("\n[1] STATISTIK PERMINTAAN HARIAN")
print("-" * 65)

print(
    daily[
        ["Total_Sales", "Average_Sales", "Total_Forecast"]
    ].describe().round(2)
)

# =====================================================
# 3. ANALISIS BULANAN
# =====================================================

daily["Month"] = daily["Date"].dt.to_period("M")

monthly = (
    daily.groupby("Month")
    .agg(
        Total_Sales=("Total_Sales", "sum"),
        Average_Daily_Sales=("Total_Sales", "mean")
    )
    .reset_index()
)

print("\n[2] POLA PERMINTAAN BULANAN")
print("-" * 65)

print(monthly.to_string(index=False))

# =====================================================
# 4. HARI DENGAN PENJUALAN TERTINGGI DAN TERENDAH
# =====================================================

highest = daily.loc[daily["Total_Sales"].idxmax()]
lowest = daily.loc[daily["Total_Sales"].idxmin()]

print("\n[3] PENJUALAN TERTINGGI")
print("-" * 65)
print("Tanggal:", highest["Date"].date())
print("Total penjualan:", int(highest["Total_Sales"]))

print("\n[4] PENJUALAN TERENDAH")
print("-" * 65)
print("Tanggal:", lowest["Date"].date())
print("Total penjualan:", int(lowest["Total_Sales"]))

# =====================================================
# 5. ANALISIS PER PRODUK
# =====================================================

product = (
    df.groupby("Product ID")
    .agg(
        Average_Sales=("Units Sold", "mean"),
        Total_Sales=("Units Sold", "sum"),
        Average_Forecast=("Demand Forecast", "mean")
    )
    .sort_values("Average_Sales", ascending=False)
)

print("\n[5] LIMA PRODUK DENGAN PENJUALAN TERTINGGI")
print("-" * 65)

print(product.head(5).round(2))

print("\n[6] LIMA PRODUK DENGAN PENJUALAN TERENDAH")
print("-" * 65)

print(product.tail(5).round(2))

# =====================================================
# 6. SIMPAN HASIL
# =====================================================

daily.to_csv(
    os.path.join(base_dir, "permintaan_harian.csv"),
    index=False
)

monthly.to_csv(
    os.path.join(base_dir, "permintaan_bulanan.csv"),
    index=False
)

product.to_csv(
    os.path.join(base_dir, "permintaan_per_produk.csv")
)

print("\nHasil analisis berhasil disimpan.")

print("\n" + "=" * 65)
print("          ANALISIS POLA PERMINTAAN SELESAI")
print("=" * 65)