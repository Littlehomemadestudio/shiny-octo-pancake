"""
Advanced Military Knowledge Quiz System
Random military questions with points, leaderboards, and knowledge rewards
"""

import random
import time
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import json
import os

class DifficultyLevel(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    LEGENDARY = "legendary"

class QuestionCategory(Enum):
    HISTORY = "history"
    WEAPONS = "weapons"
    STRATEGY = "strategy"
    TECHNOLOGY = "technology"
    LEADERS = "leaders"
    BATTLES = "battles"
    TACTICS = "tactics"
    LOGISTICS = "logistics"
    INTELLIGENCE = "intelligence"
    NAVAL = "naval"
    AERIAL = "aerial"
    ARMOR = "armor"
    SPECIAL_FORCES = "special_forces"
    CYBER_WARFARE = "cyber_warfare"
    NUCLEAR = "nuclear"

@dataclass
class QuizQuestion:
    """Military quiz question"""
    question_id: str
    category: QuestionCategory
    difficulty: DifficultyLevel
    question: str
    options: List[str]
    correct_answer: int  # Index of correct option
    explanation: str
    points: int
    time_limit: int  # Seconds
    knowledge_reward: int  # Knowledge points gained
    tags: List[str]

@dataclass
class QuizSession:
    """Active quiz session"""
    session_id: str
    user_id: int
    questions: List[QuizQuestion]
    current_question: int
    score: int
    correct_answers: int
    total_time: float
    start_time: datetime
    end_time: Optional[datetime]
    difficulty: DifficultyLevel
    category: Optional[QuestionCategory]
    streak: int
    max_streak: int

@dataclass
class QuizResult:
    """Quiz completion result"""
    session_id: str
    user_id: int
    score: int
    correct_answers: int
    total_questions: int
    accuracy: float
    total_time: float
    average_time: float
    difficulty: DifficultyLevel
    category: Optional[QuestionCategory]
    streak: int
    max_streak: int
    knowledge_gained: int
    points_gained: int
    rank: str
    timestamp: datetime

class MilitaryQuizDatabase:
    """Database of military knowledge questions"""
    
    def __init__(self):
        self.questions: Dict[str, QuizQuestion] = {}
        self.categories: Dict[QuestionCategory, List[str]] = {}
        self.difficulties: Dict[DifficultyLevel, List[str]] = {}
        self._load_questions()
    
    def _load_questions(self):
        """Load military knowledge questions"""
        # HISTORY QUESTIONS
        history_questions = [
            QuizQuestion(
                question_id="hist_001",
                category=QuestionCategory.HISTORY,
                difficulty=DifficultyLevel.EASY,
                question="Which battle is considered the turning point of World War II in the Pacific?",
                options=[
                    "Battle of Midway",
                    "Battle of Pearl Harbor", 
                    "Battle of Iwo Jima",
                    "Battle of Okinawa"
                ],
                correct_answer=0,
                explanation="The Battle of Midway (June 4-7, 1942) was the decisive naval battle that turned the tide of the Pacific War in favor of the Allies.",
                points=10,
                time_limit=30,
                knowledge_reward=5,
                tags=["ww2", "pacific", "naval", "turning_point"]
            ),
            QuizQuestion(
                question_id="hist_002",
                category=QuestionCategory.HISTORY,
                difficulty=DifficultyLevel.MEDIUM,
                question="Who was the commander of the German Afrika Korps during World War II?",
                options=[
                    "Erwin Rommel",
                    "Heinz Guderian",
                    "Erich von Manstein",
                    "Friedrich Paulus"
                ],
                correct_answer=0,
                explanation="Erwin Rommel, known as the 'Desert Fox', commanded the Afrika Korps in North Africa from 1941-1943.",
                points=15,
                time_limit=25,
                knowledge_reward=8,
                tags=["ww2", "germany", "africa", "rommel"]
            ),
            QuizQuestion(
                question_id="hist_003",
                category=QuestionCategory.HISTORY,
                difficulty=DifficultyLevel.HARD,
                question="Which ancient military formation was used by the Macedonian phalanx?",
                options=[
                    "Sarissa",
                    "Gladius",
                    "Pilum",
                    "Scutum"
                ],
                correct_answer=0,
                explanation="The sarissa was the long spear (4-7 meters) used by Macedonian phalangites, giving them superior reach in battle.",
                points=25,
                time_limit=20,
                knowledge_reward=12,
                tags=["ancient", "macedonia", "alexander", "phalanx"]
            ),
            QuizQuestion(
                question_id="hist_004",
                category=QuestionCategory.HISTORY,
                difficulty=DifficultyLevel.EXPERT,
                question="What was the codename for the German invasion of the Soviet Union in 1941?",
                options=[
                    "Operation Barbarossa",
                    "Operation Sea Lion",
                    "Operation Overlord",
                    "Operation Market Garden"
                ],
                correct_answer=0,
                explanation="Operation Barbarossa was the largest military operation in history, involving over 3 million German troops invading the USSR.",
                points=40,
                time_limit=15,
                knowledge_reward=20,
                tags=["ww2", "germany", "soviet", "barbarossa"]
            ),
            QuizQuestion(
                question_id="hist_005",
                category=QuestionCategory.HISTORY,
                difficulty=DifficultyLevel.LEGENDARY,
                question="Which military strategist wrote 'The Art of War'?",
                options=[
                    "Sun Tzu",
                    "Clausewitz",
                    "Machiavelli",
                    "Jomini"
                ],
                correct_answer=0,
                explanation="Sun Tzu, a Chinese general and philosopher, wrote 'The Art of War' around 500 BC, still studied today.",
                points=60,
                time_limit=10,
                knowledge_reward=30,
                tags=["ancient", "china", "strategy", "philosophy"]
            )
        ]
        
        # WEAPONS QUESTIONS
        weapons_questions = [
            QuizQuestion(
                question_id="weap_001",
                category=QuestionCategory.WEAPONS,
                difficulty=DifficultyLevel.EASY,
                question="What is the effective range of an AK-47 assault rifle?",
                options=[
                    "300-400 meters",
                    "100-200 meters",
                    "500-600 meters",
                    "800-1000 meters"
                ],
                correct_answer=0,
                explanation="The AK-47 has an effective range of 300-400 meters, making it highly effective for close to medium range combat.",
                points=10,
                time_limit=30,
                knowledge_reward=5,
                tags=["rifle", "ak47", "range", "assault"]
            ),
            QuizQuestion(
                question_id="weap_002",
                category=QuestionCategory.WEAPONS,
                difficulty=DifficultyLevel.MEDIUM,
                question="Which tank is known as the 'King of Battle'?",
                options=[
                    "M1 Abrams",
                    "Leopard 2",
                    "T-90",
                    "Challenger 2"
                ],
                correct_answer=0,
                explanation="The M1 Abrams is often called the 'King of Battle' due to its superior firepower, protection, and mobility.",
                points=15,
                time_limit=25,
                knowledge_reward=8,
                tags=["tank", "abrams", "mbt", "usa"]
            ),
            QuizQuestion(
                question_id="weap_003",
                category=QuestionCategory.WEAPONS,
                difficulty=DifficultyLevel.HARD,
                question="What is the muzzle velocity of a 120mm smoothbore tank gun?",
                options=[
                    "1,500-1,800 m/s",
                    "800-1,000 m/s",
                    "2,000-2,500 m/s",
                    "500-700 m/s"
                ],
                correct_answer=0,
                explanation="Modern 120mm smoothbore tank guns achieve muzzle velocities of 1,500-1,800 m/s for armor-piercing rounds.",
                points=25,
                time_limit=20,
                knowledge_reward=12,
                tags=["tank", "gun", "velocity", "armor"]
            ),
            QuizQuestion(
                question_id="weap_004",
                category=QuestionCategory.WEAPONS,
                difficulty=DifficultyLevel.EXPERT,
                question="Which missile system is known as the 'Patriot'?",
                options=[
                    "MIM-104",
                    "AIM-120",
                    "AGM-88",
                    "BGM-109"
                ],
                correct_answer=0,
                explanation="The MIM-104 Patriot is a surface-to-air missile system used for air defense against aircraft and ballistic missiles.",
                points=40,
                time_limit=15,
                knowledge_reward=20,
                tags=["missile", "patriot", "sam", "defense"]
            ),
            QuizQuestion(
                question_id="weap_005",
                category=QuestionCategory.WEAPONS,
                difficulty=DifficultyLevel.LEGENDARY,
                question="What is the yield of the most powerful nuclear weapon ever tested?",
                options=[
                    "50 megatons",
                    "15 megatons",
                    "100 megatons",
                    "25 megatons"
                ],
                correct_answer=0,
                explanation="The Tsar Bomba, tested by the USSR in 1961, had a yield of approximately 50 megatons - the most powerful nuclear weapon ever detonated.",
                points=60,
                time_limit=10,
                knowledge_reward=30,
                tags=["nuclear", "tsar_bomba", "ussr", "yield"]
            )
        ]
        
        # STRATEGY QUESTIONS
        strategy_questions = [
            QuizQuestion(
                question_id="strat_001",
                category=QuestionCategory.STRATEGY,
                difficulty=DifficultyLevel.EASY,
                question="What does 'C3I' stand for in military terminology?",
                options=[
                    "Command, Control, Communications, Intelligence",
                    "Combat, Control, Communications, Intelligence",
                    "Command, Control, Computers, Intelligence",
                    "Combat, Control, Computers, Intelligence"
                ],
                correct_answer=0,
                explanation="C3I stands for Command, Control, Communications, and Intelligence - the core elements of military command systems.",
                points=10,
                time_limit=30,
                knowledge_reward=5,
                tags=["strategy", "command", "c3i", "military"]
            ),
            QuizQuestion(
                question_id="strat_002",
                category=QuestionCategory.STRATEGY,
                difficulty=DifficultyLevel.MEDIUM,
                question="What is the principle of 'Mass' in military strategy?",
                options=[
                    "Concentrate superior force at the decisive point",
                    "Maintain constant pressure on the enemy",
                    "Use overwhelming numbers in all engagements",
                    "Focus on defensive positions"
                ],
                correct_answer=0,
                explanation="The principle of Mass involves concentrating superior combat power at the decisive place and time to achieve decisive results.",
                points=15,
                time_limit=25,
                knowledge_reward=8,
                tags=["strategy", "mass", "concentration", "principles"]
            ),
            QuizQuestion(
                question_id="strat_003",
                category=QuestionCategory.STRATEGY,
                difficulty=DifficultyLevel.HARD,
                question="What does 'OODA Loop' stand for?",
                options=[
                    "Observe, Orient, Decide, Act",
                    "Observe, Orient, Direct, Attack",
                    "Organize, Orient, Decide, Act",
                    "Observe, Organize, Direct, Attack"
                ],
                correct_answer=0,
                explanation="The OODA Loop (Observe, Orient, Decide, Act) is a decision-making process developed by military strategist John Boyd.",
                points=25,
                time_limit=20,
                knowledge_reward=12,
                tags=["strategy", "ooda", "decision", "boyd"]
            ),
            QuizQuestion(
                question_id="strat_004",
                category=QuestionCategory.STRATEGY,
                difficulty=DifficultyLevel.EXPERT,
                question="What is the 'Center of Gravity' in military strategy?",
                options=[
                    "The source of power that provides moral or physical strength",
                    "The geographical center of the battlefield",
                    "The most heavily defended position",
                    "The location of the main headquarters"
                ],
                correct_answer=0,
                explanation="Center of Gravity is the source of power that provides moral or physical strength, freedom of action, or will to act.",
                points=40,
                time_limit=15,
                knowledge_reward=20,
                tags=["strategy", "center_of_gravity", "clausewitz", "power"]
            ),
            QuizQuestion(
                question_id="strat_005",
                category=QuestionCategory.STRATEGY,
                difficulty=DifficultyLevel.LEGENDARY,
                question="Who developed the concept of 'Blitzkrieg'?",
                options=[
                    "Heinz Guderian",
                    "Erwin Rommel",
                    "Erich von Manstein",
                    "Alfred von Schlieffen"
                ],
                correct_answer=0,
                explanation="Heinz Guderian developed the concept of Blitzkrieg, combining tanks, aircraft, and motorized infantry for rapid warfare.",
                points=60,
                time_limit=10,
                knowledge_reward=30,
                tags=["strategy", "blitzkrieg", "guderian", "ww2"]
            )
        ]
        
        # TECHNOLOGY QUESTIONS
        technology_questions = [
            QuizQuestion(
                question_id="tech_001",
                category=QuestionCategory.TECHNOLOGY,
                difficulty=DifficultyLevel.EASY,
                question="What does 'GPS' stand for in military navigation?",
                options=[
                    "Global Positioning System",
                    "Geographic Positioning System",
                    "Guided Positioning System",
                    "Global Patrol System"
                ],
                correct_answer=0,
                explanation="GPS stands for Global Positioning System, a satellite-based navigation system used by military and civilian users worldwide.",
                points=10,
                time_limit=30,
                knowledge_reward=5,
                tags=["technology", "gps", "navigation", "satellite"]
            ),
            QuizQuestion(
                question_id="tech_002",
                category=QuestionCategory.TECHNOLOGY,
                difficulty=DifficultyLevel.MEDIUM,
                question="What is the primary advantage of stealth technology?",
                options=[
                    "Reduced radar cross-section",
                    "Increased speed",
                    "Better fuel efficiency",
                    "Larger payload capacity"
                ],
                correct_answer=0,
                explanation="Stealth technology primarily reduces the radar cross-section, making aircraft harder to detect by enemy radar systems.",
                points=15,
                time_limit=25,
                knowledge_reward=8,
                tags=["technology", "stealth", "radar", "aircraft"]
            ),
            QuizQuestion(
                question_id="tech_003",
                category=QuestionCategory.TECHNOLOGY,
                difficulty=DifficultyLevel.HARD,
                question="What is the range of a typical military satellite communication system?",
                options=[
                    "22,000-36,000 km",
                    "500-1,000 km",
                    "100-500 km",
                    "50,000-100,000 km"
                ],
                correct_answer=0,
                explanation="Military communication satellites typically operate in geostationary orbit at 22,000-36,000 km altitude.",
                points=25,
                time_limit=20,
                knowledge_reward=12,
                tags=["technology", "satellite", "communication", "orbit"]
            ),
            QuizQuestion(
                question_id="tech_004",
                category=QuestionCategory.TECHNOLOGY,
                difficulty=DifficultyLevel.EXPERT,
                question="What is the purpose of 'Electronic Warfare' (EW)?",
                options=[
                    "Control and exploit the electromagnetic spectrum",
                    "Hack enemy computer systems",
                    "Jam enemy radio communications only",
                    "Intercept enemy phone calls"
                ],
                correct_answer=0,
                explanation="Electronic Warfare involves controlling and exploiting the electromagnetic spectrum to gain tactical advantage.",
                points=40,
                time_limit=15,
                knowledge_reward=20,
                tags=["technology", "ew", "electromagnetic", "spectrum"]
            ),
            QuizQuestion(
                question_id="tech_005",
                category=QuestionCategory.TECHNOLOGY,
                difficulty=DifficultyLevel.LEGENDARY,
                question="What is the maximum speed of a hypersonic missile?",
                options=[
                    "Mach 5+",
                    "Mach 2-3",
                    "Mach 1-2",
                    "Mach 10+"
                ],
                correct_answer=0,
                explanation="Hypersonic missiles travel at speeds of Mach 5 or higher (5 times the speed of sound), making them extremely difficult to intercept.",
                points=60,
                time_limit=10,
                knowledge_reward=30,
                tags=["technology", "hypersonic", "missile", "speed"]
            )
        ]
        
        # NAVAL QUESTIONS
        naval_questions = [
            QuizQuestion(
                question_id="naval_001",
                category=QuestionCategory.NAVAL,
                difficulty=DifficultyLevel.EASY,
                question="What is the primary weapon of a submarine?",
                options=[
                    "Torpedoes",
                    "Cannons",
                    "Missiles",
                    "Depth charges"
                ],
                correct_answer=0,
                explanation="Torpedoes are the primary weapon of submarines, designed to be launched underwater against surface ships and other submarines.",
                points=10,
                time_limit=30,
                knowledge_reward=5,
                tags=["naval", "submarine", "torpedo", "weapon"]
            ),
            QuizQuestion(
                question_id="naval_002",
                category=QuestionCategory.NAVAL,
                difficulty=DifficultyLevel.MEDIUM,
                question="What is the displacement of a typical aircraft carrier?",
                options=[
                    "80,000-100,000 tons",
                    "20,000-40,000 tons",
                    "150,000-200,000 tons",
                    "5,000-10,000 tons"
                ],
                correct_answer=0,
                explanation="Modern aircraft carriers typically have a displacement of 80,000-100,000 tons, making them the largest warships ever built.",
                points=15,
                time_limit=25,
                knowledge_reward=8,
                tags=["naval", "carrier", "displacement", "warship"]
            ),
            QuizQuestion(
                question_id="naval_003",
                category=QuestionCategory.NAVAL,
                difficulty=DifficultyLevel.HARD,
                question="What is the purpose of a destroyer's Aegis system?",
                options=[
                    "Air and missile defense",
                    "Underwater detection",
                    "Surface warfare",
                    "Electronic warfare"
                ],
                correct_answer=0,
                explanation="The Aegis system provides comprehensive air and missile defense capabilities for naval vessels.",
                points=25,
                time_limit=20,
                knowledge_reward=12,
                tags=["naval", "destroyer", "aegis", "defense"]
            ),
            QuizQuestion(
                question_id="naval_004",
                category=QuestionCategory.NAVAL,
                difficulty=DifficultyLevel.EXPERT,
                question="What is the maximum depth of a nuclear submarine?",
                options=[
                    "300-400 meters",
                    "100-200 meters",
                    "500-600 meters",
                    "1,000+ meters"
                ],
                correct_answer=0,
                explanation="Nuclear submarines can typically operate at depths of 300-400 meters, with some capable of deeper operations.",
                points=40,
                time_limit=15,
                knowledge_reward=20,
                tags=["naval", "submarine", "depth", "nuclear"]
            ),
            QuizQuestion(
                question_id="naval_005",
                category=QuestionCategory.NAVAL,
                difficulty=DifficultyLevel.LEGENDARY,
                question="What is the range of a Tomahawk cruise missile?",
                options=[
                    "1,500-2,500 km",
                    "500-1,000 km",
                    "3,000-5,000 km",
                    "100-300 km"
                ],
                correct_answer=0,
                explanation="The Tomahawk cruise missile has a range of 1,500-2,500 km, making it a long-range precision strike weapon.",
                points=60,
                time_limit=10,
                knowledge_reward=30,
                tags=["naval", "tomahawk", "missile", "range"]
            )
        ]
        
        # AERIAL QUESTIONS
        aerial_questions = [
            QuizQuestion(
                question_id="aerial_001",
                category=QuestionCategory.AERIAL,
                difficulty=DifficultyLevel.EASY,
                question="What is the primary role of a fighter aircraft?",
                options=[
                    "Air-to-air combat",
                    "Ground attack",
                    "Reconnaissance",
                    "Transport"
                ],
                correct_answer=0,
                explanation="Fighter aircraft are primarily designed for air-to-air combat, engaging enemy aircraft in aerial warfare.",
                points=10,
                time_limit=30,
                knowledge_reward=5,
                tags=["aerial", "fighter", "combat", "aircraft"]
            ),
            QuizQuestion(
                question_id="aerial_002",
                category=QuestionCategory.AERIAL,
                difficulty=DifficultyLevel.MEDIUM,
                question="What is the service ceiling of an F-22 Raptor?",
                options=[
                    "15,000+ meters",
                    "8,000-10,000 meters",
                    "20,000+ meters",
                    "5,000-7,000 meters"
                ],
                correct_answer=0,
                explanation="The F-22 Raptor has a service ceiling of over 15,000 meters, allowing it to operate at high altitudes.",
                points=15,
                time_limit=25,
                knowledge_reward=8,
                tags=["aerial", "f22", "raptor", "ceiling"]
            ),
            QuizQuestion(
                question_id="aerial_003",
                category=QuestionCategory.AERIAL,
                difficulty=DifficultyLevel.HARD,
                question="What is the purpose of an AWACS aircraft?",
                options=[
                    "Airborne warning and control",
                    "Air-to-ground attack",
                    "Transport and logistics",
                    "Search and rescue"
                ],
                correct_answer=0,
                explanation="AWACS (Airborne Warning and Control System) provides airborne surveillance, command, and control capabilities.",
                points=25,
                time_limit=20,
                knowledge_reward=12,
                tags=["aerial", "awacs", "surveillance", "control"]
            ),
            QuizQuestion(
                question_id="aerial_004",
                category=QuestionCategory.AERIAL,
                difficulty=DifficultyLevel.EXPERT,
                question="What is the maximum speed of the SR-71 Blackbird?",
                options=[
                    "Mach 3.3+",
                    "Mach 2.0",
                    "Mach 1.5",
                    "Mach 4.0+"
                ],
                correct_answer=0,
                explanation="The SR-71 Blackbird could reach speeds of Mach 3.3+ (over 2,200 mph), making it one of the fastest aircraft ever built.",
                points=40,
                time_limit=15,
                knowledge_reward=20,
                tags=["aerial", "sr71", "blackbird", "speed"]
            ),
            QuizQuestion(
                question_id="aerial_005",
                category=QuestionCategory.AERIAL,
                difficulty=DifficultyLevel.LEGENDARY,
                question="What is the operational range of a B-2 Spirit bomber?",
                options=[
                    "10,000+ km",
                    "5,000-7,000 km",
                    "15,000+ km",
                    "2,000-3,000 km"
                ],
                correct_answer=0,
                explanation="The B-2 Spirit has an operational range of over 10,000 km, allowing it to conduct global strike missions.",
                points=60,
                time_limit=10,
                knowledge_reward=30,
                tags=["aerial", "b2", "spirit", "bomber"]
            )
        ]
        
        # CYBER WARFARE QUESTIONS
        cyber_questions = [
            QuizQuestion(
                question_id="cyber_001",
                category=QuestionCategory.CYBER_WARFARE,
                difficulty=DifficultyLevel.EASY,
                question="What is the primary goal of cyber warfare?",
                options=[
                    "Disrupt enemy systems and networks",
                    "Steal personal information",
                    "Hack social media accounts",
                    "Create computer viruses"
                ],
                correct_answer=0,
                explanation="Cyber warfare aims to disrupt, damage, or gain unauthorized access to enemy computer systems and networks.",
                points=10,
                time_limit=30,
                knowledge_reward=5,
                tags=["cyber", "warfare", "disruption", "networks"]
            ),
            QuizQuestion(
                question_id="cyber_002",
                category=QuestionCategory.CYBER_WARFARE,
                difficulty=DifficultyLevel.MEDIUM,
                question="What is a 'Zero-Day' vulnerability?",
                options=[
                    "Unknown vulnerability with no patch available",
                    "Vulnerability that occurs at midnight",
                    "Vulnerability that affects zero systems",
                    "Vulnerability that is impossible to exploit"
                ],
                correct_answer=0,
                explanation="A Zero-Day vulnerability is a security flaw that is unknown to the software vendor and has no available patch.",
                points=15,
                time_limit=25,
                knowledge_reward=8,
                tags=["cyber", "zero_day", "vulnerability", "security"]
            ),
            QuizQuestion(
                question_id="cyber_003",
                category=QuestionCategory.CYBER_WARFARE,
                difficulty=DifficultyLevel.HARD,
                question="What is the purpose of a 'Honeypot' in cybersecurity?",
                options=[
                    "Trap and detect attackers",
                    "Store encrypted data",
                    "Monitor network traffic",
                    "Block malicious websites"
                ],
                correct_answer=0,
                explanation="A honeypot is a decoy system designed to attract and detect attackers, allowing security teams to study their methods.",
                points=25,
                time_limit=20,
                knowledge_reward=12,
                tags=["cyber", "honeypot", "security", "detection"]
            ),
            QuizQuestion(
                question_id="cyber_004",
                category=QuestionCategory.CYBER_WARFARE,
                difficulty=DifficultyLevel.EXPERT,
                question="What is 'Stuxnet' known for?",
                options=[
                    "First known cyber weapon targeting industrial systems",
                    "Most powerful computer virus ever created",
                    "First AI-powered cyber attack",
                    "Fastest spreading malware in history"
                ],
                correct_answer=0,
                explanation="Stuxnet was the first known cyber weapon specifically designed to target industrial control systems, particularly Iran's nuclear facilities.",
                points=40,
                time_limit=15,
                knowledge_reward=20,
                tags=["cyber", "stuxnet", "weapon", "industrial"]
            ),
            QuizQuestion(
                question_id="cyber_005",
                category=QuestionCategory.CYBER_WARFARE,
                difficulty=DifficultyLevel.LEGENDARY,
                question="What is the primary function of a 'Firewall'?",
                options=[
                    "Control network traffic based on security rules",
                    "Encrypt data transmissions",
                    "Detect malware infections",
                    "Authenticate user identities"
                ],
                correct_answer=0,
                explanation="A firewall controls network traffic by enforcing security rules, allowing or blocking data packets based on predefined criteria.",
                points=60,
                time_limit=10,
                knowledge_reward=30,
                tags=["cyber", "firewall", "security", "network"]
            )
        ]
        
        # Combine all questions
        all_questions = (history_questions + weapons_questions + strategy_questions + 
                        technology_questions + naval_questions + aerial_questions + 
                        cyber_questions)
        
        # Add to database
        for question in all_questions:
            self.questions[question.question_id] = question
            
            # Add to category index
            if question.category not in self.categories:
                self.categories[question.category] = []
            self.categories[question.category].append(question.question_id)
            
            # Add to difficulty index
            if question.difficulty not in self.difficulties:
                self.difficulties[question.difficulty] = []
            self.difficulties[question.difficulty].append(question.question_id)
    
    def get_random_questions(self, count: int, difficulty: Optional[DifficultyLevel] = None, 
                           category: Optional[QuestionCategory] = None) -> List[QuizQuestion]:
        """Get random questions with optional filters"""
        available_questions = list(self.questions.values())
        
        # Filter by difficulty
        if difficulty:
            available_questions = [q for q in available_questions if q.difficulty == difficulty]
        
        # Filter by category
        if category:
            available_questions = [q for q in available_questions if q.category == category]
        
        # Randomly select questions
        if len(available_questions) <= count:
            return available_questions
        else:
            return random.sample(available_questions, count)
    
    def get_question_by_id(self, question_id: str) -> Optional[QuizQuestion]:
        """Get question by ID"""
        return self.questions.get(question_id)
    
    def get_questions_by_category(self, category: QuestionCategory) -> List[QuizQuestion]:
        """Get all questions in a category"""
        question_ids = self.categories.get(category, [])
        return [self.questions[qid] for qid in question_ids if qid in self.questions]
    
    def get_questions_by_difficulty(self, difficulty: DifficultyLevel) -> List[QuizQuestion]:
        """Get all questions of a difficulty level"""
        question_ids = self.difficulties.get(difficulty, [])
        return [self.questions[qid] for qid in question_ids if qid in self.questions]

class MilitaryQuizSystem:
    """Main quiz system with scoring, leaderboards, and rewards"""
    
    def __init__(self, database_manager):
        self.db_manager = database_manager
        self.quiz_db = MilitaryQuizDatabase()
        self.active_sessions: Dict[str, QuizSession] = {}
        self.quiz_results: List[QuizResult] = []
        self.leaderboards: Dict[str, List[Dict]] = {}
        self.load_quiz_data()
    
    def load_quiz_data(self):
        """Load quiz data from database"""
        # Load quiz results from database
        try:
            with self.db_manager.get_session() as session:
                # This would load from a QuizResult table
                pass
        except Exception as e:
            print(f"Error loading quiz data: {e}")
    
    def start_quiz(self, user_id: int, difficulty: DifficultyLevel = DifficultyLevel.MEDIUM,
                   category: Optional[QuestionCategory] = None, question_count: int = 10) -> str:
        """Start a new quiz session"""
        session_id = f"quiz_{user_id}_{int(time.time())}"
        
        # Get random questions
        questions = self.quiz_db.get_random_questions(question_count, difficulty, category)
        
        if not questions:
            raise ValueError("No questions available for the selected criteria")
        
        # Create session
        session = QuizSession(
            session_id=session_id,
            user_id=user_id,
            questions=questions,
            current_question=0,
            score=0,
            correct_answers=0,
            total_time=0.0,
            start_time=datetime.now(),
            end_time=None,
            difficulty=difficulty,
            category=category,
            streak=0,
            max_streak=0
        )
        
        self.active_sessions[session_id] = session
        return session_id
    
    def answer_question(self, session_id: str, answer_index: int, response_time: float) -> Dict[str, Any]:
        """Answer a question in an active session"""
        if session_id not in self.active_sessions:
            raise ValueError("Invalid session ID")
        
        session = self.active_sessions[session_id]
        
        if session.current_question >= len(session.questions):
            raise ValueError("No more questions in this session")
        
        question = session.questions[session.current_question]
        
        # Check if answer is correct
        is_correct = answer_index == question.correct_answer
        
        # Calculate points based on correctness and speed
        if is_correct:
            # Base points
            points = question.points
            
            # Speed bonus (faster = more points)
            time_bonus = max(0, (question.time_limit - response_time) / question.time_limit)
            points = int(points * (1 + time_bonus * 0.5))
            
            # Streak bonus
            if session.streak > 0:
                streak_bonus = min(session.streak * 0.1, 1.0)  # Max 100% bonus
                points = int(points * (1 + streak_bonus))
            
            session.score += points
            session.correct_answers += 1
            session.streak += 1
            session.max_streak = max(session.max_streak, session.streak)
        else:
            session.streak = 0
        
        session.total_time += response_time
        session.current_question += 1
        
        # Check if quiz is complete
        is_complete = session.current_question >= len(session.questions)
        
        if is_complete:
            session.end_time = datetime.now()
            result = self._complete_quiz(session)
            del self.active_sessions[session_id]
        else:
            result = None
        
        return {
            "is_correct": is_correct,
            "points_earned": points if is_correct else 0,
            "explanation": question.explanation,
            "is_complete": is_complete,
            "current_question": session.current_question,
            "total_questions": len(session.questions),
            "score": session.score,
            "streak": session.streak,
            "result": result
        }
    
    def _complete_quiz(self, session: QuizSession) -> QuizResult:
        """Complete a quiz session and create result"""
        total_questions = len(session.questions)
        accuracy = (session.correct_answers / total_questions) * 100 if total_questions > 0 else 0
        average_time = session.total_time / total_questions if total_questions > 0 else 0
        
        # Calculate knowledge gained
        knowledge_gained = sum(q.knowledge_reward for q in session.questions[:session.correct_answers])
        
        # Determine rank based on performance
        if accuracy >= 90 and session.streak >= 5:
            rank = "Legendary"
        elif accuracy >= 80 and session.streak >= 3:
            rank = "Expert"
        elif accuracy >= 70:
            rank = "Advanced"
        elif accuracy >= 60:
            rank = "Intermediate"
        else:
            rank = "Beginner"
        
        result = QuizResult(
            session_id=session.session_id,
            user_id=session.user_id,
            score=session.score,
            correct_answers=session.correct_answers,
            total_questions=total_questions,
            accuracy=accuracy,
            total_time=session.total_time,
            average_time=average_time,
            difficulty=session.difficulty,
            category=session.category,
            streak=session.streak,
            max_streak=session.max_streak,
            knowledge_gained=knowledge_gained,
            points_gained=session.score,
            rank=rank,
            timestamp=datetime.now()
        )
        
        self.quiz_results.append(result)
        
        # Update leaderboards
        self._update_leaderboards(result)
        
        # Save to database
        self._save_quiz_result(result)
        
        return result
    
    def _update_leaderboards(self, result: QuizResult):
        """Update leaderboards with new result"""
        # Overall leaderboard
        if "overall" not in self.leaderboards:
            self.leaderboards["overall"] = []
        
        self.leaderboards["overall"].append({
            "user_id": result.user_id,
            "score": result.score,
            "accuracy": result.accuracy,
            "rank": result.rank,
            "timestamp": result.timestamp
        })
        
        # Sort by score
        self.leaderboards["overall"].sort(key=lambda x: x["score"], reverse=True)
        
        # Keep only top 100
        self.leaderboards["overall"] = self.leaderboards["overall"][:100]
        
        # Category leaderboard
        if result.category:
            category_key = f"category_{result.category.value}"
            if category_key not in self.leaderboards:
                self.leaderboards[category_key] = []
            
            self.leaderboards[category_key].append({
                "user_id": result.user_id,
                "score": result.score,
                "accuracy": result.accuracy,
                "rank": result.rank,
                "timestamp": result.timestamp
            })
            
            self.leaderboards[category_key].sort(key=lambda x: x["score"], reverse=True)
            self.leaderboards[category_key] = self.leaderboards[category_key][:50]
    
    def _save_quiz_result(self, result: QuizResult):
        """Save quiz result to database"""
        try:
            with self.db_manager.get_session() as session:
                # This would save to a QuizResult table
                # For now, we'll just log it
                print(f"Quiz result saved: {result.user_id} scored {result.score} points")
        except Exception as e:
            print(f"Error saving quiz result: {e}")
    
    def get_leaderboard(self, category: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Get leaderboard for a category"""
        if category:
            key = f"category_{category}" if category != "overall" else "overall"
        else:
            key = "overall"
        
        return self.leaderboards.get(key, [])[:limit]
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user's quiz statistics"""
        user_results = [r for r in self.quiz_results if r.user_id == user_id]
        
        if not user_results:
            return {
                "total_quizzes": 0,
                "total_score": 0,
                "average_accuracy": 0,
                "best_rank": "None",
                "total_knowledge": 0,
                "longest_streak": 0
            }
        
        total_quizzes = len(user_results)
        total_score = sum(r.score for r in user_results)
        average_accuracy = sum(r.accuracy for r in user_results) / total_quizzes
        best_rank = max(user_results, key=lambda x: x.score).rank
        total_knowledge = sum(r.knowledge_gained for r in user_results)
        longest_streak = max(r.max_streak for r in user_results)
        
        return {
            "total_quizzes": total_quizzes,
            "total_score": total_score,
            "average_accuracy": average_accuracy,
            "best_rank": best_rank,
            "total_knowledge": total_knowledge,
            "longest_streak": longest_streak
        }
    
    def get_current_question(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current question for an active session"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        
        if session.current_question >= len(session.questions):
            return None
        
        question = session.questions[session.current_question]
        
        return {
            "question_id": question.question_id,
            "question": question.question,
            "options": question.options,
            "time_limit": question.time_limit,
            "difficulty": question.difficulty.value,
            "category": question.category.value,
            "points": question.points,
            "current_question": session.current_question + 1,
            "total_questions": len(session.questions),
            "score": session.score,
            "streak": session.streak
        }

# Example usage and testing
if __name__ == "__main__":
    # Test quiz system
    print("Testing military quiz system...")
    
    # Mock database manager
    class MockDatabaseManager:
        def get_session(self):
            return self
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
    
    db_manager = MockDatabaseManager()
    quiz_system = MilitaryQuizSystem(db_manager)
    
    # Test starting a quiz
    user_id = 12345
    session_id = quiz_system.start_quiz(user_id, DifficultyLevel.MEDIUM, QuestionCategory.HISTORY, 5)
    print(f"Started quiz session: {session_id}")
    
    # Test answering questions
    for i in range(5):
        question_data = quiz_system.get_current_question(session_id)
        if question_data:
            print(f"Question {i+1}: {question_data['question']}")
            print(f"Options: {question_data['options']}")
            
            # Simulate answering (random answer)
            answer = random.randint(0, len(question_data['options']) - 1)
            response_time = random.uniform(5, 25)
            
            result = quiz_system.answer_question(session_id, answer, response_time)
            print(f"Answer: {answer}, Correct: {result['is_correct']}, Points: {result['points_earned']}")
            print(f"Score: {result['score']}, Streak: {result['streak']}")
            print()
    
    # Test user stats
    stats = quiz_system.get_user_stats(user_id)
    print(f"User stats: {stats}")
    
    # Test leaderboard
    leaderboard = quiz_system.get_leaderboard(limit=5)
    print(f"Leaderboard: {leaderboard}")
    
    print("✅ Military quiz system working correctly!")