from typing import Dict, List, Tuple
from dataclasses import dataclass
from .gpu import GPUManager
from .llm import LLMManager

@dataclass
class InferenceResult:
    success: bool
    message: str
    estimated_time: float
    memory_usage: Dict[str, float]
    gpu_utilization: List[float]

class InferenceEngine:
    def __init__(self, gpu_manager: GPUManager, llm_manager: LLMManager):
        self.gpu_manager = gpu_manager
        self.llm_manager = llm_manager
        self.active_inferences = []
    
    def can_run_inference(self, model_name: str, batch_size: int = 1) -> InferenceResult:
        model = self.llm_manager.get_model(model_name)
        if not model:
            return InferenceResult(
                success=False,
                message="Modèle non trouvé",
                estimated_time=0,
                memory_usage={},
                gpu_utilization=[]
            )
        
        total_vram = self.gpu_manager.get_total_vram()
        required_memory = model.calculate_memory_needed(batch_size)
        
        # Vérifier la mémoire
        if required_memory > total_vram:
            return InferenceResult(
                success=False,
                message=f"Mémoire insuffisante: {required_memory:.1f}GB requis vs {total_vram:.1f}GB disponible",
                estimated_time=0,
                memory_usage={
                    "required": required_memory,
                    "available": total_vram,
                    "deficit": required_memory - total_vram
                },
                gpu_utilization=[0] * len(self.gpu_manager.slots)
            )
        
        # Vérifier la compatibilité PCIe
        incompatible_slots = [
            i for i, slot in enumerate(self.gpu_manager.slots)
            if slot.gpu and not slot.is_compatible(slot.gpu)
        ]
        
        if incompatible_slots:
            return InferenceResult(
                success=False,
                message=f"Slots PCIe incompatibles: {incompatible_slots}",
                estimated_time=0,
                memory_usage={},
                gpu_utilization=[0] * len(self.gpu_manager.slots)
            )
        
        # Calculer le temps estimé
        active_gpus = [slot.gpu for slot in self.gpu_manager.slots if slot.gpu]
        total_cuda_cores = sum(gpu.cuda_cores for gpu in active_gpus)
        estimated_time = (model.parameters_b * 1000) / (total_cuda_cores * 0.1)  # Simplifié
        
        # Répartition de la charge
        gpu_utilization = []
        for slot in self.gpu_manager.slots:
            if slot.gpu:
                utilization = (required_memory / total_vram) * 100
                gpu_utilization.append(min(utilization, 100))
            else:
                gpu_utilization.append(0)
        
        return InferenceResult(
            success=True,
            message="Inférence possible",
            estimated_time=estimated_time,
            memory_usage={
                "required": required_memory,
                "available": total_vram,
                "utilization": (required_memory / total_vram) * 100
            },
            gpu_utilization=gpu_utilization
        )
    
    def run_multiple_inferences(self, model_name: str, count: int) -> List[InferenceResult]:
        results = []
        for i in range(count):
            result = self.can_run_inference(model_name, batch_size=1)
            results.append(result)
        return results
