import spacy
import re
import pandas as pd

nlp = spacy.load("en_core_web_sm")
df = pd.read_csv("data/dummy_house_prices.csv")

def jawab_pertanyaan(pertanyaan):
    doc = nlp(pertanyaan.lower())
    tokens = [token.text for token in doc]
    teks = pertanyaan.lower()

    if any(k in teks for k in ["tertinggi", "terbesar", "paling besar", "maksimum", "termahal", "terluas"]):
        if any(k in teks for k in ["harga", "saleprice"]):
            val = df["SalePrice"].max()
            return f"Harga rumah paling mahal adalah {val:,.0f}."
        elif any(k in teks for k in ["luas", "grlivarea"]):
            row = df[df["GrLivArea"] == df["GrLivArea"].max()]
            return f"Rumah terluas:\n{row.to_string(index=False)}"
        elif any(k in teks for k in ["garasi", "garagecars"]):
            val = df["GarageCars"].max()
            return f"Jumlah garasi terbanyak adalah {val} mobil."

    if any(k in teks for k in ["rata", "average"]):
        if any(k in teks for k in ["harga", "saleprice"]):
            avg = df["SalePrice"].mean()
            return f"Rata-rata harga rumah adalah {avg:,.0f}."
        elif any(k in teks for k in ["kualitas", "overallqual"]):
            avg = df["OverallQual"].mean()
            return f"Rata-rata kualitas rumah adalah {avg:.2f}."
        elif any(k in teks for k in ["garasi", "garagecars"]):
            avg = df["GarageCars"].mean()
            return f"Rata-rata jumlah garasi adalah {avg:.2f} mobil."

    angka = [int(s) for s in re.findall(r"\d+", pertanyaan)]
    if any(k in teks for k in ["garasi", "garagecars"]) and angka:
        count = len(df[df["GarageCars"] == angka[0]])
        return f"Ada {count} rumah dengan {angka[0]} garasi."
    elif any(k in teks for k in ["kamar", "bedroom", "tidur"]) and angka:
        count = len(df[df["BedroomAbvGr"] == angka[0]])
        return f"Ada {count} rumah dengan {angka[0]} kamar tidur."
    elif any(k in teks for k in ["mandi", "bath"]) and angka:
        count = len(df[df["FullBath"] == angka[0]])
        return f"Ada {count} rumah dengan {angka[0]} kamar mandi."

    if any(k in teks for k in ["kualitas", "overallqual"]) and angka:
        filtered = df[df["OverallQual"] >= angka[0]]
        avg = filtered["SalePrice"].mean()
        return f"Rata-rata harga rumah dengan kualitas >= {angka[0]} adalah {avg:,.0f}."

    if any(k in teks for k in ["tahun", "dibangun", "yearbuilt"]):
        if "sebelum" in teks and angka:
            count = len(df[df["YearBuilt"] < angka[0]])
            return f"Ada {count} rumah yang dibangun sebelum tahun {angka[0]}."
        elif "setelah" in teks and angka:
            count = len(df[df["YearBuilt"] > angka[0]])
            return f"Ada {count} rumah yang dibangun setelah tahun {angka[0]}."

    return "Maaf, saya belum bisa menjawab pertanyaan itu. Coba gunakan kata seperti 'harga', 'garasi', 'kualitas', 'luas', atau 'dibangun'."

# Input loop
while True:
    pertanyaan = input("Ada yang bisa saya bantu? (ketik 'exit' untuk keluar): ")
    if pertanyaan.lower() in ["exit", "keluar", "stop"]:
        print("Terima kasih, sampai jumpa!")
        break
    hasil = jawab_pertanyaan(pertanyaan)
    print(hasil)
