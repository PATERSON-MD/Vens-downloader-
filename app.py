
import os
import threading
import time
import json
import logging

# Configuration du logging pour la production
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from yt_dlp import YoutubeDL

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app) # Activer CORS pour toutes les routes

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Fonction pour nettoyer les fichiers téléchargés après un certain temps
def cleanup_downloads():
    while True:
        now = time.time()
        for filename in os.listdir(DOWNLOAD_FOLDER):
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                # Supprimer les fichiers de plus d'une heure
                if now - os.path.getmtime(filepath) > 3600:
                    try:
                        os.remove(filepath)
                        print(f"Fichier nettoyé : {filename}")
                    except Exception as e:
                        print(f"Erreur lors du nettoyage de {filename}: {e}")
        time.sleep(600) # Vérifier toutes les 10 minutes

# Démarrer le thread de nettoyage en arrière-plan
cleanup_thread = threading.Thread(target=cleanup_downloads, daemon=True)
cleanup_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/info', methods=['POST'])
def get_video_info():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL manquante'}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'simulate': True, # Ne pas télécharger, juste obtenir les infos
        'force_generic_extractor': True, # Pour gérer les URLs génériques
        'extract_flat': 'in_playlist', # Spécifique pour TikTok pour éviter les playlists
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # Préférer mp4
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Gérer spécifiquement TikTok pour le sans filigrane
            if 'tiktok.com' in url:
                # yt-dlp gère déjà bien le sans filigrane par défaut pour TikTok
                # On peut chercher des formats spécifiques si nécessaire, mais 'best' devrait suffire
                pass

            formats = []
            if 'formats' in info:
                for f in info['formats']:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none': # S'assurer que c'est une vidéo avec audio
                        formats.append({
                            'format_id': f['format_id'],
                            'ext': f.get('ext'),
                            'resolution': f.get('resolution'),
                            'note': f.get('format_note'),
                            'filesize': f.get('filesize'),
                            'quality': f.get('height') # Utiliser la hauteur comme indicateur de qualité
                        })
                # Trier par qualité décroissante
                formats = sorted(formats, key=lambda x: x.get('quality') or 0, reverse=True)
            
            # Informations de base
            video_info = {
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration'),
                'platform': info.get('extractor_key'),
                'formats': formats
            }
            return jsonify(video_info)

    except Exception as e:
        app.logger.error(f"Erreur lors de l'analyse de l'URL {url}: {e}")
        return jsonify({'error': f'Impossible d\'analyser l\'URL ou plateforme non supportée: {e}'}), 500

@app.route('/api/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    format_id = request.json.get('format_id')
    if not url or not format_id:
        return jsonify({'error': 'URL ou format_id manquant'}), 400

    # Générer un nom de fichier unique et sécurisé
    filename = os.path.join(DOWNLOAD_FOLDER, f"{os.urandom(16).hex()}.mp4")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': format_id, # Utiliser le format_id choisi
        'outtmpl': filename, # Chemin de sortie
        'extract_flat': 'in_playlist', # Spécifique pour TikTok
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Retourner le fichier téléchargé
        return send_file(filename, as_attachment=True, download_name=os.path.basename(filename))

    except Exception as e:
        app.logger.error(f"Erreur lors du téléchargement de l'URL {url} avec le format {format_id}: {e}")
        return jsonify({'error': f'Impossible de télécharger la vidéo: {e}'}), 500


