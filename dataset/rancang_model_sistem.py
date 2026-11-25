import os
import pandas as pd

# =========================================================
# 1. MEMUAT DATA
# =========================================================

base_dir = os.path.dirname(__file__)

data_path = os.path.join(
    base_dir,
    "data_objek_simulasi.csv"
)

df = pd.read_csv(data_path)

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

demand = df["Units Sold"]

# =========================================================
# 2. PARAMETER DASAR
# =========================================================

service_level = 0.95

initial_inventory = df["Inventory Level"].mean()

average_demand = demand.mean()

average_order = df["Units Ordered"].mean()

lead_times = [1, 2, 3]

results = []

print("=" * 70)
print("       PERANCANGAN KEBIJAKAN PERSEDIAAN SISTEM RETAIL")
print("=" * 70)

print("\n[1] PARAMETER DASAR")
print("-" * 70)

print(f"Persediaan awal rata-rata : {initial_inventory:.2f}")
print(f"Permintaan rata-rata      : {average_demand:.2f}")
print(f"Rata-rata pemesanan       : {average_order:.2f}")
print(f"Tingkat layanan target    : {service_level * 100:.0f}%")

# =========================================================
# 3. PERHITUNGAN KEBIJAKAN (s, S)
# =========================================================

print("\n[2] HASIL KEBIJAKAN PEMESANAN")
print("-" * 70)

for lead_time in lead_times:

    # Permintaan selama lead time
    demand_lead = (
        demand
        .rolling(window=lead_time)
        .sum()
        .dropna()
    )

    # Permintaan selama lead time + 1 hari
    demand_review = (
        demand
        .rolling(window=lead_time + 1)
        .sum()
        .dropna()
    )

    # Reorder Point
    reorder_point = demand_lead.quantile(service_level)

    # Target persediaan setelah pemesanan
    order_up_to_level = demand_review.quantile(service_level)

    # Safety Stock
    safety_stock = max(
        0,
        reorder_point - demand_lead.mean()
    )

    # Status persediaan awal
    if initial_inventory <= reorder_point:
        status = "PERLU PEMESANAN ULANG"
    else:
        status = "PERSediaan DI ATAS ROP"

    results.append({
        "Lead_Time": lead_time,
        "Average_Demand": average_demand,
        "Safety_Stock": safety_stock,
        "Reorder_Point": reorder_point,
        "Order_Up_To_Level": order_up_to_level,
        "Initial_Inventory": initial_inventory,
        "Average_Order_Historical": average_order
    })

    print(f"\nLead Time: {lead_time} hari")
    print(f"Safety Stock          : {safety_stock:.2f}")
    print(f"Reorder Point (s)     : {reorder_point:.2f}")
    print(f"Target Persediaan (S) : {order_up_to_level:.2f}")
    print(f"Status Persediaan     : {status}")

# =========================================================
# 4. MENYIMPAN HASIL
# =========================================================

result_df = pd.DataFrame(results)

output_path = os.path.join(
    base_dir,
    "kebijakan_pemesanan.csv"
)

result_df.to_csv(output_path, index=False)

print("\n[3] FILE HASIL")
print("-" * 70)

print("Hasil disimpan di:")
print(output_path)

print("\n" + "=" * 70)
print("       PERANCANGAN KEBIJAKAN SELESAI")
print("=" * 70)