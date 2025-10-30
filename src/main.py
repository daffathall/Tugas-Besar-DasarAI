import time
from utils import load_data, print_state
from bin_packing import BinPacking
from objective_function import calculate_objective, get_num_bins
from hill_climbing import (steepest_ascent_hill_climbing, stochastic_hill_climbing, sideways_move_hill_climbing, random_restart_hill_climbing)
from simulated_annealing import simulated_annealing
from genetic_algorithm import genetic_algorithm
from visualizer import (plot_convergence, visualize_bins, plot_sa_probability, plot_ga_convergence, plot_hc_comparison, print_state_detailed)

def main():
    print("BIN PACKING PROBLEM SOLVER - LOCAL SEARCH ALGORITHMS")
    
    # Memuat data
    data = load_data('data/input.json')
    kapasitas = data['kapasitas_kontainer']
    barang_list = data['barang']
    barang = {item['id']: item['ukuran'] for item in barang_list}
    
    print(f"\nProblem Info:")
    print(f"  Bin Capacity: {kapasitas}")
    print(f"  Number of Items: {len(barang)}")
    print(f"  Total Size: {sum(barang.values())}")
    print(f"  Theoretical Minimum Bins: {sum(barang.values()) / kapasitas:.2f}")
    
    # Inisialisasi Bin Packing
    bp = BinPacking(kapasitas, barang)
    
    # Uji setiap algoritma
    print("TESTING ALGORITHMS")
    
    # 1. Hill Climbing - Semua 4 Varian
    print("\n[1] HILL CLIMBING ALGORITHMS")
    
    hc_histories = {}
    hc_results = {}
    
    # 1a. Steepest Ascent Hill Climbing
    print("\n[1a] Running Steepest Ascent Hill Climbing...")
    initial_state_hc1 = bp.initial_state_random_worst()  # Gunakan kondisi awal terburuk
    initial_score_1 = calculate_objective(initial_state_hc1, kapasitas, barang)
    print(f"     Initial bins: {len(initial_state_hc1)}, Score: {initial_score_1:.2f}")
    
    start = time.time()
    hc1_state, hc1_score, hc1_history, hc1_iterations = steepest_ascent_hill_climbing(bp, initial_state_hc1, max_iterations=500)
    hc1_time = time.time() - start
    
    hc_histories['steepest_ascent'] = hc1_history
    hc_results['Steepest Ascent'] = {'state': hc1_state, 'score': hc1_score, 'bins': get_num_bins(hc1_state), 'iterations': hc1_iterations, 'time': hc1_time}
    
    print(f"     Final bins: {get_num_bins(hc1_state)}, Score: {hc1_score:.2f}")
    print(f"     Iterations: {hc1_iterations}, Time: {hc1_time:.3f}s")
    
    # 1b. Stochastic Hill Climbing
    print("\n[1b] Running Stochastic Hill Climbing...")
    initial_state_hc2 = bp.initial_state_random_worst()  # Gunakan kondisi awal terburuk
    initial_score_2 = calculate_objective(initial_state_hc2, kapasitas, barang)
    print(f"     Initial bins: {len(initial_state_hc2)}, Score: {initial_score_2:.2f}")
    
    start = time.time()
    hc2_state, hc2_score, hc2_history, hc2_iterations = stochastic_hill_climbing(bp, initial_state_hc2, max_iterations=500)
    hc2_time = time.time() - start
    
    hc_histories['stochastic'] = hc2_history
    hc_results['Stochastic'] = {'state': hc2_state, 'score': hc2_score, 'bins': get_num_bins(hc2_state), 'iterations': hc2_iterations, 'time': hc2_time}
    
    print(f"     Final bins: {get_num_bins(hc2_state)}, Score: {hc2_score:.2f}")
    print(f"     Iterations: {hc2_iterations}, Time: {hc2_time:.3f}s")
    
    # 1c. Sideways Move Hill Climbing
    print("\n[1c] Running Sideways Move Hill Climbing...")
    initial_state_hc3 = bp.initial_state_random_worst()  # Gunakan kondisi awal terburuk
    initial_score_3 = calculate_objective(initial_state_hc3, kapasitas, barang)
    print(f"     Initial bins: {len(initial_state_hc3)}, Score: {initial_score_3:.2f}")
    
    start = time.time()
    hc3_state, hc3_score, hc3_history, hc3_iterations = sideways_move_hill_climbing(bp, initial_state_hc3, max_iterations=500, max_sideways=100)
    hc3_time = time.time() - start
    
    hc_histories['sideways'] = hc3_history
    hc_results['Sideways Move'] = {'state': hc3_state, 'score': hc3_score, 'bins': get_num_bins(hc3_state), 'iterations': hc3_iterations, 'time': hc3_time}
    
    print(f"     Final bins: {get_num_bins(hc3_state)}, Score: {hc3_score:.2f}")
    print(f"     Iterations: {hc3_iterations}, Time: {hc3_time:.3f}s")
    
    # 1d. Random Restart Hill Climbing
    print("\n[1d] Running Random Restart Hill Climbing...")
    print(f"     Jumlah restart: 10")
    
    start = time.time()
    hc4_state, hc4_score, hc4_history, hc4_total_iter, hc4_iter_per_restart = random_restart_hill_climbing(bp, max_restarts=10, max_iterations_per_restart=100)
    hc4_time = time.time() - start
    
    hc_histories['random_restart'] = hc4_history
    hc_results['Random Restart'] = {'state': hc4_state, 'score': hc4_score, 'bins': get_num_bins(hc4_state), 'iterations': hc4_total_iter, 'time': hc4_time}
    
    print(f"     Final bins: {get_num_bins(hc4_state)}, Score: {hc4_score:.2f}")
    print(f"     Total iterations: {hc4_total_iter}, Time: {hc4_time:.3f}s")
    
    # Visualisasikan semua varian Hill Climbing
    plot_hc_comparison(hc_histories, "hc_all_variants")
    
    # Temukan hasil Hill Climbing terbaik
    best_hc_name = min(hc_results.keys(), key=lambda k: hc_results[k]['score'])
    best_hc = hc_results[best_hc_name]
    
    print(f"\n     >> Best Hill Climbing: {best_hc_name}")
    print(f"        Bins: {best_hc['bins']}, Score: {best_hc['score']:.2f}")
    
    # Visualisasikan hasil Hill Climbing terbaik
    visualize_bins(best_hc['state'], kapasitas, barang, f"Hill Climbing ({best_hc_name}) - Final State", "hc_best_final_state")
    
    # Gunakan HC terbaik untuk ringkasan
    hc_state = best_hc['state']
    hc_score = best_hc['score']
    hc_time = best_hc['time']
    
    # 2. Simulated Annealing
    print("\n[2] Running Simulated Annealing...")
    initial_state_sa = bp.initial_state_random_worst()  # Gunakan kondisi awal terburuk
    initial_score_sa = calculate_objective(initial_state_sa, kapasitas, barang)
    print(f"    Initial bins: {len(initial_state_sa)}, Score: {initial_score_sa:.2f}")
    
    start = time.time()
    sa_state, sa_score, sa_history, sa_prob, sa_stuck = simulated_annealing(bp, initial_state_sa, T_initial=1000, T_min=0.1, alpha=0.95, max_iterations=1000)
    sa_time = time.time() - start
    
    print(f"    Final bins: {get_num_bins(sa_state)}")
    print(f"    Objective score: {sa_score:.2f}")
    print(f"    Stuck count: {sa_stuck}")
    print(f"    Time: {sa_time:.3f} seconds")
    
    # Visualisasi
    plot_convergence(sa_history, "Simulated Annealing - Convergence", "sa_convergence")
    plot_sa_probability(sa_prob, "sa_probability")
    visualize_bins(sa_state, kapasitas, barang, "Simulated Annealing - Final State", "sa_final_state")
    print_state_detailed(sa_state, kapasitas, barang, "Simulated Annealing - Final State")
    
    # 3. Genetic Algorithm
    print("\n[3] Running Genetic Algorithm...")
    
    start = time.time()
    ga_state, ga_score, ga_best_hist, ga_avg_hist = genetic_algorithm(bp, population_size=50, generations=100, mutation_rate=0.1, crossover_rate=0.8)
    ga_time = time.time() - start
    
    print(f"    Final bins: {get_num_bins(ga_state)}")
    print(f"    Objective score: {ga_score:.2f}")
    print(f"    Time: {ga_time:.3f} seconds")
    
    # Visualisasi
    plot_ga_convergence(ga_best_hist, ga_avg_hist, "Genetic Algorithm - Convergence", "ga_convergence")
    visualize_bins(ga_state, kapasitas, barang, "Genetic Algorithm - Final State", "ga_final_state")
    print_state_detailed(ga_state, kapasitas, barang, "Genetic Algorithm - Final State")
    
    # Ringkasan
    print("SUMMARY")
    print("="*70)
    
    # Ringkasan varian Hill Climbing
    print("\nHill Climbing Variants:")
    print(f"{'Variant':<25} {'Bins':<8} {'Score':<12} {'Iterations':<12} {'Time (s)':<10}")
    print("-"*70)
    for name, result in hc_results.items():
        print(f"{name:<25} {result['bins']:<8} {result['score']:<12.2f} {result['iterations']:<12} {result['time']:<10.3f}")
    
    # Overall summary
    print("\n" + "-"*70)
    print(f"{'Algorithm':<30} {'Bins':<10} {'Score':<15} {'Time (s)':<10}")
    print("-"*70)
    print(f"{'Hill Climbing (Best)':<30} {get_num_bins(hc_state):<10} {hc_score:<15.2f} {hc_time:<10.3f}")
    print(f"{'Simulated Annealing':<30} {get_num_bins(sa_state):<10} {sa_score:<15.2f} {sa_time:<10.3f}")
    print(f"{'Genetic Algorithm':<30} {get_num_bins(ga_state):<10} {ga_score:<15.2f} {ga_time:<10.3f}")
    print("="*70)
    
    print("\n>> All visualizations saved to experiments/results/")
    print(">> Program completed successfully!")

if __name__ == "__main__":
    main()