import json
import time
from typing import List, Dict, Tuple
import os

def load_data(filepath: str) -> Dict:
    """membaca data dari berkas JSON"""
    with open(filepath, 'r') as f:
        return json.load(f)

def save_result(filename: str, result: Dict):
    """menyimpan hasil eksperimen ke berkas JSON"""
    os.makedirs('results', exist_ok=True)
    with open(f'results/{filename}.json', 'w') as f:
        json.dump(result, f, indent=2)

def timing_decorator(func):
    """dekorator untuk mengukur waktu eksekusi"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return result, end - start
    return wrapper

def print_state(state: List[List[str]], kapasitas: int, barang: Dict[str, int]):
    """menampilkan kondisi saat ini dengan format yang mudah dibaca"""
    print(f"\nTotal Kontainer: {len(state)}")
    total_items = sum(len(bin_items) for bin_items in state)
    print(f"Total Barang: {total_items}")
    
    for i, bin_items in enumerate(state, 1):
        if len(bin_items) == 0:
            continue
        total = sum(barang[item] for item in bin_items)
        print(f"\nKontainer {i} (Total: {total}/{kapasitas}):")
        for item in bin_items:
            print(f"  - {item} ({barang[item]})")

def calculate_statistics(results: List[float]) -> Dict:
    """menghitung statistik dari beberapa percobaan"""
    return {
        'mean': sum(results) / len(results),
        'min': min(results),
        'max': max(results),
        'std': (sum((x - sum(results)/len(results))**2 for x in results) / len(results))**0.5
    }