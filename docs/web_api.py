#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web API pour Interface Études - Projet 44Ha
API REST simple pour connecter l'interface web aux études
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
from pathlib import Path
from auto_study_launcher import AutoStudyLauncher

app = Flask(__name__)
CORS(app)

# Instance du launcher
launcher = AutoStudyLauncher()

@app.route('/api/studies', methods=['GET'])
def list_studies():
    """Liste les études disponibles"""
    studies = {
        "faisabilite_ultra_complete": {
            "name": "Évaluation Ultra-Complète",
            "description": "Due diligence technique avec experts spécialisés",
            "duration": "2-3 minutes",
            "expert_profiles": ["Céline ÉCOLOGIE", "Sylvie GÉOMARKETING", "François AGRIVOLTAÏSME", "Paul HYDRAULIQUE", "Marc PÉDOLOGIE", "Jean CIRCUITS-COURTS"],
            "cost_estimate": "110k€ études terrain"
        },
        "structure_couts_detaillee": {
            "name": "Analyse Coûts Détaillée",
            "description": "Structure coûts récurrents et non récurrents", 
            "duration": "1-2 minutes",
            "expert_profiles": ["Expert Financier"],
            "cost_estimate": "Analyse gratuite"
        },
        "modes_financement": {
            "name": "Solutions Financement",
            "description": "Modes financement optimisés et diversifiés",
            "duration": "1-2 minutes",
            "expert_profiles": ["Expert Bancaire", "Conseiller Financement"],
            "cost_estimate": "Analyse gratuite"
        },
        "marche_hotellerie": {
            "name": "Étude Marché Hôtellerie",
            "description": "Validation besoin hôtelier + financement sans apport",
            "duration": "1-2 minutes",
            "expert_profiles": ["Expert Hôtellerie", "Expert Financement"],
            "cost_estimate": "Analyse gratuite"
        },
        "protection_patrimoine": {
            "name": "Protection Patrimoine Familial",
            "description": "Solutions mise à disposition terrain sans hypothèque",
            "duration": "1-2 minutes",
            "expert_profiles": ["Expert Succession", "Notaire Spécialisé"],
            "cost_estimate": "Analyse gratuite"
        },
        "debat_multi_agents": {
            "name": "Débat Multi-Agents",
            "description": "Débat contradictoire entre experts IA spécialisés",
            "duration": "3-5 minutes",
            "expert_profiles": ["8 experts IA spécialisés"],
            "cost_estimate": "Simulation gratuite"
        }
    }
    
    queue_status = launcher.get_queue_status()
    
    return jsonify({
        "success": True,
        "studies": studies,
        "queue_status": queue_status
    })

@app.route('/api/studies/launch', methods=['POST'])
def launch_study():
    """Lance une nouvelle étude"""
    data = request.get_json()
    
    if not data or 'study_key' not in data:
        return jsonify({"error": "study_key requis"}), 400
    
    study_key = data['study_key']
    parameters = data.get('parameters', {})
    
    # Ajouter le contexte du projet
    parameters.update({
        "project_location": "Gontaud-de-Nogaret",
        "project_surface": "44 hectares",
        "project_lake": "Lac de Cayre (150m)",
        "project_context": "Écosystème composite agritourisme + solaire + production"
    })
    
    result = launcher.add_study_to_queue(study_key, parameters)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@app.route('/api/studies/status', methods=['GET'])
def get_studies_status():
    """Récupère le statut des études"""
    return jsonify(launcher.get_queue_status())

@app.route('/api/studies/results', methods=['GET'])
def get_results():
    """Récupère les résultats des études"""
    results = launcher.get_results()
    return jsonify({
        "success": True,
        "results": results,
        "total": len(results)
    })

@app.route('/api/files/download/<path:filename>', methods=['GET'])
def download_file(filename):
    """Télécharge un fichier généré"""
    file_path = Path(__file__).parent / filename
    
    if not file_path.exists():
        return jsonify({"error": "Fichier non trouvé"}), 404
    
    # Vérifier que c'est un fichier autorisé
    allowed_extensions = ['.md', '.json', '.csv', '.pdf']
    if file_path.suffix not in allowed_extensions:
        return jsonify({"error": "Type de fichier non autorisé"}), 403
    
    return send_file(file_path, as_attachment=True)

@app.route('/api/project', methods=['GET'])
def get_project_info():
    """Informations du projet"""
    return jsonify({
        "success": True,
        "project": {
            "name": "Écosystème Lac de Cayre - 44Ha",
            "location": "Gontaud-de-Nogaret",
            "surface": "44 hectares",
            "lake": "Lac de Cayre (150m)",
            "investment": "3.1M€",
            "roi": "11.2%",
            "protection": "100%",
            "status": "Études complétées"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Santé de l'API"""
    return jsonify({
        "status": "healthy",
        "launcher_active": True,
        "timestamp": launcher.get_queue_status()
    })

if __name__ == '__main__':
    print("🌐 Démarrage Web API - Interface Études")
    print("=" * 50)
    print("📡 API disponible sur http://localhost:5001")
    print("🔗 Connecter l'interface web à cette API")
    
    # Démarrer le processeur de queue
    import threading
    processor_thread = threading.Thread(target=launcher.process_queue, daemon=True)
    processor_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5001)
