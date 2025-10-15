"""
Simplified Telegram Bot for World War Strategy Game
No environment variables, no admin requirements, simple text file storage
"""
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from simple_storage import SimpleStorage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameStates(StatesGroup):
    waiting_for_trade_quantity = State()
    waiting_for_trade_price = State()

class SimpleWorldWarBot:
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.bot = Bot(token=self.config["bot"]["token"])
        self.dp = Dispatcher(storage=MemoryStorage())
        
        # Initialize simple storage
        self.storage = SimpleStorage()
        
        # Game state
        self.player_cooldowns = {}
        
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all bot command and callback handlers"""
        
        # Basic commands
        self.dp.message.register(self.start_command, CommandStart())
        self.dp.message.register(self.help_command, Command("help"))
        self.dp.message.register(self.status_command, Command("status"))
        self.dp.message.register(self.profile_command, Command("profile"))
        
        # Economy commands
        self.dp.message.register(self.economy_command, Command("economy"))
        self.dp.message.register(self.trade_command, Command("trade"))
        self.dp.message.register(self.materials_command, Command("materials"))
        
        # Military commands
        self.dp.message.register(self.military_command, Command("military"))
        self.dp.message.register(self.attack_command, Command("attack"))
        self.dp.message.register(self.build_units_command, Command("build"))
        
        # Quest commands
        self.dp.message.register(self.quest_command, Command("quest"))
        self.dp.message.register(self.missions_command, Command("missions"))
        
        # Callback handlers
        self.dp.callback_query.register(self.handle_callback, F.data.startswith("game_"))
        
        # Error handler
        self.dp.errors.register(self.error_handler)
    
    async def start_command(self, message: types.Message):
        """Handle /start command"""
        user_id = message.from_user.id
        
        # Check if user exists
        player = self.storage.load_player(user_id)
        
        if not player:
            # Create new player
            player = {
                'telegram_id': user_id,
                'username': message.from_user.username or "Unknown",
                'first_name': message.from_user.first_name or "Unknown",
                'last_name': message.from_user.last_name or "",
                'level': 1,
                'experience': 0,
                'rank': "Commander",
                'gold': 1000.0,
                'morale': 100.0,
                'last_active': datetime.now().isoformat(),
                'created_at': datetime.now().isoformat(),
                'is_banned': False,
                'language': message.from_user.language_code or "en"
            }
            
            # Initialize player materials
            materials = {}
            for material in self.config["economy"]["materials"]:
                materials[material] = 100.0  # Starting materials
            
            # Initialize player units
            units = {}
            for unit_type in self.config["military"]["unit_types"]:
                units[unit_type] = 0
            
            # Save player data
            self.storage.save_player(player)
            self.storage.save_materials(user_id, materials)
            self.storage.save_units(user_id, units)
            self.storage.save_quests(user_id, [])
            
            welcome_text = f"""
🎖️ **Welcome to {self.config['game']['world_name']}, Commander!**

You have been assigned to lead a new nation in this world of conflict and strategy.

**Your Starting Resources:**
💰 Gold: 1,000
🛠️ Iron: 100
⛽ Oil: 100
🌾 Food: 100
🥇 Gold: 100
☢️ Uranium: 100

**Quick Commands:**
/status - View your nation's status
/military - Manage your armed forces
/economy - Trade and manage resources
/quest - Take on missions

Good luck, Commander! The world awaits your leadership.
            """
        else:
            welcome_text = f"""
🎖️ **Welcome back, {player['rank']} {player['first_name']}!**

Your nation stands ready for new challenges.

**Current Status:**
💰 Gold: {player['gold']:,.0f}
⭐ Level: {player['level']}
🏆 Rank: {player['rank']}
💪 Morale: {player['morale']:.0f}%

Use /help to see all available commands.
            """
        
        keyboard = self.get_main_menu_keyboard()
        await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")
    
    async def help_command(self, message: types.Message):
        """Handle /help command"""
        help_text = """
🎖️ **World War Strategy Bot - Commands**

**🏠 Basic Commands:**
/start - Start playing or view status
/status - Your nation's current status
/profile - Detailed player profile
/help - Show this help message

**💰 Economy:**
/economy - Economic overview and trading
/trade - Open trading interface
/materials - View your resources

**⚔️ Military:**
/military - Military management
/attack - Attack other players or provinces
/build - Build military units

**🎯 Missions:**
/quest - Available quests and missions
/missions - Your active missions

Use inline keyboards for easy navigation!
        """
        await message.answer(help_text, parse_mode="Markdown")
    
    async def status_command(self, message: types.Message):
        """Handle /status command"""
        user_id = message.from_user.id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.answer("❌ You need to start the game first with /start")
            return
        
        # Get player materials and units
        materials = self.storage.load_materials(user_id)
        units = self.storage.load_units(user_id)
        
        total_units = sum(units.values())
        
        status_text = f"""
🎖️ **{player['rank']} {player['first_name']}**

**📊 Basic Stats:**
💰 Gold: {player['gold']:,.0f}
⭐ Level: {player['level']} (XP: {player['experience']:,})
💪 Morale: {player['morale']:.0f}%
🛡️ Total Units: {total_units:,}

**📦 Resources:**
🛠️ Iron: {materials.get('iron', 0):,.0f}
⛽ Oil: {materials.get('oil', 0):,.0f}
🌾 Food: {materials.get('food', 0):,.0f}
🥇 Gold: {materials.get('gold', 0):,.0f}
☢️ Uranium: {materials.get('uranium', 0):,.0f}
🔩 Steel: {materials.get('steel', 0):,.0f}

**🌍 Language:** {player['language'].upper()}
**⏰ Last Active:** {player['last_active'][:16]}
        """
        
        keyboard = self.get_status_menu_keyboard()
        await message.answer(status_text, reply_markup=keyboard, parse_mode="Markdown")
    
    async def profile_command(self, message: types.Message):
        """Handle /profile command"""
        user_id = message.from_user.id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.answer("❌ You need to start the game first with /start")
            return
        
        # Get detailed stats
        materials = self.storage.load_materials(user_id)
        units = self.storage.load_units(user_id)
        
        profile_text = f"""
👤 **Detailed Profile - {player['rank']} {player['first_name']}**

**🎖️ Military Rank:** {player['rank']}
**⭐ Experience Level:** {player['level']}
**💯 Experience Points:** {player['experience']:,}
**💰 Treasury:** {player['gold']:,.0f} gold
**💪 Morale:** {player['morale']:.0f}%

**📦 Resource Inventory:**
"""
        for material, quantity in materials.items():
            emoji = {"iron": "🛠️", "oil": "⛽", "food": "🌾", "gold": "🥇", "uranium": "☢️", "steel": "🔩"}.get(material, "📦")
            profile_text += f"{emoji} {material.title()}: {quantity:,.0f}\n"
        
        profile_text += f"""
**⚔️ Military Forces:**
"""
        for unit_type, quantity in units.items():
            emoji = {"infantry": "👥", "tank": "🚗", "artillery": "💣", "aircraft": "✈️", "ship": "🚢"}.get(unit_type, "⚔️")
            profile_text += f"{emoji} {unit_type.title()}: {quantity:,}\n"
        
        profile_text += f"""
**🌍 Language:** {player['language'].upper()}
**📅 Member Since:** {player['created_at'][:10]}
**⏰ Last Active:** {player['last_active'][:16]}
        """
        
        await message.answer(profile_text, parse_mode="Markdown")
    
    async def economy_command(self, message: types.Message):
        """Handle /economy command"""
        user_id = message.from_user.id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.answer("❌ You need to start the game first with /start")
            return
        
        # Get current market prices
        prices = self.config["economy"]["materials"]
        
        economy_text = f"""
💰 **Economic Overview**

**📈 Current Market Prices:**
"""
        for material, price_info in prices.items():
            emoji = {"iron": "🛠️", "oil": "⛽", "food": "🌾", "gold": "🥇", "uranium": "☢️", "steel": "🔩"}.get(material, "📦")
            economy_text += f"{emoji} {material.title()}: {price_info['base_price']:.2f} gold/unit\n"
        
        economy_text += f"""
**💼 Your Resources:**
"""
        materials = self.storage.load_materials(user_id)
        for material, quantity in materials.items():
            emoji = {"iron": "🛠️", "oil": "⛽", "food": "🌾", "gold": "🥇", "uranium": "☢️", "steel": "🔩"}.get(material, "📦")
            economy_text += f"{emoji} {material.title()}: {quantity:,.0f}\n"
        
        economy_text += f"""
**💰 Treasury:** {player['gold']:,.0f} gold

Use /trade to buy and sell resources!
        """
        
        keyboard = self.get_economy_menu_keyboard()
        await message.answer(economy_text, reply_markup=keyboard, parse_mode="Markdown")
    
    async def trade_command(self, message: types.Message):
        """Handle /trade command"""
        keyboard = self.get_trade_menu_keyboard()
        await message.answer("💼 **Trading Center**\n\nSelect what you want to do:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def materials_command(self, message: types.Message):
        """Handle /materials command"""
        user_id = message.from_user.id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.answer("❌ You need to start the game first with /start")
            return
        
        materials = self.storage.load_materials(user_id)
        
        materials_text = "📦 **Your Materials Inventory**\n\n"
        
        for material, quantity in materials.items():
            emoji = {"iron": "🛠️", "oil": "⛽", "food": "🌾", "gold": "🥇", "uranium": "☢️", "steel": "🔩"}.get(material, "📦")
            materials_text += f"{emoji} **{material.title()}**: {quantity:,.0f} units\n"
        
        await message.answer(materials_text, parse_mode="Markdown")
    
    async def military_command(self, message: types.Message):
        """Handle /military command"""
        user_id = message.from_user.id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.answer("❌ You need to start the game first with /start")
            return
        
        # Get player units
        units = self.storage.load_units(user_id)
        total_units = sum(units.values())
        
        military_text = f"""
⚔️ **Military Overview**

**👥 Total Forces:** {total_units:,} units

**📊 Unit Breakdown:**
"""
        for unit_type, quantity in units.items():
            emoji = {"infantry": "👥", "tank": "🚗", "artillery": "💣", "aircraft": "✈️", "ship": "🚢"}.get(unit_type, "⚔️")
            military_text += f"{emoji} {unit_type.title()}: {quantity:,}\n"
        
        if total_units == 0:
            military_text += "\n❌ You have no military units. Use /build to create your army!"
        else:
            military_text += f"\n💪 **Morale:** {player['morale']:.0f}%"
        
        keyboard = self.get_military_menu_keyboard()
        await message.answer(military_text, reply_markup=keyboard, parse_mode="Markdown")
    
    async def attack_command(self, message: types.Message):
        """Handle /attack command"""
        keyboard = self.get_attack_menu_keyboard()
        await message.answer("⚔️ **Combat Center**\n\nSelect your target:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def build_units_command(self, message: types.Message):
        """Handle /build command"""
        keyboard = self.get_build_menu_keyboard()
        await message.answer("🏭 **Unit Production**\n\nSelect unit type to build:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def quest_command(self, message: types.Message):
        """Handle /quest command"""
        keyboard = self.get_quest_menu_keyboard()
        await message.answer("🎯 **Quest Center**\n\nTake on missions:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def missions_command(self, message: types.Message):
        """Handle /missions command"""
        user_id = message.from_user.id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.answer("❌ You need to start the game first with /start")
            return
        
        # Get active quests
        quests = self.storage.load_quests(user_id)
        active_quests = [q for q in quests if q.get('status') == 'active']
        
        if not active_quests:
            missions_text = "🎯 **Active Missions**\n\n❌ You have no active missions.\n\nUse /quest to find new missions!"
        else:
            missions_text = "🎯 **Active Missions**\n\n"
            for quest in active_quests:
                progress = quest.get('progress', 0) * 100
                missions_text += f"**{quest.get('title', 'Unknown Quest')}**\n"
                missions_text += f"Progress: {progress:.0f}%\n"
                missions_text += f"Type: {quest.get('type', 'Unknown')}\n\n"
        
        await message.answer(missions_text, parse_mode="Markdown")
    
    async def handle_callback(self, callback_query: CallbackQuery):
        """Handle inline keyboard callbacks"""
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        try:
            if data.startswith("game_main_"):
                await self.handle_main_menu_callback(callback_query)
            elif data.startswith("game_economy_"):
                await self.handle_economy_callback(callback_query)
            elif data.startswith("game_military_"):
                await self.handle_military_callback(callback_query)
            elif data.startswith("game_trade_"):
                await self.handle_trade_callback(callback_query)
            elif data.startswith("game_quest_"):
                await self.handle_quest_callback(callback_query)
            else:
                await callback_query.answer("❌ Unknown action")
        except Exception as e:
            logger.error(f"Error handling callback {data}: {e}")
            await callback_query.answer("❌ An error occurred")
    
    async def handle_main_menu_callback(self, callback_query: CallbackQuery):
        """Handle main menu callbacks"""
        data = callback_query.data
        
        if data == "game_main_status":
            await self.status_command(callback_query.message)
        elif data == "game_main_economy":
            await self.economy_command(callback_query.message)
        elif data == "game_main_military":
            await self.military_command(callback_query.message)
        elif data == "game_main_quest":
            await self.quest_command(callback_query.message)
        
        await callback_query.answer()
    
    async def handle_economy_callback(self, callback_query: CallbackQuery):
        """Handle economy menu callbacks"""
        data = callback_query.data
        
        if data == "game_economy_trade":
            await self.trade_command(callback_query.message)
        elif data == "game_economy_materials":
            await self.materials_command(callback_query.message)
        elif data == "game_economy_prices":
            await self.economy_command(callback_query.message)
        
        await callback_query.answer()
    
    async def handle_military_callback(self, callback_query: CallbackQuery):
        """Handle military menu callbacks"""
        data = callback_query.data
        
        if data == "game_military_attack":
            await self.attack_command(callback_query.message)
        elif data == "game_military_build":
            await self.build_units_command(callback_query.message)
        elif data == "game_military_units":
            await self.military_command(callback_query.message)
        
        await callback_query.answer()
    
    async def handle_trade_callback(self, callback_query: CallbackQuery):
        """Handle trade menu callbacks"""
        data = callback_query.data
        
        if data == "game_trade_buy":
            await callback_query.message.answer("💼 **Buy Resources**\n\nFeature coming soon! Use /materials to view your current resources.")
        elif data == "game_trade_sell":
            await callback_query.message.answer("💼 **Sell Resources**\n\nFeature coming soon! Use /materials to view your current resources.")
        elif data == "game_trade_market":
            await callback_query.message.answer("📈 **Market Overview**\n\nFeature coming soon! Use /economy to view current prices.")
        
        await callback_query.answer()
    
    async def handle_quest_callback(self, callback_query: CallbackQuery):
        """Handle quest menu callbacks"""
        data = callback_query.data
        
        if data == "game_quest_available":
            await callback_query.message.answer("🎯 **Available Quests**\n\nFeature coming soon! Check back later for exciting missions.")
        elif data == "game_quest_active":
            await self.missions_command(callback_query.message)
        
        await callback_query.answer()
    
    async def error_handler(self, event, exception):
        """Handle errors"""
        logger.error(f"Error occurred: {exception}")
        return True
    
    # Keyboard builders
    def get_main_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get main menu keyboard"""
        builder = InlineKeyboardBuilder()
        builder.button(text="📊 Status", callback_data="game_main_status")
        builder.button(text="💰 Economy", callback_data="game_main_economy")
        builder.button(text="⚔️ Military", callback_data="game_main_military")
        builder.button(text="🎯 Quests", callback_data="game_main_quest")
        builder.adjust(2)
        return builder.as_markup()
    
    def get_status_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get status menu keyboard"""
        builder = InlineKeyboardBuilder()
        builder.button(text="💰 Economy", callback_data="game_main_economy")
        builder.button(text="⚔️ Military", callback_data="game_main_military")
        builder.button(text="🎯 Quests", callback_data="game_main_quest")
        builder.button(text="📋 Profile", callback_data="game_main_profile")
        builder.adjust(2)
        return builder.as_markup()
    
    def get_economy_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get economy menu keyboard"""
        builder = InlineKeyboardBuilder()
        builder.button(text="💼 Trade", callback_data="game_economy_trade")
        builder.button(text="📦 Materials", callback_data="game_economy_materials")
        builder.button(text="📈 Prices", callback_data="game_economy_prices")
        builder.button(text="🏠 Main Menu", callback_data="game_main_status")
        builder.adjust(2)
        return builder.as_markup()
    
    def get_military_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get military menu keyboard"""
        builder = InlineKeyboardBuilder()
        builder.button(text="⚔️ Attack", callback_data="game_military_attack")
        builder.button(text="🏭 Build Units", callback_data="game_military_build")
        builder.button(text="👥 My Units", callback_data="game_military_units")
        builder.button(text="🏠 Main Menu", callback_data="game_main_status")
        builder.adjust(2)
        return builder.as_markup()
    
    def get_trade_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get trade menu keyboard"""
        builder = InlineKeyboardBuilder()
        builder.button(text="💰 Buy Resources", callback_data="game_trade_buy")
        builder.button(text="💸 Sell Resources", callback_data="game_trade_sell")
        builder.button(text="📈 Market", callback_data="game_trade_market")
        builder.button(text="🏠 Main Menu", callback_data="game_main_economy")
        builder.adjust(2)
        return builder.as_markup()
    
    def get_attack_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get attack menu keyboard"""
        builder = InlineKeyboardBuilder()
        builder.button(text="👤 Attack Player", callback_data="game_attack_player")
        builder.button(text="🏰 Attack Province", callback_data="game_attack_province")
        builder.button(text="🏠 Main Menu", callback_data="game_main_military")
        builder.adjust(2)
        return builder.as_markup()
    
    def get_build_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get build menu keyboard"""
        builder = InlineKeyboardBuilder()
        for unit_type in self.config["military"]["unit_types"]:
            builder.button(text=f"🏭 Build {unit_type.title()}", callback_data=f"game_build_{unit_type}")
        builder.button(text="🏠 Main Menu", callback_data="game_main_military")
        builder.adjust(2)
        return builder.as_markup()
    
    def get_quest_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get quest menu keyboard"""
        builder = InlineKeyboardBuilder()
        builder.button(text="🎯 Available Quests", callback_data="game_quest_available")
        builder.button(text="📋 My Missions", callback_data="game_quest_active")
        builder.button(text="🏠 Main Menu", callback_data="game_main_status")
        builder.adjust(2)
        return builder.as_markup()
    
    async def start(self):
        """Start the bot"""
        logger.info("Starting Simple World War Bot...")
        
        # Start polling
        await self.dp.start_polling(self.bot)
    
    async def stop(self):
        """Stop the bot"""
        logger.info("Stopping Simple World War Bot...")
        await self.bot.session.close()

if __name__ == "__main__":
    bot = SimpleWorldWarBot()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        asyncio.run(bot.stop())