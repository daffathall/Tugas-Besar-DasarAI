import random
from typing import List, Dict, Tuple
import copy

class BinPacking:
    def __init__(self, kapasitas: int, barang: Dict[str, int]):
        """
        Inisialisasi Bin Packing Problem
        
        Args:
            kapasitas: Kapasitas setiap kontainer/bin
            barang: Dictionary item_id -> ukuran
        """
        self.kapasitas = kapasitas
        self.barang = barang
        self.item_ids = list(barang.keys())
    
    def initial_state_random(self) -> List[List[str]]:
        """Generate state awal secara random"""
        state = []
        items = self.item_ids.copy()
        random.shuffle(items)
        
        for item in items:
            # Coba masukkan ke bin yang sudah ada
            placed = False
            for bin_items in state:
                if self._can_fit(bin_items, item):
                    bin_items.append(item)
                    placed = True
                    break
            
            # Buat bin baru jika tidak muat
            if not placed:
                state.append([item])
        
        return state
    
    def initial_state_first_fit(self) -> List[List[str]]:
        """Generate state awal menggunakan heuristik First Fit"""
        state = []
        
        for item in self.item_ids:
            placed = False
            
            # Coba masukkan ke bin yang sudah ada (bin pertama yang muat)
            for bin_items in state:
                if self._can_fit(bin_items, item):
                    bin_items.append(item)
                    placed = True
                    break
            
            # Buat bin baru jika tidak ada space
            if not placed:
                state.append([item])
        
        return state
    
    def initial_state_best_fit(self) -> List[List[str]]:
        """Generate state awal menggunakan heuristik Best Fit"""
        state = []
        
        for item in self.item_ids:
            best_bin = None
            best_remaining = float('inf')
            
            # Cari bin dengan sisa space minimum setelah item dimasukkan
            for bin_items in state:
                if self._can_fit(bin_items, item):
                    current_size = sum(self.barang[i] for i in bin_items)
                    remaining = self.kapasitas - current_size - self.barang[item]
                    
                    if remaining < best_remaining:
                        best_remaining = remaining
                        best_bin = bin_items
            
            if best_bin is not None:
                best_bin.append(item)
            else:
                state.append([item])
        
        return state
    
    def initial_state_worst(self) -> List[List[str]]:
        """
        Generate state awal terburuk - setiap item di bin terpisah
        Ini memberi Hill Climbing lebih banyak ruang untuk improvement
        """
        state = []
        items = self.item_ids.copy()
        random.shuffle(items)  # Shuffle untuk randomness
        
        for item in items:
            state.append([item])  # Setiap item di bin sendiri
        
        return state
    
    def initial_state_random_worst(self) -> List[List[str]]:
        """
        Generate state awal buruk secara random
        Assign item ke bin secara random dengan probabilitas tinggi membuat bin baru
        Untuk dataset kecil, gunakan worst() untuk visualisasi yang lebih baik
        """
        # Jika dataset kecil (< 15 items), gunakan worst initial state
        if len(self.item_ids) < 15:
            return self.initial_state_worst()
        
        state = []
        items = self.item_ids.copy()
        random.shuffle(items)
        
        for item in items:
            # 70% chance buat bin baru, 30% chance coba bin yang ada
            if random.random() < 0.7 or len(state) == 0:
                state.append([item])
            else:
                # Coba masukkan ke bin random yang sudah ada
                random_bin = random.choice(state)
                if self._can_fit(random_bin, item):
                    random_bin.append(item)
                else:
                    state.append([item])
        
        return state
    
    def _can_fit(self, bin_items: List[str], item: str) -> bool:
        """Cek apakah item bisa masuk ke bin"""
        current_size = sum(self.barang[i] for i in bin_items)
        return current_size + self.barang[item] <= self.kapasitas
    
    def get_bin_size(self, bin_items: List[str]) -> int:
        """Dapatkan total ukuran item dalam bin"""
        return sum(self.barang[item] for item in bin_items)
    
    def is_valid(self, state: List[List[str]]) -> bool:
        """Cek apakah state valid (tidak overflow, semua item ada)"""
        # Cek overflow
        for bin_items in state:
            if self.get_bin_size(bin_items) > self.kapasitas:
                return False
        
        # Cek semua item ada
        all_items = set()
        for bin_items in state:
            all_items.update(bin_items)
        
        return all_items == set(self.item_ids)
    
    def get_neighbors(self, state: List[List[str]]) -> List[List[List[str]]]:
        """
        Generate semua tetangga yang mungkin dengan:
        1. Memindahkan satu item ke bin lain
        2. Menukar dua item antar bin
        """
        neighbors = []
        
        # 1. Operasi Move (pindah)
        for i, bin_i in enumerate(state):
            for item in bin_i:
                # Coba pindahkan ke bin yang sudah ada
                for j, bin_j in enumerate(state):
                    if i != j:
                        new_state = copy.deepcopy(state)
                        new_state[i].remove(item)
                        new_state[j].append(item)
                        
                        # Hapus bin kosong
                        new_state = [b for b in new_state if len(b) > 0]
                        
                        if self.is_valid(new_state):
                            neighbors.append(new_state)
                
                # Coba pindahkan ke bin baru
                new_state = copy.deepcopy(state)
                new_state[i].remove(item)
                new_state.append([item])
                new_state = [b for b in new_state if len(b) > 0]
                
                if self.is_valid(new_state):
                    neighbors.append(new_state)
        
        # 2. Operasi Swap (tukar)
        for i, bin_i in enumerate(state):
            for item_i in bin_i:
                for j, bin_j in enumerate(state):
                    if i != j:
                        for item_j in bin_j:
                            new_state = copy.deepcopy(state)
                            
                            # Tukar item
                            new_state[i].remove(item_i)
                            new_state[i].append(item_j)
                            new_state[j].remove(item_j)
                            new_state[j].append(item_i)
                            
                            new_state = [b for b in new_state if len(b) > 0]
                            
                            if self.is_valid(new_state):
                                neighbors.append(new_state)
        
        return neighbors
    
    def get_random_neighbor(self, state: List[List[str]]) -> List[List[str]]:
        """Dapatkan satu tetangga random (untuk SA dan GA)"""
        max_attempts = 100
        
        for _ in range(max_attempts):
            new_state = copy.deepcopy(state)
            
            # Pilih secara random: move atau swap
            if random.random() < 0.7:  # 70% move, 30% swap
                # Operasi Move
                if len(new_state) > 0:
                    bin_idx = random.randint(0, len(new_state) - 1)
                    if len(new_state[bin_idx]) > 0:
                        item = random.choice(new_state[bin_idx])
                        new_state[bin_idx].remove(item)
                        
                        # Pilih tujuan: bin yang ada atau bin baru
                        if random.random() < 0.8 and len(new_state) > 1:
                            dest_idx = random.randint(0, len(new_state) - 1)
                            new_state[dest_idx].append(item)
                        else:
                            new_state.append([item])
            else:
                # Operasi Swap
                if len(new_state) >= 2:
                    bin1_idx = random.randint(0, len(new_state) - 1)
                    bin2_idx = random.randint(0, len(new_state) - 1)
                    
                    if bin1_idx != bin2_idx and len(new_state[bin1_idx]) > 0 and len(new_state[bin2_idx]) > 0:
                        item1 = random.choice(new_state[bin1_idx])
                        item2 = random.choice(new_state[bin2_idx])
                        
                        new_state[bin1_idx].remove(item1)
                        new_state[bin1_idx].append(item2)
                        new_state[bin2_idx].remove(item2)
                        new_state[bin2_idx].append(item1)
            
            # Hapus bin kosong
            new_state = [b for b in new_state if len(b) > 0]
            
            if self.is_valid(new_state):
                return new_state
        
        # Jika tidak ada tetangga valid, return state asli
        return copy.deepcopy(state)