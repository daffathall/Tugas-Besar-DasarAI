import random
import math
import copy
from typing import List, Dict, Tuple
from bin_packing import BinPacking
from objective_function import calculate_objective

def simulated_annealing(
    bp: BinPacking,
    initial_state: List[List[str]],
    T_initial: float = 1000.0,
    T_min: float = 0.1,
    alpha: float = 0.95,
    max_iterations: int = 1000
) -> Tuple[List[List[str]], float, List[float], List[float], int]:
    """
    Algoritma: Simulated Annealing
    
    Args:
        bp: Instance BinPacking
        initial_state: State awal
        T_initial: Temperatur awal
        T_min: Temperatur minimum (kondisi berhenti)
        alpha: Laju pendinginan (0 < alpha < 1)
        max_iterations: Iterasi maksimum
    
    Returns:
        best_state, best_score, score_history, probability_history, stuck_count
    """
    current_state = copy.deepcopy(initial_state)
    current_score = calculate_objective(current_state, bp.kapasitas, bp.barang)
    
    best_state = copy.deepcopy(current_state)
    best_score = current_score
    
    T = T_initial
    score_history = [current_score]
    probability_history = []  # Untuk plotting e^(ΔE/T)
    stuck_count = 0
    iteration = 0
    
    while T > T_min and iteration < max_iterations:
        # Dapatkan tetangga random
        neighbor = bp.get_random_neighbor(current_state)
        neighbor_score = calculate_objective(neighbor, bp.kapasitas, bp.barang)
        
        # Hitung delta E nya
        delta_E = neighbor_score - current_score
        
        # Putuskan apakah menerima tetangga
        if delta_E < 0:
            # Solusi lebih baik - selalu terima
            current_state = neighbor
            current_score = neighbor_score
            
            # Perbaruin solusi terbaik
            if current_score < best_score:
                best_state = copy.deepcopy(current_state)
                best_score = current_score
            
            probability_history.append(1.0)
        else:
            # Solusi lebih buruk - terima dengan probabilitas
            probability = math.exp(-delta_E / T)
            probability_history.append(probability)
            
            if random.random() < probability:
                current_state = neighbor
                current_score = neighbor_score
            else:
                stuck_count += 1
        
        # Catat skor saat ini setelah keputusan
        score_history.append(current_score)
        
        # Turunin temperatur
        T *= alpha
        iteration += 1
    
    return best_state, best_score, score_history, probability_history, stuck_count


def simulated_annealing_with_reheating(
    bp: BinPacking,
    initial_state: List[List[str]],
    T_initial: float = 1000.0,
    T_min: float = 0.1,
    alpha: float = 0.95,
    reheat_threshold: int = 50,
    reheat_factor: float = 2.0,
    max_iterations: int = 1000
) -> Tuple[List[List[str]], float, List[float], List[float], int]:
    """
    Simulated Annealing dengan Pemanasan Ulang
    Panaskan kembali ketika terlalu lama stuck
    """
    current_state = copy.deepcopy(initial_state)
    current_score = calculate_objective(current_state, bp.kapasitas, bp.barang)
    
    best_state = copy.deepcopy(current_state)
    best_score = current_score
    
    T = T_initial
    score_history = [current_score]
    probability_history = []
    stuck_count = 0
    no_improvement_count = 0
    iteration = 0
    
    while T > T_min and iteration < max_iterations:
        neighbor = bp.get_random_neighbor(current_state)
        neighbor_score = calculate_objective(neighbor, bp.kapasitas, bp.barang)
        
        delta_E = neighbor_score - current_score
        
        if delta_E < 0:
            current_state = neighbor
            current_score = neighbor_score
            no_improvement_count = 0
            
            if current_score < best_score:
                best_state = copy.deepcopy(current_state)
                best_score = current_score
            
            probability_history.append(1.0)
        else:
            probability = math.exp(-delta_E / T)
            probability_history.append(probability)
            
            if random.random() < probability:
                current_state = neighbor
                current_score = neighbor_score
                no_improvement_count += 1
            else:
                stuck_count += 1
                no_improvement_count += 1
        
        # Pemanasan ulang kalau stuck
        if no_improvement_count >= reheat_threshold:
            T = min(T * reheat_factor, T_initial)
            no_improvement_count = 0
        
        # Catat skor saat ini setelah keputusan
        score_history.append(current_score)
        T *= alpha
        iteration += 1
    
    return best_state, best_score, score_history, probability_history, stuck_count