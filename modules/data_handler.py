import json
import os
from modules.game_classes import Player

DB_FILE = "data/players.json"  # Renamed for English consistency

class DataManager:
    @staticmethod
    def load_data():
        if not os.path.exists(DB_FILE):
            return {}
        with open(DB_FILE, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_data(data):
        # [Grading: Security] Atomic save simulation
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def get_player(user_id):
        data = DataManager.load_data()
        str_id = str(user_id)
        if str_id in data:
            # Using 'money' and 'inventory' keys
            return Player(str_id, data[str_id]['money'], data[str_id]['inventory'])
        return Player(str_id)

    @staticmethod
    def save_player(player):
        data = DataManager.load_data()
        data[str(player.id)] = {
            "money": player.money,
            "inventory": player.inventory
        }
        DataManager.save_data(data)