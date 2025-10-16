"""
Province Management System for World War Telegram Bot
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import DatabaseManager, Player, Province, Nation

class ProvinceManager:
    def __init__(self):
        self.building_types = {
            "factory": {"cost": 1000, "production_bonus": 0.1, "description": "Increases material production"},
            "airbase": {"cost": 2000, "military_bonus": 0.15, "description": "Improves air unit effectiveness"},
            "farm": {"cost": 500, "food_bonus": 0.2, "description": "Increases food production"},
            "refinery": {"cost": 1500, "oil_bonus": 0.25, "description": "Improves oil processing"},
            "research_center": {"cost": 3000, "research_bonus": 0.3, "description": "Boosts research speed"},
            "fortress": {"cost": 2500, "defense_bonus": 0.5, "description": "Significantly improves defense"},
            "mine": {"cost": 800, "mineral_bonus": 0.2, "description": "Increases mineral extraction"}
        }
    
    def get_province_info(self, province_id: int) -> Optional[Province]:
        """Get province information"""
        with self.db.get_session() as session:
            return session.query(Province).filter_by(id=province_id).first()
    
    def get_player_provinces(self, player_id: int) -> List[Province]:
        """Get all provinces owned by a player"""
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(id=player_id).first()
            if not player or not player.nation:
                return []
            
            return session.query(Province).filter_by(owner_id=player.nation.id).all()
    
    def can_claim_province(self, player_id: int, province_id: int) -> Tuple[bool, str]:
        """Check if player can claim a province"""
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(id=player_id).first()
            province = session.query(Province).filter_by(id=province_id).first()
            
            if not player or not province:
                return False, "Player or province not found"
            
            if not player.nation:
                return False, "You must be part of a nation to claim provinces"
            
            if province.owner_id == player.nation.id:
                return False, "Province already owned by your nation"
            
            if province.owner_id is not None:
                return False, "Province is already claimed by another nation"
            
            # Check if player has enough units nearby
            nearby_units = self._get_nearby_units(player_id, province_id)
            if sum(nearby_units.values()) < 10:  # Need at least 10 units
                return False, "Not enough units nearby to claim province"
            
            return True, "Province can be claimed"
    
    def claim_province(self, player_id: int, province_id: int) -> bool:
        """Claim a province for player's nation"""
        can_claim, reason = self.can_claim_province(player_id, province_id)
        if not can_claim:
            return False
        
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(id=player_id).first()
            province = session.query(Province).filter_by(id=province_id).first()
            
            province.owner_id = player.nation.id
            province.morale = 100.0  # Reset morale for new owner
            
            session.commit()
            return True
    
    def _get_nearby_units(self, player_id: int, province_id: int) -> Dict[str, int]:
        """Get units near a province (simplified)"""
        with self.db.get_session() as session:
            # For now, just return all player units
            # In a real implementation, this would check distance
            units = session.query(PlayerUnit).filter_by(player_id=player_id).all()
            return {unit.unit_type: unit.quantity for unit in units}
    
    def can_build(self, player_id: int, province_id: int, building_type: str) -> Tuple[bool, str]:
        """Check if player can build in province"""
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(id=player_id).first()
            province = session.query(Province).filter_by(id=province_id).first()
            
            if not player or not province:
                return False, "Player or province not found"
            
            if not player.nation or province.owner_id != player.nation.id:
                return False, "You don't own this province"
            
            if building_type not in self.building_types:
                return False, "Invalid building type"
            
            building_cost = self.building_types[building_type]["cost"]
            if player.gold < building_cost:
                return False, "Not enough gold to build"
            
            # Check if building already exists
            buildings = province.buildings or []
            if building_type in buildings:
                return False, "Building already exists in this province"
            
            return True, "Can build"
    
    def build_in_province(self, player_id: int, province_id: int, building_type: str) -> bool:
        """Build a structure in a province"""
        can_build, reason = self.can_build(player_id, province_id, building_type)
        if not can_build:
            return False
        
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(id=player_id).first()
            province = session.query(Province).filter_by(id=province_id).first()
            
            building_cost = self.building_types[building_type]["cost"]
            player.gold -= building_cost
            
            # Add building to province
            buildings = province.buildings or []
            buildings.append(building_type)
            province.buildings = buildings
            
            # Apply building effects
            self._apply_building_effects(province, building_type)
            
            session.commit()
            return True
    
    def _apply_building_effects(self, province: Province, building_type: str):
        """Apply building effects to province"""
        building = self.building_types[building_type]
        
        if "production_bonus" in building:
            province.infrastructure += building["production_bonus"]
        if "defense_bonus" in building:
            province.defense_level += 1
        if "food_bonus" in building:
            province.food_production *= (1 + building["food_bonus"])
        if "oil_bonus" in building:
            province.oil_deposits *= (1 + building["oil_bonus"])
        if "mineral_bonus" in building:
            province.iron_deposits *= (1 + building["mineral_bonus"])
    
    def get_province_production(self, province_id: int) -> Dict[str, float]:
        """Calculate province resource production"""
        with self.db.get_session() as session:
            province = session.query(Province).filter_by(id=province_id).first()
            if not province:
                return {}
            
            production = {
                "iron": province.iron_deposits * province.infrastructure * 0.01,
                "oil": province.oil_deposits * province.infrastructure * 0.01,
                "food": province.food_production * province.infrastructure * 0.01,
                "gold": province.gold_mines * province.infrastructure * 0.01,
                "uranium": province.uranium_deposits * province.infrastructure * 0.01
            }
            
            # Apply building bonuses
            buildings = province.buildings or []
            for building_type in buildings:
                building = self.building_types.get(building_type, {})
                if "food_bonus" in building:
                    production["food"] *= (1 + building["food_bonus"])
                if "oil_bonus" in building:
                    production["oil"] *= (1 + building["oil_bonus"])
                if "mineral_bonus" in building:
                    production["iron"] *= (1 + building["mineral_bonus"])
            
            return production
    
    def process_daily_production(self):
        """Process daily resource production for all provinces"""
        with self.db.get_session() as session:
            provinces = session.query(Province).filter(Province.owner_id.isnot(None)).all()
            
            for province in provinces:
                production = self.get_province_production(province.id)
                
                # Add resources to nation
                if province.owner:
                    # This would need to be implemented to add resources to nation/player
                    pass
    
    def get_province_defense_strength(self, province_id: int) -> float:
        """Calculate province defense strength"""
        with self.db.get_session() as session:
            province = session.query(Province).filter_by(id=province_id).first()
            if not province:
                return 0.0
            
            base_defense = province.defense_level * 10
            morale_bonus = province.morale * 0.1
            infrastructure_bonus = province.infrastructure * 5
            
            # Building bonuses
            building_bonus = 0
            buildings = province.buildings or []
            for building_type in buildings:
                building = self.building_types.get(building_type, {})
                if "defense_bonus" in building:
                    building_bonus += building["defense_bonus"] * 10
            
            total_defense = base_defense + morale_bonus + infrastructure_bonus + building_bonus
            return max(0, total_defense)
    
    def update_province_weather(self):
        """Update weather for all provinces"""
        weather_types = ["clear", "rain", "storm", "fog", "snow"]
        weather_weights = [0.5, 0.2, 0.1, 0.15, 0.05]  # Clear is most common
        
        with self.db.get_session() as session:
            provinces = session.query(Province).all()
            
            for province in provinces:
                # Random weather change
                if random.random() < 0.1:  # 10% chance to change weather
                    province.weather = random.choices(weather_types, weights=weather_weights)[0]
                    
                    # Update temperature based on weather
                    if province.weather == "snow":
                        province.temperature = random.uniform(-10, 5)
                    elif province.weather == "storm":
                        province.temperature = random.uniform(5, 15)
                    elif province.weather == "rain":
                        province.temperature = random.uniform(10, 20)
                    else:
                        province.temperature = random.uniform(15, 30)
            
            session.commit()
    
    def get_world_map_data(self) -> List[Dict]:
        """Get world map data for display"""
        with self.db.get_session() as session:
            provinces = session.query(Province).all()
            
            map_data = []
            for province in provinces:
                map_data.append({
                    "id": province.id,
                    "name": province.name,
                    "x": province.x,
                    "y": province.y,
                    "owner_id": province.owner_id,
                    "owner_name": province.owner.name if province.owner else None,
                    "weather": province.weather,
                    "temperature": province.temperature,
                    "defense_level": province.defense_level,
                    "infrastructure": province.infrastructure,
                    "morale": province.morale
                })
            
            return map_data