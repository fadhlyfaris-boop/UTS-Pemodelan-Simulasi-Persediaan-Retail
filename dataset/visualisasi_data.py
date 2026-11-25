import os
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# EXPLORATORY DATA ANALYSIS
# RETAIL STORE INVENTORY DATASET
# =====================================================

print("=" * 65)
print("       EXPLORATORY DATA ANALYSIS RETAIL DATASET")
print("=" * 65)

# 1. MEMBACA DATASET
base_dir = os.path.dirname(__file__)

file_path = os.path.join(
    base_dir,
    "retail_store_inventory.csv"
)

df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"])

# Folder hasil visualisasi
output_dir = os.path.join(
    base_dir,
    "hasil_visualisasi"
)

os.makedirs(output_dir, exist_ok=True)

print("\nDataset berhasil dibaca!")
print(f"Jumlah data: {len(df):,}")

# =====================================================
# 2. AGREGASI DATA BULANAN
# =====================================================

print("\n[1] ANALISIS PENJUALAN DAN PEMESANAN BULANAN")
print("-" * 65)

df["Bulan"] = df["Date"].dt.to_period("M")

bulanan = df.groupby("Bulan").agg({
    "Units Sold": "sum",
    "Units Ordered": "sum",
    "Inventory Level": "mean"
}).reset_index()

bulanan["Bulan"] = bulanan["Bulan"].astype(str)

print(bulanan.to_string(index=False))

# Visualisasi penjualan dan pemesanan

plt.figure(figsize=(14, 6))

plt.plot(
    bulanan["Bulan"],
    bulanan["Units Sold"],
    marker="o",
    label="Units Sold"
)

plt.plot(
    bulanan["Bulan"],
    bulanan["Units Ordered"],
    marker="o",
    label="Units Ordered"
)

plt.title("Tren Penjualan dan Pemesanan Produk Bulanan")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Unit")
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "01_tren_penjualan_pemesanan.png"),
    dpi=300
)

plt.close()

# =====================================================
# 3. ANALISIS PERSEDIAAN
# =====================================================

print("\n[2] ANALISIS PERSEDIAAN")
print("-" * 65)

print(f"Rata-rata persediaan: {df['Inventory Level'].mean():.2f}")
print(f"Persediaan minimum  : {df['Inventory Level'].min()}")
print(f"Persediaan maksimum : {df['Inventory Level'].max()}")

# Visualisasi rata-rata persediaan bulanan

plt.figure(figsize=(14, 6))

plt.plot(
    bulanan["Bulan"],
    bulanan["Inventory Level"],
    marker="o"
)

plt.title("Tren Rata-rata Persediaan Produk Bulanan")
plt.xlabel("Bulan")
plt.ylabel("Rata-rata Inventory Level")
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "02_tren_persediaan.png"),
    dpi=300
)

plt.close()

# =====================================================
# 4. DISTRIBUSI PENJUALAN
# =====================================================

print("\n[3] DISTRIBUSI PENJUALAN")
print("-" * 65)

print(df["Units Sold"].describe())

plt.figure(figsize=(10, 6))

plt.hist(
    df["Units Sold"],
    bins=30,
    edgecolor="black"
)

plt.title("Distribusi Jumlah Produk Terjual")
plt.xlabel("Units Sold")
plt.ylabel("Frekuensi")
plt.grid(axis="y")
plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "03_distribusi_penjualan.png"),
    dpi=300
)

plt.close()

# =====================================================
# 5. HUBUNGAN PERSEDIAAN DAN PENJUALAN
# =====================================================

print("\n[4] HUBUNGAN PERSEDIAAN DAN PENJUALAN")
print("-" * 65)

korelasi = df[
    ["Inventory Level", "Units Sold"]
].corr()

print(korelasi.to_string())

nilai_korelasi = korelasi.loc[
    "Inventory Level",
    "Units Sold"
]

print(f"\nKoefisien korelasi: {nilai_korelasi:.4f}")

plt.figure(figsize=(10, 6))

plt.scatter(
    df["Inventory Level"],
    df["Units Sold"],
    alpha=0.3
)

plt.title("Hubungan Persediaan dengan Penjualan")
plt.xlabel("Inventory Level")
plt.ylabel("Units Sold")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "04_hubungan_persediaan_penjualan.png"),
    dpi=300
)

plt.close()

# =====================================================
# 6. SIMPAN HASIL AGREGASI
# =====================================================

output_csv = os.path.join(
    base_dir,
    "data_agregat_bulanan.csv"
)

bulanan.to_csv(
    output_csv,
    index=False
)

# =====================================================
# 7. KESIMPULAN
# =====================================================

print("\n[5] HASIL VISUALISASI")
print("-" * 65)

print("4 visualisasi berhasil dibuat.")

print("\nLokasi hasil visualisasi:")
print(output_dir)

print("\nData agregat bulanan disimpan:")
print(output_csv)

print("\n" + "=" * 65)
print("          EXPLORATORY DATA ANALYSIS SELESAI")
print("=" * 65)