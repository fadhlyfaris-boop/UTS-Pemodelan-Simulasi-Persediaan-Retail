import pandas as pd
import math
from pathlib import Path

print("=" * 70)
print("       SIMULASI PERSEDIAAN RETAIL - DATA PENGUJIAN")
print("=" * 70)

# ==========================================================
# 1. PERSIAPAN LOKASI DAN DATA
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "hasil_simulasi"

data = pd.read_csv(OUTPUT_DIR / "data_pengujian.csv")
parameter = pd.read_csv(OUTPUT_DIR / "parameter_kalibrasi.csv")

data["Date"] = pd.to_datetime(data["Date"])
data = data.sort_values("Date").reset_index(drop=True)

print("\n[1] INFORMASI DATA PENGUJIAN")
print("-" * 70)
print(f"Jumlah hari       : {len(data)}")
print(f"Tanggal awal      : {data['Date'].min().date()}")
print(f"Tanggal akhir     : {data['Date'].max().date()}")

# Persediaan awal menggunakan inventory aktual pada
# tanggal pertama periode pengujian.
persediaan_awal = int(data.iloc[0]["Inventory Level"])

print(f"Persediaan awal   : {persediaan_awal} unit")

# ==========================================================
# 2. FUNGSI MESIN SIMULASI
# ==========================================================

def jalankan_simulasi(lead_time, rop, target):

    inventory = persediaan_awal
    pipeline = []

    hasil = []

    total_demand = 0
    total_sales = 0
    total_lost_sales = 0
    total_order = 0
    total_arrival = 0
    jumlah_pemesanan = 0
    stockout_days = 0

    for index, row in data.iterrows():

        tanggal = row["Date"]
        demand = int(row["Units Sold"])

        # Mencatat persediaan sebelum pesanan datang
        inventory_before_arrival = inventory

        # --------------------------------------------------
        # A. PENERIMAAN PESANAN YANG TELAH TIBA
        # --------------------------------------------------

        arrivals_today = 0
        remaining_pipeline = []

        for order in pipeline:

            if order["arrival_day"] == index:
                arrivals_today += order["quantity"]
            else:
                remaining_pipeline.append(order)

        pipeline = remaining_pipeline

        inventory += arrivals_today
        total_arrival += arrivals_today

        # --------------------------------------------------
        # B. PEMENUHAN PERMINTAAN
        # --------------------------------------------------

        available_inventory = inventory

        actual_sales = min(inventory, demand)
        lost_sales = demand - actual_sales

        inventory -= actual_sales

        if lost_sales > 0:
            stockout_days += 1

        # --------------------------------------------------
        # C. MENGHITUNG POSISI PERSEDIAAN
        # --------------------------------------------------

        outstanding_orders = sum(
            order["quantity"] for order in pipeline
        )

        inventory_position = inventory + outstanding_orders

        order_quantity = 0

        # --------------------------------------------------
        # D. KEBIJAKAN PEMESANAN (s, S)
        # --------------------------------------------------

        if inventory_position <= rop:

            order_quantity = max(
                0,
                target - inventory_position
            )

            if order_quantity > 0:

                arrival_day = index + lead_time

                pipeline.append({
                    "quantity": order_quantity,
                    "arrival_day": arrival_day
                })

                total_order += order_quantity
                jumlah_pemesanan += 1

        # --------------------------------------------------
        # E. PENYIMPANAN HASIL HARIAN
        # --------------------------------------------------

        hasil.append({
            "Date": tanggal,
            "Lead_Time": lead_time,
            "Demand": demand,
            "Persediaan_Awal_Hari": inventory_before_arrival,
            "Persediaan_Tersedia": available_inventory,
            "Actual_Sales": actual_sales,
            "Lost_Sales": lost_sales,
            "Persediaan_Akhir": inventory,
            "Outstanding_Order": outstanding_orders,
            "Order_Quantity": order_quantity,
            "Arrival_Quantity": arrivals_today
        })

        total_demand += demand
        total_sales += actual_sales
        total_lost_sales += lost_sales

    # ======================================================
    # 3. PERHITUNGAN INDIKATOR KINERJA
    # ======================================================

    fill_rate = (
        total_sales / total_demand * 100
        if total_demand > 0 else 0
    )

    average_inventory = sum(
        item["Persediaan_Akhir"] for item in hasil
    ) / len(hasil)

    ringkasan = {
        "Lead_Time": lead_time,
        "ROP": rop,
        "Target_Persediaan": target,
        "Persediaan_Awal": persediaan_awal,
        "Total_Demand": total_demand,
        "Total_Sales": total_sales,
        "Lost_Sales": total_lost_sales,
        "Fill_Rate_Persen": fill_rate,
        "Rata_Rata_Persediaan": average_inventory,
        "Total_Order": total_order,
        "Jumlah_Pemesanan": jumlah_pemesanan,
        "Total_Produk_Diterima": total_arrival,
        "Hari_Stockout": stockout_days
    }

    return pd.DataFrame(hasil), ringkasan


# ==========================================================
# 4. MENJALANKAN TIGA SKENARIO
# ==========================================================

print("\n[2] MENJALANKAN SKENARIO SIMULASI")
print("-" * 70)

seluruh_ringkasan = []

for _, param in parameter.iterrows():

    lt = int(param["Lead_Time"])
    rop = int(param["Reorder_Point"])
    target = int(param["Target_Persediaan"])

    print(f"\nMemproses Lead Time {lt} hari...")

    hasil_harian, ringkasan = jalankan_simulasi(
        lead_time=lt,
        rop=rop,
        target=target
    )

    nama_file = (
        OUTPUT_DIR /
        f"hasil_uji_lead_time_{lt}_hari.csv"
    )

    hasil_harian.to_csv(nama_file, index=False)

    seluruh_ringkasan.append(ringkasan)

    print(f"ROP                 : {rop}")
    print(f"Target Persediaan   : {target}")
    print(f"Total Demand        : {ringkasan['Total_Demand']}")
    print(f"Total Sales         : {ringkasan['Total_Sales']}")
    print(f"Lost Sales          : {ringkasan['Lost_Sales']}")
    print(f"Fill Rate           : {ringkasan['Fill_Rate_Persen']:.2f}%")
    print(f"Rata-rata Inventory : {ringkasan['Rata_Rata_Persediaan']:.2f}")
    print(f"Hari Stockout       : {ringkasan['Hari_Stockout']}")

# ==========================================================
# 5. MENYIMPAN RINGKASAN
# ==========================================================

ringkasan_df = pd.DataFrame(seluruh_ringkasan)

file_ringkasan = OUTPUT_DIR / "ringkasan_uji_simulasi.csv"

ringkasan_df.to_csv(file_ringkasan, index=False)

print("\n[3] RINGKASAN PERBANDINGAN")
print("-" * 70)

kolom = [
    "Lead_Time",
    "ROP",
    "Target_Persediaan",
    "Total_Demand",
    "Total_Sales",
    "Lost_Sales",
    "Fill_Rate_Persen",
    "Rata_Rata_Persediaan",
    "Hari_Stockout"
]

print(ringkasan_df[kolom].to_string(index=False))

print("\n" + "=" * 70)
print("             SIMULASI PENGUJIAN SELESAI")
print("=" * 70)

print(f"\nRingkasan disimpan di: {file_ringkasan}")