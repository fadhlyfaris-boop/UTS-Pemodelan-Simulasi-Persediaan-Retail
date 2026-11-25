import pandas as pd
from pathlib import Path

print("=" * 70)
print("       PERSIAPAN DATA KALIBRASI DAN PENGUJIAN SIMULASI")
print("=" * 70)

# Menentukan lokasi folder
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR.parent / "dataset"
OUTPUT_DIR = BASE_DIR / "hasil_simulasi"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Membaca data objek simulasi
file_input = DATASET_DIR / "data_objek_simulasi.csv"

df = pd.read_csv(file_input)
df["Date"] = pd.to_datetime(df["Date"])

print("\n[1] INFORMASI DATA AWAL")
print("-" * 70)
print(f"Jumlah data       : {len(df)}")
print(f"Tanggal awal      : {df['Date'].min().date()}")
print(f"Tanggal akhir     : {df['Date'].max().date()}")

# Membagi periode data
data_kalibrasi = df[
    (df["Date"] >= "2022-01-01") &
    (df["Date"] <= "2022-12-31")
].copy()

data_pengujian = df[
    (df["Date"] >= "2023-01-01") &
    (df["Date"] <= "2024-01-01")
].copy()

# Mengurutkan berdasarkan tanggal
data_kalibrasi = data_kalibrasi.sort_values("Date")
data_pengujian = data_pengujian.sort_values("Date")

print("\n[2] HASIL PEMBAGIAN DATA")
print("-" * 70)

print("\nDATA KALIBRASI")
print(f"Jumlah data       : {len(data_kalibrasi)}")
print(f"Tanggal awal      : {data_kalibrasi['Date'].min().date()}")
print(f"Tanggal akhir     : {data_kalibrasi['Date'].max().date()}")
print(f"Rata-rata demand  : {data_kalibrasi['Units Sold'].mean():.2f}")

print("\nDATA PENGUJIAN")
print(f"Jumlah data       : {len(data_pengujian)}")
print(f"Tanggal awal      : {data_pengujian['Date'].min().date()}")
print(f"Tanggal akhir     : {data_pengujian['Date'].max().date()}")
print(f"Rata-rata demand  : {data_pengujian['Units Sold'].mean():.2f}")

# Validasi jumlah dan periode data
validasi = (
    len(data_kalibrasi) == 365
    and len(data_pengujian) == 366
    and data_kalibrasi["Date"].max() < data_pengujian["Date"].min()
)

print("\n[3] VALIDASI PEMBAGIAN DATA")
print("-" * 70)

if validasi:
    print("STATUS: BERHASIL")
    print("Data kalibrasi dan pengujian tidak saling tumpang tindih.")
else:
    print("STATUS: PERLU DIPERIKSA")
    print("Jumlah atau periode data tidak sesuai.")

# Menyimpan hasil pembagian
file_kalibrasi = OUTPUT_DIR / "data_kalibrasi.csv"
file_pengujian = OUTPUT_DIR / "data_pengujian.csv"

data_kalibrasi.to_csv(file_kalibrasi, index=False)
data_pengujian.to_csv(file_pengujian, index=False)

print("\n[4] PENYIMPANAN DATA")
print("-" * 70)
print(f"Data kalibrasi : {file_kalibrasi}")
print(f"Data pengujian : {file_pengujian}")

print("\n" + "=" * 70)
print("             PERSIAPAN DATA SELESAI")
print("=" * 70)