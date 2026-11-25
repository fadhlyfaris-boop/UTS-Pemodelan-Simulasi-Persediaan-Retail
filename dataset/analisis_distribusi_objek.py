import os
import pandas as pd
import numpy as np

# =====================================================
# 1. MEMBACA DATASET
# =====================================================

base_dir = os.path.dirname(__file__)

df = pd.read_csv(
    os.path.join(base_dir, "retail_store_inventory.csv")
)

df["Date"] = pd.to_datetime(df["Date"])

# Objek simulasi
store_id = "S004"
product_id = "P0020"

data = df[
    (df["Store ID"] == store_id) &
    (df["Product ID"] == product_id)
].copy()

data = data.sort_values("Date").reset_index(drop=True)

print("=" * 70)
print("       ANALISIS DISTRIBUSI PERMINTAAN OBJEK SIMULASI")
print("=" * 70)

print(f"\nToko   : {store_id}")
print(f"Produk : {product_id}")
print(f"Jumlah data: {len(data)} hari")

# =====================================================
# 2. STATISTIK PERMINTAAN
# =====================================================

print("\n[1] STATISTIK PERMINTAAN HARIAN")
print("-" * 70)

print(
    data["Units Sold"].describe(
        percentiles=[0.05, 0.25, 0.50, 0.75, 0.95]
    ).round(2)
)

# =====================================================
# 3. FREKUENSI PERMINTAAN NOL
# =====================================================

print("\n[2] FREKUENSI PERMINTAAN NOL")
print("-" * 70)

zero_count = (data["Units Sold"] == 0).sum()

print("Hari tanpa penjualan:", zero_count)
print(
    "Persentase:",
    round(zero_count / len(data) * 100, 2),
    "%"
)

# =====================================================
# 4. PERHITUNGAN PERMINTAAN SELAMA LEAD TIME
# =====================================================

print("\n[3] DISTRIBUSI PERMINTAAN SELAMA LEAD TIME")
print("-" * 70)

hasil_lead_time = []

for lead_time in [1, 2, 3]:

    rolling_demand = (
        data["Units Sold"]
        .rolling(window=lead_time)
        .sum()
        .dropna()
    )

    hasil_lead_time.append({
        "Lead_Time": lead_time,
        "Average_Demand": rolling_demand.mean(),
        "Demand_95th_Percentile": rolling_demand.quantile(0.95),
        "Demand_99th_Percentile": rolling_demand.quantile(0.99),
        "Maximum_Demand": rolling_demand.max()
    })

    print(f"\nLead time: {lead_time} hari")
    print(f"Rata-rata permintaan : {rolling_demand.mean():.2f}")
    print(f"Persentil 95%        : {rolling_demand.quantile(0.95):.2f}")
    print(f"Persentil 99%        : {rolling_demand.quantile(0.99):.2f}")
    print(f"Permintaan maksimum : {rolling_demand.max():.2f}")

# =====================================================
# 5. PERBANDINGAN PERSEDIAAN DAN PERMINTAAN
# =====================================================

print("\n[4] PERBANDINGAN PERSEDIAAN DAN PERMINTAAN")
print("-" * 70)

print(
    "Rata-rata persediaan:",
    round(data["Inventory Level"].mean(), 2)
)

print(
    "Rata-rata permintaan:",
    round(data["Units Sold"].mean(), 2)
)

print(
    "Rasio persediaan terhadap permintaan harian:",
    round(
        data["Inventory Level"].mean()
        / data["Units Sold"].mean(),
        2
    ),
    "hari"
)

# =====================================================
# 6. MENYIMPAN HASIL
# =====================================================

output = pd.DataFrame(hasil_lead_time)

output_path = os.path.join(
    base_dir,
    "distribusi_lead_time.csv"
)

output.to_csv(output_path, index=False)

data.to_csv(
    os.path.join(base_dir, "data_objek_simulasi.csv"),
    index=False
)

print("\nHasil disimpan:")
print(output_path)

print("\nData objek simulasi disimpan:")
print(os.path.join(base_dir, "data_objek_simulasi.csv"))

print("\n" + "=" * 70)
print("       ANALISIS DISTRIBUSI SELESAI")
print("=" * 70)