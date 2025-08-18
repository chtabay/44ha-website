#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Study Launcher - Pont entre Interface Web et Scripts Python
Gestion automatisée des nouvelles études pour le projet 44Ha
"""

import os
import json
import subprocess
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import time

class AutoStudyLauncher:
    """Lanceur automatique d'études depuis l'interface web"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent / "44Ha"
        self.scripts_path = self.base_path / "scripts"
        self.docs_path = Path(__file__).parent
        self.queue_file = self.docs_path / "study_queue.json"
        self.status_file = self.docs_path / "study_status.json"
        self.results_file = self.docs_path / "study_results.json"
        
        # Mapping des études vers les scripts
        self.study_scripts = {
            "faisabilite_ultra_complete": {
                "script": "evaluation/faisabilite_evaluation_ultra_complete.py",
                "output_patterns": ["evaluation_ultra_complete_*.md", "evaluation_ultra_complete_*.json"],
                "estimated_duration": 180  # 3 minutes
            },
            "structure_couts_detaillee": {
                "script": "evaluation/structure_couts_detaillee_composite.py", 
                "output_patterns": ["structure_couts_detaillee_*.md", "structure_couts_detaillee_*.json"],
                "estimated_duration": 90  # 1.5 minutes
            },
            "modes_financement": {
                "script": "evaluation/modes_financement_optimises.py",
                "output_patterns": ["modes_financement_optimises_*.md", "modes_financement_optimises_*.json"],
                "estimated_duration": 90
            },
            "marche_hotellerie": {
                "script": "evaluation/analyse_hotellerie_et_financement_sans_apport.py",
                "output_patterns": ["analyse_hotellerie_financement_*.md", "analyse_hotellerie_financement_*.json"],
                "estimated_duration": 90
            },
            "protection_patrimoine": {
                "script": "evaluation/analyse_terrain_sans_risque_heritage.py",
                "output_patterns": ["protection_patrimoine_familial_*.md", "protection_patrimoine_familial_*.json"],
                "estimated_duration": 90
            },
            "debat_multi_agents": {
                "script": "debats/launch_advanced_debate.py",
                "output_patterns": ["debate_*.md", "debate_*.json", "projets_*.csv"],
                "estimated_duration": 300  # 5 minutes
            }
        }
        
        self._init_status_files()
    
    def _init_status_files(self):
        """Initialise les fichiers de statut"""
        for file_path in [self.queue_file, self.status_file, self.results_file]:
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f)
    
    def add_study_to_queue(self, study_key: str, parameters: Dict = None) -> Dict:
        """Ajoute une étude à la queue d'exécution"""
        if study_key not in self.study_scripts:
            return {"error": f"Étude inconnue: {study_key}"}
        
        # Générer un ID unique
        study_id = f"{study_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Charger la queue actuelle
        with open(self.queue_file, 'r', encoding='utf-8') as f:
            queue = json.load(f)
        
        # Ajouter l'étude
        queue[study_id] = {
            "study_key": study_key,
            "parameters": parameters or {},
            "timestamp": datetime.now().isoformat(),
            "status": "queued",
            "estimated_duration": self.study_scripts[study_key]["estimated_duration"]
        }
        
        # Sauvegarder
        with open(self.queue_file, 'w', encoding='utf-8') as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "study_id": study_id,
            "message": f"Étude {study_key} ajoutée à la queue"
        }
    
    def process_queue(self):
        """Traite la queue d'études en arrière-plan"""
        while True:
            # Charger la queue
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                queue = json.load(f)
            
            # Chercher les études en attente
            pending_studies = {
                k: v for k, v in queue.items() 
                if v.get("status") == "queued"
            }
            
            if pending_studies:
                # Prendre la première étude
                study_id = list(pending_studies.keys())[0]
                study_data = pending_studies[study_id]
                
                print(f"🚀 Traitement étude: {study_id}")
                self._execute_study(study_id, study_data)
                
                # Mettre à jour la queue
                queue[study_id]["status"] = "completed"
                with open(self.queue_file, 'w', encoding='utf-8') as f:
                    json.dump(queue, f, indent=2, ensure_ascii=False)
            
            # Attendre avant de vérifier à nouveau
            time.sleep(10)
    
    def _execute_study(self, study_id: str, study_data: Dict):
        """Exécute une étude spécifique"""
        study_key = study_data["study_key"]
        script_info = self.study_scripts[study_key]
        
        # Chemin du script
        script_path = self.scripts_path / script_info["script"]
        
        if not script_path.exists():
            self._log_error(study_id, f"Script non trouvé: {script_path}")
            return
        
        try:
            # Mettre à jour le statut
            self._update_status(study_id, "running", "Exécution du script en cours...")
            
            # Exécuter le script
            start_time = datetime.now()
            result = subprocess.run(
                ["python", str(script_path)],
                cwd=str(self.base_path),
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes max
            )
            end_time = datetime.now()
            
            # Analyser les résultats
            if result.returncode == 0:
                # Succès - chercher les fichiers générés
                output_files = self._find_output_files(script_info["output_patterns"])
                
                # Copier les fichiers vers le site web
                web_files = self._copy_to_website(output_files)
                
                # Enregistrer le résultat
                self._save_result(study_id, {
                    "status": "completed",
                    "execution_time": (end_time - start_time).total_seconds(),
                    "output_files": output_files,
                    "web_files": web_files,
                    "stdout": result.stdout,
                    "timestamp": end_time.isoformat()
                })
                
                self._update_status(study_id, "completed", f"Étude terminée avec succès - {len(output_files)} fichiers générés")
                print(f"✅ Étude {study_id} terminée avec succès")
                
            else:
                # Erreur
                self._log_error(study_id, f"Erreur script: {result.stderr}")
                print(f"❌ Erreur étude {study_id}: {result.stderr}")
        
        except subprocess.TimeoutExpired:
            self._log_error(study_id, "Timeout - étude interrompue après 10 minutes")
        except Exception as e:
            self._log_error(study_id, f"Erreur inattendue: {str(e)}")
    
    def _find_output_files(self, patterns: List[str]) -> List[Dict]:
        """Trouve les fichiers de sortie générés"""
        output_files = []
        
        for pattern in patterns:
            files = list(self.base_path.glob(pattern))
            # Prendre les plus récents (dernière heure)
            recent_files = [
                f for f in files 
                if (datetime.now().timestamp() - f.stat().st_mtime) < 3600
            ]
            
            for file in recent_files:
                output_files.append({
                    "name": file.name,
                    "path": str(file.relative_to(self.base_path)),
                    "size": file.stat().st_size,
                    "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                })
        
        return output_files
    
    def _copy_to_website(self, output_files: List[Dict]) -> List[Dict]:
        """Copie les fichiers vers le site web"""
        web_files = []
        
        for file_info in output_files:
            source_path = self.base_path / file_info["path"]
            
            # Déterminer le dossier destination
            if file_info["name"].startswith("evaluation_"):
                dest_dir = self.docs_path / "etudes-terrain" / "data"
            elif file_info["name"].startswith("analyse_"):
                dest_dir = self.docs_path / "analyses" / "data" 
            elif file_info["name"].startswith("debate_"):
                dest_dir = self.docs_path / "debats" / "data"
            else:
                dest_dir = self.docs_path / "generated"
            
            # Créer le dossier si nécessaire
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # Copier le fichier
            dest_path = dest_dir / file_info["name"]
            
            try:
                import shutil
                shutil.copy2(source_path, dest_path)
                
                web_files.append({
                    "name": file_info["name"],
                    "web_path": str(dest_path.relative_to(self.docs_path)),
                    "size": file_info["size"],
                    "download_url": f"/docs/{dest_path.relative_to(self.docs_path)}"
                })
            except Exception as e:
                print(f"⚠️ Erreur copie {file_info['name']}: {e}")
        
        return web_files
    
    def _update_status(self, study_id: str, status: str, message: str):
        """Met à jour le statut d'une étude"""
        # Charger les statuts
        with open(self.status_file, 'r', encoding='utf-8') as f:
            statuses = json.load(f)
        
        # Mettre à jour
        statuses[study_id] = {
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        # Sauvegarder
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(statuses, f, indent=2, ensure_ascii=False)
    
    def _save_result(self, study_id: str, result_data: Dict):
        """Sauvegarde le résultat d'une étude"""
        # Charger les résultats
        with open(self.results_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        # Ajouter le nouveau résultat
        results[study_id] = result_data
        
        # Garder seulement les 50 plus récents
        if len(results) > 50:
            sorted_results = dict(sorted(results.items(), 
                                       key=lambda x: x[1].get('timestamp', ''), 
                                       reverse=True)[:50])
            results = sorted_results
        
        # Sauvegarder
        with open(self.results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    def _log_error(self, study_id: str, error_message: str):
        """Enregistre une erreur"""
        self._update_status(study_id, "error", error_message)
        self._save_result(study_id, {
            "status": "error",
            "error": error_message,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_queue_status(self) -> Dict:
        """Récupère le statut de la queue"""
        with open(self.queue_file, 'r', encoding='utf-8') as f:
            queue = json.load(f)
        
        with open(self.status_file, 'r', encoding='utf-8') as f:
            statuses = json.load(f)
        
        return {
            "queue_size": len([s for s in queue.values() if s.get("status") == "queued"]),
            "running": len([s for s in statuses.values() if s.get("status") == "running"]),
            "recent_studies": list(queue.keys())[-10:]  # 10 plus récents
        }
    
    def get_results(self) -> List[Dict]:
        """Récupère les résultats récents"""
        with open(self.results_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        # Convertir en liste triée par timestamp
        results_list = []
        for study_id, data in results.items():
            data["study_id"] = study_id
            results_list.append(data)
        
        # Trier par timestamp décroissant
        results_list.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return results_list[:20]  # 20 plus récents

def main():
    """Point d'entrée principal"""
    print("🤖 AUTO STUDY LAUNCHER - Projet 44Ha")
    print("=" * 50)
    
    launcher = AutoStudyLauncher()
    
    print(f"📁 Base path: {launcher.base_path}")
    print(f"📊 Scripts disponibles: {len(launcher.study_scripts)}")
    
    # Démarrer le processeur de queue en arrière-plan
    processor_thread = threading.Thread(target=launcher.process_queue, daemon=True)
    processor_thread.start()
    
    print("🚀 Processeur de queue démarré")
    print("📝 Ajoutez des études via l'interface web ou directement")
    
    # Exemple d'ajout d'étude
    if len(os.sys.argv) > 1:
        study_key = os.sys.argv[1]
        result = launcher.add_study_to_queue(study_key)
        print(f"📊 Résultat: {result}")
    
    # Garder le script actif
    try:
        while True:
            status = launcher.get_queue_status()
            print(f"⏳ Queue: {status['queue_size']} en attente, {status['running']} en cours")
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du launcher")

if __name__ == "__main__":
    main()
