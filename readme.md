Installation et Utilisation
bash
Copy
# Installation
pip install -r requirements.txt

# Lancement
python app.py

# Accès
Ouvrir http://localhost:5000 dans votre navigateur
Fonctionnalités
Configuration GPU :
Ajout/suppression de slots PCIe
Sélection du modèle GPU par slot
Vérification de compatibilité PCIe
Test d'inférence :
Sélection du modèle LLM
Nombre d'inférences simultanées
Feedback visuel vert/rouge
Détails sur l'utilisation mémoire
Visualisation :
Interface moderne et responsive
Cartes GPU colorées selon l'état
Résultats clairs avec indicateurs visuels
Le système est extensible et peut être enrichi avec des fonctionnalités comme la parallélisation multi-GPU, la quantification, ou des benchmarks plus précis.
