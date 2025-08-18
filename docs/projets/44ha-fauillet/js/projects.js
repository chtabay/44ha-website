
// Gestionnaire de projets
class ProjectManager {
    constructor() {
        this.projects = [];
        this.init();
    }
    
    async init() {
        await this.loadProjects();
        this.renderProjects();
        this.setupEventListeners();
    }
    
    async loadProjects() {
        try {
            const response = await fetch('config/projects.json');
            const data = await response.json();
            this.projects = data.projects || [];
        } catch (error) {
            console.log('Fichier de configuration non trouvé, utilisation des projets par défaut');
            this.projects = this.getDefaultProjects();
        }
    }
    
    getDefaultProjects() {
        return [
            {
                id: 'projet-44ha',
                title: 'Projet 44 Hectares',
                location: 'Fauillet/Gontaud-de-Nogaret (47)',
                description: 'Valorisation durable d\'une exploitation agricole familiale : agritourisme, énergies renouvelables et transmission générationnelle.',
                icon: '🌾',
                surface: '44 ha',
                planEau: '150m',
                status: 'progress',
                url: 'projets/44ha/index.html',
                type: 'agritourisme'
            }
        ];
    }
    
    renderProjects() {
        const container = document.getElementById('projects-container');
        if (!container) return;
        
        container.innerHTML = '';
        
        this.projects.forEach(project => {
            const projectCard = this.createProjectCard(project);
            container.appendChild(projectCard);
        });
        
        // Met à jour le compteur
        const counter = document.getElementById('projects-count');
        if (counter) {
            counter.textContent = this.projects.length;
        }
    }
    
    createProjectCard(project) {
        const card = document.createElement('div');
        card.className = 'project-card';
        card.innerHTML = `
            <div class="project-header">
                <span class="project-icon">${project.icon}</span>
                <div>
                    <h3 class="project-title">${project.title}</h3>
                    <p class="project-location">📍 ${project.location}</p>
                </div>
            </div>
            
            <div class="status-badge status-${project.status}">
                ${this.getStatusText(project.status)}
            </div>
            
            <p class="project-description">${project.description}</p>
            
            <div class="project-stats">
                <div class="stat-item">
                    <span class="stat-number">${project.surface}</span>
                    <span class="stat-label">Surface</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">${project.planEau || 'N/A'}</span>
                    <span class="stat-label">Plan d'eau</span>
                </div>
            </div>
            
            <div class="project-actions">
                <a href="${project.url}" class="btn btn-primary">
                    📖 Voir le projet
                </a>
                <button class="btn btn-outline" onclick="projectManager.showProjectDetails('${project.id}')">
                    ℹ️ Détails
                </button>
            </div>
        `;
        
        return card;
    }
    
    getStatusText(status) {
        const statusMap = {
            'planning': 'En planification',
            'progress': 'En cours',
            'completed': 'Terminé'
        };
        return statusMap[status] || status;
    }
    
    showProjectDetails(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (!project) return;
        
        alert(`Détails du projet ${project.title}\n\nLocalisation: ${project.location}\nStatut: ${this.getStatusText(project.status)}\n\n${project.description}`);
    }
    
    setupEventListeners() {
        // Bouton d'ajout de projet
        const addBtn = document.getElementById('add-project-btn');
        if (addBtn) {
            addBtn.addEventListener('click', () => {
                this.showAddProjectModal();
            });
        }
        
        // Filtres par type
        const filterBtns = document.querySelectorAll('.filter-btn');
        filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const type = e.target.dataset.type;
                this.filterProjects(type);
            });
        });
    }
    
    filterProjects(type) {
        const cards = document.querySelectorAll('.project-card');
        cards.forEach(card => {
            if (type === 'all') {
                card.style.display = 'block';
            } else {
                // Logique de filtrage à implémenter selon les besoins
                card.style.display = 'block';
            }
        });
    }
    
    showAddProjectModal() {
        const instructions = `
Pour ajouter un nouveau projet :

1. Créez un dossier dans /docs/projets/nom-du-projet/
2. Utilisez le template dans /docs/projets/templates/
3. Modifiez le fichier /docs/config/projects.json pour ajouter :

{
    "id": "nouveau-projet",
    "title": "Nom du Projet",
    "location": "Ville, Département",
    "description": "Description du projet...",
    "icon": "🏡",
    "surface": "XX ha",
    "planEau": "XXm",
    "status": "planning",
    "url": "projets/nouveau-projet/index.html",
    "type": "agritourisme"
}

4. Rechargez la page
        `;
        
        alert(instructions);
    }
}

// Initialisation
let projectManager;
document.addEventListener('DOMContentLoaded', () => {
    projectManager = new ProjectManager();
});

// Fonction utilitaire pour copier le template
function copyTemplate() {
    const instructions = `
Commandes pour créer un nouveau projet :

1. Copiez le template :
   cp -r docs/projets/templates/ docs/projets/nouveau-projet/

2. Modifiez les fichiers dans docs/projets/nouveau-projet/

3. Ajoutez le projet dans docs/config/projects.json

4. Actualisez la page
    `;
    
    navigator.clipboard.writeText(instructions).then(() => {
        alert('Instructions copiées dans le presse-papiers !');
    });
}
