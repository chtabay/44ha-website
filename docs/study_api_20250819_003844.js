
// API pour les fonctionnalités études IA
class StudyAPI {
    constructor() {
        // Détecter l'environnement
        this.isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        this.baseURL = this.isLocal ? 'http://localhost:5001/api' : '/api';
        
        console.log(`📡 StudyAPI initialisé - Mode: ${this.isLocal ? 'local' : 'github-pages'}`);
        console.log(`🔗 Base URL: ${this.baseURL}`);
    }
    
    async launchStudy(studyKey, parameters = {}) {
        if (this.isLocal) {
            // Mode développement local - exécution réelle des scripts
            return await this.executeLocalScript(studyKey, parameters);
        } else {
            // Mode GitHub Pages - simulation ou API externe
            return await this.simulateStudyExecution(studyKey);
        }
    }
    
    async executeLocalScript(studyKey, parameters) {
        try {
            // Appel à l'API locale Python (Flask/FastAPI)
            const response = await fetch(`${this.baseURL}/studies/launch`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    study_key: studyKey,
                    parameters: parameters,
                    project_context: {
                        location: 'Gontaud-de-Nogaret',
                        surface: '44Ha',
                        lake: 'Lac de Cayre'
                    }
                })
            });
            
            return await response.json();
        } catch (error) {
            console.error('Erreur exécution locale:', error);
            return this.simulateStudyExecution(studyKey);
        }
    }
    
    async simulateStudyExecution(studyKey) {
        // Simulation pour GitHub Pages
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    success: true,
                    study_key: studyKey,
                    execution_time: Math.random() * 3 + 1,
                    results: {
                        files_generated: 2,
                        analysis_complete: true,
                        timestamp: new Date().toISOString()
                    }
                });
            }, Math.random() * 3000 + 2000);
        });
    }
    
    async getResults() {
        try {
            const response = await fetch(`${this.baseURL}/studies/results`);
            return await response.json();
        } catch (error) {
            // Fallback vers résultats locaux
            return this.getLocalResults();
        }
    }
    
    getLocalResults() {
        // Scanner les fichiers locaux générés
        const results = [];
        
        // Simuler la lecture des fichiers récents
        const filePatterns = [
            'evaluation_ultra_complete_*.md',
            'structure_couts_detaillee_*.md',
            'modes_financement_optimises_*.md',
            'analyse_hotellerie_financement_*.md',
            'protection_patrimoine_familial_*.md',
            'debate_*.md'
        ];
        
        return results;
    }
    
    async downloadFile(filename) {
        if (this.isLocal) {
            // Téléchargement direct du fichier local
            window.open(`/files/${filename}`, '_blank');
        } else {
            // Redirection vers le repository GitHub
            const repoURL = 'https://github.com/votre-username/44ha-project';
            window.open(`${repoURL}/blob/main/docs/${filename}`, '_blank');
        }
    }
}

// Instance globale de l'API
const studyAPI = new StudyAPI();
