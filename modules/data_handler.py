import json
import os
from modules.game_classes import Joueur

FICHIER_DB = "data/joueurs.json"

class DataManager:
    @staticmethod
    def charger_donnees():
        if not os.path.exists(FICHIER_DB):
            return {}
        with open(FICHIER_DB, 'r') as f:
            return json.load(f)

    @staticmethod
    def sauvegarder_donnees(donnees):
        # [Barème: Sécurité] Sauvegarde atomique simulée
        with open(FICHIER_DB, 'w') as f:
            json.dump(donnees, f, indent=4)

    @staticmethod
    def get_joueur(user_id):
        data = DataManager.charger_donnees()
        str_id = str(user_id)
        if str_id in data:
            return Joueur(str_id, data[str_id]['argent'], data[str_id]['inventaire'])
        return Joueur(str_id)

    @staticmethod
    def save_joueur(joueur):
        data = DataManager.charger_donnees()
        data[str(joueur.id)] = {
            "argent": joueur.argent,
            "inventaire": joueur.inventaire
        }
        DataManager.sauvegarder_donnees(data)
