# Tugas-Besar-DasarAI
## Tugas Besar 1 IF3070 Dasar Inteligensi Artifisial Kelompok 43

Pemecah Bin Packing Problem menggunakan beberapa algoritma local search:

-   Berbagai varian Hill Climbing (steepest ascent, stochastic, first-choice, sideways move, random restart)

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

python src/main.py
```