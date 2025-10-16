"""
Admin System for World War Telegram Bot
"""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import DatabaseManager, Player, Nation, Province, WorldEvent

class AdminManager:
    def __init__(self, admin_ids: List[int]):
        self.admin_ids = admin_ids
        self.db = None  # Will be set by bot
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        return user_id in self.admin_ids
    
    def get_game_statistics(self) -> Dict:
        """Get comprehensive game statistics"""
        with self.db.get_session() as session:
            stats = {}
            
            # Player statistics
            stats["players"] = {
                "total": session.query(Player).count(),
                "active_24h": session.query(Player).filter(
                    Player.last_active > datetime.utcnow() - timedelta(days=1)
                ).count(),
                "active_7d": session.query(Player).filter(
                    Player.last_active > datetime.utcnow() - timedelta(days=7)
                ).count(),
                "banned": session.query(Player).filter(Player.is_banned == True).count()
            }
            
            # Nation statistics
            stats["nations"] = {
                "total": session.query(Nation).count(),
                "ai": session.query(Nation).filter(Nation.is_ai == True).count(),
                "player": session.query(Nation).filter(Nation.is_ai == False).count()
            }
            
            # Province statistics
            stats["provinces"] = {
                "total": session.query(Province).count(),
                "claimed": session.query(Province).filter(
                    Province.owner_id.isnot(None)
                ).count(),
                "unclaimed": session.query(Province).filter(
                    Province.owner_id.is_(None)
                ).count()
            }
            
            # Economy statistics
            total_gold = session.query(Player).with_entities(
                session.func.sum(Player.gold)
            ).scalar() or 0
            
            stats["economy"] = {
                "total_gold": total_gold,
                "average_gold": total_gold / max(1, stats["players"]["total"]),
                "richest_player": self._get_richest_player()
            }
            
            # Military statistics
            stats["military"] = self._get_military_stats()
            
            # World events
            stats["events"] = {
                "active": session.query(WorldEvent).filter(
                    WorldEvent.is_active == True
                ).count(),
                "total_today": session.query(WorldEvent).filter(
                    WorldEvent.created_at > datetime.utcnow() - timedelta(days=1)
                ).count()
            }
            
            return stats
    
    def _get_richest_player(self) -> Optional[Dict]:
        """Get richest player information"""
        with self.db.get_session() as session:
            richest = session.query(Player).order_by(Player.gold.desc()).first()
            if richest:
                return {
                    "name": richest.first_name,
                    "gold": richest.gold,
                    "level": richest.level,
                    "rank": richest.rank
                }
            return None
    
    def _get_military_stats(self) -> Dict:
        """Get military statistics"""
        with self.db.get_session() as session:
            # This would need to be implemented based on your unit system
            return {
                "total_units": 0,  # Placeholder
                "largest_army": None  # Placeholder
            }
    
    def reset_game_data(self, confirm: bool = False) -> bool:
        """Reset all game data (dangerous operation)"""
        if not confirm:
            return False
        
        with self.db.get_session() as session:
            # Delete all game data
            session.query(Player).delete()
            session.query(Nation).delete()
            session.query(Province).delete()
            session.query(WorldEvent).delete()
            
            # Reset other tables as needed
            # ... (add other table deletions)
            
            session.commit()
            return True
    
    def ban_player(self, player_id: int, reason: str = "Admin ban") -> bool:
        """Ban a player"""
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=player_id).first()
            if not player:
                return False
            
            player.is_banned = True
            session.commit()
            return True
    
    def unban_player(self, player_id: int) -> bool:
        """Unban a player"""
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=player_id).first()
            if not player:
                return False
            
            player.is_banned = False
            session.commit()
            return True
    
    def give_gold(self, player_id: int, amount: float) -> bool:
        """Give gold to a player"""
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=player_id).first()
            if not player:
                return False
            
            player.gold += amount
            session.commit()
            return True
    
    def set_player_level(self, player_id: int, level: int) -> bool:
        """Set player level"""
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=player_id).first()
            if not player:
                return False
            
            player.level = max(1, level)
            
            # Update rank based on level
            if player.level >= 20:
                player.rank = "Supreme Leader"
            elif player.level >= 15:
                player.rank = "Field Marshal"
            elif player.level >= 10:
                player.rank = "General"
            elif player.level >= 5:
                player.rank = "Colonel"
            else:
                player.rank = "Commander"
            
            session.commit()
            return True
    
    def create_world_event(self, title: str, description: str, event_type: str, 
                          severity: str = "medium", duration: int = 3600) -> bool:
        """Create a custom world event"""
        with self.db.get_session() as session:
            event = WorldEvent(
                title=title,
                description=description,
                event_type=event_type,
                severity=severity,
                duration=duration,
                is_active=True
            )
            session.add(event)
            session.commit()
            return True
    
    def get_player_info(self, player_id: int) -> Optional[Dict]:
        """Get detailed player information"""
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=player_id).first()
            if not player:
                return None
            
            return {
                "id": player.id,
                "telegram_id": player.telegram_id,
                "username": player.username,
                "first_name": player.first_name,
                "last_name": player.last_name,
                "level": player.level,
                "experience": player.experience,
                "rank": player.rank,
                "gold": player.gold,
                "morale": player.morale,
                "is_banned": player.is_banned,
                "language": player.language,
                "last_active": player.last_active.isoformat(),
                "created_at": player.created_at.isoformat(),
                "nation": player.nation.name if player.nation else None
            }
    
    def get_top_players(self, limit: int = 10) -> List[Dict]:
        """Get top players by various criteria"""
        with self.db.get_session() as session:
            players = session.query(Player).filter(
                Player.is_banned == False
            ).order_by(Player.gold.desc()).limit(limit).all()
            
            return [
                {
                    "name": p.first_name,
                    "gold": p.gold,
                    "level": p.level,
                    "rank": p.rank,
                    "morale": p.morale
                }
                for p in players
            ]
    
    def backup_game_data(self) -> Dict:
        """Create a backup of game data"""
        with self.db.get_session() as session:
            backup = {
                "timestamp": datetime.utcnow().isoformat(),
                "players": [],
                "nations": [],
                "provinces": [],
                "events": []
            }
            
            # Backup players
            players = session.query(Player).all()
            for player in players:
                backup["players"].append({
                    "telegram_id": player.telegram_id,
                    "username": player.username,
                    "first_name": player.first_name,
                    "last_name": player.last_name,
                    "level": player.level,
                    "experience": player.experience,
                    "rank": player.rank,
                    "gold": player.gold,
                    "morale": player.morale,
                    "is_banned": player.is_banned,
                    "language": player.language,
                    "last_active": player.last_active.isoformat(),
                    "created_at": player.created_at.isoformat()
                })
            
            # Backup nations
            nations = session.query(Nation).all()
            for nation in nations:
                backup["nations"].append({
                    "name": nation.name,
                    "flag_emoji": nation.flag_emoji,
                    "color": nation.color,
                    "government_type": nation.government_type,
                    "population": nation.population,
                    "gdp": nation.gdp,
                    "tax_rate": nation.tax_rate,
                    "research_points": nation.research_points,
                    "is_ai": nation.is_ai,
                    "created_at": nation.created_at.isoformat()
                })
            
            # Backup provinces
            provinces = session.query(Province).all()
            for province in provinces:
                backup["provinces"].append({
                    "name": province.name,
                    "x": province.x,
                    "y": province.y,
                    "population": province.population,
                    "infrastructure": province.infrastructure,
                    "defense_level": province.defense_level,
                    "morale": province.morale,
                    "weather": province.weather,
                    "temperature": province.temperature,
                    "owner_id": province.owner_id,
                    "iron_deposits": province.iron_deposits,
                    "oil_deposits": province.oil_deposits,
                    "food_production": province.food_production,
                    "gold_mines": province.gold_mines,
                    "uranium_deposits": province.uranium_deposits,
                    "buildings": province.buildings,
                    "created_at": province.created_at.isoformat()
                })
            
            # Backup events
            events = session.query(WorldEvent).all()
            for event in events:
                backup["events"].append({
                    "title": event.title,
                    "description": event.description,
                    "event_type": event.event_type,
                    "severity": event.severity,
                    "effects": event.effects,
                    "affected_regions": event.affected_regions,
                    "duration": event.duration,
                    "is_active": event.is_active,
                    "created_at": event.created_at.isoformat(),
                    "expires_at": event.expires_at.isoformat() if event.expires_at else None
                })
            
            return backup
    
    def restore_game_data(self, backup_data: Dict) -> bool:
        """Restore game data from backup"""
        try:
            with self.db.get_session() as session:
                # Clear existing data
                session.query(Player).delete()
                session.query(Nation).delete()
                session.query(Province).delete()
                session.query(WorldEvent).delete()
                
                # Restore data (simplified - would need full implementation)
                # This is a placeholder for the restore functionality
                
                session.commit()
                return True
        except Exception as e:
            print(f"Error restoring data: {e}")
            return False