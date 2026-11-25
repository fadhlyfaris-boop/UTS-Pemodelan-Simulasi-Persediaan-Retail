import pandas as pd
import math
from pathlib import Path

print("=" * 75)
print("             ANALISIS SENSITIVITAS PERSEDIAAN")
print("=" * 75)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "hasil_simulasi"

# Membaca data pengujian dan parameter kalibrasi
data = pd.read_csv(OUTPUT_DIR / "data_pengujian.csv")
parameter = pd.read_csv(OUTPUT_DIR / "parameter_kalibrasi.csv")

data["Date"] = pd.to_datetime(data["Date"])
data = data.sort_values("Date").reset_index(drop=True)

# Tingkat Safety Stock yang diuji
skenario = {
    "Rendah": 0.80,
    "Baseline": 1.00,
    "Tinggi": 1.20
}

hasil = []

# Persediaan awal menggunakan observasi hari pertama pengujian
persediaan_awal = int(data.iloc[0]["Inventory Level"])

for _, param in parameter.iterrows():

    lt = int(param["Lead_Time"])

    rata_demand_harian = float(
        param["Rata_Rata_Demand_Harian"]
    )

    rata_demand_lt = float(
        param["Rata_Rata_Demand_Lead_Time"]
    )

    safety_stock_dasar = float(
        param["Safety_Stock"]
    )

    for nama_skenario, faktor in skenario.items():

        # Mengubah Safety Stock berdasarkan skenario
        safety_stock = math.ceil(
            safety_stock_dasar * faktor
        )

        # Menghitung ROP dan target persediaan
        rop = math.ceil(
            rata_demand_lt + safety_stock
        )

        # Menyesuaikan target berdasarkan perubahan ROP
        rop_dasar = int(param["Reorder_Point"])
        target_dasar = int(param["Target_Persediaan"])

        target = math.ceil(
            target_dasar + (rop - rop_dasar)
        )

        inventory = persediaan_awal
        pipeline = []

        catatan = []

        for index, row in data.iterrows():

            demand = int(row["Units Sold"])

            # Persediaan sebelum kedatangan
            inventory_before_arrival = inventory

            # Memproses pesanan yang tiba hari ini
            arrivals = [
                order for order in pipeline
                if order["arrival_day"] == index
            ]

            arrival_quantity = sum(
                order["quantity"] for order in arrivals
            )

            inventory += arrival_quantity

            # Menghapus pesanan yang sudah tiba
            pipeline = [
                order for order in pipeline
                if order["arrival_day"] != index
            ]

            # Persediaan tersedia setelah kedatangan
            inventory_available = inventory

            # Memenuhi permintaan
            actual_sales = min(inventory, demand)

            lost_sales = demand - actual_sales

            inventory -= actual_sales

            # Posisi persediaan sebelum pesanan baru
            inventory_position = (
                inventory
                + sum(order["quantity"] for order in pipeline)
            )

            # Outstanding order dicatat setelah kedatangan
            outstanding_order = sum(
                order["quantity"] for order in pipeline
            )

            # Kebijakan pemesanan ulang
            order_quantity = 0

            if inventory_position <= rop:

                order_quantity = max(
                    0,
                    target - inventory_position
                )

                if order_quantity > 0:

                    pipeline.append({
                        "quantity": order_quantity,
                        "arrival_day": index + lt
                    })

            # Mencatat hasil harian
            catatan.append({
                "Date": row["Date"],
                "Lead_Time": lt,
                "Skenario": nama_skenario,
                "Demand": demand,
                "Persediaan_Awal_Hari": inventory_before_arrival,
                "Persediaan_Tersedia": inventory_available,
                "Actual_Sales": actual_sales,
                "Lost_Sales": lost_sales,
                "Persediaan_Akhir": inventory,
                "Outstanding_Order": outstanding_order,
                "Order_Quantity": order_quantity,
                "Arrival_Quantity": arrival_quantity
            })

        # Mengubah catatan simulasi menjadi DataFrame
        df = pd.DataFrame(catatan)

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

        error_saldo = (
            df["Persediaan_Awal_Hari"]
            + df["Arrival_Quantity"]
            - df["Actual_Sales"]
            - df["Persediaan_Akhir"]
        ).abs().sum()

        hasil.append({
            "Lead_Time": lt,
            "Skenario": nama_skenario,
            "Faktor_Safety_Stock": faktor,
            "Safety_Stock": safety_stock,
            "ROP": rop,
            "Target_Persediaan": target,
            "Total_Demand": total_demand,
            "Total_Sales": total_sales,
            "Lost_Sales": total_lost_sales,
            "Fill_Rate_Persen": fill_rate,
            "Rata_Rata_Persediaan": rata_persediaan,
            "Hari_Stockout": hari_stockout,
            "Error_Saldo": error_saldo
        })

        # Menyimpan detail simulasi setiap skenario
        nama_file = (
            f"sensitivitas_lt_{lt}_{nama_skenario.lower()}.csv"
        )

        df.to_csv(
            OUTPUT_DIR / nama_file,
            index=False
        )

# Membuat tabel ringkasan
df_hasil = pd.DataFrame(hasil)

print("\n[1] HASIL ANALISIS SENSITIVITAS")
print("-" * 75)

print(
    df_hasil[
        [
            "Lead_Time",
            "Skenario",
            "Safety_Stock",
            "ROP",
            "Lost_Sales",
            "Fill_Rate_Persen",
            "Rata_Rata_Persediaan",
            "Hari_Stockout",
            "Error_Saldo"
        ]
    ].to_string(
        index=False,
        formatters={
            "Fill_Rate_Persen": "{:.2f}%".format,
            "Rata_Rata_Persediaan": "{:.2f}".format
        }
    )
)

# Memeriksa keseimbangan persediaan
print("\n[2] PEMERIKSAAN KESEIMBANGAN PERSEDIAAN")
print("-" * 75)

if (df_hasil["Error_Saldo"] == 0).all():
    print("SELURUH SKENARIO: LULUS")
else:
    print("PERINGATAN: TERDAPAT KETIDAKSEIMBANGAN SALDO")

# Menyimpan hasil ringkasan
file_output = OUTPUT_DIR / "hasil_analisis_sensitivitas.csv"

df_hasil.to_csv(file_output, index=False)

print("\n[3] PENYIMPANAN HASIL")
print("-" * 75)

print(f"Ringkasan: {file_output}")
print("Detail simulasi 9 skenario berhasil disimpan.")

print("\n" + "=" * 75)
print("ANALISIS SENSITIVITAS SELESAI")
print("=" * 75)