# Template de Projet

## Utilisation

1. **Copiez ce dossier** vers `projets/nom-de-votre-projet/`

2. **Modifiez index.html** en remplaçant :
   - `[TITRE_PROJET]` → Titre de votre projet
   - `[DESCRIPTION_PROJET]` → Description SEO
   - `[DESCRIPTION_COURTE]` → Sous-titre
   - `[DESCRIPTION_DETAILLEE]` → Description complète
   - `[LOCALISATION]` → Ville, Département
   - `[ICON]` → Emoji représentant le projet
   - `[SURFACE]` → Surface du terrain
   - `[PLAN_EAU]` → Taille du plan d'eau

3. **Ajoutez votre projet** dans `/config/projects.json` :

```json
{
  "id": "nom-projet",
  "title": "Titre du Projet",
  "location": "Ville, Département",
  "description": "Description...",
  "icon": "🏡",
  "surface": "XX ha",
  "planEau": "XXm",
  "status": "planning",
  "url": "projets/nom-projet/index.html",
  "type": "agritourisme"
}
```

4. **Actualisez** la page d'accueil

## Structure recommandée

- 🏠 Accueil / Présentation
- 🌾 Agriculture / Activité principale  
- 🏞️ Tourisme / Loisirs
- ⚡ Énergies / Innovations
- 💰 Économie / Financement
- 🌍 Environnement / Impact

Adaptez selon votre projet !
