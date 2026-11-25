import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "hasil_simulasi"
)

lead_times = [1, 2, 3]

print("=" * 75)
print("             VALIDASI HASIL SIMULASI PERSEDIAAN")
print("=" * 75)

for lead_time in lead_times:

    filename = f"simulasi_lead_time_{lead_time}_hari.csv"

    path = os.path.join(OUTPUT_DIR, filename)

    df = pd.read_csv(path)

    # ==============================================
    # 1. VALIDASI JUMLAH DATA
    # ==============================================

    total_rows = len(df)

    # ==============================================
    # 2. VALIDASI KESEIMBANGAN PERSEDIAAN
    # ==============================================

    calculated_ending = (
        df["Beginning_Inventory"] - df["Sales"]
    )

    balance_difference = (
        calculated_ending - df["Ending_Inventory"]
    ).abs()

    balance_errors = (
        balance_difference > 0.000001
    ).sum()

    # ==============================================
    # 3. VALIDASI PERSEDIAAN NEGATIF
    # ==============================================

    negative_inventory = (
        df["Ending_Inventory"] < 0
    ).sum()

    # ==============================================
    # 4. VALIDASI PESANAN DAN KEDATANGAN
    # ==============================================

    total_orders = df["Order_Quantity"].sum()

    total_arrivals = df["Arrivals"].sum()

    pending_orders = total_orders - total_arrivals

    # ==============================================
    # 5. VALIDASI LOST SALES
    # ==============================================

    calculated_lost_sales = (
        df["Demand"] - df["Sales"]
    )

    lost_sales_difference = (
        calculated_lost_sales - df["Lost_Sales"]
    ).abs().sum()

    # ==============================================
    # 6. HASIL VALIDASI
    # ==============================================

    print("\n" + "-" * 75)
    print(f"SKENARIO LEAD TIME {lead_time} HARI")
    print("-" * 75)

    print(f"Jumlah baris data              : {total_rows}")

    print(f"Kesalahan keseimbangan stok    : {balance_errors}")

    print(f"Persediaan negatif             : {negative_inventory}")

    print(f"Total pemesanan                : {total_orders:.2f}")

    print(f"Total barang datang            : {total_arrivals:.2f}")

    print(f"Pesanan belum datang           : {pending_orders:.2f}")

    print(f"Kesalahan perhitungan lost sale: {lost_sales_difference:.6f}")

    # ==============================================
    # 7. STATUS
    # ==============================================

    valid = (
        total_rows == 731
        and balance_errors == 0
        and negative_inventory == 0
        and abs(lost_sales_difference) < 0.000001
        and pending_orders >= -0.000001
    )

    print("\nSTATUS VALIDASI:", "LOLOS" if valid else "PERLU DIPERIKSA")

print("\n" + "=" * 75)
print("                 VALIDASI SELESAI")
print("=" * 75)