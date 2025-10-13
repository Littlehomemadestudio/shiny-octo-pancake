"""
Technology System for World War Telegram Bot
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import DatabaseManager, Player, Technology, NationTechnology, Nation

class TechnologyManager:
    def __init__(self):
        self.db = None  # Will be set by bot
        self.technology_tree = {
            "military": {
                "tier_1": [
                    {
                        "name": "Basic Training",
                        "description": "Improves infantry combat effectiveness by 20%",
                        "cost": 100,
                        "prerequisites": [],
                        "effects": {"infantry_attack": 0.2, "infantry_defense": 0.2}
                    },
                    {
                        "name": "Tactical Warfare",
                        "description": "Unlocks advanced combat strategies",
                        "cost": 150,
                        "prerequisites": [],
                        "effects": {"combat_bonus": 0.15}
                    }
                ],
                "tier_2": [
                    {
                        "name": "Armored Warfare",
                        "description": "Improves tank effectiveness by 25%",
                        "cost": 300,
                        "prerequisites": ["Basic Training"],
                        "effects": {"tank_attack": 0.25, "tank_defense": 0.25}
                    },
                    {
                        "name": "Air Superiority",
                        "description": "Improves aircraft effectiveness by 30%",
                        "cost": 400,
                        "prerequisites": ["Tactical Warfare"],
                        "effects": {"aircraft_attack": 0.3, "aircraft_defense": 0.3}
                    }
                ],
                "tier_3": [
                    {
                        "name": "Nuclear Weapons",
                        "description": "Unlocks nuclear weapons and devastating attacks",
                        "cost": 1000,
                        "prerequisites": ["Armored Warfare", "Air Superiority"],
                        "effects": {"nuclear_unlock": True, "attack_power": 0.5}
                    }
                ]
            },
            "economic": {
                "tier_1": [
                    {
                        "name": "Steel Production",
                        "description": "Increases iron and steel production by 30%",
                        "cost": 120,
                        "prerequisites": [],
                        "effects": {"iron_production": 0.3, "steel_production": 0.3}
                    },
                    {
                        "name": "Agricultural Revolution",
                        "description": "Increases food production by 40%",
                        "cost": 100,
                        "prerequisites": [],
                        "effects": {"food_production": 0.4}
                    }
                ],
                "tier_2": [
                    {
                        "name": "Industrial Revolution",
                        "description": "Massive production boost for all materials",
                        "cost": 500,
                        "prerequisites": ["Steel Production"],
                        "effects": {"all_production": 0.5}
                    },
                    {
                        "name": "Oil Refining",
                        "description": "Improves oil processing and efficiency",
                        "cost": 300,
                        "prerequisites": ["Agricultural Revolution"],
                        "effects": {"oil_production": 0.4, "fuel_efficiency": 0.2}
                    }
                ],
                "tier_3": [
                    {
                        "name": "Advanced Manufacturing",
                        "description": "Revolutionary production methods",
                        "cost": 800,
                        "prerequisites": ["Industrial Revolution", "Oil Refining"],
                        "effects": {"all_production": 0.8, "efficiency": 0.3}
                    }
                ]
            },
            "research": {
                "tier_1": [
                    {
                        "name": "Scientific Method",
                        "description": "Increases research speed by 25%",
                        "cost": 150,
                        "prerequisites": [],
                        "effects": {"research_speed": 0.25}
                    },
                    {
                        "name": "Laboratory Equipment",
                        "description": "Improves research efficiency",
                        "cost": 200,
                        "prerequisites": [],
                        "effects": {"research_efficiency": 0.3}
                    }
                ],
                "tier_2": [
                    {
                        "name": "Advanced Research",
                        "description": "Unlocks higher tier technologies",
                        "cost": 400,
                        "prerequisites": ["Scientific Method"],
                        "effects": {"research_unlock": True}
                    },
                    {
                        "name": "Computer Technology",
                        "description": "Revolutionary computing power for research",
                        "cost": 600,
                        "prerequisites": ["Laboratory Equipment"],
                        "effects": {"research_speed": 0.5, "research_efficiency": 0.4}
                    }
                ],
                "tier_3": [
                    {
                        "name": "Artificial Intelligence",
                        "description": "AI-powered research and development",
                        "cost": 1200,
                        "prerequisites": ["Advanced Research", "Computer Technology"],
                        "effects": {"research_speed": 1.0, "ai_unlock": True}
                    }
                ]
            }
        }
    
    def get_available_technologies(self, nation_id: int) -> List[Dict]:
        """Get technologies available for research by a nation"""
        with self.db.get_session() as session:
            # Get nation's current technologies
            nation_techs = session.query(NationTechnology).filter_by(nation_id=nation_id).all()
            researched_techs = {nt.technology.name for nt in nation_techs if nt.completed_at}
            
            available = []
            
            for category, tiers in self.technology_tree.items():
                for tier, technologies in tiers.items():
                    for tech in technologies:
                        # Check if already researched
                        if tech["name"] in researched_techs:
                            continue
                        
                        # Check prerequisites
                        can_research = True
                        for prereq in tech["prerequisites"]:
                            if prereq not in researched_techs:
                                can_research = False
                                break
                        
                        if can_research:
                            available.append({
                                "name": tech["name"],
                                "description": tech["description"],
                                "cost": tech["cost"],
                                "category": category,
                                "tier": tier,
                                "effects": tech["effects"]
                            })
            
            return available
    
    def can_research_technology(self, nation_id: int, tech_name: str) -> Tuple[bool, str]:
        """Check if nation can research a technology"""
        with self.db.get_session() as session:
            nation = session.query(Nation).filter_by(id=nation_id).first()
            if not nation:
                return False, "Nation not found"
            
            # Find technology in tree
            tech_data = None
            for category, tiers in self.technology_tree.items():
                for tier, technologies in tiers.items():
                    for tech in technologies:
                        if tech["name"] == tech_name:
                            tech_data = tech
                            break
            
            if not tech_data:
                return False, "Technology not found"
            
            # Check if already researched
            existing = session.query(NationTechnology).filter_by(
                nation_id=nation_id,
                technology_id=tech_name  # This should be tech ID, simplified for now
            ).first()
            
            if existing and existing.completed_at:
                return False, "Technology already researched"
            
            # Check prerequisites
            nation_techs = session.query(NationTechnology).filter_by(nation_id=nation_id).all()
            researched_techs = {nt.technology.name for nt in nation_techs if nt.completed_at}
            
            for prereq in tech_data["prerequisites"]:
                if prereq not in researched_techs:
                    return False, f"Prerequisite {prereq} not researched"
            
            # Check research points
            if nation.research_points < tech_data["cost"]:
                return False, "Not enough research points"
            
            return True, "Can research technology"
    
    def start_research(self, nation_id: int, tech_name: str) -> bool:
        """Start researching a technology"""
        can_research, reason = self.can_research_technology(nation_id, tech_name)
        if not can_research:
            return False
        
        with self.db.get_session() as session:
            nation = session.query(Nation).filter_by(id=nation_id).first()
            
            # Find technology data
            tech_data = None
            for category, tiers in self.technology_tree.items():
                for tier, technologies in tiers.items():
                    for tech in technologies:
                        if tech["name"] == tech_name:
                            tech_data = tech
                            break
            
            if not tech_data:
                return False
            
            # Deduct research points
            nation.research_points -= tech_data["cost"]
            
            # Create research record
            nation_tech = NationTechnology(
                nation_id=nation_id,
                technology_id=tech_name,  # Simplified
                research_progress=0.0,
                started_at=datetime.utcnow()
            )
            session.add(nation_tech)
            session.commit()
            return True
    
    def get_active_research(self, nation_id: int) -> List[NationTechnology]:
        """Get active research projects for a nation"""
        with self.db.get_session() as session:
            return session.query(NationTechnology).filter(
                NationTechnology.nation_id == nation_id,
                NationTechnology.completed_at.is_(None)
            ).all()
    
    def update_research_progress(self, nation_id: int, research_speed: float = 1.0):
        """Update research progress for a nation"""
        with self.db.get_session() as session:
            active_research = self.get_active_research(nation_id)
            
            for research in active_research:
                # Calculate progress increment
                base_progress = 0.01  # 1% per update
                progress_increment = base_progress * research_speed
                
                research.research_progress += progress_increment
                
                # Check if research is complete
                if research.research_progress >= 1.0:
                    research.research_progress = 1.0
                    research.completed_at = datetime.utcnow()
                    
                    # Apply technology effects
                    self._apply_technology_effects(session, nation_id, research.technology_id)
            
            session.commit()
    
    def _apply_technology_effects(self, session, nation_id: int, tech_name: str):
        """Apply technology effects to nation"""
        # Find technology data
        tech_data = None
        for category, tiers in self.technology_tree.items():
            for tier, technologies in tiers.items():
                for tech in technologies:
                    if tech["name"] == tech_name:
                        tech_data = tech
                        break
        
        if not tech_data:
            return
        
        # Apply effects (simplified - would need more complex implementation)
        nation = session.query(Nation).filter_by(id=nation_id).first()
        if not nation:
            return
        
        effects = tech_data["effects"]
        
        # This would need to be implemented based on the specific effects
        # For now, just a placeholder
        if "research_speed" in effects:
            # Apply research speed bonus
            pass
        if "all_production" in effects:
            # Apply production bonus
            pass
        # ... other effects
    
    def get_research_points_per_hour(self, nation_id: int) -> float:
        """Calculate research points generated per hour"""
        with self.db.get_session() as session:
            nation = session.query(Nation).filter_by(id=nation_id).first()
            if not nation:
                return 0.0
            
            # Base research points from population and infrastructure
            base_points = nation.population * 0.001  # 0.1% of population per hour
            
            # Research center bonus
            research_centers = 0  # Would count research centers in provinces
            research_bonus = research_centers * 0.1
            
            # Technology bonuses
            tech_bonus = 1.0
            nation_techs = session.query(NationTechnology).filter_by(nation_id=nation_id).all()
            for nt in nation_techs:
                if nt.completed_at:  # Only completed technologies
                    # Apply technology bonuses (simplified)
                    pass
            
            total_points = (base_points + research_bonus) * tech_bonus
            return max(0, total_points)
    
    def generate_research_points(self):
        """Generate research points for all nations"""
        with self.db.get_session() as session:
            nations = session.query(Nation).all()
            
            for nation in nations:
                points_per_hour = self.get_research_points_per_hour(nation.id)
                nation.research_points += points_per_hour
                
                # Cap research points at 10000
                nation.research_points = min(10000, nation.research_points)
            
            session.commit()
    
    def get_technology_effects(self, nation_id: int) -> Dict:
        """Get all active technology effects for a nation"""
        with self.db.get_session() as session:
            nation_techs = session.query(NationTechnology).filter_by(nation_id=nation_id).all()
            completed_techs = [nt for nt in nation_techs if nt.completed_at]
            
            effects = {
                "military": {},
                "economic": {},
                "research": {}
            }
            
            for nt in completed_techs:
                tech_name = nt.technology_id  # Simplified
                
                # Find technology data
                tech_data = None
                for category, tiers in self.technology_tree.items():
                    for tier, technologies in tiers.items():
                        for tech in technologies:
                            if tech["name"] == tech_name:
                                tech_data = tech
                                break
                
                if tech_data:
                    category = None
                    for cat in effects.keys():
                        if any(tech_name in [t["name"] for t in self.technology_tree[cat].values()]):
                            category = cat
                            break
                    
                    if category:
                        effects[category].update(tech_data["effects"])
            
            return effects