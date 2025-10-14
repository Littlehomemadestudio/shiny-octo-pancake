"""
Simple Test Suite for World War Telegram Bot
"""
import tempfile
import os

def test_military_assets():
    """Test military assets database"""
    print("Testing military assets...")
    
    from military_assets import MilitaryAssetsDatabase
    
    # Test database creation
    db = MilitaryAssetsDatabase()
    total_assets = db.get_total_assets()
    print(f"✅ Total assets: {total_assets}")
    assert total_assets > 0
    
    # Test getting specific asset
    rifleman = db.get_asset("Rifleman")
    assert rifleman is not None
    assert rifleman.name == "Rifleman"
    assert rifleman.category == "infantry"
    print(f"✅ Rifleman: {rifleman.name} - {rifleman.cost} gold")
    
    # Test categories
    categories = db.get_asset_categories()
    print(f"✅ Categories: {categories}")
    assert len(categories) > 0
    
    # Test getting assets by category
    infantry = db.get_assets_by_category("infantry")
    print(f"✅ Infantry units: {len(infantry)}")
    assert len(infantry) > 0
    
    # Test search
    stealth_results = db.search_assets("stealth")
    print(f"✅ Stealth units: {len(stealth_results)}")
    assert len(stealth_results) > 0
    
    print("✅ Military assets tests passed\n")

def test_database():
    """Test database functionality"""
    print("Testing database...")
    
    from database import DatabaseManager, Player, PlayerUnit
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_url = f"sqlite:///{tmp.name}"
        db_manager = DatabaseManager(db_url)
        db_manager.create_tables()
        
        # Test player creation
        with db_manager.get_session() as session:
            player = Player(
                telegram_id=12345,
                username="testuser",
                first_name="Test",
                last_name="User",
                gold=1000.0
            )
            session.add(player)
            session.commit()
            
            # Test unit creation
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
            
            # Verify creation
            retrieved_player = session.query(Player).filter_by(telegram_id=12345).first()
            assert retrieved_player is not None
            assert retrieved_player.gold == 1000.0
            
            retrieved_unit = session.query(PlayerUnit).filter_by(player_id=player.id).first()
            assert retrieved_unit is not None
            assert retrieved_unit.unit_name == "Rifleman"
            assert retrieved_unit.quantity == 10
            
            print(f"✅ Player created: {retrieved_player.first_name}")
            print(f"✅ Unit created: {retrieved_unit.unit_name} x{retrieved_unit.quantity}")
        
        os.unlink(tmp.name)
    
    print("✅ Database tests passed\n")

def test_economy():
    """Test economy system"""
    print("Testing economy...")
    
    from economy import EconomyManager
    
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
    
    print(f"✅ Iron price: {prices['iron']['price']:.2f}")
    print(f"✅ Oil price: {prices['oil']['price']:.2f}")
    
    # Test trade cost calculation
    cost = economy.calculate_trade_cost("iron", 100)
    assert cost > 0
    print(f"✅ Trade cost for 100 iron: {cost:.2f}")
    
    print("✅ Economy tests passed\n")

def test_military():
    """Test military system"""
    print("Testing military...")
    
    from military import MilitaryManager
    
    config = {
        "unit_types": {
            "infantry": {"cost": 100, "upkeep": 10, "attack": 5, "defense": 3, "speed": 1}
        },
        "battle_cooldown": 300
    }
    
    military = MilitaryManager(config)
    
    # Test unit cost calculation
    cost = military.calculate_unit_cost("Rifleman", 10)
    assert cost > 0
    print(f"✅ Rifleman cost (10 units): {cost}")
    
    # Test combat power calculation
    units = {"Rifleman": 10}
    power = military.calculate_combat_power(units)
    assert power > 0
    print(f"✅ Combat power: {power:.2f}")
    
    print("✅ Military tests passed\n")

def test_quest_system():
    """Test quest system"""
    print("Testing quest system...")
    
    from quest_system import QuestManager
    
    quest_manager = QuestManager()
    
    # Test quest generation
    quest = quest_manager.generate_random_quest("recon", 1)
    assert quest is not None
    assert quest.quest_type == "recon"
    assert quest.difficulty >= 1
    assert quest.duration > 0
    
    print(f"✅ Generated quest: {quest.title}")
    print(f"✅ Difficulty: {quest.difficulty}, Duration: {quest.duration}s")
    
    print("✅ Quest system tests passed\n")

def test_technology():
    """Test technology system"""
    print("Testing technology...")
    
    from technology import TechnologyManager
    
    tech_manager = TechnologyManager()
    
    # Test technology tree
    categories = ["military", "economic", "research"]
    for category in categories:
        assert category in tech_manager.technology_tree
        tiers = tech_manager.technology_tree[category]
        assert len(tiers) > 0
    
    print(f"✅ Technology categories: {list(tech_manager.technology_tree.keys())}")
    
    print("✅ Technology tests passed\n")

def test_ui():
    """Test UI system"""
    print("Testing UI...")
    
    from ui_menus import UIManager
    
    ui = UIManager()
    
    # Test keyboard creation
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
    
    print("✅ UI keyboards created successfully")
    
    print("✅ UI tests passed\n")

def test_integration():
    """Test integration"""
    print("Testing integration...")
    
    from database import DatabaseManager, Player, PlayerUnit
    from military import MilitaryManager
    import tempfile
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_url = f"sqlite:///{tmp.name}"
        db_manager = DatabaseManager(db_url)
        db_manager.create_tables()
        
        # Create player
        with db_manager.get_session() as session:
            player = Player(
                telegram_id=12345,
                username="testuser",
                first_name="Test",
                last_name="User",
                gold=1000.0
            )
            session.add(player)
            session.commit()
            
            # Create military manager
            config = {
                "unit_types": {
                    "infantry": {"cost": 100, "upkeep": 10, "attack": 5, "defense": 3, "speed": 1}
                },
                "battle_cooldown": 300
            }
            military = MilitaryManager(config)
            military.db = db_manager
            
            # Test building units
            success = military.build_units(player.id, "Rifleman", 5)
            assert success
            
            # Verify units were created
            units = military.get_player_units(player.id)
            assert len(units) > 0
            
            # Test combat power calculation
            total_units = military.get_total_units(player.id)
            power = military.calculate_combat_power(total_units)
            assert power > 0
            
            print(f"✅ Player: {player.first_name}")
            print(f"✅ Units built: {len(units)}")
            print(f"✅ Combat power: {power:.2f}")
        
        os.unlink(tmp.name)
    
    print("✅ Integration tests passed\n")

def main():
    """Run all tests"""
    print("🧪 Running comprehensive tests...\n")
    
    try:
        test_military_assets()
        test_database()
        test_economy()
        test_military()
        test_quest_system()
        test_technology()
        test_ui()
        test_integration()
        
        print("🎉 All tests passed successfully!")
        print("🚀 Bot is ready for deployment!")
        
        # Show asset count
        from military_assets import MilitaryAssetsDatabase
        db = MilitaryAssetsDatabase()
        print(f"📊 Military Assets: {db.get_total_assets()} units available")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()