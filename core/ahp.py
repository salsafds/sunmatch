import numpy as np
import pandas as pd

KODE = ["C1", "C2", "C3", "C4", "C5"]
RI = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
BATAS_CR = 0.10

PASANGAN = [(i, j) for i in range(len(KODE)) for j in range(i + 1, len(KODE))]


def buat_matriks(nilai_pasangan):
    n = len(KODE)
    A = np.ones((n, n))
    for (i, j), nilai in zip(PASANGAN, nilai_pasangan):
        A[i, j] = nilai
        A[j, i] = 1 / nilai
    return A


def hitung_ahp(nilai_pasangan):
    A = buat_matriks(nilai_pasangan)
    n = len(A)

    jumlah_kolom = A.sum(axis=0)
    normalisasi = A / jumlah_kolom
    bobot = normalisasi.mean(axis=1)

    a_kali_w = A @ bobot
    lambda_i = a_kali_w / bobot
    lambda_max = lambda_i.mean()
    ci = (lambda_max - n) / (n - 1)
    cr = ci / RI[n] if RI[n] else 0.0

    return {
        "matriks": pd.DataFrame(A, index=KODE, columns=KODE),
        "jumlah_kolom": pd.Series(jumlah_kolom, index=KODE),
        "normalisasi": pd.DataFrame(normalisasi, index=KODE, columns=KODE),
        "bobot": pd.Series(bobot, index=KODE),
        "konsistensi": pd.DataFrame({"A × w": a_kali_w, "Bobot (w)": bobot, "(A × w) / w": lambda_i}, index=KODE),
        "lambda_max": lambda_max,
        "ci": ci,
        "ri": RI[n],
        "cr": cr,
        "konsisten": cr <= BATAS_CR,
    }