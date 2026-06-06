# ============================================================
#  mbg_mas_bahlil_ganteng.py
#  by: @vokaliz_netizen  |  genre: pop absurd  |  viral: ✓
# ============================================================

import time

# Timestamp dalam DETIK (0.01 menit = 1 detik, dikali 100)
lirik_lagu = [
    (1,   "MBG"),
    (2,   "Mas Bahlil Ganteng"),
    (4,   "Buah apa yang paling manis?"),
    (6,   "BUAAAHLILLLL"),
    (9,  "Tambah ganteng aja"),
    (11,  "My little bolu ketan"),
    (14,  "Ups kanda suka dinda punya gaya"),
    (20,  "Sialan dia"),
    (21,  "Makin lucu guys"),
    (24,  "Kalau diperhatiin lama-lama mirip"),
    (28,  "ZAYN MALIK IHH"),
    (31,  "My Bahlil Ganteng"),
    (34,  "Makin glowing aja nih"),
    (36,  "My Koko Bahlil kecintaanku"),
    (41,  "My little cilok pentol"),
    (45,  "Kecap dinda"),
    (48,  "Maafkan dinda dulu salah paham sama kanda"),
]

def sing(lirik, delay):
    for char in lirik:
        print(char, end='', flush=True)
        time.sleep(0.04)
    print()
    time.sleep(delay)

def nyanyikan():
    print("\n" + "=" * 44)
    print("  MBG - Mas Bahlil Ganteng")
    print("  by @kan_fajar")
    print("=" * 44 + "\n")
    time.sleep(1.0)

    for i, (detik, lirik) in enumerate(lirik_lagu):
        if i + 1 < len(lirik_lagu):
            next_detik = lirik_lagu[i + 1][0]
            delay = next_detik - detik
        else:
            delay = 3.0

        # kurangi waktu ngetik karakter dari delay
        waktu_ngetik = len(lirik) * 0.04
        delay_setelah = max(delay - waktu_ngetik, 0.1)

        sing(lirik, delay_setelah)

    print("\n" + "=" * 44)
    print("  ~ selesai ~")
    print("=" * 44 + "\n")

# ============================================================
if __name__ == "__main__":
    nyanyikan()
# ============================================================
