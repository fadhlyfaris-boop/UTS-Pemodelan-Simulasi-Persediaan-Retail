import pandas as pd
import numpy as np
import math
from pathlib import Path

print("=" * 70)
print("       PERHITUNGAN PARAMETER KEBIJAKAN PERSEDIAAN")
print("                  DATA KALIBRASI 2022")
print("=" * 70)

# Lokasi folder
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "hasil_simulasi"

# Membaca data kalibrasi
df = pd.read_csv(OUTPUT_DIR / "data_kalibrasi.csv")
df["Date"] = pd.to_datetime(df["Date"])

demand = df["Units Sold"].astype(float)

# Parameter dasar
rata_rata_demand = demand.mean()
standar_deviasi = demand.std()
tingkat_persentil = 0.95

lead_times = [1, 2, 3]

hasil = []

print("\n[1] PARAMETER DASAR KALIBRASI")
print("-" * 70)
print(f"Jumlah pengamatan       : {len(df)} hari")
print(f"Rata-rata permintaan    : {rata_rata_demand:.2f} unit/hari")
print(f"Standar deviasi         : {standar_deviasi:.2f}")
print(f"Persentil               : {tingkat_persentil * 100:.0f}%")

print("\n[2] PERHITUNGAN LEAD TIME")
print("-" * 70)

for lt in lead_times:

    # Menghitung total permintaan selama lead time
    rolling_demand = (
        demand.rolling(window=lt)
        .sum()
        .dropna()
    )

    rata_rata_lt = rolling_demand.mean()

    # Reorder Point berdasarkan persentil empiris 95%
    rop = math.ceil(
        rolling_demand.quantile(tingkat_persentil)
    )

    # Target persediaan menggunakan persentil 95%
    target = math.ceil(
        rolling_demand.quantile(tingkat_persentil)
        + demand.mean()
    )

    safety_stock = rop - math.ceil(rata_rata_lt)

    hasil.append({
        "Lead_Time": lt,
        "Rata_Rata_Demand_Harian": rata_rata_demand,
        "Rata_Rata_Demand_Lead_Time": rata_rata_lt,
        "Safety_Stock": safety_stock,
        "Reorder_Point": rop,
        "Target_Persediaan": target
    })

    print(f"\nLead Time: {lt} hari")
    print(f"Rata-rata demand selama LT : {rata_rata_lt:.2f}")
    print(f"Safety Stock               : {safety_stock}")
    print(f"Reorder Point (ROP)        : {rop}")
    print(f"Target Persediaan (S)      : {target}")

# Menyimpan hasil
hasil_df = pd.DataFrame(hasil)

file_output = OUTPUT_DIR / "parameter_kalibrasi.csv"
hasil_df.to_csv(file_output, index=False)

print("\n[3] PENYIMPANAN HASIL")
print("-" * 70)
print(f"File berhasil disimpan: {file_output}")

print("\n" + "=" * 70)
print("          PERHITUNGAN PARAMETER SELESAI")
print("=" * 70)