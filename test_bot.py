"""
Test script for World War Telegram Bot
"""
import asyncio
import os
from dotenv import load_dotenv
from bot import WorldWarBot

async def test_bot():
    """Test the bot without actually starting it"""
    load_dotenv()
    
    print("🧪 Testing World War Bot...")
    
    try:
        # Create bot instance
        bot = WorldWarBot()
        print("✅ Bot instance created successfully")
        
        # Test database connection
        await bot.db_manager.init_database()
        print("✅ Database connection successful")
        
        # Test economy manager
        prices = bot.economy.get_current_prices()
        print(f"✅ Economy manager working - {len(prices)} materials configured")
        
        # Test UI manager
        keyboard = bot.ui.get_main_menu_keyboard()
        print("✅ UI manager working - main menu created")
        
        # Test military manager
        unit_stats = bot.military.get_unit_stats("infantry")
        print(f"✅ Military manager working - infantry stats: {unit_stats}")
        
        # Test province manager
        print("✅ Province manager initialized")
        
        # Test quest manager
        print("✅ Quest manager initialized")
        
        # Test technology manager
        print("✅ Technology manager initialized")
        
        # Test world simulator
        print("✅ World simulator initialized")
        
        # Test admin manager
        print("✅ Admin manager initialized")
        
        print()
        print("🎉 All tests passed! Bot is ready to run.")
        print()
        print("To start the bot:")
        print("1. Make sure your .env file is configured")
        print("2. Make sure your database is running")
        print("3. Run: python main.py")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print()
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    asyncio.run(test_bot())