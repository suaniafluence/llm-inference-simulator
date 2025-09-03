from dataclasses import dataclass
from typing import List, Optional
import math

@dataclass
class GPU:
    name: str
    vram_gb: float
    cuda_cores: int
    tensor_cores: int
    memory_bandwidth_gbps: float
    pcie_version: str = "4.0"
    pcie_lanes: int = 16
    
    def get_memory_bandwidth_bytes(self) -> float:
        """Bande passante en GB/s"""
        return self.memory_bandwidth_gbps / 8

@dataclass
class GPUSlot:
    gpu: Optional[GPU] = None
    pcie_version: str = "4.0"
    pcie_lanes: int = 16
    
    def is_compatible(self, gpu: GPU) -> bool:
        """Vérifie la compatibilité PCIe"""
        return (int(self.pcie_version.split('.')[0]) >= 
                int(gpu.pcie_version.split('.')[0]))

class GPUManager:
    def __init__(self):
        self.slots: List[GPUSlot] = []
        self.supported_gpus = {
            "RTX 4090": GPU("RTX 4090", 24, 16384, 512, 1008, "4.0"),
            "RTX 4080": GPU("RTX 4080", 16, 9728, 304, 716.8, "4.0"),
            "RTX 3090": GPU("RTX 3090", 24, 10496, 328, 936.2, "4.0"),
            "RTX 3080": GPU("RTX 3080", 10, 8704, 272, 760, "4.0"),
            "A100": GPU("A100", 80, 6912, 432, 2039, "4.0"),
            "H100": GPU("H100", 80, 16896, 528, 3352, "5.0"),
            "L40": GPU("L40", 48, 18176, 568, 864, "4.0"),
            "T4": GPU("T4", 16, 2560, 320, 320, "3.0")
        }
    
    def add_slot(self, pcie_version: str = "4.0", pcie_lanes: int = 16):
        self.slots.append(GPUSlot(pcie_version=pcie_version, pcie_lanes=pcie_lanes))
    
    def install_gpu(self, slot_index: int, gpu_name: str) -> bool:
        if slot_index >= len(self.slots):
            return False
        
        gpu = self.supported_gpus.get(gpu_name)
        if not gpu:
            return False
        
        if not self.slots[slot_index].is_compatible(gpu):
            return False
        
        self.slots[slot_index].gpu = gpu
        return True
    
    def get_total_vram(self) -> float:
        return sum(slot.gpu.vram_gb for slot in self.slots if slot.gpu)
    
    def get_gpu_names(self) -> List[str]:
        return list(self.supported_gpus.keys())
