import os
import pandas as pd

# =====================================================
# 1. MEMBACA DATASET
# =====================================================

base_dir = os.path.dirname(__file__)

df = pd.read_csv(
    os.path.join(base_dir, "retail_store_inventory.csv")
)

print("=" * 70)
print("          PEMILIHAN OBJEK MODEL SIMULASI")
print("=" * 70)

# =====================================================
# 2. MENGHITUNG RATA-RATA KESELURUHAN
# =====================================================

global_demand = df["Units Sold"].mean()
global_inventory = df["Inventory Level"].mean()

print("\n[1] NILAI REFERENSI DATASET")
print("-" * 70)

print(f"Rata-rata permintaan  : {global_demand:.2f}")
print(f"Rata-rata persediaan  : {global_inventory:.2f}")

# =====================================================
# 3. MENGHITUNG STATISTIK SETIAP KOMBINASI
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

# =====================================================
# 4. MENGHITUNG JARAK DARI NILAI REFERENSI
# =====================================================

grouped["Demand_Distance"] = (
    (grouped["Average_Demand"] - global_demand)
    / global_demand
).abs()

grouped["Inventory_Distance"] = (
    (grouped["Average_Inventory"] - global_inventory)
    / global_inventory
).abs()

grouped["Total_Distance"] = (
    grouped["Demand_Distance"]
    + grouped["Inventory_Distance"]
)

# =====================================================
# 5. MEMILIH KOMBINASI PALING REPRESENTATIF
# =====================================================

selected = grouped.sort_values(
    "Total_Distance"
).iloc[0]

print("\n[2] LIMA KOMBINASI PALING MENDEKATI RATA-RATA")
print("-" * 70)

print(
    grouped.sort_values("Total_Distance")
    .head(5)
    .round(3)
    .to_string(index=False)
)

# =====================================================
# 6. MENAMPILKAN OBJEK SIMULASI
# =====================================================

print("\n[3] OBJEK SIMULASI TERPILIH")
print("-" * 70)

print("Store ID             :", selected["Store ID"])
print("Product ID           :", selected["Product ID"])
print("Rata-rata permintaan :", round(selected["Average_Demand"], 2))
print("Simpangan baku       :", round(selected["Demand_Std"], 2))
print("Rata-rata persediaan :", round(selected["Average_Inventory"], 2))
print("Rata-rata pemesanan  :", round(selected["Average_Order"], 2))
print("Total penjualan      :", int(selected["Total_Sales"]))

# =====================================================
# 7. MENYIMPAN HASIL
# =====================================================

output_path = os.path.join(
    base_dir,
    "objek_simulasi.csv"
)

grouped.sort_values("Total_Distance").to_csv(
    output_path,
    index=False
)

print("\nHasil disimpan di:")
print(output_path)

print("\n" + "=" * 70)
print("          PEMILIHAN OBJEK SIMULASI SELESAI")
print("=" * 70)