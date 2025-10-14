"""
Comprehensive Test Suite for World War Telegram Bot
"""
import asyncio
import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import bot components
from database import DatabaseManager, Player, Nation, Province, PlayerUnit, PlayerMaterial
from military_assets import MilitaryAssetsDatabase, MilitaryAsset
from economy import EconomyManager, TradeManager, DailyIncomeManager
from military import MilitaryManager, UnitUpkeepManager
from quest_system import QuestManager
from technology import TechnologyManager
from world_simulation import WorldSimulator
from admin import AdminManager
from ui_menus import UIManager

class TestMilitaryAssets:
    """Test military assets database"""
    
    def test_assets_database_creation(self):
        """Test that assets database is created correctly"""
        db = MilitaryAssetsDatabase()
        assert db.get_total_assets() > 0
        assert len(db.get_asset_categories()) > 0
    
    def test_get_asset(self):
        """Test getting specific assets"""
        db = MilitaryAssetsDatabase()
        
        # Test getting a specific asset
        rifleman = db.get_asset("Rifleman")
        assert rifleman is not None
        assert rifleman.name == "Rifleman"
        assert rifleman.category == "infantry"
        assert rifleman.tier == 1
        
        # Test getting non-existent asset
        fake = db.get_asset("Fake Unit")
        assert fake is None
    
    def test_get_assets_by_category(self):
        """Test getting assets by category"""
        db = MilitaryAssetsDatabase()
        
        infantry = db.get_assets_by_category("infantry")
        assert len(infantry) > 0
        assert all(asset.category == "infantry" for asset in infantry)
        
        armor = db.get_assets_by_category("armor")
        assert len(armor) > 0
        assert all(asset.category == "armor" for asset in armor)
    
    def test_get_assets_by_tier(self):
        """Test getting assets by tier"""
        db = MilitaryAssetsDatabase()
        
        tier1 = db.get_assets_by_tier(1)
        assert len(tier1) > 0
        assert all(asset.tier == 1 for asset in tier1)
        
        tier4 = db.get_assets_by_tier(4)
        assert len(tier4) > 0
        assert all(asset.tier == 4 for asset in tier4)
    
    def test_search_assets(self):
        """Test searching assets"""
        db = MilitaryAssetsDatabase()
        
        # Search by name
        rifle_results = db.search_assets("rifle")
        assert len(rifle_results) > 0
        
        # Search by category
        infantry_results = db.search_assets("infantry")
        assert len(infantry_results) > 0
        
        # Search by description
        stealth_results = db.search_assets("stealth")
        assert len(stealth_results) > 0
    
    def test_asset_properties(self):
        """Test asset properties are correct"""
        db = MilitaryAssetsDatabase()
        
        # Test a basic infantry unit
        rifleman = db.get_asset("Rifleman")
        assert rifleman.cost > 0
        assert rifleman.upkeep > 0
        assert rifleman.attack > 0
        assert rifleman.defense > 0
        assert rifleman.speed >= 0
        assert rifleman.range >= 0
        assert rifleman.capacity >= 0
        assert rifleman.fuel_consumption >= 0
        assert len(rifleman.description) > 0
        assert len(rifleman.emoji) > 0
        
        # Test a high-tier unit
        quantum_soldier = db.get_asset("Quantum Soldier")
        if quantum_soldier:
            assert quantum_soldier.tier == 4
            assert quantum_soldier.cost > 1000
            assert "quantum" in quantum_soldier.special_abilities

class TestDatabase:
    """Test database functionality"""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_url = f"sqlite:///{tmp.name}"
            db_manager = DatabaseManager(db_url)
            db_manager.create_tables()
            yield db_manager
            os.unlink(tmp.name)
    
    def test_database_creation(self, temp_db):
        """Test database tables are created"""
        with temp_db.get_session() as session:
            # Test that we can query the tables
            players = session.query(Player).all()
            nations = session.query(Nation).all()
            provinces = session.query(Province).all()
            units = session.query(PlayerUnit).all()
            
            assert isinstance(players, list)
            assert isinstance(nations, list)
            assert isinstance(provinces, list)
            assert isinstance(units, list)
    
    def test_player_creation(self, temp_db):
        """Test creating a player"""
        with temp_db.get_session() as session:
            player = Player(
                telegram_id=12345,
                username="testuser",
                first_name="Test",
                last_name="User",
                level=1,
                gold=1000.0
            )
            session.add(player)
            session.commit()
            
            # Verify player was created
            retrieved = session.query(Player).filter_by(telegram_id=12345).first()
            assert retrieved is not None
            assert retrieved.username == "testuser"
            assert retrieved.gold == 1000.0
    
    def test_player_units(self, temp_db):
        """Test player unit creation"""
        with temp_db.get_session() as session:
            # Create player
            player = Player(telegram_id=12345, username="testuser")
            session.add(player)
            session.commit()
            
            # Create unit
            unit = PlayerUnit(
                player_id=player.id,
                unit_name="Rifleman",
                unit_type="infantry",
                subcategory="basic",
                tier=1,
                quantity=10
            )
            session.add(unit)
            session.commit()
            
            # Verify unit was created
            retrieved = session.query(PlayerUnit).filter_by(player_id=player.id).first()
            assert retrieved is not None
            assert retrieved.unit_name == "Rifleman"
            assert retrieved.quantity == 10

class TestEconomy:
    """Test economy system"""
    
    def test_economy_manager_creation(self):
        """Test economy manager initialization"""
        config = {
            "materials": {
                "iron": {"base_price": 10, "volatility": 0.1},
                "oil": {"base_price": 15, "volatility": 0.15}
            },
            "price_update_interval": 1800
        }
        
        economy = EconomyManager(config)
        assert economy is not None
        assert len(economy.get_current_prices()) > 0
    
    def test_price_calculation(self):
        """Test price calculation"""
        config = {
            "materials": {
                "iron": {"base_price": 10, "volatility": 0.1},
                "oil": {"base_price": 15, "volatility": 0.15}
            },
            "price_update_interval": 1800
        }
        
        economy = EconomyManager(config)
        prices = economy.get_current_prices()
        
        assert "iron" in prices
        assert "oil" in prices
        assert prices["iron"]["price"] > 0
        assert prices["oil"]["price"] > 0
    
    def test_trade_cost_calculation(self):
        """Test trade cost calculation"""
        config = {
            "materials": {
                "iron": {"base_price": 10, "volatility": 0.1}
            },
            "price_update_interval": 1800
        }
        
        economy = EconomyManager(config)
        cost = economy.calculate_trade_cost("iron", 100)
        assert cost > 0
        assert cost == economy.current_prices["iron"] * 100

class TestMilitary:
    """Test military system"""
    
    def test_military_manager_creation(self):
        """Test military manager initialization"""
        config = {
            "unit_types": {
                "infantry": {"cost": 100, "upkeep": 10, "attack": 5, "defense": 3, "speed": 1}
            },
            "battle_cooldown": 300
        }
        
        military = MilitaryManager(config)
        assert military is not None
        assert military.assets_db is not None
    
    def test_unit_cost_calculation(self):
        """Test unit cost calculation"""
        config = {
            "unit_types": {
                "infantry": {"cost": 100, "upkeep": 10, "attack": 5, "defense": 3, "speed": 1}
            },
            "battle_cooldown": 300
        }
        
        military = MilitaryManager(config)
        
        # Test with new assets system
        cost = military.calculate_unit_cost("Rifleman", 10)
        assert cost > 0
        
        # Test with legacy system
        cost = military.calculate_unit_cost("infantry", 10)
        assert cost == 1000  # 100 * 10
    
    def test_combat_power_calculation(self):
        """Test combat power calculation"""
        config = {
            "unit_types": {
                "infantry": {"cost": 100, "upkeep": 10, "attack": 5, "defense": 3, "speed": 1}
            },
            "battle_cooldown": 300
        }
        
        military = MilitaryManager(config)
        
        # Test with new assets
        units = {"Rifleman": 10}
        power = military.calculate_combat_power(units)
        assert power > 0
        
        # Test with legacy system
        units = {"infantry": 10}
        power = military.calculate_combat_power(units)
        assert power > 0

class TestQuestSystem:
    """Test quest system"""
    
    def test_quest_manager_creation(self):
        """Test quest manager initialization"""
        quest_manager = QuestManager()
        assert quest_manager is not None
        assert len(quest_manager.quest_templates) > 0
    
    def test_quest_generation(self):
        """Test quest generation"""
        quest_manager = QuestManager()
        
        # Test generating different quest types
        for quest_type in quest_manager.quest_templates.keys():
            quest = quest_manager.generate_random_quest(quest_type, 1)
            assert quest is not None
            assert quest.quest_type == quest_type
            assert quest.difficulty >= 1
            assert quest.duration > 0
            assert len(quest.title) > 0
            assert len(quest.description) > 0

class TestTechnology:
    """Test technology system"""
    
    def test_technology_manager_creation(self):
        """Test technology manager initialization"""
        tech_manager = TechnologyManager()
        assert tech_manager is not None
        assert len(tech_manager.technology_tree) > 0
    
    def test_technology_tree_structure(self):
        """Test technology tree structure"""
        tech_manager = TechnologyManager()
        
        # Test that all categories exist
        categories = ["military", "economic", "research"]
        for category in categories:
            assert category in tech_manager.technology_tree
        
        # Test that tiers exist
        for category in tech_manager.technology_tree.values():
            for tier_name, technologies in category.items():
                assert tier_name.startswith("tier_")
                assert isinstance(technologies, list)
                assert len(technologies) > 0

class TestUI:
    """Test UI system"""
    
    def test_ui_manager_creation(self):
        """Test UI manager initialization"""
        ui = UIManager()
        assert ui is not None
        assert len(ui.emoji_map) > 0
    
    def test_keyboard_creation(self):
        """Test keyboard creation"""
        ui = UIManager()
        
        # Test main menu keyboard
        keyboard = ui.get_main_menu_keyboard()
        assert keyboard is not None
        
        # Test other keyboards
        keyboards = [
            ui.get_economy_menu_keyboard(),
            ui.get_military_menu_keyboard(),
            ui.get_quest_menu_keyboard(),
            ui.get_research_menu_keyboard(),
            ui.get_alliance_menu_keyboard()
        ]
        
        for kb in keyboards:
            assert kb is not None

class TestIntegration:
    """Integration tests"""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database for integration tests"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_url = f"sqlite:///{tmp.name}"
            db_manager = DatabaseManager(db_url)
            db_manager.create_tables()
            yield db_manager
            os.unlink(tmp.name)
    
    def test_full_player_workflow(self, temp_db):
        """Test complete player workflow"""
        # Create player
        with temp_db.get_session() as session:
            player = Player(
                telegram_id=12345,
                username="testuser",
                first_name="Test",
                last_name="User",
                gold=1000.0
            )
            session.add(player)
            session.commit()
            
            # Add materials
            iron = PlayerMaterial(
                player_id=player.id,
                material_type="iron",
                quantity=100.0
            )
            session.add(iron)
            session.commit()
            
            # Create military manager
            config = {
                "unit_types": {
                    "infantry": {"cost": 100, "upkeep": 10, "attack": 5, "defense": 3, "speed": 1}
                },
                "battle_cooldown": 300
            }
            military = MilitaryManager(config)
            military.db = temp_db
            
            # Build units
            success = military.build_units(player.id, "Rifleman", 5)
            assert success
            
            # Verify units were created
            units = military.get_player_units(player.id)
            assert len(units) > 0
            
            # Test combat power calculation
            total_units = military.get_total_units(player.id)
            power = military.calculate_combat_power(total_units)
            assert power > 0

def run_tests():
    """Run all tests"""
    print("🧪 Running comprehensive tests...")
    
    # Test military assets
    print("Testing military assets...")
    test_assets = TestMilitaryAssets()
    test_assets.test_assets_database_creation()
    test_assets.test_get_asset()
    test_assets.test_get_assets_by_category()
    test_assets.test_get_assets_by_tier()
    test_assets.test_search_assets()
    test_assets.test_asset_properties()
    print("✅ Military assets tests passed")
    
    # Test database
    print("Testing database...")
    test_db = TestDatabase()
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_url = f"sqlite:///{tmp.name}"
        temp_db = DatabaseManager(db_url)
        temp_db.create_tables()
        test_db.test_database_creation(temp_db)
        test_db.test_player_creation(temp_db)
        test_db.test_player_units(temp_db)
        os.unlink(tmp.name)
    print("✅ Database tests passed")
    
    # Test economy
    print("Testing economy...")
    test_economy = TestEconomy()
    test_economy.test_economy_manager_creation()
    test_economy.test_price_calculation()
    test_economy.test_trade_cost_calculation()
    print("✅ Economy tests passed")
    
    # Test military
    print("Testing military...")
    test_military = TestMilitary()
    test_military.test_military_manager_creation()
    test_military.test_unit_cost_calculation()
    test_military.test_combat_power_calculation()
    print("✅ Military tests passed")
    
    # Test quest system
    print("Testing quest system...")
    test_quest = TestQuestSystem()
    test_quest.test_quest_manager_creation()
    test_quest.test_quest_generation()
    print("✅ Quest system tests passed")
    
    # Test technology
    print("Testing technology...")
    test_tech = TestTechnology()
    test_tech.test_technology_manager_creation()
    test_tech.test_technology_tree_structure()
    print("✅ Technology tests passed")
    
    # Test UI
    print("Testing UI...")
    test_ui = TestUI()
    test_ui.test_ui_manager_creation()
    test_ui.test_keyboard_creation()
    print("✅ UI tests passed")
    
    # Test integration
    print("Testing integration...")
    test_integration = TestIntegration()
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_url = f"sqlite:///{tmp.name}"
        temp_db = DatabaseManager(db_url)
        temp_db.create_tables()
        test_integration.test_full_player_workflow(temp_db)
        os.unlink(tmp.name)
    print("✅ Integration tests passed")
    
    print("\n🎉 All tests passed successfully!")
    print(f"📊 Military Assets: {MilitaryAssetsDatabase().get_total_assets()} units available")
    print("🚀 Bot is ready for deployment!")

if __name__ == "__main__":
    run_tests()