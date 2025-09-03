let config = {};

async function loadConfig() {
    const response = await fetch('/api/config');
    config = await response.json();
    renderSlots();
    renderModelSelect();
}

function renderSlots() {
    const container = document.getElementById('gpu-slots');
    container.innerHTML = '';
    
    config.slots.forEach((slot, index) => {
        const slotDiv = document.createElement('div');
        slotDiv.className = 'slot';
        
        const select = document.createElement('select');
        select.innerHTML = '<option value="">Aucune GPU</option>';
        
        config.gpu_models.forEach(gpu => {
            const option = document.createElement('option');
            option.value = gpu;
            option.textContent = gpu;
            if (slot.gpu && slot.gpu.name === gpu) {
                option.selected = true;
            }
            select.appendChild(option);
        });
        
        select.onchange = () => installGPU(index, select.value);
        
        slotDiv.innerHTML = `
            <div class="slot-info">
                <strong>Slot ${index + 1}</strong><br>
                PCIe ${slot.pcie_version} x${slot.pcie_lanes}
            </div>
            <div class="gpu-info ${slot.gpu ? 'gpu-selected' : 'gpu-empty'}">
                ${slot.gpu ? 
                    `GPU: ${slot.gpu.name}<br>
                     VRAM: ${slot.gpu.vram_gb}GB<br>
                     CUDA: ${slot.gpu.cuda_cores} cores` :
                    'Aucune GPU installée'
                }
            </div>
        `;
        
        const selectContainer = document.createElement('div');
        selectContainer.appendChild(select);
        slotDiv.appendChild(selectContainer);
        
        container.appendChild(slotDiv);
    });
}

function renderModelSelect() {
    const select = document.getElementById('model-select');
    select.innerHTML = '<option value="">Choisir un modèle LLM</option>';
    
    config.llm_models.forEach(model => {
        const option = document.createElement('option');
        option.value = model;
        option.textContent = model;
        select.appendChild(option);
    });
}

async function installGPU(slotIndex, gpuName) {
    const response = await fetch('/api/install_gpu', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({slot_index: slotIndex, gpu_name: gpuName})
    });
    
    const result = await response.json();
    if (result.success) {
        loadConfig();
    }
}

async function addSlot() {
    await fetch('/api/slots', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action: 'add', pcie_version: '4.0', pcie_lanes: 16})
    });
    loadConfig();
}

async function runInference() {
    const modelName = document.getElementById('model-select').value;
   
