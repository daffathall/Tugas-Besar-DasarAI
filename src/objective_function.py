from typing import List, Dict

def calculate_objective(state: List[List[str]], kapasitas: int, barang: Dict[str, int]) -> float:
    """
    Menghitung nilai fungsi objektif (SEMAKIN RENDAH SEMAKIN BAIK)
    
    Komponen:
    1. Penalti untuk kontainer yang melebihi kapasitas (KRITIS - harus valid)
    2. Jumlah kontainer yang digunakan (objektif utama)
    3. Penalti ruang terbuang (mendorong kontainer lebih penuh)
    
    Args:
        state: State saat ini (daftar kontainer)
        kapasitas: Kapasitas kontainer
        barang: Dictionary dari id_barang -> ukuran
    
    Returns:
        Nilai objektif (semakin rendah semakin baik)
    """
    
    if len(state) == 0:
        return float('inf')
    
    score = 0.0
    
    # 1. PENALTI OVERFLOW (sangat besar!)
    # Ini memastikan solusi akhir VALID
    overflow_penalty = 0
    for bin_items in state:
        bin_size = sum(barang[item] for item in bin_items)
        if bin_size > kapasitas:
            overflow = bin_size - kapasitas
            overflow_penalty += 10000 * overflow  # PENALTI SANGAT BESAR
    
    score += overflow_penalty
    
    # 2. JUMLAH KONTAINER (objektif utama)
    # Semakin sedikit kontainer, semakin baik
    num_bins = len(state)
    score += num_bins * 100
    
    # 3. PENALTI RUANG TERBUANG
    # Mendorong kontainer yang lebih penuh
    wasted_space = 0
    for bin_items in state:
        bin_size = sum(barang[item] for item in bin_items)
        if bin_size <= kapasitas:
            wasted = kapasitas - bin_size
            wasted_space += wasted
    
    # Penalti kecil untuk ruang terbuang
    score += wasted_space * 0.1
    
    return score


def calculate_fitness(state: List[List[str]], kapasitas: int, barang: Dict[str, int]) -> float:
    """
    Menghitung fitness untuk Algoritma Genetika (SEMAKIN TINGGI SEMAKIN BAIK)
    Hanya kebalikan dari fungsi objektif
    """
    obj_value = calculate_objective(state, kapasitas, barang)
    
    # Hindari pembagian dengan nol
    if obj_value == 0:
        return float('inf')
    
    return 1.0 / obj_value


def get_num_bins(state: List[List[str]]) -> int:
    """Mendapatkan jumlah kontainer yang digunakan"""
    return len(state)


def get_total_wasted_space(state: List[List[str]], kapasitas: int, barang: Dict[str, int]) -> int:
    """Menghitung total ruang terbuang di semua kontainer"""
    wasted = 0
    for bin_items in state:
        bin_size = sum(barang[item] for item in bin_items)
        if bin_size <= kapasitas:
            wasted += kapasitas - bin_size
    return wasted