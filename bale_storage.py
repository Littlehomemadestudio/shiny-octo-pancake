"""
Storage system for Bale bot with global purchase sync
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class BaleStorage:
    """File-based storage system for Bale bot with global sync"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_player(self, player_data: Dict[str, Any]) -> bool:
        """Save player data to file"""
        try:
            player_id = player_data.get('bale_id')
            if not player_id:
                return False
            
            file_path = os.path.join(self.data_dir, f"player_{player_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(player_data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            print(f"Error saving player data: {e}")
            return False
    
    def load_player(self, bale_id: int) -> Optional[Dict[str, Any]]:
        """Load player data from file"""
        try:
            file_path = os.path.join(self.data_dir, f"player_{bale_id}.json")
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading player data: {e}")
            return None
    
    def get_all_players(self) -> List[Dict[str, Any]]:
        """Get all players"""
        players = []
        try:
            for filename in os.listdir(self.data_dir):
                if filename.startswith("player_") and filename.endswith(".json"):
                    player_id = int(filename.replace("player_", "").replace(".json", ""))
                    player_data = self.load_player(player_id)
                    if player_data:
                        players.append(player_data)
        except Exception as e:
            print(f"Error getting all players: {e}")
        return players
    
    def save_materials(self, player_id: int, materials: Dict[str, float]) -> bool:
        """Save player materials"""
        try:
            file_path = os.path.join(self.data_dir, f"materials_{player_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(materials, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving materials: {e}")
            return False
    
    def load_materials(self, player_id: int) -> Dict[str, float]:
        """Load player materials"""
        try:
            file_path = os.path.join(self.data_dir, f"materials_{player_id}.json")
            if not os.path.exists(file_path):
                return {}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading materials: {e}")
            return {}
    
    def save_units(self, player_id: int, units: Dict[str, int]) -> bool:
        """Save player units"""
        try:
            file_path = os.path.join(self.data_dir, f"units_{player_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(units, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving units: {e}")
            return False
    
    def load_units(self, player_id: int) -> Dict[str, int]:
        """Load player units"""
        try:
            file_path = os.path.join(self.data_dir, f"units_{player_id}.json")
            if not os.path.exists(file_path):
                return {}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading units: {e}")
            return {}
    
    def save_quests(self, player_id: int, quests: List[Dict[str, Any]]) -> bool:
        """Save player quests"""
        try:
            file_path = os.path.join(self.data_dir, f"quests_{player_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(quests, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            print(f"Error saving quests: {e}")
            return False
    
    def load_quests(self, player_id: int) -> List[Dict[str, Any]]:
        """Load player quests"""
        try:
            file_path = os.path.join(self.data_dir, f"quests_{player_id}.json")
            if not os.path.exists(file_path):
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading quests: {e}")
            return []
    
    def save_global_purchases(self, purchases: List[Dict[str, Any]]) -> bool:
        """Save global purchase history"""
        try:
            file_path = os.path.join(self.data_dir, "global_purchases.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(purchases, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            print(f"Error saving global purchases: {e}")
            return False
    
    def load_global_purchases(self) -> List[Dict[str, Any]]:
        """Load global purchase history"""
        try:
            file_path = os.path.join(self.data_dir, "global_purchases.json")
            if not os.path.exists(file_path):
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading global purchases: {e}")
            return []
    
    def add_global_purchase(self, purchase_data: Dict[str, Any]) -> bool:
        """Add a new purchase to global history"""
        try:
            purchases = self.load_global_purchases()
            purchase_data['timestamp'] = datetime.now().isoformat()
            purchases.append(purchase_data)
            return self.save_global_purchases(purchases)
        except Exception as e:
            print(f"Error adding global purchase: {e}")
            return False
    
    def get_recent_global_purchases(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent global purchases"""
        purchases = self.load_global_purchases()
        return sorted(purchases, key=lambda x: x.get('timestamp', ''), reverse=True)[:limit]
    
    def delete_player(self, bale_id: int) -> bool:
        """Delete player data"""
        try:
            files_to_delete = [
                f"player_{bale_id}.json",
                f"materials_{bale_id}.json",
                f"units_{bale_id}.json",
                f"quests_{bale_id}.json"
            ]
            
            for filename in files_to_delete:
                file_path = os.path.join(self.data_dir, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            return True
        except Exception as e:
            print(f"Error deleting player: {e}")
            return False
