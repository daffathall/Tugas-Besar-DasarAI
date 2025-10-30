# Tugas-Besar-DasarAI
## Tugas Besar 1 IF3070 Dasar Inteligensi Artifisial Kelompok 43

Pemecah Bin Packing Problem menggunakan beberapa algoritma local search:

-   Berbagai varian Hill Climbing (steepest ascent, stochastic, sideways move, random restart)

-   Simulated Annealing

-   Genetic Algorithm

Kode ditulis dalam Python dan menghasilkan ringkasan performa di terminal serta visualisasi yang disimpan ke folder results/.

---

## Struktur Repository
```
Tugas-Besar-DasarAI/
├─ data/
│  └─ input.json              # Dataset contoh (kapasitas kontainer & daftar barang)
├─ results/                   # Hasil visualisasi & eksperimen (akan dibuat otomatis)
├─ src/
│  ├─ bin_packing.py          # Representasi & operasi state bin packing
│  ├─ objective_function.py   # Fungsi objektif & utilitas evaluasi
│  ├─ hill_climbing.py        # Implementasi berbagai varian hill climbing
│  ├─ simulated_annealing.py  # Implementasi simulated annealing
│  ├─ genetic_algorithm.py    # Implementasi genetic algorithm
│  ├─ visualizer.py           # Plot konvergensi dan ringkasan state
│  ├─ utils.py                # Loader data, printer state, helper lain
│  └─ main.py                 # Entry point untuk menjalankan semua eksperimen
└─ README.md (dokumen ini)
```

---
## Setup Lingkungan
### 1) Clone atau ekstrak proyek
```bash
# Clone dari GitHub
git clone https://github.com/daffathall/Tugas-Besar-DasarAI.git
cd Tugas-Besar-DasarAI
```

### 2) (Opsional) Buat virtual environment
```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS/Linux (bash/zsh)
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Instal dependensi
```bash
pip install matplotlib numpy
```

---

## Menjalankan Program
Dari direktori root repo:
```bash
# Windows
python src/main.py

# macOS/Linux
python3 src/main.py
```

---


## Pembagian Tugas
-   Fawwaz Aydin Mustofa 18222109: 
    Membuat README.md 
    Melakukan testing dan running code
    Mengisi laporan bagian pembahasan
    Mengisi laporan bagian kesimpulan dan saran
    
-   Daffa Athalla Rajasa 18223053: 
    Membuat representasi state dengan file bin_packing.py
    Mengimplementasikan seluruh varian Hill Climbing: steepest ascent, stochastic, sideways, dan random restart dengan file hill_climbing.py
    Menangani I/O data (load JSON, save hasil) dan utilitas pendukung (timer, logger) dengan file utils.py
    Menyusun script untuk menjalankan seluruh algoritma secara terpusat dengan main.py
    Membuat cover dan kerangka laporan
    
-   Adam Joaquin Girsang 18223089:
    Merancang fungsi objektif dan fitness untuk mengukur kualitas solusi dengan objective_function.py
    Mengembangkan algoritma Simulated Annealing (cooling schedule, acceptance probability) dengan simulated_annealing.py
    Mengimplementasikan Genetic Algorithm dengan seleksi turnamen, crossover OX, mutasi move/swap, serta repair function dengan genetic_algorithm.py
    Mengembangkan fungsi visualisasi konvergensi, probabilitas SA, perbandingan GA, dan isi kontainer dengan visualizer.py
    Membuat laporan bagian desain persoalan