import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

print("=" * 70)
print("       VISUALISASI HASIL SIMULASI PENGUJIAN")
print("=" * 70)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "hasil_simulasi"

OUTPUT_DIR.mkdir(exist_ok=True)

# Membaca ringkasan hasil simulasi
ringkasan = pd.read_csv(
    OUTPUT_DIR / "ringkasan_uji_simulasi.csv"
)

# Membaca hasil harian setiap skenario
data = {}

for lt in [1, 2, 3]:
    df = pd.read_csv(
        OUTPUT_DIR / f"hasil_uji_lead_time_{lt}_hari.csv"
    )

    df["Date"] = pd.to_datetime(df["Date"])
    data[lt] = df


# ==========================================================
# 1. GRAFIK TREN PERSEDIAAN
# ==========================================================

plt.figure(figsize=(14, 6))

for lt in [1, 2, 3]:
    plt.plot(
        data[lt]["Date"],
        data[lt]["Persediaan_Akhir"],
        label=f"Lead Time {lt} Hari",
        alpha=0.85
    )

plt.title("Perbandingan Tren Persediaan Antar Skenario")
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Persediaan (Unit)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "06_tren_persediaan_uji.png",
    dpi=300
)

plt.close()


# ==========================================================
# 2. GRAFIK PERBANDINGAN LOST SALES
# ==========================================================

plt.figure(figsize=(9, 6))

plt.bar(
    ringkasan["Lead_Time"].astype(str) + " Hari",
    ringkasan["Lost_Sales"]
)

plt.title("Perbandingan Lost Sales")
plt.xlabel("Lead Time")
plt.ylabel("Jumlah Lost Sales (Unit)")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "07_perbandingan_lost_sales_uji.png",
    dpi=300
)

plt.close()


# ==========================================================
# 3. GRAFIK FILL RATE
# ==========================================================

plt.figure(figsize=(9, 6))

plt.bar(
    ringkasan["Lead_Time"].astype(str) + " Hari",
    ringkasan["Fill_Rate_Persen"]
)

plt.title("Perbandingan Fill Rate")
plt.xlabel("Lead Time")
plt.ylabel("Fill Rate (%)")
plt.ylim(0, 105)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "08_perbandingan_fill_rate_uji.png",
    dpi=300
)

plt.close()


# ==========================================================
# 4. GRAFIK RATA-RATA PERSEDIAAN
# ==========================================================

plt.figure(figsize=(9, 6))

plt.bar(
    ringkasan["Lead_Time"].astype(str) + " Hari",
    ringkasan["Rata_Rata_Persediaan"]
)

plt.title("Perbandingan Rata-rata Persediaan")
plt.xlabel("Lead Time")
plt.ylabel("Rata-rata Persediaan (Unit)")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "09_rata_rata_persediaan_uji.png",
    dpi=300
)

plt.close()


# ==========================================================
# 5. GRAFIK PERMINTAAN DAN PENJUALAN
# ==========================================================

plt.figure(figsize=(14, 6))

for lt in [1, 2, 3]:
    plt.plot(
        data[lt]["Date"],
        data[lt]["Actual_Sales"],
        label=f"Penjualan LT {lt} Hari",
        alpha=0.7
    )

plt.plot(
    data[1]["Date"],
    data[1]["Demand"],
    label="Permintaan",
    color="black",
    linestyle="--",
    alpha=0.7
)

plt.title("Perbandingan Permintaan dan Penjualan Aktual")
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Unit")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "10_permintaan_penjualan_uji.png",
    dpi=300
)

plt.close()


# ==========================================================
# 6. INFORMASI HASIL
# ==========================================================

print("\nGrafik berhasil dibuat:")

daftar_grafik = [
    "06_tren_persediaan_uji.png",
    "07_perbandingan_lost_sales_uji.png",
    "08_perbandingan_fill_rate_uji.png",
    "09_rata_rata_persediaan_uji.png",
    "10_permintaan_penjualan_uji.png"
]

for nama in daftar_grafik:
    print(f"- {nama}")

print("\n" + "=" * 70)
print("          VISUALISASI SELESAI")
print("=" * 70)