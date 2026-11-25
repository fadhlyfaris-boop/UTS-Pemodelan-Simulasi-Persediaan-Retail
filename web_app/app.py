import os
import math
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from flask import Flask, render_template, request


# =========================================================
# KONFIGURASI APLIKASI
# =========================================================

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FILE = os.path.join(
    BASE_DIR,
    "simulasi",
    "hasil_simulasi",
    "data_pengujian.csv"
)

PARAMETER_FILE = os.path.join(
    BASE_DIR,
    "simulasi",
    "hasil_simulasi",
    "parameter_kalibrasi.csv"
)

STATIC_IMAGE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "static",
    "images"
)

os.makedirs(STATIC_IMAGE_DIR, exist_ok=True)


# =========================================================
# MEMBACA DATA DAN PARAMETER
# =========================================================

data_pengujian = pd.read_csv(DATA_FILE)
data_pengujian["Date"] = pd.to_datetime(
    data_pengujian["Date"]
)

data_pengujian = data_pengujian.sort_values(
    "Date"
).reset_index(drop=True)

parameter_kalibrasi = pd.read_csv(PARAMETER_FILE)


# =========================================================
# FUNGSI SIMULASI PERSEDIAAN
# =========================================================

def jalankan_simulasi(
    data,
    lead_time,
    reorder_point,
    target_persediaan
):

    persediaan = int(data.loc[0, "Inventory Level"])

    pipeline = []
    hasil = []

    for index, row in data.iterrows():

        tanggal = row["Date"]
        demand = int(row["Units Sold"])

        # Menghitung pesanan yang tiba pada hari ini
        arrival_quantity = sum(
            pesanan["quantity"]
            for pesanan in pipeline
            if pesanan["arrival_day"] == index
        )

        # Menghapus pesanan yang sudah tiba
        pipeline = [
            pesanan
            for pesanan in pipeline
            if pesanan["arrival_day"] != index
        ]

        persediaan_awal = persediaan

        # Persediaan tersedia setelah kedatangan pesanan
        persediaan_tersedia = (
            persediaan_awal + arrival_quantity
        )

        # Penjualan aktual
        actual_sales = min(
            demand,
            persediaan_tersedia
        )

        # Permintaan yang tidak terpenuhi
        lost_sales = demand - actual_sales

        # Persediaan akhir hari
        persediaan_akhir = (
            persediaan_tersedia - actual_sales
        )

        # Total pesanan yang masih dalam perjalanan
        outstanding_order = sum(
            pesanan["quantity"]
            for pesanan in pipeline
        )

        # Posisi persediaan
        inventory_position = (
            persediaan_akhir + outstanding_order
        )

        # Keputusan pemesanan ulang
        order_quantity = 0

        if inventory_position <= reorder_point:

            order_quantity = max(
                0,
                target_persediaan - inventory_position
            )

            if order_quantity > 0:

                pipeline.append({
                    "quantity": order_quantity,
                    "arrival_day": index + lead_time
                })

        # Menyimpan hasil simulasi harian
        hasil.append({
            "Date": tanggal,
            "Demand": demand,
            "Persediaan_Awal_Hari": persediaan_awal,
            "Arrival_Quantity": arrival_quantity,
            "Persediaan_Tersedia": persediaan_tersedia,
            "Actual_Sales": actual_sales,
            "Lost_Sales": lost_sales,
            "Persediaan_Akhir": persediaan_akhir,
            "Outstanding_Order": outstanding_order,
            "Inventory_Position": inventory_position,
            "Order_Quantity": order_quantity,
            "Lead_Time": lead_time
        })

        persediaan = persediaan_akhir

    return pd.DataFrame(hasil)


# =========================================================
# MENGHITUNG RINGKASAN HASIL SIMULASI
# =========================================================

def hitung_ringkasan(hasil):

    total_demand = hasil["Demand"].sum()
    total_sales = hasil["Actual_Sales"].sum()
    total_lost_sales = hasil["Lost_Sales"].sum()

    fill_rate = (
        total_sales / total_demand * 100
        if total_demand > 0
        else 0
    )

    rata_rata_persediaan = (
        hasil["Persediaan_Akhir"].mean()
    )

    hari_stockout = (
        hasil["Lost_Sales"] > 0
    ).sum()

    total_order = hasil["Order_Quantity"].sum()

    total_arrival = hasil["Arrival_Quantity"].sum()

    return {
        "total_demand": int(total_demand),
        "total_sales": int(total_sales),
        "lost_sales": int(total_lost_sales),
        "fill_rate": round(fill_rate, 2),
        "rata_rata_persediaan": round(
            rata_rata_persediaan, 2
        ),
        "hari_stockout": int(hari_stockout),
        "total_order": int(total_order),
        "total_arrival": int(total_arrival)
    }


# =========================================================
# MEMBUAT GRAFIK HASIL SIMULASI
# =========================================================

def buat_grafik(hasil):

    nama_file = "grafik_simulasi_web.png"

    lokasi_file = os.path.join(
        STATIC_IMAGE_DIR,
        nama_file
    )

    plt.figure(figsize=(12, 5))

    plt.plot(
        hasil["Date"],
        hasil["Persediaan_Akhir"],
        label="Persediaan Akhir",
        linewidth=1.5
    )

    plt.plot(
        hasil["Date"],
        hasil["Demand"],
        label="Permintaan",
        alpha=0.7
    )

    plt.title(
        "Tren Persediaan dan Permintaan Selama Simulasi"
    )

    plt.xlabel("Tanggal")
    plt.ylabel("Jumlah Unit")

    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        lokasi_file,
        dpi=150
    )

    plt.close()

    return nama_file


# =========================================================
# HALAMAN UTAMA
# =========================================================

@app.route("/", methods=["GET", "POST"])
def index():

    hasil = None
    ringkasan = None
    grafik = None
    parameter_terpilih = None
    pesan_error = None

    lead_time = 1
    safety_stock = None
    reorder_point = None
    target_persediaan = None

    if request.method == "POST":

        try:

            lead_time = int(
                request.form.get("lead_time", 1)
            )

            if lead_time not in [1, 2, 3]:
                raise ValueError(
                    "Lead Time harus 1, 2, atau 3 hari."
                )

            parameter = parameter_kalibrasi[
                parameter_kalibrasi["Lead_Time"] == lead_time
            ]

            if parameter.empty:
                raise ValueError(
                    "Parameter kalibrasi tidak ditemukan."
                )

            parameter = parameter.iloc[0]

            nilai_safety_stock = request.form.get(
                "safety_stock", ""
            ).strip()

            if nilai_safety_stock:
                safety_stock = int(nilai_safety_stock)
            else:
                safety_stock = int(parameter["Safety_Stock"])

            if safety_stock < 0:
                raise ValueError(
                    "Safety Stock tidak boleh negatif."
                )

            rata_demand_lt = float(
                parameter["Rata_Rata_Demand_Lead_Time"]
            )

            reorder_point = math.ceil(
                rata_demand_lt + safety_stock
            )

            reorder_point_dasar = int(
                parameter["Reorder_Point"]
            )

            target_dasar = int(
                parameter["Target_Persediaan"]
            )

            target_persediaan = (
                target_dasar
                + (reorder_point - reorder_point_dasar)
            )

            hasil = jalankan_simulasi(
                data_pengujian,
                lead_time,
                reorder_point,
                target_persediaan
            )

            ringkasan = hitung_ringkasan(hasil)

            grafik = buat_grafik(hasil)

            parameter_terpilih = {
                "lead_time": lead_time,
                "safety_stock": safety_stock,
                "reorder_point": reorder_point,
                "target_persediaan": target_persediaan
            }

        except (ValueError, TypeError) as error:

            pesan_error = str(error)

    return render_template(
        "index.html",
        hasil=hasil,
        ringkasan=ringkasan,
        grafik=grafik,
        parameter=parameter_terpilih,
        lead_time=lead_time,
        safety_stock=safety_stock,
        pesan_error=pesan_error
    )


# =========================================================
# MENJALANKAN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )