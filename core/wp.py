import pandas as pd

from core.scoring import KRITERIA

KODE = list(KRITERIA)


def hitung_wp(matriks, bobot):
    pangkat = pd.Series(
        [-bobot[k] if KRITERIA[k][1] == "Cost" else bobot[k] for k in KODE],
        index=KODE,
    )

    dipangkatkan = matriks[KODE] ** pangkat
    s = dipangkatkan.prod(axis=1)
    v = s / s.sum()

    hasil = matriks[["kode", "nama_produk"]].copy()
    hasil[[f"{k}^w" for k in KODE]] = dipangkatkan.values
    hasil["S"] = s
    hasil["V"] = v
    hasil["ranking"] = v.rank(ascending=False, method="first").astype(int)

    return {
        "pangkat": pangkat,
        "hasil": hasil,
        "ranking": hasil.sort_values("ranking").reset_index(drop=True),
    }