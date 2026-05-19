# Vens-Downloader

Vens-Downloader est une application web conviviale qui vous permet de télécharger des vidéos depuis diverses plateformes populaires, y compris TikTok (sans filigrane), YouTube, Instagram, Twitter/X, Facebook et Twitch.

## Fonctionnalités

-   **Téléchargement multi-plateformes** : Supporte TikTok (sans filigrane), YouTube, Instagram, Twitter/X, Facebook, Twitch.
-   **Sélection de qualité** : Choisissez parmi les formats et qualités disponibles pour chaque vidéo.
-   **Interface moderne** : Design sombre avec des éléments néon et glassmorphism pour une expérience utilisateur agréable.
-   **Nettoyage automatique** : Les fichiers téléchargés sont automatiquement supprimés après 1 heure pour économiser de l'espace.
-   **Facile à utiliser** : Collez simplement l'URL, analysez, puis téléchargez.

## Installation et Lancement (Local)

Pour installer et lancer Vens-Downloader en local, suivez ces étapes :

1.  **Cloner le dépôt (si applicable) ou télécharger les fichiers du projet.**

2.  **Naviguer vers le répertoire du projet :**
    ```bash
    cd Vens-downloader
    ```

3.  **Installer les dépendances Python :**
    ```bash
    pip install -r requirements.txt
    ```
    *Assurez-vous d'avoir Python 3 et pip installés sur votre système.*

### Lancement de l'application en local

Vous pouvez lancer l'application de deux manières :

#### Pour Windows

Double-cliquez sur `start.bat` ou exécutez-le via l'invite de commande :

```cmd
start.bat
```

#### Pour macOS/Linux

Rendez le script exécutable et lancez-le :

```bash
chmod +x start.sh
./start.sh
```

Une fois l'application lancée, ouvrez votre navigateur web et accédez à : [http://localhost:5000](http://localhost:5000)

## Déploiement en Production (Site Web Permanent)

Pour rendre Vens-Downloader accessible 24h/24 sur Internet, vous pouvez le déployer sur des plateformes cloud. Ce projet est configuré pour être facilement déployable grâce à `gunicorn` et un `Dockerfile`.

### Options de Déploiement Recommandées

#### 1. Déploiement sur Render.com

Render est une plateforme cloud moderne qui simplifie le déploiement d'applications web. Il supporte les applications Python/Flask avec Gunicorn et les Dockerfiles.

**Étapes :**

1.  **Créez un compte Render** et connectez-vous.
2.  **Connectez votre dépôt Git** (GitHub, GitLab, Bitbucket) où se trouve votre projet Vens-Downloader.
3.  **Créez un nouveau 
Web Service** :
    *   **Build Command** : `pip install -r requirements.txt`
    *   **Start Command** : `gunicorn app:app --bind 0.0.0.0:$PORT`
    *   Render détectera automatiquement le `Procfile` et le `Dockerfile` si vous les avez inclus, simplifiant la configuration.
4.  **Configurez les variables d'environnement** si nécessaire (bien que ce projet n'en ait pas de spécifiques pour le moment).
5.  **Déployez** votre service. Render gérera la construction de l'image Docker et le déploiement de votre application.

#### 2. Déploiement sur Railway.app

Railway est une autre plateforme d'hébergement moderne qui offre une expérience de déploiement fluide, notamment pour les applications Python et Docker.

**Étapes :**

1.  **Créez un compte Railway** et connectez-vous.
2.  **Connectez votre dépôt Git**.
3.  **Créez un nouveau projet** et choisissez de déployer depuis un dépôt Git.
4.  Railway détectera automatiquement votre application Python et le `Procfile`.
5.  **Configurez les variables d'environnement** si nécessaire.
6.  **Déployez** votre service. Railway construira et déploiera votre application.

#### 3. Déploiement sur un Cloud Computer Manus

Pour un contrôle total et un environnement persistant, vous pouvez déployer Vens-Downloader sur un Cloud Computer Manus.

**Étapes :**

1.  **Provisionnez un Cloud Computer Manus** (si vous n'en avez pas déjà un). Assurez-vous de choisir une taille adaptée à vos besoins.
2.  **Connectez-vous à votre Cloud Computer** via SSH ou l'interface web.
3.  **Clonez votre dépôt Git** sur le Cloud Computer :
    ```bash
    git clone <URL_DE_VOTRE_DEPOT>
    cd Vens-downloader
    ```
4.  **Installez Docker** si ce n'est pas déjà fait :
    ```bash
    sudo apt update
    sudo apt install docker.io -y
    sudo systemctl start docker
    sudo systemctl enable docker
    ```
5.  **Construisez l'image Docker** :
    ```bash
    docker build -t vens-downloader .
    ```
6.  **Lancez le conteneur Docker** :
    ```bash
    docker run -d -p 80:5000 --name vens-downloader-app vens-downloader
    ```
    *Ceci fera tourner l'application sur le port 80 de votre Cloud Computer, accessible via l'adresse IP publique de votre VM.*

7.  **Configurez un nom de domaine** (facultatif) : Si vous avez un nom de domaine, vous pouvez le pointer vers l'adresse IP de votre Cloud Computer et configurer un proxy inverse (comme Nginx) pour gérer le SSL et les requêtes.

## Structure du projet (pour le déploiement)

```
Vens-downloader/
├── app.py
├── requirements.txt
├── README.md
├── start.bat
├── start.sh
├── Procfile             # Pour Render, Railway, Heroku
├── Dockerfile           # Pour Docker, Cloud Computer
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Dépannage

-   **Problèmes de dépendances** : Assurez-vous que `requirements.txt` est à jour et que toutes les dépendances sont installées.
-   **Erreurs de déploiement** : Vérifiez les logs de votre plateforme d'hébergement pour des messages d'erreur spécifiques.
-   **Accès au site** : Assurez-vous que le port 5000 (ou 80 si vous utilisez Docker avec redirection) est bien exposé et accessible.

---

J'ai mis à jour le `README.md` avec toutes les instructions nécessaires pour le déploiement permanent. Je vais maintenant passer à la phase de livraison finale.
