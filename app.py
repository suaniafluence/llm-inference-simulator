from flask import Flask, render_template, jsonify, request
from models.gpu import GPUManager
from models.llm import LLMManager
from models.inference import InferenceEngine
import json

app = Flask(__name__)

# Initialisation des managers
gpu_manager = GPUManager()
llm_manager = LLMManager()
inference_engine = InferenceEngine(gpu_manager, llm_manager)

# Configuration initiale
for _ in range(4):  # 4 slots PCIe par défaut
    gpu_manager.add_slot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({
        'gpu_models': gpu_manager.get_gpu_names(),
        'llm_models': llm_manager.get_model_names(),
        'slots': [
            {
                'index': i,
                'pcie_version': slot.pcie_version,
                'pcie_lanes': slot.pcie_lanes,
                'gpu': {
                    'name': slot.gpu.name,
                    'vram_gb': slot.gpu.vram_gb,
                    'cuda_cores': slot.gpu.cuda_cores
                } if slot.gpu else None
            }
            for i, slot in enumerate(gpu_manager.slots)
        ]
    })

@app.route('/api/slots', methods=['POST'])
def update_slots():
    data = request.json
    action = data.get('action')
    
    if action == 'add':
        pcie_version = data.get('pcie_version', '4.0')
        pcie_lanes = data.get('pcie_lanes', 16)
        gpu_manager.add_slot(pcie_version, pcie_lanes)
    elif action == 'remove' and len(gpu_manager.slots) > 1:
        gpu_manager.slots.pop()
    
    return jsonify({'success': True})

@app.route('/api/install_gpu', methods=['POST'])
def install_gpu():
    data = request.json
    slot_index = data.get('slot_index')
    gpu_name = data.get('gpu_name')
    
    success = gpu_manager.install_gpu(slot_index, gpu_name)
    return jsonify({'success': success})

@app.route('/api/test_inference', methods=['POST'])
def test_inference():
    data = request.json
    model_name = data.get('model_name')
    inference_count = data.get('inference_count', 1)
    
    results = inference_engine.run_multiple_inferences(model_name, inference_count)
    
    return jsonify({
        'results': [
            {
                'success': r.success,
                'message': r.message,
                'estimated_time': r.estimated_time,
                'memory_usage': r.memory_usage,
                'gpu_utilization': r.gpu_utilization,
                'color': 'green' if r.success else 'red'
            }
            for r in results
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
