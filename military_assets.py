"""
Comprehensive Military Assets Database for World War Telegram Bot
250+ military units, weapons, and defense systems
"""
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class MilitaryAsset:
    name: str
    category: str
    subcategory: str
    tier: int
    cost: int
    upkeep: int
    attack: int
    defense: int
    speed: int
    range: int
    capacity: int
    fuel_consumption: float
    description: str
    requirements: List[str]
    special_abilities: List[str]
    emoji: str

class MilitaryAssetsDatabase:
    def __init__(self):
        self.assets = self._create_assets_database()
    
    def _create_assets_database(self) -> Dict[str, MilitaryAsset]:
        """Create comprehensive military assets database"""
        assets = {}
        
        # INFANTRY UNITS (50 units)
        infantry_units = [
            # Basic Infantry
            MilitaryAsset("Rifleman", "infantry", "basic", 1, 50, 5, 3, 2, 1, 1, 1, 0.1, "Basic foot soldier with rifle", [], [], "🪖"),
            MilitaryAsset("Grenadier", "infantry", "basic", 1, 75, 7, 4, 2, 1, 2, 1, 0.1, "Infantry with grenade launcher", [], ["explosive"], "💣"),
            MilitaryAsset("Machine Gunner", "infantry", "basic", 1, 100, 10, 5, 3, 1, 2, 1, 0.1, "Heavy machine gun operator", [], ["suppressive_fire"], "🔫"),
            MilitaryAsset("Sniper", "infantry", "basic", 1, 120, 12, 6, 1, 1, 4, 1, 0.1, "Long-range precision shooter", [], ["stealth", "precision"], "🎯"),
            MilitaryAsset("Medic", "infantry", "support", 1, 80, 8, 2, 2, 1, 1, 1, 0.1, "Medical support unit", [], ["healing"], "🏥"),
            
            # Elite Infantry
            MilitaryAsset("Special Forces", "infantry", "elite", 2, 200, 20, 8, 6, 2, 3, 1, 0.2, "Elite special operations unit", ["Basic Training"], ["stealth", "infiltration"], "🕴️"),
            MilitaryAsset("Marine", "infantry", "elite", 2, 180, 18, 7, 5, 2, 2, 1, 0.2, "Amphibious assault specialist", ["Basic Training"], ["amphibious"], "🌊"),
            MilitaryAsset("Paratrooper", "infantry", "elite", 2, 160, 16, 6, 4, 2, 2, 1, 0.2, "Airborne assault unit", ["Basic Training"], ["airdrop"], "🪂"),
            MilitaryAsset("Ranger", "infantry", "elite", 2, 190, 19, 7, 5, 2, 3, 1, 0.2, "Reconnaissance specialist", ["Basic Training"], ["recon", "stealth"], "🔍"),
            MilitaryAsset("Commando", "infantry", "elite", 2, 220, 22, 9, 7, 2, 2, 1, 0.2, "High-skill combat specialist", ["Basic Training"], ["infiltration", "demolition"], "⚔️"),
            
            # Advanced Infantry
            MilitaryAsset("Cyber Warrior", "infantry", "advanced", 3, 300, 30, 6, 8, 2, 2, 1, 0.3, "Electronic warfare specialist", ["Cyber Warfare"], ["hacking", "jamming"], "💻"),
            MilitaryAsset("Exoskeleton Soldier", "infantry", "advanced", 3, 400, 40, 10, 12, 3, 2, 1, 0.4, "Powered exoskeleton infantry", ["Advanced Materials"], ["enhanced_strength"], "🤖"),
            MilitaryAsset("Stealth Operative", "infantry", "advanced", 3, 350, 35, 8, 6, 2, 3, 1, 0.3, "Invisible stealth specialist", ["Stealth Technology"], ["invisibility"], "👻"),
            MilitaryAsset("Psionic Soldier", "infantry", "advanced", 3, 500, 50, 12, 8, 2, 4, 1, 0.5, "Mind-powered combat unit", ["Psionic Research"], ["mind_control", "telekinesis"], "🧠"),
            MilitaryAsset("Nanobot Swarm", "infantry", "advanced", 3, 250, 25, 15, 2, 4, 1, 10, 0.2, "Microscopic combat robots", ["Nanotechnology"], ["swarm", "repair"], "🦠"),
            
            # Support Infantry
            MilitaryAsset("Engineer", "infantry", "support", 1, 90, 9, 3, 3, 1, 1, 1, 0.1, "Construction and repair specialist", [], ["construction", "repair"], "🔧"),
            MilitaryAsset("Radio Operator", "infantry", "support", 1, 70, 7, 2, 2, 1, 5, 1, 0.1, "Communications specialist", [], ["communications"], "📡"),
            MilitaryAsset("Demolition Expert", "infantry", "support", 1, 110, 11, 4, 2, 1, 2, 1, 0.1, "Explosives specialist", [], ["demolition"], "💥"),
            MilitaryAsset("Anti-Tank Infantry", "infantry", "support", 2, 150, 15, 8, 3, 1, 3, 1, 0.2, "Anti-armor specialist", ["Basic Training"], ["anti_armor"], "🚫"),
            MilitaryAsset("Anti-Air Infantry", "infantry", "support", 2, 140, 14, 7, 3, 1, 4, 1, 0.2, "Anti-aircraft specialist", ["Basic Training"], ["anti_air"], "🚁"),
            
            # Specialized Infantry
            MilitaryAsset("Mountain Troops", "infantry", "specialized", 2, 130, 13, 5, 4, 1, 2, 1, 0.2, "High-altitude combat specialist", ["Basic Training"], ["mountain_warfare"], "⛰️"),
            MilitaryAsset("Desert Warriors", "infantry", "specialized", 2, 125, 12, 5, 4, 1, 2, 1, 0.2, "Desert combat specialist", ["Basic Training"], ["desert_warfare"], "🏜️"),
            MilitaryAsset("Arctic Soldiers", "infantry", "specialized", 2, 135, 13, 5, 5, 1, 2, 1, 0.2, "Cold weather specialist", ["Basic Training"], ["arctic_warfare"], "🧊"),
            MilitaryAsset("Urban Assault", "infantry", "specialized", 2, 145, 14, 6, 4, 1, 2, 1, 0.2, "City combat specialist", ["Basic Training"], ["urban_warfare"], "🏙️"),
            MilitaryAsset("Jungle Fighters", "infantry", "specialized", 2, 120, 12, 5, 4, 1, 2, 1, 0.2, "Jungle warfare specialist", ["Basic Training"], ["jungle_warfare"], "🌴"),
            
            # Future Infantry
            MilitaryAsset("Quantum Soldier", "infantry", "future", 4, 800, 80, 20, 15, 4, 5, 1, 0.8, "Quantum-enhanced super soldier", ["Quantum Technology"], ["quantum_shift", "phase"], "⚛️"),
            MilitaryAsset("Bionic Commando", "infantry", "future", 4, 600, 60, 15, 12, 3, 3, 1, 0.6, "Cyborg combat unit", ["Bionics"], ["enhanced_senses", "regeneration"], "🔬"),
            MilitaryAsset("Plasma Trooper", "infantry", "future", 4, 700, 70, 18, 10, 3, 4, 1, 0.7, "Plasma weapon specialist", ["Plasma Technology"], ["plasma_weapons"], "⚡"),
            MilitaryAsset("Gravity Warrior", "infantry", "future", 4, 900, 90, 16, 14, 3, 3, 1, 0.9, "Gravity manipulation specialist", ["Gravity Control"], ["gravity_field", "levitation"], "🌌"),
            MilitaryAsset("Time Dilation Troop", "infantry", "future", 4, 1000, 100, 25, 8, 5, 2, 1, 1.0, "Time manipulation specialist", ["Temporal Technology"], ["time_slow", "precognition"], "⏰"),
        ]
        
        # ARMORED VEHICLES (50 units)
        armored_vehicles = [
            # Light Armor
            MilitaryAsset("Scout Car", "armor", "light", 1, 200, 20, 4, 3, 3, 2, 2, 0.3, "Fast reconnaissance vehicle", [], ["recon"], "🚗"),
            MilitaryAsset("Armored Car", "armor", "light", 1, 300, 30, 6, 5, 3, 2, 2, 0.4, "Lightly armored wheeled vehicle", [], ["fast"], "🚙"),
            MilitaryAsset("Light Tank", "armor", "light", 1, 500, 50, 8, 6, 2, 3, 2, 0.5, "Basic tracked combat vehicle", [], [], "🚗"),
            MilitaryAsset("APC", "armor", "light", 1, 400, 40, 5, 7, 2, 2, 6, 0.4, "Armored personnel carrier", [], ["transport"], "🚐"),
            MilitaryAsset("IFV", "armor", "light", 2, 600, 60, 10, 8, 3, 3, 4, 0.6, "Infantry fighting vehicle", ["Basic Training"], ["transport", "fire_support"], "🚛"),
            
            # Main Battle Tanks
            MilitaryAsset("Main Battle Tank", "armor", "main", 2, 1000, 100, 15, 12, 2, 4, 3, 1.0, "Primary combat tank", ["Armored Warfare"], [], "🚗"),
            MilitaryAsset("Heavy Tank", "armor", "main", 2, 1200, 120, 18, 15, 1, 4, 3, 1.2, "Heavily armored tank", ["Armored Warfare"], ["armor_piercing"], "🚗"),
            MilitaryAsset("Assault Tank", "armor", "main", 2, 1100, 110, 20, 10, 2, 3, 3, 1.1, "High-firepower tank", ["Armored Warfare"], ["high_explosive"], "🚗"),
            MilitaryAsset("Anti-Air Tank", "armor", "main", 2, 900, 90, 12, 8, 2, 5, 3, 0.9, "Anti-aircraft tank", ["Armored Warfare"], ["anti_air"], "🚗"),
            MilitaryAsset("Flame Tank", "armor", "main", 2, 800, 80, 14, 9, 2, 2, 3, 0.8, "Flamethrower-equipped tank", ["Armored Warfare"], ["flame_weapon"], "🔥"),
            
            # Advanced Armor
            MilitaryAsset("Stealth Tank", "armor", "advanced", 3, 1500, 150, 16, 14, 3, 4, 3, 1.5, "Radar-invisible tank", ["Stealth Technology"], ["stealth"], "👻"),
            MilitaryAsset("Plasma Tank", "armor", "advanced", 3, 1800, 180, 25, 12, 2, 5, 3, 1.8, "Plasma weapon tank", ["Plasma Technology"], ["plasma_weapons"], "⚡"),
            MilitaryAsset("Railgun Tank", "armor", "advanced", 3, 2000, 200, 30, 10, 2, 6, 3, 2.0, "Electromagnetic cannon tank", ["Electromagnetic Weapons"], ["railgun"], "⚡"),
            MilitaryAsset("Laser Tank", "armor", "advanced", 3, 1600, 160, 22, 11, 3, 5, 3, 1.6, "Laser weapon tank", ["Laser Technology"], ["laser_weapons"], "🔴"),
            MilitaryAsset("Missile Tank", "armor", "advanced", 3, 1400, 140, 20, 9, 2, 8, 3, 1.4, "Missile launcher tank", ["Advanced Missiles"], ["missile_launcher"], "🚀"),
            
            # Super Heavy Armor
            MilitaryAsset("Super Heavy Tank", "armor", "super", 4, 3000, 300, 35, 25, 1, 5, 4, 3.0, "Massive super tank", ["Advanced Materials"], ["massive_armor"], "🏰"),
            MilitaryAsset("Mech Walker", "armor", "super", 4, 2500, 250, 30, 20, 3, 4, 3, 2.5, "Humanoid combat mech", ["Mech Technology"], ["humanoid", "versatile"], "🤖"),
            MilitaryAsset("Land Battleship", "armor", "super", 4, 4000, 400, 40, 30, 1, 6, 6, 4.0, "Giant land-based warship", ["Advanced Materials"], ["massive", "multi_weapon"], "🏰"),
            MilitaryAsset("Quantum Tank", "armor", "super", 4, 5000, 500, 50, 35, 4, 8, 4, 5.0, "Quantum-powered super tank", ["Quantum Technology"], ["quantum_shift", "phase"], "⚛️"),
            MilitaryAsset("Gravity Tank", "armor", "super", 4, 3500, 350, 45, 28, 3, 5, 4, 3.5, "Gravity manipulation tank", ["Gravity Control"], ["gravity_field", "levitation"], "🌌"),
            
            # Specialized Armor
            MilitaryAsset("Amphibious Tank", "armor", "specialized", 2, 800, 80, 12, 10, 2, 3, 3, 0.8, "Water-capable tank", ["Basic Training"], ["amphibious"], "🌊"),
            MilitaryAsset("Arctic Tank", "armor", "specialized", 2, 900, 90, 13, 11, 2, 3, 3, 0.9, "Cold weather tank", ["Basic Training"], ["arctic_warfare"], "🧊"),
            MilitaryAsset("Desert Tank", "armor", "specialized", 2, 850, 85, 12, 10, 2, 3, 3, 0.85, "Desert warfare tank", ["Basic Training"], ["desert_warfare"], "🏜️"),
            MilitaryAsset("Urban Tank", "armor", "specialized", 2, 950, 95, 14, 12, 2, 2, 3, 0.95, "City combat tank", ["Basic Training"], ["urban_warfare"], "🏙️"),
            MilitaryAsset("Mountain Tank", "armor", "specialized", 2, 1000, 100, 13, 11, 2, 3, 3, 1.0, "Mountain warfare tank", ["Basic Training"], ["mountain_warfare"], "⛰️"),
        ]
        
        # AIRCRAFT (50 units)
        aircraft = [
            # Fighter Aircraft
            MilitaryAsset("Fighter Jet", "aircraft", "fighter", 2, 800, 80, 20, 8, 8, 6, 1, 1.0, "Air superiority fighter", ["Air Superiority"], ["air_superiority"], "✈️"),
            MilitaryAsset("Interceptor", "aircraft", "fighter", 2, 700, 70, 18, 6, 9, 5, 1, 0.9, "High-speed interceptor", ["Air Superiority"], ["intercept"], "🚀"),
            MilitaryAsset("Stealth Fighter", "aircraft", "fighter", 3, 1200, 120, 22, 10, 8, 6, 1, 1.2, "Radar-invisible fighter", ["Stealth Technology"], ["stealth"], "👻"),
            MilitaryAsset("Plasma Fighter", "aircraft", "fighter", 3, 1500, 150, 28, 8, 7, 7, 1, 1.5, "Plasma weapon fighter", ["Plasma Technology"], ["plasma_weapons"], "⚡"),
            MilitaryAsset("Laser Fighter", "aircraft", "fighter", 3, 1300, 130, 25, 9, 8, 6, 1, 1.3, "Laser weapon fighter", ["Laser Technology"], ["laser_weapons"], "🔴"),
            
            # Bomber Aircraft
            MilitaryAsset("Bomber", "aircraft", "bomber", 2, 1000, 100, 15, 12, 4, 8, 4, 1.2, "Heavy bomber aircraft", ["Air Superiority"], ["bombing"], "💣"),
            MilitaryAsset("Stealth Bomber", "aircraft", "bomber", 3, 2000, 200, 20, 15, 5, 10, 6, 2.0, "Invisible bomber", ["Stealth Technology"], ["stealth", "bombing"], "👻"),
            MilitaryAsset("Strategic Bomber", "aircraft", "bomber", 3, 2500, 250, 25, 18, 3, 12, 8, 2.5, "Long-range strategic bomber", ["Advanced Materials"], ["strategic", "long_range"], "💣"),
            MilitaryAsset("Nuclear Bomber", "aircraft", "bomber", 4, 3000, 300, 30, 20, 4, 15, 10, 3.0, "Nuclear weapon bomber", ["Nuclear Weapons"], ["nuclear", "devastating"], "☢️"),
            MilitaryAsset("Plasma Bomber", "aircraft", "bomber", 3, 1800, 180, 22, 14, 4, 9, 5, 1.8, "Plasma weapon bomber", ["Plasma Technology"], ["plasma_weapons"], "⚡"),
            
            # Attack Aircraft
            MilitaryAsset("Attack Helicopter", "aircraft", "attack", 2, 600, 60, 12, 8, 4, 4, 2, 0.8, "Ground attack helicopter", ["Air Superiority"], ["ground_attack"], "🚁"),
            MilitaryAsset("Gunship", "aircraft", "attack", 2, 800, 80, 15, 10, 3, 5, 3, 1.0, "Heavy attack aircraft", ["Air Superiority"], ["heavy_attack"], "🚁"),
            MilitaryAsset("Stealth Attack", "aircraft", "attack", 3, 1000, 100, 18, 12, 5, 6, 3, 1.2, "Stealth attack aircraft", ["Stealth Technology"], ["stealth", "attack"], "👻"),
            MilitaryAsset("Drone Swarm", "aircraft", "attack", 3, 400, 40, 20, 4, 6, 3, 10, 0.5, "Swarm of attack drones", ["Drone Technology"], ["swarm", "autonomous"], "🦠"),
            MilitaryAsset("Laser Attack", "aircraft", "attack", 3, 1200, 120, 22, 10, 5, 7, 3, 1.4, "Laser attack aircraft", ["Laser Technology"], ["laser_weapons"], "🔴"),
            
            # Transport Aircraft
            MilitaryAsset("Transport Plane", "aircraft", "transport", 2, 500, 50, 5, 15, 6, 2, 20, 0.6, "Cargo transport aircraft", ["Air Superiority"], ["transport"], "✈️"),
            MilitaryAsset("Heavy Transport", "aircraft", "transport", 2, 800, 80, 6, 18, 5, 2, 30, 0.8, "Heavy cargo transport", ["Air Superiority"], ["heavy_transport"], "✈️"),
            MilitaryAsset("Stealth Transport", "aircraft", "transport", 3, 1000, 100, 8, 20, 6, 3, 25, 1.0, "Invisible transport", ["Stealth Technology"], ["stealth", "transport"], "👻"),
            MilitaryAsset("VTOL Transport", "aircraft", "transport", 2, 700, 70, 7, 12, 4, 2, 15, 0.7, "Vertical takeoff transport", ["VTOL Technology"], ["vtol"], "🚁"),
            MilitaryAsset("Quantum Transport", "aircraft", "transport", 4, 2000, 200, 15, 25, 10, 5, 40, 2.0, "Quantum teleportation transport", ["Quantum Technology"], ["quantum_teleport"], "⚛️"),
            
            # Reconnaissance Aircraft
            MilitaryAsset("Recon Plane", "aircraft", "recon", 1, 300, 30, 3, 5, 7, 8, 1, 0.4, "Reconnaissance aircraft", [], ["recon"], "🔍"),
            MilitaryAsset("AWACS", "aircraft", "recon", 2, 600, 60, 4, 8, 5, 10, 2, 0.6, "Airborne warning system", ["Air Superiority"], ["radar", "command"], "📡"),
            MilitaryAsset("Stealth Recon", "aircraft", "recon", 3, 800, 80, 5, 10, 8, 12, 2, 0.8, "Invisible reconnaissance", ["Stealth Technology"], ["stealth", "recon"], "👻"),
            MilitaryAsset("Satellite", "aircraft", "recon", 3, 1000, 100, 2, 15, 10, 20, 1, 0.5, "Orbital reconnaissance", ["Space Technology"], ["orbital", "global"], "🛰️"),
            MilitaryAsset("Quantum Scanner", "aircraft", "recon", 4, 1500, 150, 8, 12, 9, 15, 2, 1.5, "Quantum-enhanced recon", ["Quantum Technology"], ["quantum_scan", "precognition"], "⚛️"),
        ]
        
        # WARSHIPS (50 units)
        warships = [
            # Patrol Boats
            MilitaryAsset("Patrol Boat", "naval", "patrol", 1, 300, 30, 6, 4, 4, 3, 2, 0.4, "Fast coastal patrol vessel", [], ["patrol"], "🚤"),
            MilitaryAsset("Gunboat", "naval", "patrol", 1, 400, 40, 8, 6, 3, 4, 3, 0.5, "Armed patrol boat", [], ["gunboat"], "🚤"),
            MilitaryAsset("Missile Boat", "naval", "patrol", 2, 500, 50, 12, 5, 4, 6, 2, 0.6, "Missile-armed patrol boat", ["Basic Training"], ["missile_launcher"], "🚤"),
            MilitaryAsset("Stealth Boat", "naval", "patrol", 3, 700, 70, 10, 8, 5, 4, 2, 0.7, "Radar-invisible patrol boat", ["Stealth Technology"], ["stealth"], "👻"),
            MilitaryAsset("Hovercraft", "naval", "patrol", 2, 600, 60, 9, 7, 6, 3, 3, 0.8, "Amphibious hovercraft", ["Basic Training"], ["amphibious"], "🌊"),
            
            # Frigates
            MilitaryAsset("Frigate", "naval", "frigate", 2, 800, 80, 15, 12, 3, 5, 4, 1.0, "Multi-role warship", ["Basic Training"], ["versatile"], "🚢"),
            MilitaryAsset("Stealth Frigate", "naval", "frigate", 3, 1200, 120, 18, 15, 4, 6, 4, 1.2, "Invisible frigate", ["Stealth Technology"], ["stealth"], "👻"),
            MilitaryAsset("Missile Frigate", "naval", "frigate", 2, 1000, 100, 20, 10, 3, 8, 4, 1.1, "Missile-focused frigate", ["Basic Training"], ["missile_launcher"], "🚀"),
            MilitaryAsset("Anti-Air Frigate", "naval", "frigate", 2, 900, 90, 12, 14, 3, 7, 4, 1.0, "Air defense frigate", ["Basic Training"], ["anti_air"], "🚁"),
            MilitaryAsset("Plasma Frigate", "naval", "frigate", 3, 1500, 150, 25, 12, 3, 6, 4, 1.5, "Plasma weapon frigate", ["Plasma Technology"], ["plasma_weapons"], "⚡"),
            
            # Destroyers
            MilitaryAsset("Destroyer", "naval", "destroyer", 2, 1500, 150, 25, 18, 2, 6, 6, 1.8, "Heavy combat destroyer", ["Basic Training"], ["heavy_weapons"], "🚢"),
            MilitaryAsset("Stealth Destroyer", "naval", "destroyer", 3, 2000, 200, 28, 22, 3, 7, 6, 2.0, "Invisible destroyer", ["Stealth Technology"], ["stealth"], "👻"),
            MilitaryAsset("Missile Destroyer", "naval", "destroyer", 2, 1800, 180, 30, 15, 2, 10, 6, 1.9, "Missile destroyer", ["Basic Training"], ["missile_launcher"], "🚀"),
            MilitaryAsset("Laser Destroyer", "naval", "destroyer", 3, 2200, 220, 32, 20, 3, 8, 6, 2.2, "Laser weapon destroyer", ["Laser Technology"], ["laser_weapons"], "🔴"),
            MilitaryAsset("Railgun Destroyer", "naval", "destroyer", 3, 2500, 250, 35, 18, 2, 9, 6, 2.5, "Electromagnetic destroyer", ["Electromagnetic Weapons"], ["railgun"], "⚡"),
            
            # Cruisers
            MilitaryAsset("Cruiser", "naval", "cruiser", 3, 3000, 300, 40, 25, 2, 8, 8, 3.0, "Heavy combat cruiser", ["Advanced Materials"], ["heavy_weapons"], "🚢"),
            MilitaryAsset("Battle Cruiser", "naval", "cruiser", 3, 3500, 350, 45, 30, 2, 9, 8, 3.5, "Battle-focused cruiser", ["Advanced Materials"], ["battle"], "🚢"),
            MilitaryAsset("Stealth Cruiser", "naval", "cruiser", 4, 4000, 400, 42, 28, 3, 10, 8, 4.0, "Invisible cruiser", ["Stealth Technology"], ["stealth"], "👻"),
            MilitaryAsset("Plasma Cruiser", "naval", "cruiser", 4, 4500, 450, 50, 25, 2, 10, 8, 4.5, "Plasma weapon cruiser", ["Plasma Technology"], ["plasma_weapons"], "⚡"),
            MilitaryAsset("Quantum Cruiser", "naval", "cruiser", 4, 5000, 500, 55, 35, 4, 12, 8, 5.0, "Quantum-powered cruiser", ["Quantum Technology"], ["quantum_shift"], "⚛️"),
            
            # Battleships
            MilitaryAsset("Battleship", "naval", "battleship", 3, 5000, 500, 60, 40, 1, 10, 12, 5.0, "Heavy battleship", ["Advanced Materials"], ["massive_weapons"], "🚢"),
            MilitaryAsset("Dreadnought", "naval", "battleship", 4, 6000, 600, 70, 50, 1, 12, 15, 6.0, "Super battleship", ["Advanced Materials"], ["super_weapons"], "🚢"),
            MilitaryAsset("Stealth Battleship", "naval", "battleship", 4, 7000, 700, 65, 45, 2, 13, 15, 7.0, "Invisible battleship", ["Stealth Technology"], ["stealth"], "👻"),
            MilitaryAsset("Plasma Battleship", "naval", "battleship", 4, 8000, 800, 80, 40, 1, 15, 15, 8.0, "Plasma weapon battleship", ["Plasma Technology"], ["plasma_weapons"], "⚡"),
            MilitaryAsset("Quantum Battleship", "naval", "battleship", 4, 10000, 1000, 100, 60, 3, 20, 20, 10.0, "Quantum battleship", ["Quantum Technology"], ["quantum_weapons"], "⚛️"),
            
            # Carriers
            MilitaryAsset("Aircraft Carrier", "naval", "carrier", 3, 4000, 400, 20, 30, 2, 5, 30, 4.0, "Aircraft carrier", ["Air Superiority"], ["aircraft_carrier"], "🚢"),
            MilitaryAsset("Stealth Carrier", "naval", "carrier", 4, 5000, 500, 25, 35, 3, 6, 35, 5.0, "Invisible carrier", ["Stealth Technology"], ["stealth", "aircraft_carrier"], "👻"),
            MilitaryAsset("Plasma Carrier", "naval", "carrier", 4, 6000, 600, 30, 40, 2, 8, 40, 6.0, "Plasma weapon carrier", ["Plasma Technology"], ["plasma_weapons", "aircraft_carrier"], "⚡"),
            MilitaryAsset("Quantum Carrier", "naval", "carrier", 4, 8000, 800, 40, 50, 4, 10, 50, 8.0, "Quantum carrier", ["Quantum Technology"], ["quantum_weapons", "aircraft_carrier"], "⚛️"),
            MilitaryAsset("Space Carrier", "naval", "carrier", 4, 12000, 1200, 50, 60, 6, 15, 60, 12.0, "Space-capable carrier", ["Space Technology"], ["space", "aircraft_carrier"], "🚀"),
            
            # Submarines
            MilitaryAsset("Attack Submarine", "naval", "submarine", 2, 1000, 100, 20, 15, 3, 4, 3, 1.0, "Underwater attack vessel", ["Basic Training"], ["underwater"], "🛸"),
            MilitaryAsset("Stealth Submarine", "naval", "submarine", 3, 1500, 150, 25, 18, 4, 5, 3, 1.5, "Invisible submarine", ["Stealth Technology"], ["stealth", "underwater"], "👻"),
            MilitaryAsset("Missile Submarine", "naval", "submarine", 3, 2000, 200, 30, 12, 3, 8, 4, 2.0, "Missile submarine", ["Basic Training"], ["missile_launcher", "underwater"], "🚀"),
            MilitaryAsset("Nuclear Submarine", "naval", "submarine", 4, 3000, 300, 35, 20, 4, 10, 5, 3.0, "Nuclear submarine", ["Nuclear Weapons"], ["nuclear", "underwater"], "☢️"),
            MilitaryAsset("Quantum Submarine", "naval", "submarine", 4, 4000, 400, 45, 25, 5, 12, 6, 4.0, "Quantum submarine", ["Quantum Technology"], ["quantum_shift", "underwater"], "⚛️"),
        ]
        
        # MISSILES & ROCKETS (50 units)
        missiles = [
            # Basic Missiles
            MilitaryAsset("Rocket", "missile", "basic", 1, 50, 5, 8, 1, 4, 3, 1, 0.1, "Basic unguided rocket", [], ["basic"], "🚀"),
            MilitaryAsset("Guided Missile", "missile", "basic", 1, 100, 10, 12, 2, 5, 4, 1, 0.2, "Guided missile", [], ["guided"], "🎯"),
            MilitaryAsset("Anti-Tank Missile", "missile", "basic", 1, 150, 15, 15, 1, 3, 3, 1, 0.15, "Armor-piercing missile", [], ["anti_armor"], "🚫"),
            MilitaryAsset("Anti-Air Missile", "missile", "basic", 1, 120, 12, 10, 1, 6, 5, 1, 0.12, "Air defense missile", [], ["anti_air"], "🚁"),
            MilitaryAsset("Surface-to-Surface", "missile", "basic", 2, 200, 20, 18, 2, 4, 6, 1, 0.2, "Ground attack missile", ["Basic Training"], ["ground_attack"], "💥"),
            
            # Advanced Missiles
            MilitaryAsset("Cruise Missile", "missile", "advanced", 2, 300, 30, 25, 3, 6, 8, 1, 0.3, "Long-range cruise missile", ["Basic Training"], ["long_range"], "✈️"),
            MilitaryAsset("Stealth Missile", "missile", "advanced", 3, 400, 40, 22, 4, 5, 7, 1, 0.4, "Radar-invisible missile", ["Stealth Technology"], ["stealth"], "👻"),
            MilitaryAsset("Plasma Missile", "missile", "advanced", 3, 500, 50, 30, 2, 4, 6, 1, 0.5, "Plasma weapon missile", ["Plasma Technology"], ["plasma_weapons"], "⚡"),
            MilitaryAsset("Laser Missile", "missile", "advanced", 3, 450, 45, 28, 3, 5, 7, 1, 0.45, "Laser-guided missile", ["Laser Technology"], ["laser_weapons"], "🔴"),
            MilitaryAsset("EMP Missile", "missile", "advanced", 3, 350, 35, 15, 1, 4, 5, 1, 0.35, "Electromagnetic pulse missile", ["Electromagnetic Weapons"], ["emp"], "⚡"),
            
            # Strategic Missiles
            MilitaryAsset("Ballistic Missile", "missile", "strategic", 3, 800, 80, 40, 5, 8, 12, 1, 0.8, "Long-range ballistic missile", ["Advanced Missiles"], ["strategic"], "🚀"),
            MilitaryAsset("ICBM", "missile", "strategic", 4, 1500, 150, 60, 8, 10, 20, 1, 1.5, "Intercontinental ballistic missile", ["Nuclear Weapons"], ["intercontinental"], "🌍"),
            MilitaryAsset("Nuclear Missile", "missile", "strategic", 4, 2000, 200, 100, 10, 8, 15, 1, 2.0, "Nuclear weapon missile", ["Nuclear Weapons"], ["nuclear", "devastating"], "☢️"),
            MilitaryAsset("Stealth ICBM", "missile", "strategic", 4, 2500, 250, 70, 12, 10, 18, 1, 2.5, "Invisible ICBM", ["Stealth Technology", "Nuclear Weapons"], ["stealth", "nuclear"], "👻"),
            MilitaryAsset("Quantum Missile", "missile", "strategic", 4, 3000, 300, 80, 15, 12, 25, 1, 3.0, "Quantum-enhanced missile", ["Quantum Technology"], ["quantum_weapons"], "⚛️"),
            
            # Specialized Missiles
            MilitaryAsset("Cluster Missile", "missile", "specialized", 2, 250, 25, 20, 2, 4, 5, 5, 0.25, "Multi-warhead missile", ["Basic Training"], ["cluster"], "💥"),
            MilitaryAsset("Penetrator Missile", "missile", "specialized", 2, 300, 30, 25, 1, 3, 4, 1, 0.3, "Bunker-busting missile", ["Basic Training"], ["penetrator"], "💥"),
            MilitaryAsset("Homing Missile", "missile", "specialized", 2, 180, 18, 15, 2, 5, 6, 1, 0.18, "Heat-seeking missile", ["Basic Training"], ["homing"], "🎯"),
            MilitaryAsset("Swarm Missile", "missile", "specialized", 3, 200, 20, 18, 1, 4, 4, 10, 0.2, "Swarm of small missiles", ["Drone Technology"], ["swarm"], "🦠"),
            MilitaryAsset("Time-Delayed Missile", "missile", "specialized", 3, 400, 40, 22, 3, 4, 6, 1, 0.4, "Delayed detonation missile", ["Temporal Technology"], ["time_delay"], "⏰"),
            
            # Future Missiles
            MilitaryAsset("Gravity Missile", "missile", "future", 4, 1000, 100, 35, 5, 6, 8, 1, 1.0, "Gravity manipulation missile", ["Gravity Control"], ["gravity_field"], "🌌"),
            MilitaryAsset("Phase Missile", "missile", "future", 4, 1200, 120, 40, 8, 7, 10, 1, 1.2, "Phase-shifting missile", ["Quantum Technology"], ["phase_shift"], "⚛️"),
            MilitaryAsset("Reality Missile", "missile", "future", 4, 1500, 150, 50, 10, 8, 12, 1, 1.5, "Reality-bending missile", ["Reality Technology"], ["reality_bend"], "🌀"),
            MilitaryAsset("Dimensional Missile", "missile", "future", 4, 2000, 200, 60, 12, 10, 15, 1, 2.0, "Dimensional weapon missile", ["Dimensional Technology"], ["dimensional"], "🌌"),
            MilitaryAsset("Universe Missile", "missile", "future", 4, 5000, 500, 100, 20, 15, 30, 1, 5.0, "Universe-ending missile", ["Universe Technology"], ["universe_ending"], "🌌"),
        ]
        
        # DEFENSE SYSTEMS (50 units)
        defense_systems = [
            # Basic Defenses
            MilitaryAsset("Bunker", "defense", "basic", 1, 200, 20, 5, 15, 0, 2, 5, 0.1, "Basic defensive structure", [], ["fortified"], "🏰"),
            MilitaryAsset("Pillbox", "defense", "basic", 1, 150, 15, 8, 12, 0, 3, 2, 0.1, "Small defensive position", [], ["fortified"], "🏰"),
            MilitaryAsset("Trench", "defense", "basic", 1, 100, 10, 3, 8, 0, 1, 10, 0.05, "Defensive trench system", [], ["fortified"], "🛡️"),
            MilitaryAsset("Barbed Wire", "defense", "basic", 1, 50, 5, 1, 5, 0, 1, 1, 0.02, "Obstacle barrier", [], ["obstacle"], "🕸️"),
            MilitaryAsset("Landmine", "defense", "basic", 1, 30, 3, 10, 1, 0, 1, 1, 0.01, "Explosive trap", [], ["trap"], "💣"),
            
            # Anti-Air Defenses
            MilitaryAsset("AA Gun", "defense", "anti_air", 1, 300, 30, 12, 8, 0, 5, 1, 0.2, "Anti-aircraft gun", [], ["anti_air"], "🚁"),
            MilitaryAsset("SAM Site", "defense", "anti_air", 2, 500, 50, 20, 10, 0, 8, 1, 0.3, "Surface-to-air missile site", ["Basic Training"], ["anti_air"], "🚀"),
            MilitaryAsset("Radar Station", "defense", "anti_air", 2, 400, 40, 5, 15, 0, 10, 1, 0.25, "Air detection radar", ["Basic Training"], ["radar"], "📡"),
            MilitaryAsset("Stealth AA", "defense", "anti_air", 3, 800, 80, 25, 12, 0, 9, 1, 0.5, "Invisible anti-air system", ["Stealth Technology"], ["stealth", "anti_air"], "👻"),
            MilitaryAsset("Laser AA", "defense", "anti_air", 3, 1000, 100, 30, 15, 0, 10, 1, 0.6, "Laser anti-air system", ["Laser Technology"], ["laser_weapons", "anti_air"], "🔴"),
            
            # Anti-Ground Defenses
            MilitaryAsset("Artillery Emplacement", "defense", "anti_ground", 2, 600, 60, 25, 12, 0, 6, 1, 0.4, "Heavy artillery position", ["Basic Training"], ["artillery"], "💣"),
            MilitaryAsset("Mortar Pit", "defense", "anti_ground", 1, 200, 20, 15, 8, 0, 4, 1, 0.15, "Mortar defensive position", [], ["mortar"], "💣"),
            MilitaryAsset("Machine Gun Nest", "defense", "anti_ground", 1, 150, 15, 10, 10, 0, 3, 1, 0.1, "Machine gun position", [], ["machine_gun"], "🔫"),
            MilitaryAsset("Anti-Tank Gun", "defense", "anti_ground", 2, 400, 40, 20, 15, 0, 5, 1, 0.3, "Anti-tank defensive gun", ["Basic Training"], ["anti_armor"], "🚫"),
            MilitaryAsset("Rocket Launcher", "defense", "anti_ground", 2, 350, 35, 18, 8, 0, 6, 1, 0.25, "Rocket launcher emplacement", ["Basic Training"], ["rocket"], "🚀"),
            
            # Advanced Defenses
            MilitaryAsset("Fortress", "defense", "advanced", 3, 2000, 200, 30, 40, 0, 8, 20, 1.0, "Heavy defensive fortress", ["Advanced Materials"], ["fortified"], "🏰"),
            MilitaryAsset("Stealth Base", "defense", "advanced", 3, 1500, 150, 25, 35, 0, 7, 15, 0.8, "Invisible defensive base", ["Stealth Technology"], ["stealth", "fortified"], "👻"),
            MilitaryAsset("Plasma Turret", "defense", "advanced", 3, 1200, 120, 35, 20, 0, 8, 1, 0.7, "Plasma weapon turret", ["Plasma Technology"], ["plasma_weapons"], "⚡"),
            MilitaryAsset("Laser Turret", "defense", "advanced", 3, 1000, 100, 30, 18, 0, 7, 1, 0.6, "Laser weapon turret", ["Laser Technology"], ["laser_weapons"], "🔴"),
            MilitaryAsset("Railgun Turret", "defense", "advanced", 3, 1300, 130, 40, 15, 0, 9, 1, 0.8, "Electromagnetic turret", ["Electromagnetic Weapons"], ["railgun"], "⚡"),
            
            # Shield Systems
            MilitaryAsset("Energy Shield", "defense", "shield", 3, 800, 80, 0, 30, 0, 5, 1, 0.5, "Protective energy barrier", ["Energy Technology"], ["energy_shield"], "🛡️"),
            MilitaryAsset("Plasma Shield", "defense", "shield", 3, 1000, 100, 0, 40, 0, 6, 1, 0.6, "Plasma energy shield", ["Plasma Technology"], ["plasma_shield"], "⚡"),
            MilitaryAsset("Quantum Shield", "defense", "shield", 4, 1500, 150, 0, 50, 0, 8, 1, 0.9, "Quantum field shield", ["Quantum Technology"], ["quantum_shield"], "⚛️"),
            MilitaryAsset("Gravity Shield", "defense", "shield", 4, 1200, 120, 0, 45, 0, 7, 1, 0.8, "Gravity manipulation shield", ["Gravity Control"], ["gravity_shield"], "🌌"),
            MilitaryAsset("Reality Shield", "defense", "shield", 4, 2000, 200, 0, 60, 0, 10, 1, 1.2, "Reality-bending shield", ["Reality Technology"], ["reality_shield"], "🌀"),
            
            # Super Defenses
            MilitaryAsset("Mega Fortress", "defense", "super", 4, 5000, 500, 60, 80, 0, 15, 50, 2.5, "Massive defensive fortress", ["Advanced Materials"], ["mega_fortress"], "🏰"),
            MilitaryAsset("Stealth Citadel", "defense", "super", 4, 6000, 600, 55, 85, 0, 16, 60, 3.0, "Invisible mega fortress", ["Stealth Technology"], ["stealth", "mega_fortress"], "👻"),
            MilitaryAsset("Plasma Citadel", "defense", "super", 4, 7000, 700, 80, 70, 0, 18, 70, 3.5, "Plasma weapon fortress", ["Plasma Technology"], ["plasma_weapons", "mega_fortress"], "⚡"),
            MilitaryAsset("Quantum Citadel", "defense", "super", 4, 8000, 800, 90, 90, 0, 20, 80, 4.0, "Quantum fortress", ["Quantum Technology"], ["quantum_weapons", "mega_fortress"], "⚛️"),
            MilitaryAsset("Dimensional Fortress", "defense", "super", 4, 10000, 1000, 100, 100, 0, 25, 100, 5.0, "Dimensional fortress", ["Dimensional Technology"], ["dimensional", "mega_fortress"], "🌌"),
        ]
        
        # Add all assets to the database
        all_assets = (infantry_units + armored_vehicles + aircraft + warships + 
                     missiles + defense_systems)
        
        for asset in all_assets:
            assets[asset.name.lower().replace(" ", "_")] = asset
        
        return assets
    
    def get_asset(self, name: str) -> Optional[MilitaryAsset]:
        """Get asset by name"""
        return self.assets.get(name.lower().replace(" ", "_"))
    
    def get_assets_by_category(self, category: str) -> List[MilitaryAsset]:
        """Get all assets in a category"""
        return [asset for asset in self.assets.values() if asset.category == category]
    
    def get_assets_by_tier(self, tier: int) -> List[MilitaryAsset]:
        """Get all assets of a specific tier"""
        return [asset for asset in self.assets.values() if asset.tier == tier]
    
    def get_assets_by_subcategory(self, category: str, subcategory: str) -> List[MilitaryAsset]:
        """Get assets by category and subcategory"""
        return [asset for asset in self.assets.values() 
                if asset.category == category and asset.subcategory == subcategory]
    
    def search_assets(self, query: str) -> List[MilitaryAsset]:
        """Search assets by name or description"""
        query = query.lower()
        results = []
        for asset in self.assets.values():
            if (query in asset.name.lower() or 
                query in asset.description.lower() or
                query in asset.category.lower() or
                query in asset.subcategory.lower()):
                results.append(asset)
        return results
    
    def get_total_assets(self) -> int:
        """Get total number of assets"""
        return len(self.assets)
    
    def get_asset_categories(self) -> List[str]:
        """Get all asset categories"""
        return list(set(asset.category for asset in self.assets.values()))
    
    def get_asset_subcategories(self, category: str) -> List[str]:
        """Get subcategories for a category"""
        return list(set(asset.subcategory for asset in self.assets.values() 
                       if asset.category == category))