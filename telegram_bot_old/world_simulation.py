"""
World Simulation System for World War Telegram Bot
"""
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import DatabaseManager, WorldEvent, Province, Nation, Player

class WorldSimulator:
    def __init__(self, config: Dict):
        self.config = config
        self.world_events_interval = config["world_events_interval"]
        self.season_duration = config["season_duration"]
        self.ai_factions = config["ai_factions"]
        self.is_running = False
        self.db = None  # Will be set by bot
        
        self.event_types = {
            "economic": {
                "names": [
                    "Economic Boom",
                    "Market Crash",
                    "Trade Embargo",
                    "Resource Discovery",
                    "Inflation Crisis",
                    "Economic Sanctions"
                ],
                "descriptions": [
                    "A period of economic prosperity increases production across the world.",
                    "A sudden market crash affects global trade and prices.",
                    "A major trade embargo disrupts international commerce.",
                    "New resource deposits have been discovered, boosting production.",
                    "Rapid inflation affects the global economy.",
                    "Economic sanctions are imposed, affecting trade relations."
                ],
                "effects": {
                    "production_bonus": (0.1, 0.3),
                    "price_modifier": (0.8, 1.2),
                    "trade_penalty": (0.0, 0.5)
                }
            },
            "military": {
                "names": [
                    "Arms Race",
                    "Peace Treaty",
                    "Military Coup",
                    "Weapons Development",
                    "Defense Pact",
                    "War Declaration"
                ],
                "descriptions": [
                    "An arms race begins, increasing military production.",
                    "A major peace treaty is signed, reducing tensions.",
                    "A military coup destabilizes a region.",
                    "Breakthrough in weapons technology is achieved.",
                    "A new defense pact is formed between nations.",
                    "War is declared between major powers."
                ],
                "effects": {
                    "military_bonus": (0.1, 0.4),
                    "morale_penalty": (0.0, 0.3),
                    "defense_bonus": (0.0, 0.2)
                }
            },
            "natural": {
                "names": [
                    "Hurricane",
                    "Drought",
                    "Earthquake",
                    "Flood",
                    "Volcanic Eruption",
                    "Pandemic"
                ],
                "descriptions": [
                    "A powerful hurricane devastates coastal regions.",
                    "Severe drought affects agricultural production.",
                    "A major earthquake causes widespread damage.",
                    "Flooding disrupts transportation and production.",
                    "A volcanic eruption affects global climate.",
                    "A pandemic spreads across the world."
                ],
                "effects": {
                    "production_penalty": (0.1, 0.5),
                    "infrastructure_damage": (0.1, 0.3),
                    "population_loss": (0.05, 0.2)
                }
            },
            "political": {
                "names": [
                    "Election",
                    "Revolution",
                    "Alliance Formation",
                    "Diplomatic Crisis",
                    "Government Change",
                    "International Summit"
                ],
                "descriptions": [
                    "A major election changes the political landscape.",
                    "A revolution overthrows the government.",
                    "A new alliance is formed between nations.",
                    "A diplomatic crisis threatens international relations.",
                    "A change in government affects policies.",
                    "An international summit addresses global issues."
                ],
                "effects": {
                    "stability_bonus": (0.0, 0.2),
                    "morale_bonus": (0.0, 0.3),
                    "diplomacy_bonus": (0.0, 0.4)
                }
            }
        }
    
    async def run(self):
        """Main simulation loop"""
        self.is_running = True
        
        while self.is_running:
            try:
                # Generate world events
                if random.random() < 0.1:  # 10% chance per cycle
                    await self.generate_world_event()
                
                # Update weather
                await self.update_weather()
                
                # Process AI factions
                await self.process_ai_factions()
                
                # Update world state
                await self.update_world_state()
                
                # Wait before next cycle
                await asyncio.sleep(3600)  # 1 hour
                
            except Exception as e:
                print(f"Error in world simulation: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retrying
    
    def stop(self):
        """Stop the simulation"""
        self.is_running = False
    
    async def generate_world_event(self):
        """Generate a random world event"""
        event_type = random.choice(list(self.event_types.keys()))
        event_data = self.event_types[event_type]
        
        name = random.choice(event_data["names"])
        description = random.choice(event_data["descriptions"])
        
        # Generate effects
        effects = {}
        for effect_name, (min_val, max_val) in event_data["effects"].items():
            effects[effect_name] = random.uniform(min_val, max_val)
        
        # Determine affected regions
        affected_regions = self._get_random_regions(3)  # Affect 3 random regions
        
        # Create event
        with self.db.get_session() as session:
            event = WorldEvent(
                title=name,
                description=description,
                event_type=event_type,
                severity=random.choice(["low", "medium", "high", "critical"]),
                effects=effects,
                affected_regions=affected_regions,
                duration=random.randint(3600, 86400)  # 1 hour to 1 day
            )
            session.add(event)
            session.commit()
    
    def _get_random_regions(self, count: int) -> List[int]:
        """Get random region IDs"""
        with self.db.get_session() as session:
            provinces = session.query(Province).all()
            region_ids = [p.id for p in provinces]
            return random.sample(region_ids, min(count, len(region_ids)))
    
    async def update_weather(self):
        """Update weather for all provinces"""
        with self.db.get_session() as session:
            provinces = session.query(Province).all()
            
            for province in provinces:
                # Random weather change
                if random.random() < 0.05:  # 5% chance to change weather
                    province.weather = random.choice([
                        "clear", "rain", "storm", "fog", "snow", "cloudy"
                    ])
                    
                    # Update temperature based on weather
                    if province.weather == "snow":
                        province.temperature = random.uniform(-10, 5)
                    elif province.weather == "storm":
                        province.temperature = random.uniform(5, 15)
                    elif province.weather == "rain":
                        province.temperature = random.uniform(10, 20)
                    elif province.weather == "fog":
                        province.temperature = random.uniform(5, 15)
                    elif province.weather == "cloudy":
                        province.temperature = random.uniform(10, 25)
                    else:  # clear
                        province.temperature = random.uniform(15, 30)
            
            session.commit()
    
    async def process_ai_factions(self):
        """Process AI faction actions"""
        with self.db.get_session() as session:
            ai_nations = session.query(Nation).filter(Nation.is_ai == True).all()
            
            for nation in ai_nations:
                # Random AI actions
                action = random.choice([
                    "expand", "research", "build", "attack", "diplomacy"
                ])
                
                if action == "expand":
                    await self._ai_expand(nation)
                elif action == "research":
                    await self._ai_research(nation)
                elif action == "build":
                    await self._ai_build(nation)
                elif action == "attack":
                    await self._ai_attack(nation)
                elif action == "diplomacy":
                    await self._ai_diplomacy(nation)
    
    async def _ai_expand(self, nation: Nation):
        """AI expansion logic"""
        # Find unclaimed provinces
        with self.db.get_session() as session:
            unclaimed = session.query(Province).filter(Province.owner_id.is_(None)).all()
            
            if unclaimed and random.random() < 0.3:  # 30% chance to expand
                province = random.choice(unclaimed)
                province.owner_id = nation.id
                province.morale = 100.0
                session.commit()
    
    async def _ai_research(self, nation: Nation):
        """AI research logic"""
        # Simple AI research - just add research points
        with self.db.get_session() as session:
            nation.research_points += random.randint(10, 50)
            session.commit()
    
    async def _ai_build(self, nation: Nation):
        """AI building logic"""
        # AI builds in their provinces
        with self.db.get_session() as session:
            provinces = session.query(Province).filter(Province.owner_id == nation.id).all()
            
            if provinces and random.random() < 0.2:  # 20% chance to build
                province = random.choice(provinces)
                building_types = ["factory", "farm", "mine", "refinery"]
                building = random.choice(building_types)
                
                buildings = province.buildings or []
                if building not in buildings:
                    buildings.append(building)
                    province.buildings = buildings
                    session.commit()
    
    async def _ai_attack(self, nation: Nation):
        """AI attack logic"""
        # AI attacks other nations (simplified)
        with self.db.get_session() as session:
            other_nations = session.query(Nation).filter(
                Nation.id != nation.id,
                Nation.is_ai == False  # Attack player nations
            ).all()
            
            if other_nations and random.random() < 0.1:  # 10% chance to attack
                target = random.choice(other_nations)
                # This would trigger a battle (simplified)
                pass
    
    async def _ai_diplomacy(self, nation: Nation):
        """AI diplomacy logic"""
        # AI forms alliances or breaks them
        with self.db.get_session() as session:
            if random.random() < 0.05:  # 5% chance for diplomacy
                # This would create or break alliances
                pass
    
    async def update_world_state(self):
        """Update overall world state"""
        with self.db.get_session() as session:
            # Update active events
            active_events = session.query(WorldEvent).filter(
                WorldEvent.is_active == True,
                WorldEvent.expires_at < datetime.utcnow()
            ).all()
            
            for event in active_events:
                event.is_active = False
            
            # Update player morale based on world events
            players = session.query(Player).all()
            for player in players:
                # Apply world event effects to player morale
                active_events = session.query(WorldEvent).filter(
                    WorldEvent.is_active == True
                ).all()
                
                morale_change = 0
                for event in active_events:
                    if "morale_bonus" in event.effects:
                        morale_change += event.effects["morale_bonus"] * 10
                    if "morale_penalty" in event.effects:
                        morale_change -= event.effects["morale_penalty"] * 10
                
                player.morale = max(0, min(100, player.morale + morale_change))
            
            session.commit()
    
    def get_world_status(self) -> Dict:
        """Get current world status"""
        with self.db.get_session() as session:
            # Count active events
            active_events = session.query(WorldEvent).filter(
                WorldEvent.is_active == True
            ).count()
            
            # Count nations
            total_nations = session.query(Nation).count()
            ai_nations = session.query(Nation).filter(Nation.is_ai == True).count()
            player_nations = total_nations - ai_nations
            
            # Count provinces
            total_provinces = session.query(Province).count()
            claimed_provinces = session.query(Province).filter(
                Province.owner_id.isnot(None)
            ).count()
            
            # Count players
            total_players = session.query(Player).count()
            active_players = session.query(Player).filter(
                Player.last_active > datetime.utcnow() - timedelta(days=1)
            ).count()
            
            return {
                "active_events": active_events,
                "total_nations": total_nations,
                "player_nations": player_nations,
                "ai_nations": ai_nations,
                "total_provinces": total_provinces,
                "claimed_provinces": claimed_provinces,
                "total_players": total_players,
                "active_players": active_players
            }
    
    def get_active_events(self) -> List[WorldEvent]:
        """Get currently active world events"""
        with self.db.get_session() as session:
            return session.query(WorldEvent).filter(
                WorldEvent.is_active == True
            ).order_by(WorldEvent.created_at.desc()).all()
    
    def get_event_history(self, limit: int = 10) -> List[WorldEvent]:
        """Get recent event history"""
        with self.db.get_session() as session:
            return session.query(WorldEvent).order_by(
                WorldEvent.created_at.desc()
            ).limit(limit).all()