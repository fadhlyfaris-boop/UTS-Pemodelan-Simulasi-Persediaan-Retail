import os
import pandas as pd

# =====================================================
# 1. MEMBACA DATA OBJEK SIMULASI
# =====================================================

base_dir = os.path.dirname(__file__)

file_path = os.path.join(
    base_dir,
    "data_objek_simulasi.csv"
)

df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

demand = df["Units Sold"]

# =====================================================
# 2. PARAMETER DASAR
# =====================================================

initial_inventory = df["Inventory Level"].mean()
average_demand = demand.mean()
demand_std = demand.std()

service_level = 0.95

print("=" * 70)
print("          PERHITUNGAN PARAMETER PERSEDIAAN")
print("=" * 70)

print("\n[1] PARAMETER DASAR")
print("-" * 70)

print(f"Persediaan awal rata-rata : {initial_inventory:.2f}")
print(f"Permintaan rata-rata      : {average_demand:.2f}")
print(f"Simpangan baku permintaan : {demand_std:.2f}")
print(f"Tingkat layanan           : {service_level * 100:.0f}%")

# =====================================================
# 3. MENGHITUNG PARAMETER SETIAP LEAD TIME
# =====================================================

results = []

print("\n[2] HASIL PERHITUNGAN SAFETY STOCK DAN ROP")
print("-" * 70)

for lead_time in [1, 2, 3]:

    demand_during_lead_time = (
        demand.rolling(window=lead_time)
        .sum()
        .dropna()
    )

    average_lead_demand = demand_during_lead_time.mean()

    reorder_point = demand_during_lead_time.quantile(
        service_level
    )

    safety_stock = (
        reorder_point - average_lead_demand
    )

    safety_stock = max(0, safety_stock)

    result = {
        "Lead_Time": lead_time,
        "Average_Lead_Demand": average_lead_demand,
        "Safety_Stock": safety_stock,
        "Reorder_Point": reorder_point,
        "Initial_Inventory": initial_inventory
    }

    results.append(result)

    print(f"\nLead Time: {lead_time} hari")
    print(f"Rata-rata permintaan selama lead time: {average_lead_demand:.2f}")
    print(f"Safety Stock                       : {safety_stock:.2f}")
    print(f"Reorder Point                      : {reorder_point:.2f}")
    print(
        "Status persediaan awal             :",
        "DI BAWAH ROP"
        if initial_inventory <= reorder_point
        else "DI ATAS ROP"
    )

# =====================================================
# 4. MENYIMPAN HASIL
# =====================================================

result_df = pd.DataFrame(results)

output_path = os.path.join(
    base_dir,
    "parameter_persediaan.csv"
)

result_df.to_csv(output_path, index=False)

print("\n[3] FILE HASIL")
print("-" * 70)
print("Hasil disimpan di:")
print(output_path)

print("\n" + "=" * 70)
print("          PERHITUNGAN PARAMETER SELESAI")
print("=" * 70)