"""
Main Telegram Bot for World War Strategy Game
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

from database import DatabaseManager, Player, Nation, Province, PlayerMaterial, PlayerUnit
from economy import EconomyManager, TradeManager, DailyIncomeManager
from military import MilitaryManager, UnitUpkeepManager
from military_assets import MilitaryAssetsDatabase
from province_manager import ProvinceManager
from quest_system import QuestManager
from technology import TechnologyManager
from world_simulation import WorldSimulator
from admin import AdminManager
from ui_menus import UIManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameStates(StatesGroup):
    waiting_for_trade_quantity = State()
    waiting_for_trade_price = State()
    waiting_for_alliance_response = State()
    waiting_for_battle_confirmation = State()

class WorldWarBot:
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.bot = Bot(token=self.config["bot"]["token"])
        self.dp = Dispatcher(storage=MemoryStorage())
        
        # Initialize managers
        self.db_manager = DatabaseManager(self.config["database"]["url"])
        self.economy = EconomyManager(self.config["economy"])
        self.trade_manager = TradeManager(self.db_manager, self.economy)
        self.daily_income = DailyIncomeManager(self.db_manager, self.config["game"])
        self.military = MilitaryManager(self.config["military"])
        self.military.db = self.db_manager  # Set database reference
        self.unit_upkeep = UnitUpkeepManager(self.db_manager, self.config["military"])
        self.province_manager = ProvinceManager()
        self.province_manager.db = self.db_manager  # Set database reference
        self.quest_manager = QuestManager()
        self.quest_manager.db = self.db_manager  # Set database reference
        self.technology = TechnologyManager()
        self.technology.db = self.db_manager  # Set database reference
        self.world_simulator = WorldSimulator(self.config["world"])
        self.world_simulator.db = self.db_manager  # Set database reference
        self.admin = AdminManager(self.config["bot"]["admin_ids"])
        self.admin.db = self.db_manager  # Set database reference
        self.ui = UIManager()
        
        # Game state
        self.game_tasks = {}
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
        self.dp.message.register(self.assets_command, Command("assets"))
        
        # Province commands
        self.dp.message.register(self.province_command, Command("province"))
        self.dp.message.register(self.map_command, Command("map"))
        
        # Quest commands
        self.dp.message.register(self.quest_command, Command("quest"))
        self.dp.message.register(self.missions_command, Command("missions"))
        
        # Technology commands
        self.dp.message.register(self.research_command, Command("research"))
        self.dp.message.register(self.tech_tree_command, Command("tech"))
        
        # Alliance commands
        self.dp.message.register(self.alliance_command, Command("alliance"))
        self.dp.message.register(self.diplomacy_command, Command("diplomacy"))
        
        # Admin commands
        self.dp.message.register(self.admin_command, Command("admin"))
        
        # Callback handlers
        self.dp.callback_query.register(self.handle_callback, F.data.startswith("game_"))
        
        # Error handler
        self.dp.errors.register(self.error_handler)
    
    async def start_command(self, message: types.Message):
        """Handle /start command"""
        user_id = message.from_user.id
        chat_id = message.chat.id
        
        # Check if user exists
        with self.db_manager.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=user_id).first()
            
            if not player:
                # Create new player
                player = Player(
                    telegram_id=user_id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    language=message.from_user.language_code or "en"
                )
                session.add(player)
                session.commit()
                
                # Initialize player materials
                for material in self.config["economy"]["materials"]:
                    player_material = PlayerMaterial(
                        player_id=player.id,
                        material_type=material,
                        quantity=100.0  # Starting materials
                    )
                    session.add(player_material)
                
                session.commit()
                
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
/map - View the world map

Good luck, Commander! The world awaits your leadership.
                """
            else:
                welcome_text = f"""
🎖️ **Welcome back, {player.rank} {player.first_name}!**

Your nation stands ready for new challenges.

**Current Status:**
💰 Gold: {player.gold:,.0f}
⭐ Level: {player.level}
🏆 Rank: {player.rank}
💪 Morale: {player.morale:.0f}%

Use /help to see all available commands.
                """
        
        keyboard = self.ui.get_main_menu_keyboard()
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
/assets - View all available military assets

**🗺️ World:**
/map - View world map
/province - Manage your provinces

**🎯 Missions:**
/quest - Available quests and missions
/missions - Your active missions

**🔬 Research:**
/research - Research new technologies
/tech - Technology tree

**🤝 Diplomacy:**
/alliance - Alliance management
/diplomacy - Diplomatic relations

**⚙️ Admin:**
/admin - Admin commands (admin only)

Use inline keyboards for easy navigation!
        """
        await message.answer(help_text, parse_mode="Markdown")
    
    async def status_command(self, message: types.Message):
        """Handle /status command"""
        user_id = message.from_user.id
        
        with self.db_manager.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=user_id).first()
            if not player:
                await message.answer("❌ You need to start the game first with /start")
                return
            
            # Get player materials
            materials = {pm.material_type: pm.quantity for pm in player.materials}
            
            # Get player units
            total_units = sum(pu.quantity for pu in player.units)
            
            status_text = f"""
🎖️ **{player.rank} {player.first_name}**

**📊 Basic Stats:**
💰 Gold: {player.gold:,.0f}
⭐ Level: {player.level} (XP: {player.experience:,})
💪 Morale: {player.morale:.0f}%
🛡️ Total Units: {total_units:,}

**📦 Resources:**
🛠️ Iron: {materials.get('iron', 0):,.0f}
⛽ Oil: {materials.get('oil', 0):,.0f}
🌾 Food: {materials.get('food', 0):,.0f}
🥇 Gold: {materials.get('gold', 0):,.0f}
☢️ Uranium: {materials.get('uranium', 0):,.0f}
🔩 Steel: {materials.get('steel', 0):,.0f}

**🏛️ Nation:** {player.nation.name if player.nation else "None"}
**🌍 Language:** {player.language.upper()}
**⏰ Last Active:** {player.last_active.strftime('%Y-%m-%d %H:%M')}
            """
            
            keyboard = self.ui.get_status_menu_keyboard()
            await message.answer(status_text, reply_markup=keyboard, parse_mode="Markdown")
    
    async def profile_command(self, message: types.Message):
        """Handle /profile command"""
        user_id = message.from_user.id
        
        with self.db_manager.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=user_id).first()
            if not player:
                await message.answer("❌ You need to start the game first with /start")
                return
            
            # Calculate detailed stats
            materials = {pm.material_type: pm.quantity for pm in player.materials}
            units = {pu.unit_type: pu.quantity for pu in player.units}
            
            profile_text = f"""
👤 **Detailed Profile - {player.rank} {player.first_name}**

**🎖️ Military Rank:** {player.rank}
**⭐ Experience Level:** {player.level}
**💯 Experience Points:** {player.experience:,}
**💰 Treasury:** {player.gold:,.0f} gold
**💪 Morale:** {player.morale:.0f}%

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
**🏛️ Nation:** {player.nation.name if player.nation else "None"}
**🌍 Language:** {player.language.upper()}
**📅 Member Since:** {player.created_at.strftime('%Y-%m-%d')}
**⏰ Last Active:** {player.last_active.strftime('%Y-%m-%d %H:%M')}
            """
            
            await message.answer(profile_text, parse_mode="Markdown")
    
    async def economy_command(self, message: types.Message):
        """Handle /economy command"""
        user_id = message.from_user.id
        
        with self.db_manager.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=user_id).first()
            if not player:
                await message.answer("❌ You need to start the game first with /start")
                return
            
            # Get current market prices
            prices = self.economy.get_current_prices()
            
            economy_text = f"""
💰 **Economic Overview**

**📈 Current Market Prices:**
"""
            for material, price_info in prices.items():
                emoji = {"iron": "🛠️", "oil": "⛽", "food": "🌾", "gold": "🥇", "uranium": "☢️", "steel": "🔩"}.get(material, "📦")
                economy_text += f"{emoji} {material.title()}: {price_info['price']:.2f} gold/unit\n"
            
            economy_text += f"""
**💼 Your Resources:**
"""
            for pm in player.materials:
                emoji = {"iron": "🛠️", "oil": "⛽", "food": "🌾", "gold": "🥇", "uranium": "☢️", "steel": "🔩"}.get(pm.material_type, "📦")
                economy_text += f"{emoji} {pm.material_type.title()}: {pm.quantity:,.0f}\n"
            
            economy_text += f"""
**💰 Treasury:** {player.gold:,.0f} gold

Use /trade to buy and sell resources!
            """
            
            keyboard = self.ui.get_economy_menu_keyboard()
            await message.answer(economy_text, reply_markup=keyboard, parse_mode="Markdown")
    
    async def trade_command(self, message: types.Message):
        """Handle /trade command"""
        keyboard = self.ui.get_trade_menu_keyboard()
        await message.answer("💼 **Trading Center**\n\nSelect what you want to do:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def materials_command(self, message: types.Message):
        """Handle /materials command"""
        user_id = message.from_user.id
        
        with self.db_manager.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=user_id).first()
            if not player:
                await message.answer("❌ You need to start the game first with /start")
                return
            
            materials_text = "📦 **Your Materials Inventory**\n\n"
            
            for pm in player.materials:
                emoji = {"iron": "🛠️", "oil": "⛽", "food": "🌾", "gold": "🥇", "uranium": "☢️", "steel": "🔩"}.get(pm.material_type, "📦")
                materials_text += f"{emoji} **{pm.material_type.title()}**: {pm.quantity:,.0f} units\n"
            
            await message.answer(materials_text, parse_mode="Markdown")
    
    async def military_command(self, message: types.Message):
        """Handle /military command"""
        user_id = message.from_user.id
        
        with self.db_manager.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=user_id).first()
            if not player:
                await message.answer("❌ You need to start the game first with /start")
                return
            
            # Get player units
            units = {pu.unit_type: pu.quantity for pu in player.units}
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
                military_text += f"\n💪 **Morale:** {player.morale:.0f}%"
            
            keyboard = self.ui.get_military_menu_keyboard()
            await message.answer(military_text, reply_markup=keyboard, parse_mode="Markdown")
    
    async def attack_command(self, message: types.Message):
        """Handle /attack command"""
        keyboard = self.ui.get_attack_menu_keyboard()
        await message.answer("⚔️ **Combat Center**\n\nSelect your target:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def build_units_command(self, message: types.Message):
        """Handle /build command"""
        keyboard = self.ui.get_build_menu_keyboard()
        await message.answer("🏭 **Unit Production**\n\nSelect unit type to build:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def assets_command(self, message: types.Message):
        """Handle /assets command - show available military assets"""
        user_id = message.from_user.id
        
        with self.db_manager.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=user_id).first()
            if not player:
                await message.answer("❌ You need to start the game first with /start")
                return
            
            # Get available assets by category
            assets_db = self.military.assets_db
            categories = assets_db.get_asset_categories()
            
            assets_text = "🎖️ **Military Assets Database**\n\n"
            assets_text += f"📊 **Total Assets Available:** {assets_db.get_total_assets()}\n"
            assets_text += f"🏷️ **Categories:** {len(categories)}\n"
            assets_text += f"⭐ **Tiers:** 1-10\n\n"
            
            # Show tier distribution
            tier_counts = {}
            for asset in assets_db.assets.values():
                tier = asset.tier
                tier_counts[tier] = tier_counts.get(tier, 0) + 1
            
            assets_text += "**Tier Distribution:**\n"
            for tier in sorted(tier_counts.keys()):
                count = tier_counts[tier]
                stars = "⭐" * min(tier, 5)
                if tier > 5:
                    stars = ["👑", "🌌", "♾️", "🌟", "👑"][tier - 6]
                assets_text += f"{stars} Tier {tier}: {count} units\n"
            
            assets_text += "\n**Categories Available:**\n"
            category_emojis = {
                "infantry": "👥", "armor": "🚗", "aircraft": "✈️", "naval": "🚢", 
                "missile": "🚀", "defense": "🛡️", "cyber": "💻", "space": "🚀", 
                "biological": "🧬", "magical": "🧙"
            }
            
            for category in categories:
                emoji = category_emojis.get(category, "⚔️")
                count = len(assets_db.get_assets_by_category(category))
                assets_text += f"{emoji} {category.title()}: {count} units\n"
            
            assets_text += "\nUse the buttons below to explore!"
            
            keyboard = self.ui.get_assets_menu_keyboard()
            await message.answer(assets_text, reply_markup=keyboard, parse_mode="Markdown")
    
    async def province_command(self, message: types.Message):
        """Handle /province command"""
        keyboard = self.ui.get_province_menu_keyboard()
        await message.answer("🗺️ **Province Management**\n\nManage your territories:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def map_command(self, message: types.Message):
        """Handle /map command"""
        keyboard = self.ui.get_map_menu_keyboard()
        await message.answer("🗺️ **World Map**\n\nExplore the world:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def quest_command(self, message: types.Message):
        """Handle /quest command"""
        keyboard = self.ui.get_quest_menu_keyboard()
        await message.answer("🎯 **Quest Center**\n\nTake on missions:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def missions_command(self, message: types.Message):
        """Handle /missions command"""
        user_id = message.from_user.id
        
        with self.db_manager.get_session() as session:
            player = session.query(Player).filter_by(telegram_id=user_id).first()
            if not player:
                await message.answer("❌ You need to start the game first with /start")
                return
            
            # Get active quests
            active_quests = [pq for pq in player.quests if pq.status == "active"]
            
            if not active_quests:
                missions_text = "🎯 **Active Missions**\n\n❌ You have no active missions.\n\nUse /quest to find new missions!"
            else:
                missions_text = "🎯 **Active Missions**\n\n"
                for pq in active_quests:
                    progress = pq.progress * 100
                    missions_text += f"**{pq.quest.title}**\n"
                    missions_text += f"Progress: {progress:.0f}%\n"
                    missions_text += f"Type: {pq.quest.quest_type.title()}\n\n"
            
            await message.answer(missions_text, parse_mode="Markdown")
    
    async def research_command(self, message: types.Message):
        """Handle /research command"""
        keyboard = self.ui.get_research_menu_keyboard()
        await message.answer("🔬 **Research Center**\n\nAdvance your technology:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def tech_tree_command(self, message: types.Message):
        """Handle /tech command"""
        keyboard = self.ui.get_tech_tree_menu_keyboard()
        await message.answer("🌳 **Technology Tree**\n\nView available technologies:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def alliance_command(self, message: types.Message):
        """Handle /alliance command"""
        keyboard = self.ui.get_alliance_menu_keyboard()
        await message.answer("🤝 **Alliance Center**\n\nManage diplomatic relations:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def diplomacy_command(self, message: types.Message):
        """Handle /diplomacy command"""
        keyboard = self.ui.get_diplomacy_menu_keyboard()
        await message.answer("🌍 **Diplomacy**\n\nInternational relations:", reply_markup=keyboard, parse_mode="Markdown")
    
    async def admin_command(self, message: types.Message):
        """Handle /admin command"""
        user_id = message.from_user.id
        
        if not self.admin.is_admin(user_id):
            await message.answer("❌ Access denied. Admin privileges required.")
            return
        
        keyboard = self.ui.get_admin_menu_keyboard()
        await message.answer("⚙️ **Admin Panel**\n\nAdministrative controls:", reply_markup=keyboard, parse_mode="Markdown")
    
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
            elif data.startswith("game_research_"):
                await self.handle_research_callback(callback_query)
            elif data.startswith("game_alliance_"):
                await self.handle_alliance_callback(callback_query)
            elif data.startswith("game_admin_"):
                await self.handle_admin_callback(callback_query)
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
        elif data == "game_main_research":
            await self.research_command(callback_query.message)
        elif data == "game_main_alliance":
            await self.alliance_command(callback_query.message)
        
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
        elif data == "game_military_assets":
            await self.assets_command(callback_query.message)
        elif data.startswith("game_assets_"):
            await self.handle_assets_callback(callback_query)
        
        await callback_query.answer()
    
    async def handle_assets_callback(self, callback_query: CallbackQuery):
        """Handle assets menu callbacks"""
        data = callback_query.data
        
        if data == "game_assets_tier":
            keyboard = self.ui.get_tier_menu_keyboard()
            await callback_query.message.answer("⭐ **Select Tier**\n\nChoose a tier to view units:", reply_markup=keyboard, parse_mode="Markdown")
        elif data.startswith("game_assets_tier_"):
            tier = int(data.split("_")[3])
            await self.show_assets_by_tier(callback_query, tier)
        elif data.startswith("game_assets_"):
            category = data.split("_")[2]
            await self.show_assets_by_category(callback_query, category)
        elif data == "game_assets_search":
            await callback_query.message.answer("🔍 **Asset Search**\n\nSearch functionality coming soon! Use the category buttons for now.", parse_mode="Markdown")
    
    async def show_assets_by_category(self, callback_query: CallbackQuery, category: str):
        """Show assets by category"""
        assets_db = self.military.assets_db
        assets = assets_db.get_assets_by_category(category)
        
        if not assets:
            await callback_query.message.answer(f"❌ No {category} units found.")
            return
        
        category_emojis = {
            "infantry": "👥", "armor": "🚗", "aircraft": "✈️", "naval": "🚢", 
            "missile": "🚀", "defense": "🛡️", "cyber": "💻", "space": "🚀", 
            "biological": "🧬", "magical": "🧙"
        }
        
        emoji = category_emojis.get(category, "⚔️")
        text = f"{emoji} **{category.title()} Units**\n\n"
        
        # Show first 10 assets
        for asset in assets[:10]:
            tier_stars = "⭐" * min(asset.tier, 5)
            if asset.tier > 5:
                tier_stars = ["👑", "🌌", "♾️", "🌟", "👑"][asset.tier - 6]
            
            text += f"{asset.emoji} **{asset.name}** {tier_stars}\n"
            text += f"   Cost: {asset.cost} gold | Attack: {asset.attack} | Defense: {asset.defense}\n\n"
        
        if len(assets) > 10:
            text += f"... and {len(assets) - 10} more units"
        
        keyboard = self.ui.get_assets_menu_keyboard()
        await callback_query.message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
    
    async def show_assets_by_tier(self, callback_query: CallbackQuery, tier: int):
        """Show assets by tier"""
        assets_db = self.military.assets_db
        assets = assets_db.get_assets_by_tier(tier)
        
        if not assets:
            await callback_query.message.answer(f"❌ No Tier {tier} units found.")
            return
        
        tier_names = {
            1: "⭐ Basic", 2: "⭐⭐ Advanced", 3: "⭐⭐⭐ Elite", 4: "⭐⭐⭐⭐ Future",
            5: "⭐⭐⭐⭐⭐ Transcendent", 6: "👑 Divine", 7: "🌌 Cosmic", 8: "♾️ Infinite",
            9: "🌟 Transcendental", 10: "👑 Ultimate"
        }
        
        tier_name = tier_names.get(tier, f"Tier {tier}")
        text = f"{tier_name} **Units**\n\n"
        
        # Show first 10 assets
        for asset in assets[:10]:
            text += f"{asset.emoji} **{asset.name}** ({asset.category})\n"
            text += f"   Cost: {asset.cost} gold | Attack: {asset.attack} | Defense: {asset.defense}\n\n"
        
        if len(assets) > 10:
            text += f"... and {len(assets) - 10} more units"
        
        keyboard = self.ui.get_tier_menu_keyboard()
        await callback_query.message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
    
    async def handle_trade_callback(self, callback_query: CallbackQuery):
        """Handle trade menu callbacks"""
        data = callback_query.data
        
        if data.startswith("game_trade_buy_"):
            material = data.split("_")[3]
            await self.start_trade_buy(callback_query, material)
        elif data.startswith("game_trade_sell_"):
            material = data.split("_")[3]
            await self.start_trade_sell(callback_query, material)
        elif data == "game_trade_market":
            await self.show_market(callback_query)
        
        await callback_query.answer()
    
    async def handle_quest_callback(self, callback_query: CallbackQuery):
        """Handle quest menu callbacks"""
        data = callback_query.data
        
        if data == "game_quest_available":
            await self.show_available_quests(callback_query)
        elif data == "game_quest_active":
            await self.missions_command(callback_query.message)
        elif data.startswith("game_quest_accept_"):
            quest_id = int(data.split("_")[3])
            await self.accept_quest(callback_query, quest_id)
        
        await callback_query.answer()
    
    async def handle_research_callback(self, callback_query: CallbackQuery):
        """Handle research menu callbacks"""
        data = callback_query.data
        
        if data == "game_research_available":
            await self.show_available_research(callback_query)
        elif data == "game_research_active":
            await self.show_active_research(callback_query)
        elif data.startswith("game_research_start_"):
            tech_id = int(data.split("_")[3])
            await self.start_research(callback_query, tech_id)
        
        await callback_query.answer()
    
    async def handle_alliance_callback(self, callback_query: CallbackQuery):
        """Handle alliance menu callbacks"""
        data = callback_query.data
        
        if data == "game_alliance_list":
            await self.show_alliances(callback_query)
        elif data == "game_alliance_create":
            await self.create_alliance(callback_query)
        elif data == "game_alliance_requests":
            await self.show_alliance_requests(callback_query)
        
        await callback_query.answer()
    
    async def handle_admin_callback(self, callback_query: CallbackQuery):
        """Handle admin menu callbacks"""
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        if not self.admin.is_admin(user_id):
            await callback_query.answer("❌ Access denied")
            return
        
        if data == "game_admin_reset":
            await self.admin_reset_game(callback_query)
        elif data == "game_admin_ban":
            await self.admin_ban_player(callback_query)
        elif data == "game_admin_stats":
            await self.admin_show_stats(callback_query)
        
        await callback_query.answer()
    
    # Placeholder methods for callback handlers
    async def start_trade_buy(self, callback_query: CallbackQuery, material: str):
        await callback_query.message.answer(f"💼 Buying {material} - Feature coming soon!")
    
    async def start_trade_sell(self, callback_query: CallbackQuery, material: str):
        await callback_query.message.answer(f"💼 Selling {material} - Feature coming soon!")
    
    async def show_market(self, callback_query: CallbackQuery):
        await callback_query.message.answer("📈 Market Overview - Feature coming soon!")
    
    async def show_available_quests(self, callback_query: CallbackQuery):
        await callback_query.message.answer("🎯 Available Quests - Feature coming soon!")
    
    async def accept_quest(self, callback_query: CallbackQuery, quest_id: int):
        await callback_query.message.answer(f"✅ Quest {quest_id} accepted - Feature coming soon!")
    
    async def show_available_research(self, callback_query: CallbackQuery):
        await callback_query.message.answer("🔬 Available Research - Feature coming soon!")
    
    async def show_active_research(self, callback_query: CallbackQuery):
        await callback_query.message.answer("🔬 Active Research - Feature coming soon!")
    
    async def start_research(self, callback_query: CallbackQuery, tech_id: int):
        await callback_query.message.answer(f"🔬 Research {tech_id} started - Feature coming soon!")
    
    async def show_alliances(self, callback_query: CallbackQuery):
        await callback_query.message.answer("🤝 Alliances - Feature coming soon!")
    
    async def create_alliance(self, callback_query: CallbackQuery):
        await callback_query.message.answer("🤝 Create Alliance - Feature coming soon!")
    
    async def show_alliance_requests(self, callback_query: CallbackQuery):
        await callback_query.message.answer("🤝 Alliance Requests - Feature coming soon!")
    
    async def admin_reset_game(self, callback_query: CallbackQuery):
        await callback_query.message.answer("⚙️ Reset Game - Feature coming soon!")
    
    async def admin_ban_player(self, callback_query: CallbackQuery):
        await callback_query.message.answer("⚙️ Ban Player - Feature coming soon!")
    
    async def admin_show_stats(self, callback_query: CallbackQuery):
        await callback_query.message.answer("⚙️ Game Stats - Feature coming soon!")
    
    async def error_handler(self, event, exception):
        """Handle errors"""
        logger.error(f"Error occurred: {exception}")
        return True
    
    async def start(self):
        """Start the bot"""
        logger.info("Starting World War Bot...")
        
        # Initialize database
        await self.db_manager.init_database()
        
        # Start background tasks
        asyncio.create_task(self.world_simulator.run())
        asyncio.create_task(self.economy.update_prices_loop())
        asyncio.create_task(self.daily_income_loop())
        asyncio.create_task(self.unit_upkeep_loop())
        
        # Start polling
        await self.dp.start_polling(self.bot)
    
    async def daily_income_loop(self):
        """Background task for daily income processing"""
        while True:
            try:
                await asyncio.sleep(3600)  # Wait 1 hour
                self.daily_income.process_daily_income()
                logger.info("Processed daily income for all players")
            except Exception as e:
                logger.error(f"Error processing daily income: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retrying
    
    async def unit_upkeep_loop(self):
        """Background task for unit upkeep processing"""
        while True:
            try:
                await asyncio.sleep(3600)  # Wait 1 hour
                self.unit_upkeep.process_daily_upkeep()
                logger.info("Processed unit upkeep for all players")
            except Exception as e:
                logger.error(f"Error processing unit upkeep: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retrying
    
    async def stop(self):
        """Stop the bot"""
        logger.info("Stopping World War Bot...")
        self.economy.stop()
        self.world_simulator.stop()
        await self.bot.session.close()

if __name__ == "__main__":
    bot = WorldWarBot()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        asyncio.run(bot.stop())