from core.ahp import hitung_ahp
from core.database import load_alternatif
from core.scoring import matriks_keputusan
from core.wp import hitung_wp

NILAI_PASANGAN = [2, 3, 1/2, 2, 2, 1/3, 1, 1/4, 1/2, 3]

ahp = hitung_ahp(NILAI_PASANGAN)
print("Bobot:", ahp["bobot"].round(4).to_dict())
print(f"Lambda max: {ahp['lambda_max']:.4f} | CI: {ahp['ci']:.4f} | CR: {ahp['cr']:.4f} | Konsisten: {ahp['konsisten']}")

matriks = matriks_keputusan(load_alternatif(), "Berjerawat", "Tinted")
wp = hitung_wp(matriks, ahp["bobot"])
print(wp["ranking"][["ranking", "kode", "nama_produk", "S", "V"]].head(5).round(4).to_string(index=False))
print("Total V:", round(wp["hasil"]["V"].sum(), 6))