
// Gestionnaire principal pour le site multi-projets
document.addEventListener('DOMContentLoaded', function() {
    
    // Animation des cartes de projets
    const projectCards = document.querySelectorAll('.project-card');
    
    // Observer pour les animations au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observer les cartes
    projectCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });
    
    // Effet parallax léger sur le header
    window.addEventListener('scroll', function() {
        const header = document.querySelector('.main-header');
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.3;
        
        if (header) {
            header.style.transform = `translateY(${rate}px)`;
        }
    });
    
    // Recherche de projets (si implémentée)
    const searchInput = document.getElementById('project-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            projectCards.forEach(card => {
                const title = card.querySelector('.project-title').textContent.toLowerCase();
                const description = card.querySelector('.project-description').textContent.toLowerCase();
                const location = card.querySelector('.project-location')?.textContent.toLowerCase() || '';
                
                if (title.includes(searchTerm) || 
                    description.includes(searchTerm) || 
                    location.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Statistiques animées
    function animateStats() {
        const stats = document.querySelectorAll('.stat-number');
        
        stats.forEach(stat => {
            const finalValue = parseInt(stat.textContent);
            let currentValue = 0;
            const increment = finalValue / 50;
            
            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= finalValue) {
                    currentValue = finalValue;
                    clearInterval(timer);
                }
                stat.textContent = Math.round(currentValue);
            }, 30);
        });
    }
    
    // Observer pour les stats
    const statsSection = document.querySelector('.stats-section');
    if (statsSection) {
        const statsObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateStats();
                    statsObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        statsObserver.observe(statsSection);
    }
});

// Fonction pour générer des projets d'exemple
function generateExampleProjects() {
    return [
        {
            id: 'provence-lavande',
            nom: 'Domaine de Lavande - Provence',
            description: 'Reconversion de 30 hectares de lavande en agritourisme premium',
            localisation: 'Valensole, Alpes-de-Haute-Provence (04)',
            surface: '30 hectares',
            particularites: ['Champs de lavande', 'Vue panoramique', 'Mas provençal'],
            activites: ['Agritourisme', 'Cosmétiques bio', 'Gastronomie'],
            statut: 'En développement',
            emoji: '💜',
            couleur: '#8B4CB8'
        },
        {
            id: 'normandie-pommiers',
            nom: 'Vergers de Normandie',
            description: 'Transformation de vergers de pommiers en éco-domaine touristique',
            localisation: 'Pays d\'Auge, Calvados (14)',
            surface: '25 hectares',
            particularites: ['Vergers centenaires', 'Cidrerie', 'Architecture normande'],
            activites: ['Cidre artisanal', 'Chambres d\'hôtes', 'Cours de cuisine'],
            statut: 'Étude de faisabilité',
            emoji: '🍎',
            couleur: '#DC143C'
        }
    ];
}
