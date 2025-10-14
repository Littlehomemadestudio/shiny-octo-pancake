"""
Military System for World War Telegram Bot
"""
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import DatabaseManager, Player, PlayerUnit, Battle, Province
from military_assets import MilitaryAssetsDatabase, MilitaryAsset

class MilitaryManager:
    def __init__(self, config: Dict):
        self.config = config
        self.unit_types = config["unit_types"]
        self.battle_cooldown = config["battle_cooldown"]
        self.db = None  # Will be set by bot
        self.assets_db = MilitaryAssetsDatabase()
    
    def get_unit_stats(self, unit_name: str) -> Optional[MilitaryAsset]:
        """Get unit statistics from assets database"""
        return self.assets_db.get_asset(unit_name)
    
    def get_legacy_unit_stats(self, unit_type: str) -> Dict:
        """Get legacy unit statistics for backward compatibility"""
        return self.unit_types.get(unit_type, {})
    
    def calculate_unit_cost(self, unit_name: str, quantity: int) -> float:
        """Calculate cost to build units"""
        asset = self.get_unit_stats(unit_name)
        if asset:
            return asset.cost * quantity
        # Fallback to legacy system
        stats = self.get_legacy_unit_stats(unit_name)
        return stats.get("cost", 0) * quantity
    
    def calculate_upkeep_cost(self, unit_name: str, quantity: int) -> float:
        """Calculate daily upkeep cost for units"""
        asset = self.get_unit_stats(unit_name)
        if asset:
            return asset.upkeep * quantity
        # Fallback to legacy system
        stats = self.get_legacy_unit_stats(unit_name)
        return stats.get("upkeep", 0) * quantity
    
    def can_afford_units(self, player: Player, unit_type: str, quantity: int) -> bool:
        """Check if player can afford to build units"""
        cost = self.calculate_unit_cost(unit_type, quantity)
        return player.gold >= cost
    
    def build_units(self, player_id: int, unit_name: str, quantity: int, 
                   province_id: Optional[int] = None) -> bool:
        """Build units for a player"""
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(id=player_id).first()
            if not player:
                return False
            
            if not self.can_afford_units(player, unit_name, quantity):
                return False
            
            cost = self.calculate_unit_cost(unit_name, quantity)
            player.gold -= cost
            
            # Get asset information
            asset = self.get_unit_stats(unit_name)
            if not asset:
                return False
            
            # Find existing unit or create new one
            existing_unit = session.query(PlayerUnit).filter_by(
                player_id=player_id,
                unit_name=unit_name,
                province_id=province_id
            ).first()
            
            if existing_unit:
                existing_unit.quantity += quantity
            else:
                new_unit = PlayerUnit(
                    player_id=player_id,
                    unit_name=unit_name,
                    unit_type=asset.category,
                    subcategory=asset.subcategory,
                    tier=asset.tier,
                    quantity=quantity,
                    province_id=province_id
                )
                session.add(new_unit)
            
            session.commit()
            return True
    
    def get_player_units(self, player_id: int) -> List[PlayerUnit]:
        """Get all units for a player"""
        with self.db.get_session() as session:
            return session.query(PlayerUnit).filter_by(player_id=player_id).all()
    
    def get_total_units(self, player_id: int) -> Dict[str, int]:
        """Get total unit counts for a player"""
        units = self.get_player_units(player_id)
        total_units = {}
        
        for unit in units:
            if unit.unit_name in total_units:
                total_units[unit.unit_name] += unit.quantity
            else:
                total_units[unit.unit_name] = unit.quantity
        
        return total_units
    
    def get_units_by_category(self, player_id: int, category: str) -> Dict[str, int]:
        """Get units by category for a player"""
        units = self.get_player_units(player_id)
        category_units = {}
        
        for unit in units:
            if unit.unit_type == category:
                if unit.unit_name in category_units:
                    category_units[unit.unit_name] += unit.quantity
                else:
                    category_units[unit.unit_name] = unit.quantity
        
        return category_units
    
    def calculate_combat_power(self, units: Dict[str, int], morale: float = 100.0) -> float:
        """Calculate total combat power of units"""
        total_power = 0.0
        
        for unit_name, quantity in units.items():
            asset = self.get_unit_stats(unit_name)
            if asset:
                # Use asset stats
                attack = asset.attack
                defense = asset.defense
            else:
                # Fallback to legacy system
                stats = self.get_legacy_unit_stats(unit_name)
                attack = stats.get("attack", 0)
                defense = stats.get("defense", 0)
            
            # Average of attack and defense
            unit_power = (attack + defense) / 2
            
            # Apply morale modifier
            morale_factor = morale / 100.0
            unit_power *= morale_factor
            
            total_power += unit_power * quantity
        
        return total_power
    
    def calculate_combat_odds(self, attacker_units: Dict[str, int], defender_units: Dict[str, int],
                             attacker_morale: float = 100.0, defender_morale: float = 100.0,
                             terrain_modifier: float = 1.0, weather_modifier: float = 1.0) -> float:
        """Calculate combat odds (0.0 to 1.0, where 0.5 is even)"""
        attacker_power = self.calculate_combat_power(attacker_units, attacker_morale)
        defender_power = self.calculate_combat_power(defender_units, defender_morale)
        
        # Apply terrain and weather modifiers
        attacker_power *= terrain_modifier * weather_modifier
        
        # Calculate odds
        total_power = attacker_power + defender_power
        if total_power == 0:
            return 0.5
        
        odds = attacker_power / total_power
        return max(0.0, min(1.0, odds))
    
    def simulate_battle(self, attacker_id: int, defender_id: int, province_id: int,
                       attacker_units: Dict[str, int], defender_units: Dict[str, int],
                       battle_type: str = "attack") -> Battle:
        """Simulate a battle between two players"""
        with self.db.get_session() as session:
            attacker = session.query(Player).filter_by(id=attacker_id).first()
            defender = session.query(Player).filter_by(id=defender_id).first()
            province = session.query(Province).filter_by(id=province_id).first()
            
            if not all([attacker, defender, province]):
                return None
            
            # Get terrain and weather modifiers
            terrain_modifier = self._get_terrain_modifier(province)
            weather_modifier = self._get_weather_modifier(province)
            
            # Calculate combat odds
            odds = self.calculate_combat_odds(
                attacker_units, defender_units,
                attacker.morale, defender.morale,
                terrain_modifier, weather_modifier
            )
            
            # Determine winner
            winner_id = attacker_id if random.random() < odds else defender_id
            
            # Calculate casualties
            casualties = self._calculate_casualties(
                attacker_units, defender_units, odds, winner_id == attacker_id
            )
            
            # Create battle record
            battle = Battle(
                attacker_id=attacker_id,
                defender_id=defender_id,
                province_id=province_id,
                battle_type=battle_type,
                status="completed",
                attacker_units=attacker_units,
                defender_units=defender_units,
                winner_id=winner_id,
                casualties=casualties,
                ended_at=datetime.utcnow()
            )
            
            session.add(battle)
            session.commit()
            
            # Apply casualties to units
            self._apply_casualties(session, attacker_id, defender_id, casualties)
            
            # Update morale
            self._update_morale_after_battle(session, attacker, defender, winner_id == attacker_id)
            
            session.commit()
            return battle
    
    def _get_terrain_modifier(self, province: Province) -> float:
        """Get terrain combat modifier"""
        # Simple terrain modifiers based on province characteristics
        if province.infrastructure > 0.8:
            return 1.1  # Urban areas favor defenders
        elif province.infrastructure < 0.3:
            return 0.9  # Rural areas favor attackers
        else:
            return 1.0  # Neutral terrain
    
    def _get_weather_modifier(self, province: Province) -> float:
        """Get weather combat modifier"""
        weather = province.weather.lower()
        
        if weather == "clear":
            return 1.0
        elif weather == "rain":
            return 0.9  # Slightly favors defenders
        elif weather == "storm":
            return 0.8  # Favors defenders
        elif weather == "fog":
            return 0.85  # Slightly favors defenders
        else:
            return 1.0
    
    def _calculate_casualties(self, attacker_units: Dict[str, int], defender_units: Dict[str, int],
                             odds: float, attacker_wins: bool) -> Dict:
        """Calculate casualties for both sides"""
        casualties = {"attacker": {}, "defender": {}}
        
        # Base casualty rate
        base_casualty_rate = 0.1  # 10% base casualties
        
        if attacker_wins:
            # Winner takes fewer casualties
            attacker_casualty_rate = base_casualty_rate * 0.5
            defender_casualty_rate = base_casualty_rate * 1.5
        else:
            # Loser takes more casualties
            attacker_casualty_rate = base_casualty_rate * 1.5
            defender_casualty_rate = base_casualty_rate * 0.5
        
        # Calculate casualties for each unit type
        for unit_type, quantity in attacker_units.items():
            casualties["attacker"][unit_type] = max(0, int(quantity * attacker_casualty_rate))
        
        for unit_type, quantity in defender_units.items():
            casualties["defender"][unit_type] = max(0, int(quantity * defender_casualty_rate))
        
        return casualties
    
    def _apply_casualties(self, session, attacker_id: int, defender_id: int, casualties: Dict):
        """Apply casualties to player units"""
        # Apply attacker casualties
        for unit_type, casualty_count in casualties["attacker"].items():
            if casualty_count > 0:
                unit = session.query(PlayerUnit).filter_by(
                    player_id=attacker_id,
                    unit_type=unit_type
                ).first()
                
                if unit:
                    unit.quantity = max(0, unit.quantity - casualty_count)
        
        # Apply defender casualties
        for unit_type, casualty_count in casualties["defender"].items():
            if casualty_count > 0:
                unit = session.query(PlayerUnit).filter_by(
                    player_id=defender_id,
                    unit_type=unit_type
                ).first()
                
                if unit:
                    unit.quantity = max(0, unit.quantity - casualty_count)
    
    def _update_morale_after_battle(self, session, attacker: Player, defender: Player, attacker_wins: bool):
        """Update player morale after battle"""
        if attacker_wins:
            attacker.morale = min(100, attacker.morale + 5)
            defender.morale = max(0, defender.morale - 10)
        else:
            attacker.morale = max(0, attacker.morale - 10)
            defender.morale = min(100, defender.morale + 5)
    
    def get_battle_history(self, player_id: int, limit: int = 10) -> List[Battle]:
        """Get battle history for a player"""
        with self.db.get_session() as session:
            return session.query(Battle).filter(
                (Battle.attacker_id == player_id) | (Battle.defender_id == player_id)
            ).order_by(Battle.started_at.desc()).limit(limit).all()
    
    def can_attack(self, attacker_id: int, target_id: int) -> Tuple[bool, str]:
        """Check if player can attack target"""
        with self.db.get_session() as session:
            attacker = session.query(Player).filter_by(id=attacker_id).first()
            target = session.query(Player).filter_by(id=target_id).first()
            
            if not attacker or not target:
                return False, "Player not found"
            
            if attacker.id == target.id:
                return False, "Cannot attack yourself"
            
            if attacker.morale < 20:
                return False, "Morale too low to attack"
            
            # Check if target has any units
            target_units = self.get_total_units(target_id)
            if sum(target_units.values()) == 0:
                return False, "Target has no units to attack"
            
            # Check cooldown (simplified)
            recent_battles = session.query(Battle).filter(
                Battle.attacker_id == attacker_id,
                Battle.started_at > datetime.utcnow() - timedelta(seconds=self.battle_cooldown)
            ).count()
            
            if recent_battles > 0:
                return False, "Attack cooldown active"
            
            return True, "Attack allowed"
    
    def get_available_targets(self, attacker_id: int) -> List[Player]:
        """Get list of available attack targets"""
        with self.db.get_session() as session:
            # Get all players except the attacker
            targets = session.query(Player).filter(
                Player.id != attacker_id,
                Player.is_banned == False
            ).all()
            
            # Filter out players with no units
            available_targets = []
            for target in targets:
                target_units = self.get_total_units(target.id)
                if sum(target_units.values()) > 0:
                    available_targets.append(target)
            
            return available_targets

class UnitUpkeepManager:
    def __init__(self, db_manager: DatabaseManager, config: Dict):
        self.db = db_manager
        self.config = config
        self.morale_decay = config["morale_decay"]
    
    def process_daily_upkeep(self):
        """Process daily upkeep for all units"""
        with self.db.get_session() as session:
            players = session.query(Player).filter(Player.is_banned == False).all()
            
            for player in players:
                # Calculate total upkeep cost
                total_upkeep = 0
                units = session.query(PlayerUnit).filter_by(player_id=player.id).all()
                
                for unit in units:
                    stats = self.get_unit_stats(unit.unit_type)
                    upkeep_per_unit = stats.get("upkeep", 0)
                    total_upkeep += upkeep_per_unit * unit.quantity
                
                # Deduct upkeep from player gold
                if player.gold >= total_upkeep:
                    player.gold -= total_upkeep
                else:
                    # If can't afford upkeep, reduce morale
                    player.morale = max(0, player.morale - 10)
                
                # Apply morale decay
                player.morale = max(0, player.morale - self.morale_decay)
            
            session.commit()
    
    def get_unit_stats(self, unit_type: str) -> Dict:
        """Get unit statistics (placeholder)"""
        # This should use the same unit stats as MilitaryManager
        unit_types = {
            "infantry": {"cost": 100, "upkeep": 10, "attack": 5, "defense": 3, "speed": 1},
            "tank": {"cost": 500, "upkeep": 50, "attack": 15, "defense": 10, "speed": 2},
            "artillery": {"cost": 300, "upkeep": 30, "attack": 20, "defense": 2, "speed": 1},
            "aircraft": {"cost": 800, "upkeep": 80, "attack": 25, "defense": 5, "speed": 5},
            "ship": {"cost": 1000, "upkeep": 100, "attack": 30, "defense": 15, "speed": 3}
        }
        return unit_types.get(unit_type, {})