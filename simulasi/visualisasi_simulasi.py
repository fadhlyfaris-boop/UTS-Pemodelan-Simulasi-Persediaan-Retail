import os
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# 1. KONFIGURASI DIREKTORI
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "hasil_simulasi"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

lead_times = [1, 2, 3]

data = {}

for lt in lead_times:

    filename = f"simulasi_lead_time_{lt}_hari.csv"

    path = os.path.join(OUTPUT_DIR, filename)

    df = pd.read_csv(path)

    df["Date"] = pd.to_datetime(df["Date"])

    data[lt] = df

summary = pd.read_csv(
    os.path.join(OUTPUT_DIR, "ringkasan_simulasi.csv")
)

# =====================================================
# 2. GRAFIK PERUBAHAN PERSEDIAAN
# =====================================================

plt.figure(figsize=(14, 6))

for lt in lead_times:

    df = data[lt]

    plt.plot(
        df["Date"],
        df["Ending_Inventory"],
        label=f"Lead Time {lt} Hari",
        linewidth=1
    )

plt.title("Perubahan Persediaan Selama Periode Simulasi")
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Persediaan (Unit)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "01_tren_persediaan.png"),
    dpi=300
)

plt.close()

# =====================================================
# 3. GRAFIK PERMINTAAN DAN PENJUALAN
# =====================================================

plt.figure(figsize=(14, 6))

for lt in lead_times:

    df = data[lt]

    monthly = df.copy()

    monthly["Month"] = (
        monthly["Date"].dt.to_period("M")
    )

    monthly = monthly.groupby("Month")[
        ["Demand", "Sales"]
    ].sum()

    plt.plot(
        monthly.index.astype(str),
        monthly["Demand"],
        label=f"Permintaan LT {lt}",
        marker="o"
    )

    plt.plot(
        monthly.index.astype(str),
        monthly["Sales"],
        label=f"Penjualan LT {lt}",
        linestyle="--"
    )

plt.title("Perbandingan Permintaan dan Penjualan Bulanan")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Unit")
plt.xticks(rotation=90)
plt.legend(ncol=2)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "02_permintaan_penjualan.png"),
    dpi=300
)

plt.close()

# =====================================================
# 4. GRAFIK LOST SALES
# =====================================================

plt.figure(figsize=(8, 5))

plt.bar(
    summary["Lead_Time"].astype(str) + " Hari",
    summary["Total_Lost_Sales"]
)

plt.title("Perbandingan Total Lost Sales")
plt.xlabel("Lead Time")
plt.ylabel("Lost Sales (Unit)")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "03_perbandingan_lost_sales.png"),
    dpi=300
)

plt.close()

# =====================================================
# 5. GRAFIK RATA-RATA PERSEDIAAN
# =====================================================

plt.figure(figsize=(8, 5))

plt.bar(
    summary["Lead_Time"].astype(str) + " Hari",
    summary["Average_Inventory"]
)

plt.title("Perbandingan Rata-rata Persediaan")
plt.xlabel("Lead Time")
plt.ylabel("Rata-rata Persediaan (Unit)")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "04_rata_rata_persediaan.png"),
    dpi=300
)

plt.close()

# =====================================================
# 6. GRAFIK TINGKAT PEMENUHAN
# =====================================================

plt.figure(figsize=(8, 5))

plt.bar(
    summary["Lead_Time"].astype(str) + " Hari",
    summary["Service_Rate_Percent"]
)

plt.title("Perbandingan Tingkat Pemenuhan Permintaan")
plt.xlabel("Lead Time")
plt.ylabel("Tingkat Pemenuhan (%)")
plt.ylim(0, 105)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "05_tingkat_pemenuhan.png"),
    dpi=300
)

plt.close()

# =====================================================
# 7. SELESAI
# =====================================================

print("=" * 70)
print("             VISUALISASI SIMULASI PERSEDIAAN")
print("=" * 70)

print("\nGrafik berhasil dibuat:")

files = [
    "01_tren_persediaan.png",
    "02_permintaan_penjualan.png",
    "03_perbandingan_lost_sales.png",
    "04_rata_rata_persediaan.png",
    "05_tingkat_pemenuhan.png"
]

for filename in files:

    print(f"- {filename}")

print("\nLokasi penyimpanan:")
print(OUTPUT_DIR)

print("\n" + "=" * 70)
print("              VISUALISASI SELESAI")
print("=" * 70)