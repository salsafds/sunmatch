import pandas as pd

from core.database import get_connection

KOLOM = [
    "kode", "nama_produk", "merek", "spf", "pa", "tekstur",
    "jenis_kulit", "hasil_akhir", "ukuran", "harga", "alasan", "sumber",
]

df = pd.read_csv("data/alternatif.csv", sep=None, engine="python", encoding="utf-8-sig")
df = df.dropna(how="all")

if len(df.columns) != len(KOLOM):
    raise ValueError(f"CSV punya {len(df.columns)} kolom, seharusnya {len(KOLOM)}. Cek baris judul di CSV.")

df.columns = KOLOM
df["harga"] = df["harga"].astype(str).str.replace(r"\D", "", regex=True).astype(int)
df["ukuran"] = df["ukuran"].astype(str).str.extract(r"(\d+)")[0].astype(int)
df["spf"] = df["spf"].astype(str).str.replace(".0", "", regex=False)

with get_connection() as con:
    df.to_sql("alternatif", con, if_exists="replace", index=False)
    con.execute("""
        CREATE TABLE IF NOT EXISTS riwayat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu TEXT DEFAULT CURRENT_TIMESTAMP,
            jenis_kulit TEXT,
            hasil_akhir TEXT,
            bobot TEXT,
            cr REAL,
            ranking TEXT
        )
    """)

print(f"Berhasil memasukkan {len(df)} alternatif.")
print(df[["kode", "nama_produk", "spf", "pa", "ukuran", "harga"]].head())