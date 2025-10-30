import random
import copy
from typing import List, Dict, Tuple
from bin_packing import BinPacking
from objective_function import calculate_objective, calculate_fitness

def genetic_algorithm(
    bp: BinPacking,
    population_size: int = 50,
    generations: int = 100,
    mutation_rate: float = 0.1,
    crossover_rate: float = 0.8,
    elitism: int = 2
) -> Tuple[List[List[str]], float, List[float], List[float]]:
    """
    Algoritma: Genetika untuk Bin Packing
    
    Args:
        bp: Instance BinPacking
        population_size: Jumlah individu dalam populasi
        generations: Jumlah generasi
        mutation_rate: Probabilitas mutasi
        crossover_rate: Probabilitas crossover
        elitism: Jumlah individu terbaik yang dipertahankan
    
    Returns:
        best_state, best_score, best_history, avg_history
    """
    # Inisialisasi populasi
    population = [bp.initial_state_random() for _ in range(population_size)]
    
    best_history = []
    avg_history = []
    
    for generation in range(generations):
        # Evaluasi fitness
        fitness_scores = []
        objective_scores = []
        
        for individual in population:
            obj_score = calculate_objective(individual, bp.kapasitas, bp.barang)
            fit_score = calculate_fitness(individual, bp.kapasitas, bp.barang)
            objective_scores.append(obj_score)
            fitness_scores.append(fit_score)
        
        # Lacak statistik
        best_history.append(min(objective_scores))
        avg_history.append(sum(objective_scores) / len(objective_scores))
        
        # Seleksi + Crossover + Mutasi
        new_population = []
        
        # Elitisme: pertahankan individu terbaik
        if elitism > 0:
            elite_indices = sorted(range(len(objective_scores)), 
                                 key=lambda i: objective_scores[i])[:elitism]
            for idx in elite_indices:
                new_population.append(copy.deepcopy(population[idx]))
        
        # Generate keturunan
        while len(new_population) < population_size:
            # Seleksi
            parent1 = tournament_selection(population, fitness_scores)
            parent2 = tournament_selection(population, fitness_scores)
            
            # Crossover
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2, bp)
            else:
                child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
            
            # Mutasi
            if random.random() < mutation_rate:
                child1 = mutate(child1, bp)
            if random.random() < mutation_rate:
                child2 = mutate(child2, bp)
            
            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)
        
        population = new_population[:population_size]
    
    # Kembalikan individu terbaik
    final_scores = [calculate_objective(ind, bp.kapasitas, bp.barang) for ind in population]
    best_idx = final_scores.index(min(final_scores))
    best_state = population[best_idx]
    best_score = final_scores[best_idx]
    
    return best_state, best_score, best_history, avg_history


def tournament_selection(population: List, fitness_scores: List[float], tournament_size: int = 3) -> List[List[str]]:
    """
    Seleksi Turnamen
    Pilih individu terbaik dari subset acak
    """
    tournament_indices = random.sample(range(len(population)), tournament_size)
    best_idx = max(tournament_indices, key=lambda i: fitness_scores[i])
    return copy.deepcopy(population[best_idx])


def roulette_wheel_selection(population: List, fitness_scores: List[float]) -> List[List[str]]:
    """
    Seleksi Roulette Wheel
    Probabilitas proporsional terhadap fitness
    """
    total_fitness = sum(fitness_scores)
    
    if total_fitness == 0:
        return copy.deepcopy(random.choice(population))
    
    pick = random.uniform(0, total_fitness)
    current = 0
    
    for individual, fitness in zip(population, fitness_scores):
        current += fitness
        if current >= pick:
            return copy.deepcopy(individual)
    
    return copy.deepcopy(population[-1])


def crossover(parent1: List[List[str]], parent2: List[List[str]], bp: BinPacking) -> Tuple[List[List[str]], List[List[str]]]:
    """
    One-Point Crossover untuk Bin Packing
    Pisahkan kontainer dan gabungkan
    """
    if len(parent1) == 0 or len(parent2) == 0:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)
    
    # One-point crossover
    cut1 = random.randint(0, len(parent1))
    cut2 = random.randint(0, len(parent2))
    
    # Buat anak
    child1_bins = parent1[:cut1] + parent2[cut2:]
    child2_bins = parent2[:cut2] + parent1[cut1:]
    
    # Perbaiki: pastikan semua item ada tepat satu kali
    child1 = repair_solution(child1_bins, bp)
    child2 = repair_solution(child2_bins, bp)
    
    return child1, child2


def repair_solution(bins: List[List[str]], bp: BinPacking) -> List[List[str]]:
    """
    Perbaiki solusi untuk memastikan semua item ada tepat satu kali
    """
    # Kumpulkan semua item dalam kontainer saat ini
    present_items = set()
    for bin_items in bins:
        present_items.update(bin_items)
    
    # Temukan item yang hilang dan duplikat
    all_items = set(bp.item_ids)
    missing_items = all_items - present_items
    
    # Hapus duplikat
    seen = set()
    cleaned_bins = []
    for bin_items in bins:
        cleaned_bin = []
        for item in bin_items:
            if item not in seen:
                cleaned_bin.append(item)
                seen.add(item)
        if len(cleaned_bin) > 0:
            cleaned_bins.append(cleaned_bin)
    
    # Tambahkan item yang hilang menggunakan First Fit
    for item in missing_items:
        placed = False
        for bin_items in cleaned_bins:
            bin_size = sum(bp.barang[i] for i in bin_items)
            if bin_size + bp.barang[item] <= bp.kapasitas:
                bin_items.append(item)
                placed = True
                break
        
        if not placed:
            cleaned_bins.append([item])
    
    return cleaned_bins


def mutate(individual: List[List[str]], bp: BinPacking) -> List[List[str]]:
    """
    Mutasi: pindahkan atau tukar item secara acak
    """
    mutated = copy.deepcopy(individual)
    
    if len(mutated) == 0:
        return mutated
    
    # Pilih tipe mutasi
    mutation_type = random.choice(['move', 'swap'])
    
    if mutation_type == 'move' and len(mutated) > 0:
        # Pindahkan item acak ke kontainer acak
        source_bin_idx = random.randint(0, len(mutated) - 1)
        if len(mutated[source_bin_idx]) > 0:
            item = random.choice(mutated[source_bin_idx])
            mutated[source_bin_idx].remove(item)
            
            # Tambahkan ke kontainer acak atau kontainer baru
            if random.random() < 0.5 and len(mutated) > 1:
                dest_bin_idx = random.randint(0, len(mutated) - 1)
                mutated[dest_bin_idx].append(item)
            else:
                mutated.append([item])
    
    elif mutation_type == 'swap' and len(mutated) >= 2:
        # Tukar item antara dua kontainer acak
        bin1_idx = random.randint(0, len(mutated) - 1)
        bin2_idx = random.randint(0, len(mutated) - 1)
        
        if bin1_idx != bin2_idx and len(mutated[bin1_idx]) > 0 and len(mutated[bin2_idx]) > 0:
            item1 = random.choice(mutated[bin1_idx])
            item2 = random.choice(mutated[bin2_idx])
            
            mutated[bin1_idx].remove(item1)
            mutated[bin1_idx].append(item2)
            mutated[bin2_idx].remove(item2)
            mutated[bin2_idx].append(item1)
    
    # Hapus kontainer kosong
    mutated = [b for b in mutated if len(b) > 0]
    
    # Pastikan valid
    if not bp.is_valid(mutated):
        mutated = repair_solution(mutated, bp)
    
    return mutated