import pandas as pd
from pathlib import Path

print("=" * 70)
print("          VALIDASI HASIL SIMULASI PENGUJIAN")
print("=" * 70)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "hasil_simulasi"

semua_valid = True

for lt in [1, 2, 3]:

    file_input = OUTPUT_DIR / f"hasil_uji_lead_time_{lt}_hari.csv"

    df = pd.read_csv(file_input)
    df["Date"] = pd.to_datetime(df["Date"])

    print(f"\n[LEAD TIME {lt} HARI]")
    print("-" * 70)

    # 1. Validasi jumlah dan rentang tanggal
    valid_jumlah = len(df) == 366

    valid_tanggal = (
        df["Date"].min() == pd.Timestamp("2023-01-01")
        and df["Date"].max() == pd.Timestamp("2024-01-01")
        and df["Date"].nunique() == 366
    )

    # 2. Validasi keseimbangan persediaan
    saldo_hitung = (
        df["Persediaan_Awal_Hari"]
        + df["Arrival_Quantity"]
        - df["Actual_Sales"]
    )

    error_saldo = (
        saldo_hitung - df["Persediaan_Akhir"]
    ).abs().sum()

    valid_saldo = error_saldo == 0

    # 3. Validasi persediaan dan kuantitas tidak negatif
    kolom_nonnegatif = [
        "Persediaan_Awal_Hari",
        "Persediaan_Tersedia",
        "Persediaan_Akhir",
        "Arrival_Quantity",
        "Actual_Sales",
        "Lost_Sales",
        "Order_Quantity",
        "Outstanding_Order"
    ]

    valid_nonnegatif = (
        df[kolom_nonnegatif] >= 0
    ).all().all()

    # 4. Validasi persediaan tersedia
    tersedia_hitung = (
        df["Persediaan_Awal_Hari"]
        + df["Arrival_Quantity"]
    )

    valid_tersedia = (
        tersedia_hitung == df["Persediaan_Tersedia"]
    ).all()

    # 5. Validasi keseimbangan permintaan
    selisih_demand = (
        df["Demand"].sum()
        - df["Actual_Sales"].sum()
        - df["Lost_Sales"].sum()
    )

    valid_demand = selisih_demand == 0

    # 6. Validasi lost sales harian
    lost_harian = (
        df["Demand"] - df["Actual_Sales"]
    )

    valid_lost = (
        lost_harian == df["Lost_Sales"]
    ).all()

    # 7. Validasi jumlah pesanan
    valid_order = (
        df["Order_Quantity"] >= 0
    ).all()

    # 8. Validasi outstanding order
    # Outstanding_Order dicatat setelah kedatangan hari ini
    # dan sebelum pesanan baru hari ini ditambahkan.
    valid_pipeline = True

    for index in range(1, len(df)):

        pipeline_seharusnya = (
            df.loc[index - 1, "Outstanding_Order"]
            + df.loc[index - 1, "Order_Quantity"]
            - df.loc[index, "Arrival_Quantity"]
        )

        if pipeline_seharusnya < 0:
            valid_pipeline = False
            break

        if index < len(df) - 1:
            if pipeline_seharusnya != df.loc[index, "Outstanding_Order"]:
                valid_pipeline = False
                break

    # 9. Validasi jumlah hari stockout
    hari_stockout = (
        df["Lost_Sales"] > 0
    ).sum()

    # Ringkasan hasil
    hasil = [
        ("Jumlah data 366 hari", valid_jumlah),
        ("Rentang tanggal pengujian", valid_tanggal),
        ("Keseimbangan persediaan", valid_saldo),
        ("Tidak ada nilai negatif", valid_nonnegatif),
        ("Keseimbangan persediaan tersedia", valid_tersedia),
        ("Keseimbangan permintaan", valid_demand),
        ("Perhitungan lost sales harian", valid_lost),
        ("Jumlah pesanan tidak negatif", valid_order),
        ("Konsistensi pipeline", valid_pipeline)
    ]

    for nama, status in hasil:

        print(
            f"{nama:<42}: "
            f"{'LULUS' if status else 'GAGAL'}"
        )

        if not status:
            semua_valid = False

    print(f"\nTotal demand       : {df['Demand'].sum()}")
    print(f"Total sales        : {df['Actual_Sales'].sum()}")
    print(f"Total lost sales   : {df['Lost_Sales'].sum()}")
    print(f"Total order        : {df['Order_Quantity'].sum()}")
    print(f"Total arrival      : {df['Arrival_Quantity'].sum()}")
    print(f"Error saldo        : {error_saldo}")
    print(f"Hari stockout      : {hari_stockout}")

print("\n" + "=" * 70)

if semua_valid:
    print("STATUS AKHIR: SEMUA VALIDASI BERHASIL")
else:
    print("STATUS AKHIR: TERDAPAT VALIDASI YANG GAGAL")

print("=" * 70)