import pandas as pd
from pathlib import Path

print("=" * 75)
print("          ANALISIS PERBANDINGAN HASIL SIMULASI PENGUJIAN")
print("=" * 75)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "hasil_simulasi"

hasil = []

for lt in [1, 2, 3]:

    file_input = OUTPUT_DIR / f"hasil_uji_lead_time_{lt}_hari.csv"

    df = pd.read_csv(file_input)

    total_demand = df["Demand"].sum()
    total_sales = df["Actual_Sales"].sum()
    total_lost_sales = df["Lost_Sales"].sum()

    fill_rate = (
        total_sales / total_demand * 100
        if total_demand > 0 else 0
    )

    rata_persediaan = df["Persediaan_Akhir"].mean()

    hari_stockout = (
        df["Lost_Sales"] > 0
    ).sum()

    total_order = df["Order_Quantity"].sum()
    total_arrival = df["Arrival_Quantity"].sum()

    hasil.append({
        "Lead_Time": lt,
        "Total_Demand": total_demand,
        "Total_Sales": total_sales,
        "Lost_Sales": total_lost_sales,
        "Fill_Rate_Persen": fill_rate,
        "Rata_Rata_Persediaan": rata_persediaan,
        "Hari_Stockout": hari_stockout,
        "Total_Order": total_order,
        "Total_Arrival": total_arrival
    })

df_hasil = pd.DataFrame(hasil)

print("\n[1] TABEL PERBANDINGAN KINERJA SIMULASI")
print("-" * 75)

print(
    df_hasil.to_string(
        index=False,
        formatters={
            "Fill_Rate_Persen": "{:.2f}%".format,
            "Rata_Rata_Persediaan": "{:.2f}".format
        }
    )
)

# Perbandingan perubahan terhadap Lead Time 1 hari
print("\n[2] PERUBAHAN LOST SALES TERHADAP LEAD TIME 1 HARI")
print("-" * 75)

lost_awal = df_hasil.loc[
    df_hasil["Lead_Time"] == 1,
    "Lost_Sales"
].iloc[0]

for _, row in df_hasil.iterrows():

    if lost_awal > 0:
        perubahan = (
            (row["Lost_Sales"] - lost_awal)
            / lost_awal * 100
        )
    else:
        perubahan = 0

    print(
        f"Lead Time {int(row['Lead_Time'])} hari: "
        f"{perubahan:+.2f}%"
    )

# Perbandingan perubahan rata-rata persediaan
print("\n[3] PERUBAHAN RATA-RATA PERSEDIAAN")
print("-" * 75)

persediaan_awal = df_hasil.loc[
    df_hasil["Lead_Time"] == 1,
    "Rata_Rata_Persediaan"
].iloc[0]

for _, row in df_hasil.iterrows():

    if persediaan_awal > 0:
        perubahan = (
            (row["Rata_Rata_Persediaan"] - persediaan_awal)
            / persediaan_awal * 100
        )
    else:
        perubahan = 0

    print(
        f"Lead Time {int(row['Lead_Time'])} hari: "
        f"{perubahan:+.2f}%"
    )

# Menentukan skenario dengan kinerja tertentu
print("\n[4] IDENTIFIKASI HASIL SIMULASI")
print("-" * 75)

terbaik_lost = df_hasil.loc[
    df_hasil["Lost_Sales"].idxmin()
]

terbaik_fill = df_hasil.loc[
    df_hasil["Fill_Rate_Persen"].idxmax()
]

print(
    f"Lost sales terendah       : "
    f"Lead Time {int(terbaik_lost['Lead_Time'])} hari"
)

print(
    f"Fill rate tertinggi       : "
    f"Lead Time {int(terbaik_fill['Lead_Time'])} hari"
)

# Simpan hasil analisis
file_output = OUTPUT_DIR / "analisis_perbandingan_uji.csv"

df_hasil.to_csv(file_output, index=False)

print("\n[5] PENYIMPANAN HASIL")
print("-" * 75)
print(f"Hasil analisis disimpan: {file_output}")

print("\n" + "=" * 75)
print("ANALISIS PERBANDINGAN SELESAI")
print("=" * 75)