import random
import copy
from typing import List, Dict, Tuple
from bin_packing import BinPacking
from objective_function import calculate_objective

def steepest_ascent_hill_climbing(bp: BinPacking, initial_state: List[List[str]], max_iterations: int = 1000) -> Tuple[List[List[str]], float, List[float], int]:
    """
    Steepest Ascent Hill Climbing
    Selalu pilih tetangga TERBAIK
    
    Returns:
        best_state, best_score, history, iterations
    """
    current_state = copy.deepcopy(initial_state)
    current_score = calculate_objective(current_state, bp.kapasitas, bp.barang)
    
    history = [current_score]
    iteration = 0
    
    while iteration < max_iterations:
        # dapatin semua tetangga
        neighbors = bp.get_neighbors(current_state)
        
        if len(neighbors) == 0:
            # ga ada tetangga, catat skor dan berhenti
            history.append(current_score)
            break
        
        # cari tetangga terbaik
        best_neighbor = None
        best_neighbor_score = current_score
        
        for neighbor in neighbors:
            score = calculate_objective(neighbor, bp.kapasitas, bp.barang)
            if score < best_neighbor_score:  # Minimisasi
                best_neighbor_score = score
                best_neighbor = neighbor
        
        # kalo ga ada improvement, catat skor dan berhenti
        if best_neighbor is None:
            history.append(current_score)
            break
        
        current_state = best_neighbor
        current_score = best_neighbor_score
        history.append(current_score)
        iteration += 1
    
    return current_state, current_score, history, iteration


def stochastic_hill_climbing(bp: BinPacking, initial_state: List[List[str]], max_iterations: int = 1000) -> Tuple[List[List[str]], float, List[float], int]:
    """
    Stochastic Hill Climbing
    Pilih tetangga yang lebih baik secara RANDOM
    
    Returns:
        best_state, best_score, history, iterations
    """
    current_state = copy.deepcopy(initial_state)
    current_score = calculate_objective(current_state, bp.kapasitas, bp.barang)
    
    history = [current_score]
    iteration = 0
    
    while iteration < max_iterations:
        # dapatin semua tetangga
        neighbors = bp.get_neighbors(current_state)
        
        if len(neighbors) == 0:
            # gaada tetangga, catat skor dan berhenti
            history.append(current_score)
            break
        
        # cari semua tetangga yang lebih baik
        better_neighbors = []
        for neighbor in neighbors:
            score = calculate_objective(neighbor, bp.kapasitas, bp.barang)
            if score < current_score:
                better_neighbors.append((neighbor, score))
        
        # kalo ga ada tetangga yang lebih baik, catat skor dan berhenti
        if len(better_neighbors) == 0:
            history.append(current_score)
            break
        
        # pilih tetangga yang lebih baik secara random
        current_state, current_score = random.choice(better_neighbors)
        history.append(current_score)
        iteration += 1
    
    return current_state, current_score, history, iteration


def sideways_move_hill_climbing(bp: BinPacking, initial_state: List[List[str]], max_iterations: int = 1000, max_sideways: int = 100) -> Tuple[List[List[str]], float, List[float], int]:
    """
    Hill Climbing with Sideways Move
    Izinin perpindahan ke tetangga dengan skor SAMA (maksimal max_sideways kali)
    
    Returns:
        best_state, best_score, history, iterations
    """
    current_state = copy.deepcopy(initial_state)
    current_score = calculate_objective(current_state, bp.kapasitas, bp.barang)
    
    history = [current_score]
    iteration = 0
    sideways_count = 0
    
    while iteration < max_iterations and sideways_count < max_sideways:
        neighbors = bp.get_neighbors(current_state)
        
        if len(neighbors) == 0:
            # ga ada tetangga, catat skor dan berhenti
            history.append(current_score)
            break
        
        best_neighbor = None
        best_neighbor_score = current_score
        
        for neighbor in neighbors:
            score = calculate_objective(neighbor, bp.kapasitas, bp.barang)
            if score < best_neighbor_score:
                best_neighbor_score = score
                best_neighbor = neighbor
        
        # kalo ga ada improvement
        if best_neighbor is None:
            # coba sideways move
            sideways_neighbors = [n for n in neighbors 
                                if calculate_objective(n, bp.kapasitas, bp.barang) == current_score]
            
            if len(sideways_neighbors) > 0:
                best_neighbor = random.choice(sideways_neighbors)
                best_neighbor_score = current_score
                sideways_count += 1
            else:
                # ga ada improvement dan sideways move, catat dan berhenti
                history.append(current_score)
                break
        else:
            sideways_count = 0  # reset kalo ada improvement
        
        current_state = best_neighbor
        current_score = best_neighbor_score
        history.append(current_score)
        iteration += 1
    
    return current_state, current_score, history, iteration


def random_restart_hill_climbing(bp: BinPacking, max_restarts: int = 10, max_iterations_per_restart: int = 100) -> Tuple[List[List[str]], float, List[float], int, List[int]]:
    """
    Random Restart Hill Climbing
    Jalanin steepest ascent berkali-kali dengan initial state berbeda
    
    Returns:
        best_state, best_score, history, total_iterations, iterations_per_restart
    """
    global_best_state = None
    global_best_score = float('inf')
    global_history = []
    total_iterations = 0
    iterations_per_restart = []
    
    for restart in range(max_restarts):
        # generate state awal random baru
        initial_state = bp.initial_state_random()
        
        # jalanin steepest ascent
        state, score, history, iterations = steepest_ascent_hill_climbing(bp, initial_state, max_iterations_per_restart)
        
        iterations_per_restart.append(iterations)
        total_iterations += iterations
        global_history.extend(history)
        
        # update global best
        if score < global_best_score:
            global_best_score = score
            global_best_state = state
    
    return global_best_state, global_best_score, global_history, total_iterations, iterations_per_restart