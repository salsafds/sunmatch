import pandas as pd

KRITERIA = {
    "C1": ("Harga per ml", "Cost"),
    "C2": ("SPF", "Benefit"),
    "C3": ("PA Rating", "Benefit"),
    "C4": ("Kesesuaian Jenis Kulit", "Benefit"),
    "C5": ("Kesesuaian Hasil Akhir", "Benefit"),
}

JENIS_KULIT = ["Normal", "Kering", "Berminyak", "Kombinasi", "Sensitif", "Berjerawat"]
HASIL_AKHIR = ["Matte", "Natural", "Dewy", "Tinted"]

NILAI_SPF_PLUS = 51
SKOR_PA = {"PA+": 1, "PA++": 2, "PA+++": 3, "PA++++": 4}

SKOR_C5 = {
    "Matte": {"Matte": 5, "Natural": 3, "Dewy": 1, "Tinted": 4},
    "Natural": {"Matte": 3, "Natural": 5, "Dewy": 3, "Tinted": 2},
    "Dewy": {"Matte": 1, "Natural": 3, "Dewy": 5, "Tinted": 3},
    "Tinted": {"Matte": 2, "Natural": 2, "Dewy": 3, "Tinted": 5},
}


def skor_c1(harga, ukuran):
    return harga / ukuran


def skor_c2(spf):
    spf = str(spf).strip()
    return NILAI_SPF_PLUS if spf == "50+" else float(spf)


def skor_c3(pa):
    return SKOR_PA[str(pa).strip()]


def skor_c4(klaim, jenis_kulit):
    klaim = str(klaim).lower()
    if jenis_kulit.lower() in klaim:
        return 3
    if "semua jenis kulit" in klaim:
        return 2
    return 1


def skor_c5(finish, preferensi):
    finish = str(finish).lower()
    cocok = [skor for kategori, skor in SKOR_C5[preferensi].items() if kategori.lower() in finish]
    return max(cocok) if cocok else 1


def matriks_keputusan(df, jenis_kulit, preferensi):
    hasil = pd.DataFrame({
        "kode": df["kode"],
        "nama_produk": df["nama_produk"],
        "C1": [skor_c1(h, u) for h, u in zip(df["harga"], df["ukuran"])],
        "C2": df["spf"].apply(skor_c2),
        "C3": df["pa"].apply(skor_c3),
        "C4": df["jenis_kulit"].apply(lambda k: skor_c4(k, jenis_kulit)),
        "C5": df["hasil_akhir"].apply(lambda f: skor_c5(f, preferensi)),
    })
    return hasil