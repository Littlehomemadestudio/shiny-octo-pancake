"""
Quest System for World War Telegram Bot
"""
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import DatabaseManager, Player, Quest, PlayerQuest, PlayerUnit, PlayerMaterial

class QuestManager:
    def __init__(self):
        self.db = None  # Will be set by bot
        self.quest_templates = {
            "recon": {
                "titles": [
                    "Scout Enemy Territory",
                    "Gather Intelligence",
                    "Reconnaissance Mission",
                    "Spy on Enemy Base"
                ],
                "descriptions": [
                    "Scout the enemy territory and gather valuable intelligence about their forces.",
                    "Infiltrate enemy lines and report back with tactical information.",
                    "Conduct a reconnaissance mission to assess enemy capabilities.",
                    "Gather intelligence on enemy troop movements and positions."
                ],
                "difficulty_range": (1, 3),
                "duration_range": (1800, 7200),  # 30 minutes to 2 hours
                "base_rewards": {"gold": 200, "experience": 50}
            },
            "sabotage": {
                "titles": [
                    "Sabotage Enemy Supply Lines",
                    "Destroy Enemy Infrastructure",
                    "Disrupt Enemy Communications",
                    "Sabotage Enemy Weapons"
                ],
                "descriptions": [
                    "Infiltrate enemy territory and sabotage their supply lines.",
                    "Destroy key enemy infrastructure to weaken their position.",
                    "Disrupt enemy communications to create confusion.",
                    "Sabotage enemy weapons and equipment."
                ],
                "difficulty_range": (2, 4),
                "duration_range": (3600, 14400),  # 1 to 4 hours
                "base_rewards": {"gold": 500, "experience": 100}
            },
            "escort": {
                "titles": [
                    "Escort Supply Convoy",
                    "Protect VIP Transport",
                    "Guard Diplomatic Mission",
                    "Escort Research Team"
                ],
                "descriptions": [
                    "Escort a valuable supply convoy through dangerous territory.",
                    "Protect a VIP during their journey to a secure location.",
                    "Guard a diplomatic mission to ensure safe negotiations.",
                    "Escort a research team to a remote location."
                ],
                "difficulty_range": (1, 3),
                "duration_range": (2400, 10800),  # 40 minutes to 3 hours
                "base_rewards": {"gold": 300, "experience": 75}
            },
            "invasion": {
                "titles": [
                    "Invade Enemy Province",
                    "Capture Strategic Location",
                    "Launch Offensive Operation",
                    "Conquer Enemy Territory"
                ],
                "descriptions": [
                    "Lead an invasion force to capture enemy territory.",
                    "Capture a strategic location to gain tactical advantage.",
                    "Launch an offensive operation against enemy forces.",
                    "Conquer enemy territory and establish control."
                ],
                "difficulty_range": (3, 5),
                "duration_range": (7200, 28800),  # 2 to 8 hours
                "base_rewards": {"gold": 1000, "experience": 200}
            },
            "research": {
                "titles": [
                    "Research New Technology",
                    "Develop Advanced Weapons",
                    "Study Enemy Technology",
                    "Conduct Scientific Experiment"
                ],
                "descriptions": [
                    "Research new technology to improve your nation's capabilities.",
                    "Develop advanced weapons to gain military advantage.",
                    "Study captured enemy technology to learn their secrets.",
                    "Conduct a scientific experiment with potential military applications."
                ],
                "difficulty_range": (2, 4),
                "duration_range": (10800, 43200),  # 3 to 12 hours
                "base_rewards": {"gold": 800, "experience": 150}
            }
        }
    
    def generate_random_quest(self, quest_type: str, player_level: int = 1) -> Quest:
        """Generate a random quest of specified type"""
        if quest_type not in self.quest_templates:
            return None
        
        template = self.quest_templates[quest_type]
        
        # Select random title and description
        title = random.choice(template["titles"])
        description = random.choice(template["descriptions"])
        
        # Calculate difficulty based on player level
        min_diff, max_diff = template["difficulty_range"]
        difficulty = min(max_diff, max(min_diff, player_level + random.randint(-1, 1)))
        
        # Calculate duration
        min_dur, max_dur = template["duration_range"]
        duration = random.randint(min_dur, max_dur)
        
        # Calculate rewards based on difficulty
        base_rewards = template["base_rewards"].copy()
        rewards = {}
        for reward_type, base_amount in base_rewards.items():
            if reward_type == "gold":
                rewards[reward_type] = int(base_amount * difficulty * random.uniform(0.8, 1.2))
            elif reward_type == "experience":
                rewards[reward_type] = int(base_amount * difficulty * random.uniform(0.8, 1.2))
            else:
                rewards[reward_type] = base_amount
        
        # Add random material rewards for higher difficulty quests
        if difficulty >= 3:
            materials = ["iron", "oil", "food", "gold", "uranium", "steel"]
            material_reward = random.choice(materials)
            rewards["materials"] = {material_reward: random.randint(10, 50) * difficulty}
        
        # Create quest requirements
        requirements = {"level": max(1, difficulty - 1)}
        
        # Add unit requirements for military quests
        if quest_type in ["invasion", "sabotage"]:
            unit_requirements = {}
            if difficulty >= 3:
                unit_requirements["infantry"] = random.randint(5, 20)
            if difficulty >= 4:
                unit_requirements["tank"] = random.randint(2, 8)
            if difficulty >= 5:
                unit_requirements["aircraft"] = random.randint(1, 3)
            
            if unit_requirements:
                requirements["units"] = unit_requirements
        
        return Quest(
            title=title,
            description=description,
            quest_type=quest_type,
            difficulty=difficulty,
            duration=duration,
            rewards=rewards,
            requirements=requirements
        )
    
    def get_available_quests(self, player_id: int, limit: int = 10) -> List[Quest]:
        """Get available quests for a player"""
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(id=player_id).first()
            if not player:
                return []
            
            # Get quests that player can accept
            available_quests = session.query(Quest).filter(
                Quest.is_active == True,
                Quest.difficulty <= player.level + 2  # Allow some higher level quests
            ).limit(limit).all()
            
            return available_quests
    
    def can_accept_quest(self, player_id: int, quest_id: int) -> Tuple[bool, str]:
        """Check if player can accept a quest"""
        with self.db.get_session() as session:
            player = session.query(Player).filter_by(id=player_id).first()
            quest = session.query(Quest).filter_by(id=quest_id).first()
            
            if not player or not quest:
                return False, "Player or quest not found"
            
            if not quest.is_active:
                return False, "Quest is not available"
            
            # Check level requirement
            if player.level < quest.requirements.get("level", 1):
                return False, "Level too low for this quest"
            
            # Check unit requirements
            if "units" in quest.requirements:
                player_units = self._get_player_units(session, player_id)
                for unit_type, required_count in quest.requirements["units"].items():
                    if player_units.get(unit_type, 0) < required_count:
                        return False, f"Not enough {unit_type} units (need {required_count})"
            
            # Check if player already has this quest
            existing_quest = session.query(PlayerQuest).filter_by(
                player_id=player_id,
                quest_id=quest_id,
                status="active"
            ).first()
            
            if existing_quest:
                return False, "You already have this quest"
            
            # Check quest limit (max 3 active quests)
            active_quests = session.query(PlayerQuest).filter_by(
                player_id=player_id,
                status="active"
            ).count()
            
            if active_quests >= 3:
                return False, "You can only have 3 active quests at a time"
            
            return True, "Can accept quest"
    
    def accept_quest(self, player_id: int, quest_id: int) -> bool:
        """Accept a quest for a player"""
        can_accept, reason = self.can_accept_quest(player_id, quest_id)
        if not can_accept:
            return False
        
        with self.db.get_session() as session:
            player_quest = PlayerQuest(
                player_id=player_id,
                quest_id=quest_id,
                status="active",
                started_at=datetime.utcnow()
            )
            session.add(player_quest)
            session.commit()
            return True
    
    def get_player_quests(self, player_id: int) -> List[PlayerQuest]:
        """Get all quests for a player"""
        with self.db.get_session() as session:
            return session.query(PlayerQuest).filter_by(player_id=player_id).all()
    
    def get_active_quests(self, player_id: int) -> List[PlayerQuest]:
        """Get active quests for a player"""
        with self.db.get_session() as session:
            return session.query(PlayerQuest).filter_by(
                player_id=player_id,
                status="active"
            ).all()
    
    def update_quest_progress(self, player_id: int, quest_id: int, progress: float):
        """Update quest progress"""
        with self.db.get_session() as session:
            player_quest = session.query(PlayerQuest).filter_by(
                player_id=player_id,
                quest_id=quest_id,
                status="active"
            ).first()
            
            if player_quest:
                player_quest.progress = min(1.0, max(0.0, progress))
                session.commit()
    
    def complete_quest(self, player_id: int, quest_id: int) -> bool:
        """Complete a quest and give rewards"""
        with self.db.get_session() as session:
            player_quest = session.query(PlayerQuest).filter_by(
                player_id=player_id,
                quest_id=quest_id,
                status="active"
            ).first()
            
            if not player_quest:
                return False
            
            quest = player_quest.quest
            player = player_quest.player
            
            # Give rewards
            rewards = quest.rewards or {}
            
            # Gold reward
            if "gold" in rewards:
                player.gold += rewards["gold"]
            
            # Experience reward
            if "experience" in rewards:
                player.experience += rewards["experience"]
                # Check for level up
                self._check_level_up(session, player)
            
            # Material rewards
            if "materials" in rewards:
                for material_type, quantity in rewards["materials"].items():
                    player_material = session.query(PlayerMaterial).filter_by(
                        player_id=player_id,
                        material_type=material_type
                    ).first()
                    
                    if player_material:
                        player_material.quantity += quantity
                    else:
                        player_material = PlayerMaterial(
                            player_id=player_id,
                            material_type=material_type,
                            quantity=quantity
                        )
                        session.add(player_material)
            
            # Update quest status
            player_quest.status = "completed"
            player_quest.completed_at = datetime.utcnow()
            player_quest.progress = 1.0
            
            session.commit()
            return True
    
    def fail_quest(self, player_id: int, quest_id: int) -> bool:
        """Mark a quest as failed"""
        with self.db.get_session() as session:
            player_quest = session.query(PlayerQuest).filter_by(
                player_id=player_id,
                quest_id=quest_id,
                status="active"
            ).first()
            
            if not player_quest:
                return False
            
            player_quest.status = "failed"
            player_quest.completed_at = datetime.utcnow()
            
            session.commit()
            return True
    
    def process_quest_timeouts(self):
        """Process quest timeouts and failures"""
        with self.db.get_session() as session:
            # Get expired active quests
            expired_quests = session.query(PlayerQuest).filter(
                PlayerQuest.status == "active",
                PlayerQuest.started_at < datetime.utcnow() - timedelta(seconds=PlayerQuest.quest.duration)
            ).all()
            
            for player_quest in expired_quests:
                player_quest.status = "expired"
                player_quest.completed_at = datetime.utcnow()
            
            session.commit()
    
    def _get_player_units(self, session, player_id: int) -> Dict[str, int]:
        """Get player unit counts"""
        units = session.query(PlayerUnit).filter_by(player_id=player_id).all()
        return {unit.unit_type: unit.quantity for unit in units}
    
    def _check_level_up(self, session, player: Player):
        """Check if player should level up"""
        required_exp = player.level * 1000  # Simple level formula
        
        if player.experience >= required_exp:
            player.level += 1
            player.experience -= required_exp
            
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
    
    def generate_daily_quests(self):
        """Generate new daily quests"""
        with self.db.get_session() as session:
            # Generate 5 random quests of each type
            for quest_type in self.quest_templates.keys():
                for _ in range(5):
                    quest = self.generate_random_quest(quest_type)
                    if quest:
                        # Check if similar quest already exists
                        existing = session.query(Quest).filter_by(
                            title=quest.title,
                            quest_type=quest.quest_type
                        ).first()
                        
                        if not existing:
                            session.add(quest)
            
            session.commit()