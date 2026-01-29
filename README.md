# 🍎 Fruit Slicer

Un jeu de type *Fruit Ninja* codé en Python avec Pygame.  
Le joueur peut choisir entre un **mode souris** (slice avec la souris) et un **mode clavier** (une touche par type de fruit).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table des matières

- [Installation](#-installation)
- [Structure du projet](#-structure-du-projet)
- [Comment jouer](#-comment-jouer)
- [Architecture des fichiers](#-architecture-des-fichiers)
- [Fonctionnalités](#-fonctionnalités)

---

## 🚀 Installation

### Prérequis

- Python 3.8+
- pip

### Étapes

1. **Cloner le repository**
   ```bash
   git clone https://github.com/marion-ory/fruit-slicer.git
   cd fruit-slicer/fruitslicer_mayeul
   ```

2. **Installer les dépendances**
   ```bash
   pip install pygame librosa
   ```

3. **Vérifier la structure des dossiers**
   ```
   fruitslicer_mayeul/
   ├── assets/      # Images (.png, .jpg)
   ├── music/       # Musique de fond (track.mp3)
   ├── sounds/      # Effets sonores (.mp3)
   └── *.py         # Fichiers Python
   ```

4. **Lancer le jeu**
   ```bash
   python main.py
   ```

---

## 📁 Structure du projet

```
fruitslicer_mayeul/
│
├── assets/                    # Ressources graphiques
│   ├── backgroundmenu.jpg
│   ├── backgroundjeu.jpg
│   ├── logo.png
│   ├── apple.png
│   ├── banana.png
│   ├── orange.png
│   ├── goldenfruit.png
│   ├── bomb.png
│   ├── icecube.png
│   ├── combo.png
│   └── heart.png
│
├── music/                     # Musique de fond
│   └── track.mp3
│
├── sounds/                    # Effets sonores
│   ├── fruit.mp3
│   ├── goldenfruit.mp3
│   ├── bomb.mp3
│   └── combo.mp3
│
├── main.py                    # Point d'entrée du jeu
├── config.py                  # Configuration globale
├── sounds.py                  # Gestion audio
├── rendering.py               # Fonctions de rendu
├── screens.py                 # Menus et écrans
├── entities.py                # Objets du jeu
├── physics.py                 # Physique et gravité
├── spawner.py                 # Apparition des objets
├── audio_analysis.py          # Analyse BPM
├── game_mouse.py              # Mode souris
├── game_keyboard.py           # Mode clavier
│
├── scores.json                # Scores (généré automatiquement)
└── beat_cache.json            # Cache BPM (généré automatiquement)
```

---

## 🎮 Comment jouer

### Mode Souris 🖱️

- **Déplacez la souris** pour slicer les fruits
- **Évitez les bombes** 💣 (toucher = -2 vies)
- **Slicez les glaces** 🧊 pour activer le slow-motion
- **Slicez les fruits dorés** ⭐ pour gagner +5 points et +1 vie

### Mode Clavier ⌨️

| Touche | Action |
|--------|--------|
| **A** | Slice la pomme 🍎 la plus proche |
| **B** | Slice la banane 🍌 la plus proche |
| **O** | Slice l'orange 🍊 la plus proche |
| **S** | Slice le fruit doré ⭐ le plus proche |
| **I** | Slice la glace 🧊 (slow-motion) |
| **ESPACE** | Désactive la bombe 💣 la plus proche |

### Système de score

- **Fruit normal** : +1 point (x3 en combo)
- **Fruit doré** : +5 points (x3 en combo) + 1 vie
- **Combo** : Activé après 10 slices → points x3
- **Perdre une vie** : Rater un fruit OU toucher une bombe (mode souris)
- **Bombe (mode clavier)** : Doit être désactivée avant explosion

---

## 🏗️ Architecture des fichiers

### `main.py` – Point d'entrée
Lance l'écran de splash, affiche le menu principal, récupère le choix du joueur (mode + difficulté) et démarre la boucle de jeu appropriée.

### `config.py` – Configuration globale
- Dimensions logiques (800×600)
- Couleurs, polices, FPS
- Chargement de toutes les images
- Paramètres de difficulté (EASY/HARD)

### `sounds.py` – Gestion audio
- Chargement des effets sonores (fruit, bombe, combo, goldenfruit)
- Gestion de la musique de fond
- Fonctions `play_fruit_sound()`, `play_bomb_sound()`, etc.

### `rendering.py` – Fonctions de rendu
- `draw_text()` : Affiche du texte centré
- `draw_sword_trail()` : Dessine la traînée de souris
- `blit_scaled()` : Gère le redimensionnement de la fenêtre
- `logical_mouse_pos()` : Convertit les coordonnées souris

### `screens.py` – Menus et écrans
- Écran de splash (logo)
- Menu principal (Jouer, Scores, Quitter)
- Choix du mode (Souris/Clavier)
- Choix de difficulté (Easy/Hard)
- Tableau des scores
- Écran Game Over
- Gestion du fichier `scores.json`

### `entities.py` – Objets du jeu
- Définition des types de fruits (`FRUIT_TYPES`)
- Types spéciaux : `ICE_TYPE`, `BOMB_TYPE`, `GOLDENFRUIT_TYPE`
- Classe `FallingObject` (position, vitesse, dessin)
- Fonctions de spawn : `random_fruit()`, `bomb()`, `goldenfruit()`, etc.
- `make_slices_from_fruit()` : Crée les tranches après un slice

### `physics.py` – Physique et mouvement
- Constante `GRAVITY` pour la chute des objets
- `apply_gravity_and_move()` : Applique la gravité et déplace les objets
- `is_off_screen()` : Détecte si un objet est sorti de l'écran

### `spawner.py` – Apparition des objets
- Classe `BeatSpawner` qui fait apparaître les objets sur le rythme de la musique
- Gestion des probabilités (bombes, glaces, fruits dorés)
- Adaptation selon la difficulté

### `audio_analysis.py` – Analyse du rythme
- Utilise `librosa` pour détecter le BPM et les beats
- Cache les résultats dans `beat_cache.json`
- Fonction `analyze_music()` qui retourne `(tempo, beat_times_ms)`

### `game_mouse.py` – Mode souris
- Boucle de jeu principale pour le mode souris
- Détection des slices via `segment_intersects_rect()`
- Gestion du combo, slow-motion, vies
- Traînée de souris avec effet de fondu

### `game_keyboard.py` – Mode clavier
- Boucle de jeu principale pour le mode clavier
- Mapping touches → fruits (`A`=pomme, `B`=banane, etc.)
- Fonction `find_closest_fruit_by_type()` pour cibler le bon fruit
- Les bombes explosent automatiquement si non désactivées

---

## ✨ Fonctionnalités

### Système de jeu
- ✅ 2 modes de jeu (souris et clavier)
- ✅ 2 difficultés (Easy et Hard)
- ✅ Système de combo (×3 après 10 slices)
- ✅ Slow-motion activé par les glaces
- ✅ Fruits dorés donnent des vies bonus
- ✅ Synchronisation avec le rythme de la musique

### Audio
- ✅ Musique de fond
- ✅ Effets sonores distincts (fruits, bombe, combo, goldenfruit)
- ✅ Analyse BPM automatique avec cache

### Interface
- ✅ Menu principal avec choix du mode
- ✅ Tableau des scores (top 10)
- ✅ Fenêtre redimensionnable
- ✅ Effets visuels (traînée souris, clignotement bombes)

---

## 🛠️ Technologies utilisées

- **Python 3.8+**
- **Pygame** : Moteur de jeu 2D
- **Librosa** : Analyse audio et détection de BPM
- **JSON** : Sauvegarde des scores

---

## 📝 License

MIT License - Libre d'utilisation et de modification

---

## 👥 Auteurs

Développé par **Mayeul** / **Marion** / **Antuat** dans le cadre d'un projet scolaire

---

## 🐛 Problèmes connus

- Aucun pour le moment

---

## 🚀 Améliorations futures

- [ ] Ajouter d'autres fruits (pastèque, kiwi, etc.)
- [ ] Mode multijoueur local
- [ ] Power-ups supplémentaires
- [ ] Animations de particules
- [ ] Leaderboard en ligne

---

**Bon jeu ! 🍎🍌🍊**
```
