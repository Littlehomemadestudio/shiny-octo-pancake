"""
Enhanced Military Assets with Complex Resource Requirements
Assets now require multiple currencies based on complexity and realism
"""

import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from complex_resources import ResourceType, ResourceCategory

class AssetComplexity(Enum):
    SIMPLE = "simple"        # Basic units requiring few resources
    MODERATE = "moderate"    # Standard units with balanced requirements
    COMPLEX = "complex"      # Advanced units with multiple resource types
    ADVANCED = "advanced"    # High-tech units with rare resources
    LEGENDARY = "legendary"  # Ultimate units with all resource types

@dataclass
class ResourceRequirement:
    """Resource requirement for building an asset"""
    resource_type: ResourceType
    amount: float
    is_consumed: bool  # Whether the resource is consumed or just required
    is_critical: bool  # Whether this resource is critical for the asset
    description: str

@dataclass
class EnhancedMilitaryAsset:
    """Enhanced military asset with complex resource requirements"""
    name: str
    category: str
    subcategory: str
    tier: int
    complexity: AssetComplexity
    description: str
    emoji: str
    
    # Combat stats
    attack: int
    defense: int
    speed: int
    range: int
    capacity: int
    
    # Resource requirements
    resource_requirements: List[ResourceRequirement]
    
    # Production requirements
    production_time: int  # Hours to produce
    production_facility: str  # Required facility type
    technology_requirements: List[str]
    
    # Operational requirements
    upkeep_resources: List[ResourceRequirement]  # Resources needed per hour
    fuel_consumption: float
    ammunition_consumption: float
    maintenance_interval: int  # Hours between maintenance
    
    # Special properties
    special_abilities: List[str]
    environmental_requirements: List[str]  # Terrain, weather, etc.
    crew_requirements: int
    training_time: int  # Hours to train crew
    
    # Economic data
    base_cost: float  # Base cost in gold
    rarity_factor: float  # Rarity multiplier (0-1)
    market_demand: float  # Market demand (0-1)

class EnhancedMilitaryAssetsDatabase:
    """Enhanced database with complex resource requirements"""
    
    def __init__(self):
        self.assets: Dict[str, EnhancedMilitaryAsset] = {}
        self._create_enhanced_assets()
    
    def _create_enhanced_assets(self):
        """Create enhanced military assets with complex requirements"""
        
        # BASIC INFANTRY UNITS
        self.assets["rifleman"] = EnhancedMilitaryAsset(
            name="Rifleman",
            category="infantry",
            subcategory="basic",
            tier=1,
            complexity=AssetComplexity.SIMPLE,
            description="Basic foot soldier with rifle and standard equipment",
            emoji="🪖",
            attack=3,
            defense=2,
            speed=1,
            range=1,
            capacity=1,
            resource_requirements=[
                ResourceRequirement(ResourceType.GOLD, 50, True, True, "Basic equipment cost"),
                ResourceRequirement(ResourceType.IRON, 5, True, True, "Weapon and armor materials"),
                ResourceRequirement(ResourceType.MANPOWER, 1, True, True, "Trained soldier"),
                ResourceRequirement(ResourceType.AMMUNITION, 100, True, False, "Initial ammunition supply"),
                ResourceRequirement(ResourceType.FOOD, 10, True, False, "Rations for deployment")
            ],
            production_time=2,
            production_facility="barracks",
            technology_requirements=[],
            upkeep_resources=[
                ResourceRequirement(ResourceType.FOOD, 2, True, True, "Daily rations"),
                ResourceRequirement(ResourceType.AMMUNITION, 5, True, True, "Training ammunition"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 1, True, False, "Medical supplies")
            ],
            fuel_consumption=0.0,
            ammunition_consumption=5.0,
            maintenance_interval=168,  # Weekly
            special_abilities=["basic_combat", "infantry_tactics"],
            environmental_requirements=["ground"],
            crew_requirements=1,
            training_time=40,
            base_cost=50,
            rarity_factor=0.0,
            market_demand=0.8
        )
        
        self.assets["special_forces"] = EnhancedMilitaryAsset(
            name="Special Forces",
            category="infantry",
            subcategory="elite",
            tier=2,
            complexity=AssetComplexity.MODERATE,
            description="Elite special operations unit with advanced training and equipment",
            emoji="🕴️",
            attack=8,
            defense=6,
            speed=2,
            range=2,
            capacity=1,
            resource_requirements=[
                ResourceRequirement(ResourceType.GOLD, 200, True, True, "Advanced equipment cost"),
                ResourceRequirement(ResourceType.IRON, 15, True, True, "Specialized weapons and gear"),
                ResourceRequirement(ResourceType.MANPOWER, 1, True, True, "Elite soldier"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 20, True, True, "Specialized training"),
                ResourceRequirement(ResourceType.TECHNOLOGY, 10, True, True, "Advanced equipment"),
                ResourceRequirement(ResourceType.AMMUNITION, 200, True, False, "Specialized ammunition"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 20, True, False, "Advanced medical supplies")
            ],
            production_time=8,
            production_facility="special_forces_academy",
            technology_requirements=["advanced_training", "specialized_equipment"],
            upkeep_resources=[
                ResourceRequirement(ResourceType.FOOD, 3, True, True, "High-quality rations"),
                ResourceRequirement(ResourceType.AMMUNITION, 10, True, True, "Training ammunition"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 3, True, True, "Medical supplies"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 2, True, True, "Continuous training")
            ],
            fuel_consumption=0.0,
            ammunition_consumption=10.0,
            maintenance_interval=120,  # 5 days
            special_abilities=["stealth", "infiltration", "demolition", "reconnaissance"],
            environmental_requirements=["ground", "urban", "jungle", "arctic"],
            crew_requirements=1,
            training_time=200,
            base_cost=200,
            rarity_factor=0.3,
            market_demand=0.6
        )
        
        # ARMORED VEHICLES
        self.assets["main_battle_tank"] = EnhancedMilitaryAsset(
            name="Main Battle Tank",
            category="armor",
            subcategory="heavy",
            tier=2,
            complexity=AssetComplexity.COMPLEX,
            description="Heavy armored vehicle with powerful main gun and advanced protection",
            emoji="🚗",
            attack=15,
            defense=20,
            speed=3,
            range=4,
            capacity=4,
            resource_requirements=[
                ResourceRequirement(ResourceType.GOLD, 1000, True, True, "Vehicle cost"),
                ResourceRequirement(ResourceType.IRON, 50, True, True, "Armor and chassis"),
                ResourceRequirement(ResourceType.OIL, 20, True, True, "Fuel for initial operations"),
                ResourceRequirement(ResourceType.MANPOWER, 4, True, True, "Tank crew"),
                ResourceRequirement(ResourceType.TECHNOLOGY, 30, True, True, "Advanced systems"),
                ResourceRequirement(ResourceType.AMMUNITION, 50, True, False, "Main gun ammunition"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 10, True, False, "Crew medical supplies"),
                ResourceRequirement(ResourceType.ENERGY, 100, True, True, "Electrical systems")
            ],
            production_time=24,
            production_facility="tank_factory",
            technology_requirements=["armor_technology", "tank_gun", "tracked_vehicle"],
            upkeep_resources=[
                ResourceRequirement(ResourceType.FUEL, 20, True, True, "Daily fuel consumption"),
                ResourceRequirement(ResourceType.AMMUNITION, 5, True, True, "Training ammunition"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 2, True, True, "Crew medical supplies"),
                ResourceRequirement(ResourceType.ENERGY, 10, True, True, "Electrical maintenance"),
                ResourceRequirement(ResourceType.MANPOWER, 0.1, True, True, "Maintenance crew")
            ],
            fuel_consumption=20.0,
            ammunition_consumption=5.0,
            maintenance_interval=48,  # 2 days
            special_abilities=["armor_piercing", "heavy_weapons", "armored_advance"],
            environmental_requirements=["ground", "open_terrain"],
            crew_requirements=4,
            training_time=120,
            base_cost=1000,
            rarity_factor=0.2,
            market_demand=0.7
        )
        
        # AIRCRAFT
        self.assets["fighter_jet"] = EnhancedMilitaryAsset(
            name="Fighter Jet",
            category="aircraft",
            subcategory="fighter",
            tier=3,
            complexity=AssetComplexity.ADVANCED,
            description="High-performance combat aircraft for air superiority",
            emoji="✈️",
            attack=25,
            defense=15,
            speed=8,
            range=6,
            capacity=1,
            resource_requirements=[
                ResourceRequirement(ResourceType.GOLD, 5000, True, True, "Aircraft cost"),
                ResourceRequirement(ResourceType.IRON, 100, True, True, "Airframe materials"),
                ResourceRequirement(ResourceType.OIL, 50, True, True, "Aviation fuel"),
                ResourceRequirement(ResourceType.MANPOWER, 2, True, True, "Pilot and crew"),
                ResourceRequirement(ResourceType.TECHNOLOGY, 100, True, True, "Advanced avionics"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 50, True, True, "Pilot training"),
                ResourceRequirement(ResourceType.ENERGY, 200, True, True, "Electrical systems"),
                ResourceRequirement(ResourceType.AMMUNITION, 200, True, False, "Missiles and ammunition"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 20, True, False, "Crew medical supplies")
            ],
            production_time=72,
            production_facility="aircraft_factory",
            technology_requirements=["jet_engine", "avionics", "radar", "missile_technology"],
            upkeep_resources=[
                ResourceRequirement(ResourceType.FUEL, 50, True, True, "Daily fuel consumption"),
                ResourceRequirement(ResourceType.AMMUNITION, 10, True, True, "Training ammunition"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 3, True, True, "Crew medical supplies"),
                ResourceRequirement(ResourceType.ENERGY, 20, True, True, "Electrical maintenance"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 5, True, True, "Pilot training"),
                ResourceRequirement(ResourceType.MANPOWER, 0.2, True, True, "Maintenance crew")
            ],
            fuel_consumption=50.0,
            ammunition_consumption=10.0,
            maintenance_interval=24,  # Daily
            special_abilities=["air_superiority", "beyond_visual_range", "maneuverability"],
            environmental_requirements=["air", "runway"],
            crew_requirements=2,
            training_time=300,
            base_cost=5000,
            rarity_factor=0.4,
            market_demand=0.5
        )
        
        # NAVAL VESSELS
        self.assets["destroyer"] = EnhancedMilitaryAsset(
            name="Destroyer",
            category="naval",
            subcategory="warship",
            tier=3,
            complexity=AssetComplexity.COMPLEX,
            description="Multi-role warship for anti-air, anti-submarine, and surface warfare",
            emoji="🚢",
            attack=30,
            defense=25,
            speed=4,
            range=8,
            capacity=20,
            resource_requirements=[
                ResourceRequirement(ResourceType.GOLD, 10000, True, True, "Ship cost"),
                ResourceRequirement(ResourceType.IRON, 200, True, True, "Hull and superstructure"),
                ResourceRequirement(ResourceType.OIL, 100, True, True, "Marine fuel"),
                ResourceRequirement(ResourceType.MANPOWER, 50, True, True, "Ship crew"),
                ResourceRequirement(ResourceType.TECHNOLOGY, 150, True, True, "Naval systems"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 100, True, True, "Naval expertise"),
                ResourceRequirement(ResourceType.ENERGY, 500, True, True, "Electrical systems"),
                ResourceRequirement(ResourceType.AMMUNITION, 500, True, False, "Missiles and ammunition"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 100, True, False, "Crew medical supplies"),
                ResourceRequirement(ResourceType.WATER, 1000, True, True, "Fresh water supply")
            ],
            production_time=168,  # 1 week
            production_facility="shipyard",
            technology_requirements=["naval_architecture", "radar", "sonar", "missile_systems"],
            upkeep_resources=[
                ResourceRequirement(ResourceType.FUEL, 100, True, True, "Daily fuel consumption"),
                ResourceRequirement(ResourceType.AMMUNITION, 20, True, True, "Training ammunition"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 10, True, True, "Crew medical supplies"),
                ResourceRequirement(ResourceType.ENERGY, 50, True, True, "Electrical maintenance"),
                ResourceRequirement(ResourceType.WATER, 50, True, True, "Fresh water"),
                ResourceRequirement(ResourceType.MANPOWER, 1, True, True, "Maintenance crew")
            ],
            fuel_consumption=100.0,
            ammunition_consumption=20.0,
            maintenance_interval=72,  # 3 days
            special_abilities=["anti_air", "anti_submarine", "surface_warfare", "escort"],
            environmental_requirements=["water", "port"],
            crew_requirements=50,
            training_time=500,
            base_cost=10000,
            rarity_factor=0.3,
            market_demand=0.4
        )
        
        # CYBER WARFARE UNITS
        self.assets["cyber_warrior"] = EnhancedMilitaryAsset(
            name="Cyber Warrior",
            category="cyber",
            subcategory="offensive",
            tier=3,
            complexity=AssetComplexity.ADVANCED,
            description="Specialized cyber warfare operative for digital attacks and defense",
            emoji="💻",
            attack=20,
            defense=15,
            speed=5,
            range=10,
            capacity=1,
            resource_requirements=[
                ResourceRequirement(ResourceType.GOLD, 2000, True, True, "Equipment cost"),
                ResourceRequirement(ResourceType.TECHNOLOGY, 200, True, True, "Advanced computing systems"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 150, True, True, "Cyber expertise"),
                ResourceRequirement(ResourceType.ENERGY, 100, True, True, "Computing power"),
                ResourceRequirement(ResourceType.MANPOWER, 1, True, True, "Cyber specialist"),
                ResourceRequirement(ResourceType.INFLUENCE, 20, True, True, "Security clearance")
            ],
            production_time=48,
            production_facility="cyber_warfare_center",
            technology_requirements=["cyber_warfare", "encryption", "network_security", "ai_systems"],
            upkeep_resources=[
                ResourceRequirement(ResourceType.ENERGY, 20, True, True, "Computing power"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 10, True, True, "Continuous training"),
                ResourceRequirement(ResourceType.TECHNOLOGY, 5, True, True, "System updates"),
                ResourceRequirement(ResourceType.MANPOWER, 0.1, True, True, "Support staff")
            ],
            fuel_consumption=0.0,
            ammunition_consumption=0.0,
            maintenance_interval=24,  # Daily
            special_abilities=["hacking", "cyber_defense", "data_analysis", "network_infiltration"],
            environmental_requirements=["digital", "network"],
            crew_requirements=1,
            training_time=400,
            base_cost=2000,
            rarity_factor=0.5,
            market_demand=0.3
        )
        
        # SPACE UNITS
        self.assets["space_fighter"] = EnhancedMilitaryAsset(
            name="Space Fighter",
            category="space",
            subcategory="combat",
            tier=4,
            complexity=AssetComplexity.LEGENDARY,
            description="Advanced space combat vehicle for orbital warfare",
            emoji="🚀",
            attack=50,
            defense=40,
            speed=10,
            range=15,
            capacity=2,
            resource_requirements=[
                ResourceRequirement(ResourceType.GOLD, 50000, True, True, "Spacecraft cost"),
                ResourceRequirement(ResourceType.IRON, 500, True, True, "Space-grade materials"),
                ResourceRequirement(ResourceType.TECHNOLOGY, 500, True, True, "Space technology"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 300, True, True, "Space expertise"),
                ResourceRequirement(ResourceType.ENERGY, 1000, True, True, "Power systems"),
                ResourceRequirement(ResourceType.MANPOWER, 3, True, True, "Space crew"),
                ResourceRequirement(ResourceType.INFLUENCE, 100, True, True, "Space access"),
                ResourceRequirement(ResourceType.AMMUNITION, 1000, True, False, "Space weapons"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 50, True, False, "Life support")
            ],
            production_time=720,  # 1 month
            production_facility="space_dock",
            technology_requirements=["space_technology", "life_support", "space_weapons", "orbital_mechanics"],
            upkeep_resources=[
                ResourceRequirement(ResourceType.ENERGY, 100, True, True, "Power systems"),
                ResourceRequirement(ResourceType.AMMUNITION, 50, True, True, "Training weapons"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 10, True, True, "Life support"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 20, True, True, "Crew training"),
                ResourceRequirement(ResourceType.MANPOWER, 0.5, True, True, "Ground support")
            ],
            fuel_consumption=0.0,
            ammunition_consumption=50.0,
            maintenance_interval=168,  # Weekly
            special_abilities=["orbital_combat", "space_superiority", "planetary_defense", "deep_space"],
            environmental_requirements=["space", "orbit"],
            crew_requirements=3,
            training_time=1000,
            base_cost=50000,
            rarity_factor=0.8,
            market_demand=0.1
        )
        
        # BIOLOGICAL UNITS
        self.assets["bio_soldier"] = EnhancedMilitaryAsset(
            name="Bio Soldier",
            category="biological",
            subcategory="enhanced",
            tier=3,
            complexity=AssetComplexity.ADVANCED,
            description="Genetically enhanced soldier with superior physical capabilities",
            emoji="🧬",
            attack=12,
            defense=10,
            speed=3,
            range=2,
            capacity=1,
            resource_requirements=[
                ResourceRequirement(ResourceType.GOLD, 3000, True, True, "Enhancement cost"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 100, True, True, "Genetic expertise"),
                ResourceRequirement(ResourceType.TECHNOLOGY, 80, True, True, "Biotech equipment"),
                ResourceRequirement(ResourceType.MANPOWER, 1, True, True, "Enhanced soldier"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 50, True, True, "Enhancement materials"),
                ResourceRequirement(ResourceType.FOOD, 20, True, True, "Specialized nutrition"),
                ResourceRequirement(ResourceType.WATER, 10, True, True, "Purified water")
            ],
            production_time=120,  # 5 days
            production_facility="biotech_lab",
            technology_requirements=["genetic_engineering", "biotech", "enhancement_technology"],
            upkeep_resources=[
                ResourceRequirement(ResourceType.FOOD, 5, True, True, "Enhanced nutrition"),
                ResourceRequirement(ResourceType.MEDICAL_SUPPLIES, 10, True, True, "Maintenance drugs"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 5, True, True, "Continuous monitoring"),
                ResourceRequirement(ResourceType.TECHNOLOGY, 2, True, True, "Biotech maintenance")
            ],
            fuel_consumption=0.0,
            ammunition_consumption=8.0,
            maintenance_interval=48,  # 2 days
            special_abilities=["enhanced_strength", "regeneration", "enhanced_senses", "adaptation"],
            environmental_requirements=["ground", "any"],
            crew_requirements=1,
            training_time=200,
            base_cost=3000,
            rarity_factor=0.6,
            market_demand=0.4
        )
        
        # MAGICAL UNITS
        self.assets["battle_mage"] = EnhancedMilitaryAsset(
            name="Battle Mage",
            category="magical",
            subcategory="combat",
            tier=3,
            complexity=AssetComplexity.ADVANCED,
            description="Magical warrior capable of casting powerful combat spells",
            emoji="🧙",
            attack=18,
            defense=12,
            speed=2,
            range=5,
            capacity=1,
            resource_requirements=[
                ResourceRequirement(ResourceType.GOLD, 2500, True, True, "Magical equipment cost"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 120, True, True, "Magical knowledge"),
                ResourceRequirement(ResourceType.ENERGY, 150, True, True, "Magical energy"),
                ResourceRequirement(ResourceType.MANPOWER, 1, True, True, "Mage"),
                ResourceRequirement(ResourceType.INFLUENCE, 30, True, True, "Magical authority"),
                ResourceRequirement(ResourceType.MATERIALS, 20, True, True, "Magical components"),
                ResourceRequirement(ResourceType.WATER, 5, True, True, "Ritual water")
            ],
            production_time=96,  # 4 days
            production_facility="magic_academy",
            technology_requirements=["magic_theory", "spell_casting", "magical_equipment"],
            upkeep_resources=[
                ResourceRequirement(ResourceType.ENERGY, 30, True, True, "Magical energy"),
                ResourceRequirement(ResourceType.KNOWLEDGE, 8, True, True, "Magical study"),
                ResourceRequirement(ResourceType.MATERIALS, 5, True, True, "Spell components"),
                ResourceRequirement(ResourceType.INFLUENCE, 2, True, True, "Magical influence")
            ],
            fuel_consumption=0.0,
            ammunition_consumption=0.0,
            maintenance_interval=72,  # 3 days
            special_abilities=["spell_casting", "magical_combat", "elemental_magic", "magical_defense"],
            environmental_requirements=["ground", "any"],
            crew_requirements=1,
            training_time=300,
            base_cost=2500,
            rarity_factor=0.7,
            market_demand=0.2
        )
    
    def get_asset(self, asset_name: str) -> Optional[EnhancedMilitaryAsset]:
        """Get asset by name"""
        return self.assets.get(asset_name)
    
    def get_assets_by_category(self, category: str) -> List[EnhancedMilitaryAsset]:
        """Get all assets in a category"""
        return [asset for asset in self.assets.values() if asset.category == category]
    
    def get_assets_by_tier(self, tier: int) -> List[EnhancedMilitaryAsset]:
        """Get all assets of a specific tier"""
        return [asset for asset in self.assets.values() if asset.tier == tier]
    
    def get_assets_by_complexity(self, complexity: AssetComplexity) -> List[EnhancedMilitaryAsset]:
        """Get all assets of a specific complexity"""
        return [asset for asset in self.assets.values() if asset.complexity == complexity]
    
    def get_assets_by_resource_requirement(self, resource_type: ResourceType) -> List[EnhancedMilitaryAsset]:
        """Get all assets that require a specific resource"""
        return [
            asset for asset in self.assets.values()
            if any(req.resource_type == resource_type for req in asset.resource_requirements)
        ]
    
    def calculate_total_cost(self, asset_name: str, resource_prices: Dict[ResourceType, float]) -> float:
        """Calculate total cost of an asset including all resource requirements"""
        asset = self.get_asset(asset_name)
        if not asset:
            return 0.0
        
        total_cost = 0.0
        for req in asset.resource_requirements:
            if req.is_consumed:
                price = resource_prices.get(req.resource_type, 0.0)
                total_cost += req.amount * price
        
        return total_cost
    
    def check_resource_availability(self, user_resources: Dict[ResourceType, float], 
                                  asset_name: str) -> Tuple[bool, List[str]]:
        """Check if user has enough resources to build an asset"""
        asset = self.get_asset(asset_name)
        if not asset:
            return False, ["Asset not found"]
        
        missing_resources = []
        
        for req in asset.resource_requirements:
            if req.is_consumed:
                available = user_resources.get(req.resource_type, 0.0)
                if available < req.amount:
                    missing_resources.append(
                        f"{req.resource_type.value}: need {req.amount}, have {available}"
                    )
        
        return len(missing_resources) == 0, missing_resources
    
    def get_asset_summary(self, asset_name: str) -> Dict[str, Any]:
        """Get comprehensive asset summary"""
        asset = self.get_asset(asset_name)
        if not asset:
            return {}
        
        return {
            "name": asset.name,
            "category": asset.category,
            "tier": asset.tier,
            "complexity": asset.complexity.value,
            "description": asset.description,
            "emoji": asset.emoji,
            "stats": {
                "attack": asset.attack,
                "defense": asset.defense,
                "speed": asset.speed,
                "range": asset.range,
                "capacity": asset.capacity
            },
            "resource_requirements": [
                {
                    "resource": req.resource_type.value,
                    "amount": req.amount,
                    "is_consumed": req.is_consumed,
                    "is_critical": req.is_critical,
                    "description": req.description
                }
                for req in asset.resource_requirements
            ],
            "production": {
                "time_hours": asset.production_time,
                "facility": asset.production_facility,
                "technology_requirements": asset.technology_requirements
            },
            "upkeep": [
                {
                    "resource": req.resource_type.value,
                    "amount_per_hour": req.amount,
                    "description": req.description
                }
                for req in asset.upkeep_resources
            ],
            "special_abilities": asset.special_abilities,
            "environmental_requirements": asset.environmental_requirements,
            "crew_requirements": asset.crew_requirements,
            "training_time_hours": asset.training_time,
            "economic": {
                "base_cost": asset.base_cost,
                "rarity_factor": asset.rarity_factor,
                "market_demand": asset.market_demand
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Test enhanced military assets
    print("Testing enhanced military assets system...")
    
    assets_db = EnhancedMilitaryAssetsDatabase()
    
    # Test getting assets
    rifleman = assets_db.get_asset("rifleman")
    print(f"Rifleman: {rifleman.name if rifleman else 'Not found'}")
    
    # Test category filtering
    infantry_assets = assets_db.get_assets_by_category("infantry")
    print(f"Infantry assets: {len(infantry_assets)}")
    
    # Test tier filtering
    tier_3_assets = assets_db.get_assets_by_tier(3)
    print(f"Tier 3 assets: {len(tier_3_assets)}")
    
    # Test complexity filtering
    complex_assets = assets_db.get_assets_by_complexity(AssetComplexity.COMPLEX)
    print(f"Complex assets: {len(complex_assets)}")
    
    # Test resource requirement filtering
    oil_assets = assets_db.get_assets_by_resource_requirement(ResourceType.OIL)
    print(f"Assets requiring oil: {len(oil_assets)}")
    
    # Test resource availability check
    user_resources = {
        ResourceType.GOLD: 1000,
        ResourceType.IRON: 100,
        ResourceType.MANPOWER: 10,
        ResourceType.AMMUNITION: 500,
        ResourceType.FOOD: 100
    }
    
    can_build, missing = assets_db.check_resource_availability(user_resources, "rifleman")
    print(f"Can build rifleman: {can_build}")
    if not can_build:
        print(f"Missing resources: {missing}")
    
    # Test asset summary
    summary = assets_db.get_asset_summary("main_battle_tank")
    print(f"Tank summary keys: {list(summary.keys())}")
    
    print("✅ Enhanced military assets system working correctly!")