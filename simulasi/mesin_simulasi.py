import os
import pandas as pd
import math

# =========================================================
# 1. KONFIGURASI DIREKTORI
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DATA_DIR = os.path.join(PROJECT_DIR, "dataset")
OUTPUT_DIR = os.path.join(BASE_DIR, "hasil_simulasi")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# 2. MEMUAT DATA
# =========================================================

data_path = os.path.join(
    DATA_DIR,
    "data_objek_simulasi.csv"
)

df = pd.read_csv(data_path)

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# =========================================================
# 3. MENENTUKAN PARAMETER MODEL
# =========================================================

demand = df["Units Sold"].astype(float)

service_level = 0.95

# Persediaan awal menggunakan data hari pertama
initial_inventory = float(df.loc[0, "Inventory Level"])

lead_times = [1, 2, 3]

print("=" * 75)
print("              MESIN SIMULASI SISTEM PERSEDIAAN RETAIL")
print("=" * 75)

print(f"\nJumlah hari simulasi : {len(df)}")
print(f"Tanggal awal         : {df['Date'].min().date()}")
print(f"Tanggal akhir        : {df['Date'].max().date()}")
print(f"Persediaan awal      : {initial_inventory:.2f} unit")

# =========================================================
# 4. FUNGSI SIMULASI
# =========================================================

def jalankan_simulasi(lead_time):

    # Menghitung ROP berdasarkan permintaan selama lead time
    demand_lead = (
        demand.rolling(window=lead_time)
        .sum()
        .dropna()
    )

    reorder_point = math.ceil(
        demand_lead.quantile(service_level)
    )

    # Menghitung target persediaan berdasarkan
    # permintaan selama lead time + 1 hari
    demand_review = (
        demand.rolling(window=lead_time + 1)
        .sum()
        .dropna()
    )

    order_up_to_level = math.ceil(
        demand_review.quantile(service_level)
    )

    # Stok awal simulasi
    inventory = initial_inventory

    # Daftar pesanan yang belum datang
    pipeline = {}

    # Catatan hasil harian
    records = []

    total_demand = 0
    total_sales = 0
    total_lost_sales = 0
    total_ordered = 0
    total_arrivals = 0
    stockout_days = 0
    order_count = 0

    # =====================================================
    # SIMULASI HARIAN
    # =====================================================

    for day in range(len(df)):

        date = df.loc[day, "Date"]
        daily_demand = float(demand.iloc[day])

        # ---------------------------------------------
        # A. BARANG PESANAN DATANG
        # ---------------------------------------------

        arrivals = pipeline.pop(day, 0.0)

        inventory += arrivals

        # ---------------------------------------------
        # B. PERMINTAAN PELANGGAN
        # ---------------------------------------------

        beginning_inventory = inventory

        sales = min(inventory, daily_demand)

        lost_sales = daily_demand - sales

        inventory -= sales

        # ---------------------------------------------
        # C. MENGHITUNG POSISI PERSEDIAAN
        # ---------------------------------------------

        outstanding_orders = sum(pipeline.values())

        inventory_position = (
            inventory + outstanding_orders
        )

        # ---------------------------------------------
        # D. KEBIJAKAN PEMESANAN ULANG (s, S)
        # ---------------------------------------------

        order_quantity = 0.0

        if inventory_position <= reorder_point:

            order_quantity = max(
                0.0,
                order_up_to_level - inventory_position
            )

            if order_quantity > 0:

                arrival_day = day + lead_time

                # Pesanan yang datang setelah periode
                # simulasi tidak dimasukkan ke penerimaan
                if arrival_day < len(df):

                    pipeline[arrival_day] = (
                        pipeline.get(arrival_day, 0.0)
                        + order_quantity
                    )

                else:

                    # Tetap dicatat sebagai pesanan terbuka
                    pipeline[arrival_day] = (
                        pipeline.get(arrival_day, 0.0)
                        + order_quantity
                    )

        # ---------------------------------------------
        # E. POSISI PERSEDIAAN SETELAH PEMESANAN
        # ---------------------------------------------

        outstanding_after_order = sum(pipeline.values())

        inventory_position_after_order = (
            inventory + outstanding_after_order
        )

        # ---------------------------------------------
        # F. MENYIMPAN CATATAN HARIAN
        # ---------------------------------------------

        records.append({

            "Date": date,

            "Lead_Time": lead_time,

            "Beginning_Inventory": beginning_inventory,

            "Arrivals": arrivals,

            "Demand": daily_demand,

            "Sales": sales,

            "Lost_Sales": lost_sales,

            "Ending_Inventory": inventory,

            "Reorder_Point": reorder_point,

            "Order_Up_To_Level": order_up_to_level,

            "Order_Quantity": order_quantity,

            "Outstanding_Orders": outstanding_after_order,

            "Inventory_Position": inventory_position_after_order

        })

        # ---------------------------------------------
        # G. AKUMULASI STATISTIK
        # ---------------------------------------------

        total_demand += daily_demand
        total_sales += sales
        total_lost_sales += lost_sales
        total_ordered += order_quantity
        total_arrivals += arrivals

        if lost_sales > 0:
            stockout_days += 1

        if order_quantity > 0:
            order_count += 1

    # =====================================================
    # 5. MENYIMPAN HASIL SIMULASI
    # =====================================================

    result = pd.DataFrame(records)

    filename = f"simulasi_lead_time_{lead_time}_hari.csv"

    output_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    result.to_csv(output_path, index=False)

    # =====================================================
    # 6. MENGHITUNG INDIKATOR KINERJA
    # =====================================================

    service_rate = (
        total_sales / total_demand * 100
        if total_demand > 0 else 0
    )

    lost_sales_rate = (
        total_lost_sales / total_demand * 100
        if total_demand > 0 else 0
    )

    average_inventory = result[
        "Ending_Inventory"
    ].mean()

    ending_inventory = result[
        "Ending_Inventory"
    ].iloc[-1]

    summary = {

        "Lead_Time": lead_time,

        "Initial_Inventory": initial_inventory,

        "Reorder_Point": reorder_point,

        "Order_Up_To_Level": order_up_to_level,

        "Total_Demand": total_demand,

        "Total_Sales": total_sales,

        "Total_Lost_Sales": total_lost_sales,

        "Service_Rate_Percent": service_rate,

        "Lost_Sales_Rate_Percent": lost_sales_rate,

        "Average_Inventory": average_inventory,

        "Ending_Inventory": ending_inventory,

        "Total_Order_Quantity": total_ordered,

        "Total_Arrivals": total_arrivals,

        "Order_Count": order_count,

        "Stockout_Days": stockout_days

    }

    return summary


# =========================================================
# 7. MENJALANKAN TIGA SKENARIO
# =========================================================

all_summaries = []

for lead_time in lead_times:

    print("\n" + "=" * 75)
    print(f"SIMULASI LEAD TIME {lead_time} HARI")
    print("=" * 75)

    summary = jalankan_simulasi(lead_time)

    all_summaries.append(summary)

    print(f"Reorder Point          : {summary['Reorder_Point']:.2f}")
    print(f"Target Persediaan      : {summary['Order_Up_To_Level']:.2f}")
    print(f"Total Permintaan       : {summary['Total_Demand']:.2f}")
    print(f"Total Penjualan        : {summary['Total_Sales']:.2f}")
    print(f"Total Lost Sales       : {summary['Total_Lost_Sales']:.2f}")
    print(f"Tingkat Pemenuhan      : {summary['Service_Rate_Percent']:.2f}%")
    print(f"Rata-rata Persediaan   : {summary['Average_Inventory']:.2f}")
    print(f"Jumlah Pemesanan       : {summary['Order_Count']}")
    print(f"Hari Kehabisan Stok    : {summary['Stockout_Days']}")

# =========================================================
# 8. MENYIMPAN RINGKASAN
# =========================================================

summary_df = pd.DataFrame(all_summaries)

summary_path = os.path.join(
    OUTPUT_DIR,
    "ringkasan_simulasi.csv"
)

summary_df.to_csv(summary_path, index=False)

# =========================================================
# 9. SELESAI
# =========================================================

print("\n" + "=" * 75)
print("                 SIMULASI SELESAI")
print("=" * 75)

print("\nFile hasil simulasi tersimpan di:")

print(OUTPUT_DIR)

print("\nFile yang dihasilkan:")

for lead_time in lead_times:

    print(f"- simulasi_lead_time_{lead_time}_hari.csv")

print("- ringkasan_simulasi.csv")

print("\n" + "=" * 75)