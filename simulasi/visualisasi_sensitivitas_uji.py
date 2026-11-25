import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================================
# 1. KONFIGURASI DIREKTORI
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "hasil_simulasi"

FILE_INPUT = OUTPUT_DIR / "hasil_analisis_sensitivitas.csv"

# ==========================================================
# 2. MEMBACA DATA
# ==========================================================

df = pd.read_csv(FILE_INPUT)

print("=" * 75)
print("          VISUALISASI ANALISIS SENSITIVITAS PERSEDIAAN")
print("=" * 75)

print("\n[1] DATA ANALISIS SENSITIVITAS")
print("-" * 75)

print(df.to_string(index=False))

# Urutan skenario pada grafik
urutan_skenario = ["Rendah", "Baseline", "Tinggi"]

lead_times = sorted(df["Lead_Time"].unique())

df["Skenario"] = pd.Categorical(
    df["Skenario"],
    categories=urutan_skenario,
    ordered=True
)

df = df.sort_values(
    ["Lead_Time", "Skenario"]
)

# ==========================================================
# 3. VISUALISASI LOST SALES
# ==========================================================

plt.figure(figsize=(10, 6))

for lt in lead_times:

    data_lt = df[df["Lead_Time"] == lt]

    plt.plot(
        data_lt["Skenario"],
        data_lt["Lost_Sales"],
        marker="o",
        linewidth=2,
        label=f"Lead Time {lt} Hari"
    )

plt.title(
    "Pengaruh Safety Stock terhadap Lost Sales",
    fontsize=13
)

plt.xlabel("Skenario Safety Stock")
plt.ylabel("Total Lost Sales")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "11_sensitivitas_lost_sales.png",
    dpi=300
)

plt.close()

# ==========================================================
# 4. VISUALISASI FILL RATE
# ==========================================================

plt.figure(figsize=(10, 6))

for lt in lead_times:

    data_lt = df[df["Lead_Time"] == lt]

    plt.plot(
        data_lt["Skenario"],
        data_lt["Fill_Rate_Persen"],
        marker="o",
        linewidth=2,
        label=f"Lead Time {lt} Hari"
    )

plt.title(
    "Pengaruh Safety Stock terhadap Fill Rate",
    fontsize=13
)

plt.xlabel("Skenario Safety Stock")
plt.ylabel("Fill Rate (%)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "12_sensitivitas_fill_rate.png",
    dpi=300
)

plt.close()

# ==========================================================
# 5. VISUALISASI RATA-RATA PERSEDIAAN
# ==========================================================

plt.figure(figsize=(10, 6))

for lt in lead_times:

    data_lt = df[df["Lead_Time"] == lt]

    plt.plot(
        data_lt["Skenario"],
        data_lt["Rata_Rata_Persediaan"],
        marker="o",
        linewidth=2,
        label=f"Lead Time {lt} Hari"
    )

plt.title(
    "Pengaruh Safety Stock terhadap Rata-rata Persediaan",
    fontsize=13
)

plt.xlabel("Skenario Safety Stock")
plt.ylabel("Rata-rata Persediaan")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "13_sensitivitas_rata_rata_persediaan.png",
    dpi=300
)

plt.close()

# ==========================================================
# 6. VISUALISASI HARI STOCKOUT
# ==========================================================

plt.figure(figsize=(10, 6))

for lt in lead_times:

    data_lt = df[df["Lead_Time"] == lt]

    plt.plot(
        data_lt["Skenario"],
        data_lt["Hari_Stockout"],
        marker="o",
        linewidth=2,
        label=f"Lead Time {lt} Hari"
    )

plt.title(
    "Pengaruh Safety Stock terhadap Hari Stockout",
    fontsize=13
)

plt.xlabel("Skenario Safety Stock")
plt.ylabel("Jumlah Hari Stockout")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "14_sensitivitas_hari_stockout.png",
    dpi=300
)

plt.close()

# ==========================================================
# 7. INFORMASI HASIL
# ==========================================================

print("\n[2] GRAFIK BERHASIL DIBUAT")
print("-" * 75)

daftar_gambar = [
    "11_sensitivitas_lost_sales.png",
    "12_sensitivitas_fill_rate.png",
    "13_sensitivitas_rata_rata_persediaan.png",
    "14_sensitivitas_hari_stockout.png"
]

for nama_file in daftar_gambar:

    print(f"- {nama_file}")

print("\nLokasi penyimpanan:")
print(OUTPUT_DIR)

print("\n" + "=" * 75)
print("       VISUALISASI ANALISIS SENSITIVITAS SELESAI")
print("=" * 75)