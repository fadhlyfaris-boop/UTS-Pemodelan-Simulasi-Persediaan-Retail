import os
import pandas as pd

# =====================================================
# 1. KONFIGURASI
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "hasil_simulasi"
)

summary_path = os.path.join(
    OUTPUT_DIR,
    "ringkasan_simulasi.csv"
)

df = pd.read_csv(summary_path)

df = df.sort_values("Lead_Time").reset_index(drop=True)

# =====================================================
# 2. PERBANDINGAN KINERJA
# =====================================================

print("=" * 75)
print("              ANALISIS HASIL SIMULASI PERSEDIAAN")
print("=" * 75)

print("\n[1] PERBANDINGAN KINERJA SETIAP SKENARIO")
print("-" * 75)

columns = [
    "Lead_Time",
    "Total_Demand",
    "Total_Sales",
    "Total_Lost_Sales",
    "Service_Rate_Percent",
    "Average_Inventory",
    "Stockout_Days"
]

print(
    df[columns].to_string(
        index=False,
        float_format=lambda x: f"{x:,.2f}"
    )
)

# =====================================================
# 3. PERUBAHAN LOST SALES
# =====================================================

print("\n[2] ANALISIS PERUBAHAN LOST SALES")
print("-" * 75)

baseline_lost = df.loc[0, "Total_Lost_Sales"]

for i in range(len(df)):

    lead_time = int(df.loc[i, "Lead_Time"])

    lost_sales = df.loc[i, "Total_Lost_Sales"]

    if baseline_lost > 0:

        increase = (
            (lost_sales - baseline_lost)
            / baseline_lost
        ) * 100

    else:

        increase = 0

    print(
        f"Lead Time {lead_time} hari: "
        f"{lost_sales:.2f} unit "
        f"({increase:+.2f}% dibanding LT 1)"
    )

# =====================================================
# 4. ANALISIS RATA-RATA PERSEDIAAN
# =====================================================

print("\n[3] ANALISIS RATA-RATA PERSEDIAAN")
print("-" * 75)

baseline_inventory = df.loc[0, "Average_Inventory"]

for i in range(len(df)):

    lead_time = int(df.loc[i, "Lead_Time"])

    inventory = df.loc[i, "Average_Inventory"]

    difference = inventory - baseline_inventory

    print(
        f"Lead Time {lead_time} hari: "
        f"{inventory:.2f} unit "
        f"(selisih {difference:+.2f} unit dibanding LT 1)"
    )

# =====================================================
# 5. ANALISIS TINGKAT PEMENUHAN
# =====================================================

print("\n[4] ANALISIS TINGKAT PEMENUHAN PERMINTAAN")
print("-" * 75)

for _, row in df.iterrows():

    print(
        f"Lead Time {int(row['Lead_Time'])} hari: "
        f"{row['Service_Rate_Percent']:.2f}%"
    )

# =====================================================
# 6. IDENTIFIKASI HASIL TERBAIK BERDASARKAN INDIKATOR
# =====================================================

print("\n[5] IDENTIFIKASI HASIL TERBAIK")
print("-" * 75)

best_service = df.loc[
    df["Service_Rate_Percent"].idxmax()
]

lowest_lost_sales = df.loc[
    df["Total_Lost_Sales"].idxmin()
]

lowest_inventory = df.loc[
    df["Average_Inventory"].idxmin()
]

print(
    "Tingkat pemenuhan tertinggi : "
    f"Lead Time {int(best_service['Lead_Time'])} hari"
)

print(
    "Lost sales terendah        : "
    f"Lead Time {int(lowest_lost_sales['Lead_Time'])} hari"
)

print(
    "Rata-rata persediaan terendah: "
    f"Lead Time {int(lowest_inventory['Lead_Time'])} hari"
)

# =====================================================
# 7. MENYIMPAN HASIL ANALISIS
# =====================================================

analysis_path = os.path.join(
    OUTPUT_DIR,
    "analisis_perbandingan.csv"
)

df[columns].to_csv(
    analysis_path,
    index=False
)

print("\n[6] FILE HASIL")
print("-" * 75)

print("Analisis disimpan di:")
print(analysis_path)

print("\n" + "=" * 75)
print("                 ANALISIS SELESAI")
print("=" * 75)