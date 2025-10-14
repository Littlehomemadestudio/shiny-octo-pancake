"""
Database models and configuration for World War Telegram Bot
"""
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    rank = Column(String(50), default="Commander")
    gold = Column(Float, default=1000.0)
    morale = Column(Float, default=100.0)
    last_active = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_banned = Column(Boolean, default=False)
    language = Column(String(10), default="en")
    
    # Relationships
    nation_id = Column(Integer, ForeignKey("nations.id"))
    nation = relationship("Nation", back_populates="players")
    
    materials = relationship("PlayerMaterial", back_populates="player")
    units = relationship("PlayerUnit", back_populates="player")
    quests = relationship("PlayerQuest", back_populates="player")
    trades = relationship("Trade", foreign_keys="[Trade.seller_id]", back_populates="seller")
    trades_received = relationship("Trade", foreign_keys="[Trade.buyer_id]", back_populates="buyer")

class Nation(Base):
    __tablename__ = "nations"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    flag_emoji = Column(String(10), default="🏴")
    color = Column(String(7), default="#000000")
    government_type = Column(String(50), default="Democracy")
    population = Column(Integer, default=1000000)
    gdp = Column(Float, default=1000000.0)
    tax_rate = Column(Float, default=0.1)
    research_points = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_ai = Column(Boolean, default=False)
    
    # Relationships
    players = relationship("Player", back_populates="nation")
    provinces = relationship("Province", back_populates="owner")
    alliances = relationship("Alliance", foreign_keys="[Alliance.nation1_id]", back_populates="nation1")
    alliances_received = relationship("Alliance", foreign_keys="[Alliance.nation2_id]", back_populates="nation2")
    technologies = relationship("NationTechnology", back_populates="nation")

class Province(Base):
    __tablename__ = "provinces"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    population = Column(Integer, default=100000)
    infrastructure = Column(Float, default=1.0)
    defense_level = Column(Integer, default=0)
    morale = Column(Float, default=100.0)
    weather = Column(String(50), default="clear")
    temperature = Column(Float, default=20.0)
    owner_id = Column(Integer, ForeignKey("nations.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Resources
    iron_deposits = Column(Float, default=1000.0)
    oil_deposits = Column(Float, default=500.0)
    food_production = Column(Float, default=200.0)
    gold_mines = Column(Float, default=100.0)
    uranium_deposits = Column(Float, default=50.0)
    
    # Buildings
    buildings = Column(JSON, default=list)
    
    # Relationships
    owner = relationship("Nation", back_populates="provinces")
    units = relationship("PlayerUnit", back_populates="province")

class PlayerMaterial(Base):
    __tablename__ = "player_materials"
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    material_type = Column(String(50), nullable=False)
    quantity = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    player = relationship("Player", back_populates="materials")

class PlayerUnit(Base):
    __tablename__ = "player_units"
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    province_id = Column(Integer, ForeignKey("provinces.id"))
    unit_name = Column(String(100), nullable=False)  # Full name of the unit
    unit_type = Column(String(50), nullable=False)   # Category (infantry, armor, etc.)
    subcategory = Column(String(50), nullable=False) # Subcategory (basic, elite, etc.)
    tier = Column(Integer, default=1)
    quantity = Column(Integer, default=0)
    experience = Column(Float, default=0.0)
    morale = Column(Float, default=100.0)
    fuel = Column(Float, default=100.0)
    ammunition = Column(Float, default=100.0)
    last_supplied = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    player = relationship("Player", back_populates="units")
    province = relationship("Province", back_populates="units")

class Quest(Base):
    __tablename__ = "quests"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    quest_type = Column(String(50), nullable=False)  # recon, sabotage, escort, invasion, research
    difficulty = Column(Integer, default=1)
    duration = Column(Integer, default=3600)  # seconds
    rewards = Column(JSON, default=dict)
    requirements = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    player_quests = relationship("PlayerQuest", back_populates="quest")

class PlayerQuest(Base):
    __tablename__ = "player_quests"
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)
    status = Column(String(50), default="active")  # active, completed, failed, expired
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    progress = Column(Float, default=0.0)
    
    # Relationships
    player = relationship("Player", back_populates="quests")
    quest = relationship("Quest", back_populates="player_quests")

class Technology(Base):
    __tablename__ = "technologies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    tier = Column(Integer, default=1)
    cost = Column(Integer, default=100)
    prerequisites = Column(JSON, default=list)
    effects = Column(JSON, default=dict)
    is_military = Column(Boolean, default=False)
    is_economic = Column(Boolean, default=False)
    is_research = Column(Boolean, default=False)

class NationTechnology(Base):
    __tablename__ = "nation_technologies"
    
    id = Column(Integer, primary_key=True)
    nation_id = Column(Integer, ForeignKey("nations.id"), nullable=False)
    technology_id = Column(Integer, ForeignKey("technologies.id"), nullable=False)
    research_progress = Column(Float, default=0.0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    nation = relationship("Nation", back_populates="technologies")
    technology = relationship("Technology")

class Alliance(Base):
    __tablename__ = "alliances"
    
    id = Column(Integer, primary_key=True)
    nation1_id = Column(Integer, ForeignKey("nations.id"), nullable=False)
    nation2_id = Column(Integer, ForeignKey("nations.id"), nullable=False)
    alliance_type = Column(String(50), default="defense")  # defense, trade, research, military
    status = Column(String(50), default="active")  # active, inactive, broken
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    
    # Relationships
    nation1 = relationship("Nation", foreign_keys=[nation1_id], back_populates="alliances")
    nation2 = relationship("Nation", foreign_keys=[nation2_id], back_populates="alliances_received")

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("players.id"))
    material_type = Column(String(50), nullable=False)
    quantity = Column(Float, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(50), default="open")  # open, completed, cancelled, expired
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    expires_at = Column(DateTime)
    
    # Relationships
    seller = relationship("Player", foreign_keys=[seller_id], back_populates="trades")
    buyer = relationship("Player", foreign_keys=[buyer_id], back_populates="trades_received")

class Battle(Base):
    __tablename__ = "battles"
    
    id = Column(Integer, primary_key=True)
    attacker_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    defender_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    province_id = Column(Integer, ForeignKey("provinces.id"), nullable=False)
    battle_type = Column(String(50), default="attack")  # attack, defense, raid
    status = Column(String(50), default="ongoing")  # ongoing, completed, cancelled
    attacker_units = Column(JSON, default=dict)
    defender_units = Column(JSON, default=dict)
    battle_log = Column(JSON, default=list)
    winner_id = Column(Integer, ForeignKey("players.id"))
    casualties = Column(JSON, default=dict)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    
    # Relationships
    attacker = relationship("Player", foreign_keys=[attacker_id])
    defender = relationship("Player", foreign_keys=[defender_id])
    winner = relationship("Player", foreign_keys=[winner_id])
    province = relationship("Province")

class WorldEvent(Base):
    __tablename__ = "world_events"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    event_type = Column(String(50), nullable=False)  # economic, military, natural, political
    severity = Column(String(50), default="medium")  # low, medium, high, critical
    effects = Column(JSON, default=dict)
    affected_regions = Column(JSON, default=list)
    duration = Column(Integer, default=3600)  # seconds
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class DatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
        
    async def init_database(self):
        """Initialize database with default data"""
        self.create_tables()
        
        with self.get_session() as session:
            # Create default technologies
            default_technologies = [
                Technology(name="Basic Training", description="Improves infantry combat effectiveness", tier=1, cost=100, is_military=True),
                Technology(name="Steel Production", description="Increases iron and steel production", tier=1, cost=150, is_economic=True),
                Technology(name="Advanced Tactics", description="Unlocks new military strategies", tier=2, cost=300, is_military=True),
                Technology(name="Industrial Revolution", description="Massive production boost", tier=2, cost=500, is_economic=True),
                Technology(name="Nuclear Research", description="Unlocks nuclear weapons", tier=3, cost=1000, is_military=True),
            ]
            
            for tech in default_technologies:
                if not session.query(Technology).filter_by(name=tech.name).first():
                    session.add(tech)
            
            # Create default quests
            default_quests = [
                Quest(
                    title="Reconnaissance Mission",
                    description="Scout enemy territory and gather intelligence",
                    quest_type="recon",
                    difficulty=1,
                    duration=1800,
                    rewards={"gold": 200, "experience": 50},
                    requirements={"level": 1}
                ),
                Quest(
                    title="Sabotage Operation",
                    description="Disrupt enemy supply lines",
                    quest_type="sabotage",
                    difficulty=2,
                    duration=3600,
                    rewards={"gold": 500, "experience": 100, "materials": {"iron": 50}},
                    requirements={"level": 3}
                ),
                Quest(
                    title="Escort Convoy",
                    description="Protect valuable cargo from bandits",
                    quest_type="escort",
                    difficulty=1,
                    duration=2400,
                    rewards={"gold": 300, "experience": 75},
                    requirements={"level": 2}
                ),
            ]
            
            for quest in default_quests:
                if not session.query(Quest).filter_by(title=quest.title).first():
                    session.add(quest)
            
            session.commit()