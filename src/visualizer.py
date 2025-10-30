import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
import os

def plot_convergence(history: List[float], title: str, filename: str):
    """Plot nilai fungsi objektif terhadap nilai iterasi"""
    plt.figure(figsize=(10, 6))
    plt.plot(history, linewidth=2)
    plt.xlabel('Iterasi', fontsize=12)
    plt.ylabel('Nilai Fungsi Objektif', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    os.makedirs('results', exist_ok=True)
    plt.savefig(f'results/{filename}.png', dpi=300)
    plt.close()


def plot_sa_probability(probability_history: List[float], filename: str):
    """Plot e^(ΔE/T) untuk Simulated Annealing"""
    plt.figure(figsize=(10, 6))
    plt.plot(probability_history, linewidth=2, color='red')
    plt.xlabel('Iterasi', fontsize=12)
    plt.ylabel('Probabilitas Penerimaan e^(ΔE/T)', fontsize=12)
    plt.title('Simulated Annealing - Probabilitas Penerimaan', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    os.makedirs('results', exist_ok=True)
    plt.savefig(f'results/{filename}.png', dpi=300)
    plt.close()


def plot_ga_convergence(best_history: List[float], avg_history: List[float], title: str, filename: str):
    """Plot konvergensi GA dengan nilai terbaik dan rata-rata"""
    plt.figure(figsize=(10, 6))
    plt.plot(best_history, label='Terbaik', linewidth=2, color='green')
    plt.plot(avg_history, label='Rata-rata', linewidth=2, color='blue', alpha=0.7)
    plt.xlabel('Generasi', fontsize=12)
    plt.ylabel('Nilai Fungsi Objektif', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    os.makedirs('results', exist_ok=True)
    plt.savefig(f'results/{filename}.png', dpi=300)
    plt.close()


def plot_hc_comparison(histories: Dict[str, List[float]], filename: str):
    """Plot semua 4 varian Hill Climbing dalam satu figure dengan subplot 2x2"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Varian Hill Climbing - Perbandingan Konvergensi', fontsize=16, fontweight='bold')
    
    colors = ['blue', 'green', 'red', 'purple']
    variants = [
        ('Steepest Ascent', 'steepest_ascent'),
        ('Stochastic', 'stochastic'),
        ('Sideways Move', 'sideways'),
        ('Random Restart', 'random_restart')
    ]
    
    for idx, (title, key) in enumerate(variants):
        row = idx // 2
        col = idx % 2
        ax = axes[row, col]
        
        if key in histories and len(histories[key]) > 0:
            history = histories[key]
            ax.plot(history, linewidth=2, color=colors[idx])
            ax.set_xlabel('Iterasi', fontsize=11)
            ax.set_ylabel('Nilai Fungsi Objektif', fontsize=11)
            ax.set_title(f'{title} Hill Climbing', fontsize=13, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # Tambahkan statistik
            initial_score = history[0]
            final_score = history[-1]
            improvement = initial_score - final_score
            ax.text(0.98, 0.97, 
                   f'Awal: {initial_score:.2f}\nAkhir: {final_score:.2f}\nPerbaikan: {improvement:.2f}\nIterasi: {len(history)-1}',
                   transform=ax.transAxes,
                   verticalalignment='top',
                   horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                   fontsize=9)
        else:
            ax.text(0.5, 0.5, 'Data tidak tersedia', 
                   ha='center', va='center', fontsize=12)
            ax.set_title(f'{title} Hill Climbing', fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    os.makedirs('results', exist_ok=True)
    plt.savefig(f'results/{filename}.png', dpi=300)
    plt.close()


def visualize_bins(state: List[List[str]], kapasitas: int, barang: Dict[str, int], title: str, filename: str):
    """Visualisasi kontainer sebagai bar horizontal"""
    if len(state) == 0:
        return
    
    fig, ax = plt.subplots(figsize=(12, max(6, len(state) * 0.5)))
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(state)))
    
    for i, bin_items in enumerate(state):
        bin_size = sum(barang[item] for item in bin_items)
        
        # Gambar kapasitas kontainer
        ax.barh(i, kapasitas, color='lightgray', alpha=0.3, edgecolor='black', linewidth=2)
        
        # Gambar item-item
        cumulative = 0
        for item in bin_items:
            item_size = barang[item]
            ax.barh(i, item_size, left=cumulative, color=colors[i], 
                   edgecolor='black', linewidth=1)
            
            # Tambahkan label item
            ax.text(cumulative + item_size/2, i, item, 
                   ha='center', va='center', fontsize=8, fontweight='bold')
            
            cumulative += item_size
        
        # Tambahkan info kontainer
        usage_percent = (bin_size / kapasitas) * 100
        ax.text(kapasitas + 5, i, f'{bin_size}/{kapasitas} ({usage_percent:.1f}%)', 
               va='center', fontsize=10)
    
    ax.set_yticks(range(len(state)))
    ax.set_yticklabels([f'Kontainer {i+1}' for i in range(len(state))])
    ax.set_xlabel('Kapasitas', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlim(0, kapasitas + 50)
    plt.tight_layout()
    
    os.makedirs('results', exist_ok=True)
    plt.savefig(f'results/{filename}.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_comparison(results: Dict, filename: str):
    """Bandingkan beberapa algoritma"""
    algorithms = list(results.keys())
    scores = [results[alg]['best_score'] for alg in algorithms]
    times = [results[alg]['time'] for alg in algorithms]
    bins_used = [results[alg]['bins_used'] for alg in algorithms]
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Skor objektif
    axes[0].bar(algorithms, scores, color=['blue', 'green', 'red'])
    axes[0].set_ylabel('Nilai Fungsi Objektif')
    axes[0].set_title('Skor Objektif Terbaik')
    axes[0].tick_params(axis='x', rotation=45)
    
    # Waktu eksekusi
    axes[1].bar(algorithms, times, color=['blue', 'green', 'red'])
    axes[1].set_ylabel('Waktu (detik)')
    axes[1].set_title('Waktu Eksekusi')
    axes[1].tick_params(axis='x', rotation=45)
    
    # Kontainer yang digunakan
    axes[2].bar(algorithms, bins_used, color=['blue', 'green', 'red'])
    axes[2].set_ylabel('Jumlah Kontainer')
    axes[2].set_title('Kontainer yang Digunakan')
    axes[2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    os.makedirs('results', exist_ok=True)
    plt.savefig(f'results/{filename}.png', dpi=300)
    plt.close()


def print_state_detailed(state: List[List[str]], kapasitas: int, barang: Dict[str, int], title: str = "State"):
    """Cetak informasi state secara detail"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Total Kontainer yang Digunakan: {len(state)}")
    
    total_items = sum(len(bin_items) for bin_items in state)
    total_size = sum(sum(barang[item] for item in bin_items) for bin_items in state)
    total_capacity = len(state) * kapasitas
    utilization = (total_size / total_capacity * 100) if total_capacity > 0 else 0
    
    print(f"Total Barang: {total_items}")
    print(f"Total Ukuran: {total_size}")
    print(f"Total Kapasitas: {total_capacity}")
    print(f"Utilisasi: {utilization:.2f}%")
    print(f"{'-'*60}")
    
    for i, bin_items in enumerate(state, 1):
        bin_size = sum(barang[item] for item in bin_items)
        bin_utilization = (bin_size / kapasitas * 100)
        
        print(f"\nKontainer {i}: {bin_size}/{kapasitas} ({bin_utilization:.1f}%)")
        for item in bin_items:
            print(f"  - {item}: {barang[item]}")
    
    print(f"{'='*60}\n")