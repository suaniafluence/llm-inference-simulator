from dataclasses import dataclass
from typing import Dict, List

@dataclass
class LLMModel:
    name: str
    parameters_b: float
    precision_bits: int
    context_length: int
    memory_required_gb: float
    
    def calculate_memory_needed(self, batch_size: int = 1) -> float:
        """Calcule la mémoire nécessaire pour l'inférence"""
        # Formule simplifiée : poids + activations + KV cache
        model_memory = (self.parameters_b * self.precision_bits) / 8  # GB
        kv_cache = (self.context_length * self.parameters_b * 0.01) / 8  # Estimation
        return model_memory + kv_cache * batch_size

class LLMManager:
    def __init__(self):
        self.models = {
            "Llama-2-7B": LLMModel("Llama-2-7B", 7, 16, 4096, 14),
            "Llama-2-13B": LLMModel("Llama-2-13B", 13, 16, 4096, 26),
            "Llama-2-70B": LLMModel("Llama-2-70B", 70, 16, 4096, 140),
            "Llama-4-70B": LLMModel("Llama-4-70B", 70, 16, 8192, 140),
            "Mistral-7B": LLMModel("Mistral-7B", 7, 16, 8192, 14),
            "Mixtral-8x7B": LLMModel("Mixtral-8x7B", 47, 16, 32768, 94),
            "GPT-3.5": LLMModel("GPT-3.5", 175, 16, 4096, 350),
            "Falcon-40B": LLMModel("Falcon-40B", 40, 16, 2048, 80),
            "GPT-OSS-20B": LLMModel("GPT-OSS-20B", 20, 16, 4096, 40),
            "GPT-OSS-120B": LLMModel("GPT-OSS-120B", 120, 16, 4096, 240)
        }
    
    def get_model_names(self) -> List[str]:
        return list(self.models.keys())
    
    def get_model(self, name: str) -> LLMModel:
        return self.models.get(name)
