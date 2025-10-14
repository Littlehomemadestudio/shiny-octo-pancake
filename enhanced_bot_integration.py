"""
Enhanced Bot Integration
Complete integration of all advanced features including quiz system and complex resources
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Import all our enhanced systems
from military_quiz_system import MilitaryQuizSystem, DifficultyLevel, QuestionCategory
from complex_resources import ComplexResourceManager, ResourceType
from enhanced_military_assets import EnhancedMilitaryAssetsDatabase, AssetComplexity
from bot_settings import BotSettingsManager, NotificationManager, LanguageManager
from settings_ui import SettingsUIManager
from admin_panel import AdminPanel
from monitoring_analytics import UserAnalytics, PerformanceMonitor, AnalyticsDashboard
from database import DatabaseManager

class EnhancedWorldWarBot:
    """Fully enhanced bot with all advanced features"""
    
    def __init__(self, bot_token: str, config: Dict[str, Any]):
        self.bot = Bot(token=bot_token)
        self.dp = Dispatcher()
        self.config = config
        
        # Initialize core systems
        self.db_manager = DatabaseManager(config["database"]["url"])
        
        # Initialize enhanced systems
        self.quiz_system = MilitaryQuizSystem(self.db_manager)
        self.resource_manager = ComplexResourceManager(self.db_manager)
        self.assets_db = EnhancedMilitaryAssetsDatabase()
        
        # Initialize settings and UI
        self.settings_manager = BotSettingsManager()
        self.notification_manager = NotificationManager(self.settings_manager)
        self.language_manager = LanguageManager()
        self.settings_ui = SettingsUIManager(self.settings_manager)
        
        # Initialize monitoring
        self.user_analytics = UserAnalytics()
        self.performance_monitor = PerformanceMonitor()
        self.analytics_dashboard = AnalyticsDashboard(self.performance_monitor, self.user_analytics)
        
        # Initialize admin panel
        self.admin_panel = AdminPanel(self.settings_manager, self.db_manager)
        
        # Setup logging
        self.setup_logging()
        
        # Register handlers
        self.register_handlers()
        
        # Start background tasks
        self.background_tasks = []
    
    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('enhanced_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def register_handlers(self):
        """Register all bot handlers"""
        # Basic commands
        self.dp.message.register(self.start_command, Command("start"))
        self.dp.message.register(self.help_command, Command("help"))
        self.dp.message.register(self.status_command, Command("status"))
        self.dp.message.register(self.settings_command, Command("settings"))
        self.dp.message.register(self.admin_command, Command("admin"))
        self.dp.message.register(self.analytics_command, Command("analytics"))
        
        # Quiz commands
        self.dp.message.register(self.quiz_command, Command("quiz"))
        self.dp.message.register(self.quiz_easy_command, Command("quiz_easy"))
        self.dp.message.register(self.quiz_medium_command, Command("quiz_medium"))
        self.dp.message.register(self.quiz_hard_command, Command("quiz_hard"))
        self.dp.message.register(self.quiz_expert_command, Command("quiz_expert"))
        self.dp.message.register(self.quiz_legendary_command, Command("quiz_legendary"))
        self.dp.message.register(self.leaderboard_command, Command("leaderboard"))
        self.dp.message.register(self.quiz_stats_command, Command("quiz_stats"))
        
        # Resource commands
        self.dp.message.register(self.economy_command, Command("economy"))
        self.dp.message.register(self.buy_command, Command("buy"))
        self.dp.message.register(self.sell_command, Command("sell"))
        self.dp.message.register(self.trade_command, Command("trade"))
        self.dp.message.register(self.market_command, Command("market"))
        self.dp.message.register(self.prices_command, Command("prices"))
        self.dp.message.register(self.storage_command, Command("storage"))
        
        # Military commands
        self.dp.message.register(self.military_command, Command("military"))
        self.dp.message.register(self.build_command, Command("build"))
        self.dp.message.register(self.assets_command, Command("assets"))
        self.dp.message.register(self.units_command, Command("units"))
        self.dp.message.register(self.attack_command, Command("attack"))
        
        # Callback handlers
        self.dp.callback_query.register(self.handle_quiz_callback, lambda c: c.data.startswith("quiz_"))
        self.dp.callback_query.register(self.handle_economy_callback, lambda c: c.data.startswith("economy_"))
        self.dp.callback_query.register(self.handle_military_callback, lambda c: c.data.startswith("military_"))
        self.dp.callback_query.register(self.handle_settings_callback, lambda c: c.data.startswith("settings_"))
        self.dp.callback_query.register(self.handle_admin_callback, lambda c: c.data.startswith("admin_"))
    
    async def start_command(self, message: Message):
        """Enhanced start command with all features"""
        user_id = message.from_user.id
        start_time = time.time()
        
        try:
            # Start user session
            session_id = self.user_analytics.start_user_session(user_id)
            self.user_analytics.record_event(user_id, "command", {"command": "start"})
            
            # Get user preferences
            prefs = self.settings_manager.get_user_preferences(user_id)
            
            # Get localized text
            welcome_text = self.language_manager.get_text("welcome", prefs.language)
            
            # Create player if not exists
            with self.db_manager.get_session() as session:
                from database import Player
                player = session.query(Player).filter_by(telegram_id=user_id).first()
                if not player:
                    player = Player(
                        telegram_id=user_id,
                        username=message.from_user.username or "Unknown",
                        first_name=message.from_user.first_name or "Unknown",
                        last_name=message.from_user.last_name,
                        gold=1000,
                        level=1,
                        experience=0,
                        military_power=0,
                        last_active=datetime.now()
                    )
                    session.add(player)
                    session.commit()
                    
                    # Give starting resources
                    self.resource_manager.add_resource(user_id, ResourceType.GOLD, 1000, "starting")
                    self.resource_manager.add_resource(user_id, ResourceType.OIL, 100, "starting")
                    self.resource_manager.add_resource(user_id, ResourceType.IRON, 50, "starting")
                    self.resource_manager.add_resource(user_id, ResourceType.POPULATION, 100, "starting")
                    self.resource_manager.add_resource(user_id, ResourceType.KNOWLEDGE, 10, "starting")
                    
                    # Record new user event
                    self.user_analytics.record_event(user_id, "user_registration", {
                        "username": message.from_user.username,
                        "first_name": message.from_user.first_name
                    })
                else:
                    # Update last active
                    player.last_active = datetime.now()
                    session.commit()
            
            # Create welcome message
            text = f"{welcome_text}\n\n"
            text += f"🎖️ **World War Strategy Bot**\n"
            text += f"🌐 Language: {prefs.language.upper()}\n"
            text += f"🎭 Theme: {prefs.theme.title()}\n"
            text += f"🎯 Difficulty: {prefs.difficulty_level.title()}\n\n"
            text += f"**🎮 New Features:**\n"
            text += f"• 🧠 Military Knowledge Quiz System\n"
            text += f"• 💰 15 Different Resource Types\n"
            text += f"• 🎖️ 293+ Military Assets with Complex Requirements\n"
            text += f"• 📊 Real-time Market Dynamics\n"
            text += f"• ⚙️ 100+ Customizable Settings\n\n"
            text += f"Use /help to see all commands!\n"
            text += f"Try /quiz to test your military knowledge!"
            
            # Create main menu keyboard
            keyboard = self.get_main_menu_keyboard()
            
            await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
            
        except Exception as e:
            self.logger.error(f"Error in start command: {e}")
            await message.answer("❌ An error occurred. Please try again.")
        finally:
            # Record performance
            response_time = time.time() - start_time
            self.performance_monitor.record_command("start", response_time, True)
    
    async def quiz_command(self, message: Message):
        """Start military knowledge quiz"""
        user_id = message.from_user.id
        start_time = time.time()
        
        try:
            self.user_analytics.record_event(user_id, "command", {"command": "quiz"})
            
            # Create quiz difficulty selection keyboard
            keyboard = self.get_quiz_difficulty_keyboard()
            
            text = "🧠 **Military Knowledge Quiz**\n\n"
            text += "Test your military knowledge and earn points!\n"
            text += "Choose your difficulty level:"
            
            await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
            
        except Exception as e:
            self.logger.error(f"Error in quiz command: {e}")
            await message.answer("❌ An error occurred. Please try again.")
        finally:
            response_time = time.time() - start_time
            self.performance_monitor.record_command("quiz", response_time, True)
    
    async def quiz_easy_command(self, message: Message):
        """Start easy difficulty quiz"""
        await self.start_quiz_with_difficulty(message, DifficultyLevel.EASY)
    
    async def quiz_medium_command(self, message: Message):
        """Start medium difficulty quiz"""
        await self.start_quiz_with_difficulty(message, DifficultyLevel.MEDIUM)
    
    async def quiz_hard_command(self, message: Message):
        """Start hard difficulty quiz"""
        await self.start_quiz_with_difficulty(message, DifficultyLevel.HARD)
    
    async def quiz_expert_command(self, message: Message):
        """Start expert difficulty quiz"""
        await self.start_quiz_with_difficulty(message, DifficultyLevel.EXPERT)
    
    async def quiz_legendary_command(self, message: Message):
        """Start legendary difficulty quiz"""
        await self.start_quiz_with_difficulty(message, DifficultyLevel.LEGENDARY)
    
    async def start_quiz_with_difficulty(self, message: Message, difficulty: DifficultyLevel):
        """Start quiz with specific difficulty"""
        user_id = message.from_user.id
        
        try:
            # Start quiz session
            session_id = self.quiz_system.start_quiz(user_id, difficulty, question_count=10)
            
            # Get first question
            question_data = self.quiz_system.get_current_question(session_id)
            
            if question_data:
                text = f"🧠 **Quiz Started - {difficulty.value.title()} Difficulty**\n\n"
                text += f"**Question 1 of {question_data['total_questions']}**\n"
                text += f"**Points:** {question_data['points']}\n"
                text += f"**Time Limit:** {question_data['time_limit']} seconds\n\n"
                text += f"**{question_data['question']}**\n\n"
                
                # Create answer keyboard
                keyboard = self.get_quiz_answer_keyboard(session_id, question_data['options'])
                
                await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
            else:
                await message.answer("❌ No questions available. Please try again later.")
                
        except Exception as e:
            self.logger.error(f"Error starting quiz: {e}")
            await message.answer("❌ An error occurred starting the quiz.")
    
    async def economy_command(self, message: Message):
        """Enhanced economy command with complex resources"""
        user_id = message.from_user.id
        start_time = time.time()
        
        try:
            self.user_analytics.record_event(user_id, "command", {"command": "economy"})
            
            # Get user resources
            user_resources = self.resource_manager.get_user_resources(user_id)
            
            # Get market summary
            market_summary = self.resource_manager.get_market_summary()
            
            # Create economy overview
            text = "💰 **Economic Overview**\n\n"
            text += f"**Your Resources:**\n"
            
            for resource_type, amount in user_resources.items():
                if amount > 0:
                    resource_info = self.resource_manager.resources.get(resource_type)
                    if resource_info:
                        text += f"{resource_info.emoji} {resource_info.name}: {amount:,.1f} {resource_info.unit}\n"
            
            text += f"\n**Market Status:** {market_summary['market_health'].title()}\n"
            text += f"**Active Events:** {len(market_summary['active_events'])}\n"
            text += f"**Total Resources:** {market_summary['total_resources']}\n\n"
            
            # Show price changes
            text += "**Recent Price Changes:**\n"
            for resource_name, price_data in list(market_summary['price_changes'].items())[:5]:
                change_emoji = "📈" if price_data['change'] > 0 else "📉" if price_data['change'] < 0 else "➡️"
                text += f"{change_emoji} {resource_name}: {price_data['price']:.2f} ({price_data['change_percent']:+.1f}%)\n"
            
            # Create economy keyboard
            keyboard = self.get_economy_keyboard()
            
            await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
            
        except Exception as e:
            self.logger.error(f"Error in economy command: {e}")
            await message.answer("❌ An error occurred. Please try again.")
        finally:
            response_time = time.time() - start_time
            self.performance_monitor.record_command("economy", response_time, True)
    
    async def assets_command(self, message: Message):
        """Enhanced assets command with complex requirements"""
        user_id = message.from_user.id
        start_time = time.time()
        
        try:
            self.user_analytics.record_event(user_id, "command", {"command": "assets"})
            
            # Get user resources
            user_resources = self.resource_manager.get_user_resources(user_id)
            
            # Get resource prices
            resource_prices = {rt: self.resource_manager.get_resource_price(rt).price 
                             for rt in ResourceType}
            
            # Create assets overview
            text = "🎖️ **Military Assets Database**\n\n"
            text += f"**Total Assets:** {len(self.assets_db.assets)}\n"
            text += f"**Categories:** 10\n"
            text += f"**Tiers:** 1-10\n"
            text += f"**Complexity Levels:** 5\n\n"
            
            # Show some example assets with costs
            text += "**Example Assets (with current costs):**\n"
            example_assets = ["rifleman", "special_forces", "main_battle_tank", "fighter_jet", "destroyer"]
            
            for asset_name in example_assets:
                asset = self.assets_db.get_asset(asset_name)
                if asset:
                    total_cost = self.assets_db.calculate_total_cost(asset_name, resource_prices)
                    text += f"{asset.emoji} **{asset.name}** - {total_cost:,.0f} gold\n"
            
            text += f"\n**Your Resources:**\n"
            for resource_type, amount in list(user_resources.items())[:5]:
                if amount > 0:
                    resource_info = self.resource_manager.resources.get(resource_type)
                    if resource_info:
                        text += f"{resource_info.emoji} {resource_info.name}: {amount:,.1f}\n"
            
            # Create assets keyboard
            keyboard = self.get_assets_keyboard()
            
            await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
            
        except Exception as e:
            self.logger.error(f"Error in assets command: {e}")
            await message.answer("❌ An error occurred. Please try again.")
        finally:
            response_time = time.time() - start_time
            self.performance_monitor.record_command("assets", response_time, True)
    
    async def handle_quiz_callback(self, callback_query: CallbackQuery):
        """Handle quiz callback queries"""
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        try:
            if data.startswith("quiz_answer_"):
                # Parse answer
                parts = data.split("_")
                session_id = parts[2]
                answer_index = int(parts[3])
                
                # Answer the question
                result = self.quiz_system.answer_question(session_id, answer_index, 10.0)  # 10 second response time
                
                if result["is_complete"]:
                    # Quiz completed
                    quiz_result = result["result"]
                    text = f"🎉 **Quiz Completed!**\n\n"
                    text += f"**Score:** {quiz_result.score:,} points\n"
                    text += f"**Correct Answers:** {quiz_result.correct_answers}/{quiz_result.total_questions}\n"
                    text += f"**Accuracy:** {quiz_result.accuracy:.1f}%\n"
                    text += f"**Rank:** {quiz_result.rank}\n"
                    text += f"**Knowledge Gained:** {quiz_result.knowledge_gained} points\n"
                    text += f"**Max Streak:** {quiz_result.max_streak}\n\n"
                    text += f"Great job! Use /quiz to try again!"
                    
                    # Give knowledge reward
                    self.resource_manager.add_resource(user_id, ResourceType.KNOWLEDGE, 
                                                     quiz_result.knowledge_gained, "quiz_reward")
                    
                    await callback_query.message.answer(text, parse_mode="Markdown")
                else:
                    # Next question
                    question_data = self.quiz_system.get_current_question(session_id)
                    if question_data:
                        text = f"🧠 **Quiz - Question {question_data['current_question']} of {question_data['total_questions']}**\n\n"
                        text += f"**Score:** {question_data['score']:,} points\n"
                        text += f"**Streak:** {question_data['streak']}\n"
                        text += f"**Points:** {question_data['points']}\n"
                        text += f"**Time Limit:** {question_data['time_limit']} seconds\n\n"
                        text += f"**{question_data['question']}**\n\n"
                        
                        keyboard = self.get_quiz_answer_keyboard(session_id, question_data['options'])
                        await callback_query.message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
                    else:
                        await callback_query.message.answer("❌ No more questions available.")
                
            elif data.startswith("quiz_difficulty_"):
                # Start quiz with selected difficulty
                difficulty_name = data.split("_")[2]
                difficulty = DifficultyLevel(difficulty_name)
                await self.start_quiz_with_difficulty(callback_query.message, difficulty)
                
        except Exception as e:
            self.logger.error(f"Error handling quiz callback: {e}")
            await callback_query.message.answer("❌ An error occurred. Please try again.")
        
        await callback_query.answer()
    
    def get_main_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get enhanced main menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="🎮 Start Game",
            callback_data="main_start"
        ))
        builder.add(InlineKeyboardButton(
            text="🧠 Quiz",
            callback_data="main_quiz"
        ))
        builder.add(InlineKeyboardButton(
            text="💰 Economy",
            callback_data="main_economy"
        ))
        builder.add(InlineKeyboardButton(
            text="🎖️ Assets",
            callback_data="main_assets"
        ))
        builder.add(InlineKeyboardButton(
            text="📊 Status",
            callback_data="main_status"
        ))
        builder.add(InlineKeyboardButton(
            text="⚙️ Settings",
            callback_data="main_settings"
        ))
        builder.add(InlineKeyboardButton(
            text="❓ Help",
            callback_data="main_help"
        ))
        
        builder.adjust(2, 2, 2, 1)
        return builder.as_markup()
    
    def get_quiz_difficulty_keyboard(self) -> InlineKeyboardMarkup:
        """Get quiz difficulty selection keyboard"""
        builder = InlineKeyboardBuilder()
        
        difficulties = [
            (DifficultyLevel.EASY, "⭐ Easy", "quiz_difficulty_easy"),
            (DifficultyLevel.MEDIUM, "⭐⭐ Medium", "quiz_difficulty_medium"),
            (DifficultyLevel.HARD, "⭐⭐⭐ Hard", "quiz_difficulty_hard"),
            (DifficultyLevel.EXPERT, "⭐⭐⭐⭐ Expert", "quiz_difficulty_expert"),
            (DifficultyLevel.LEGENDARY, "⭐⭐⭐⭐⭐ Legendary", "quiz_difficulty_legendary")
        ]
        
        for difficulty, name, callback_data in difficulties:
            builder.add(InlineKeyboardButton(
                text=name,
                callback_data=callback_data
            ))
        
        builder.add(InlineKeyboardButton(
            text="⬅️ Back",
            callback_data="main_menu"
        ))
        
        builder.adjust(1, 1, 1, 1, 1, 1)
        return builder.as_markup()
    
    def get_quiz_answer_keyboard(self, session_id: str, options: List[str]) -> InlineKeyboardMarkup:
        """Get quiz answer keyboard"""
        builder = InlineKeyboardBuilder()
        
        for i, option in enumerate(options):
            builder.add(InlineKeyboardButton(
                text=f"{chr(65 + i)}. {option}",
                callback_data=f"quiz_answer_{session_id}_{i}"
            ))
        
        builder.add(InlineKeyboardButton(
            text="❌ Quit Quiz",
            callback_data="quiz_quit"
        ))
        
        builder.adjust(1, 1, 1, 1, 1)
        return builder.as_markup()
    
    def get_economy_keyboard(self) -> InlineKeyboardMarkup:
        """Get economy management keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="💰 Buy Resources",
            callback_data="economy_buy"
        ))
        builder.add(InlineKeyboardButton(
            text="💸 Sell Resources",
            callback_data="economy_sell"
        ))
        builder.add(InlineKeyboardButton(
            text="🔄 Trade Resources",
            callback_data="economy_trade"
        ))
        builder.add(InlineKeyboardButton(
            text="📊 Market Prices",
            callback_data="economy_prices"
        ))
        builder.add(InlineKeyboardButton(
            text="📈 Market Events",
            callback_data="economy_events"
        ))
        builder.add(InlineKeyboardButton(
            text="⬅️ Back",
            callback_data="main_menu"
        ))
        
        builder.adjust(2, 2, 2)
        return builder.as_markup()
    
    def get_assets_keyboard(self) -> InlineKeyboardMarkup:
        """Get assets management keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="🏗️ Build Units",
            callback_data="military_build"
        ))
        builder.add(InlineKeyboardButton(
            text="📋 View Units",
            callback_data="military_units"
        ))
        builder.add(InlineKeyboardButton(
            text="🔍 Search Assets",
            callback_data="military_search"
        ))
        builder.add(InlineKeyboardButton(
            text="📊 By Category",
            callback_data="military_category"
        ))
        builder.add(InlineKeyboardButton(
            text="⭐ By Tier",
            callback_data="military_tier"
        ))
        builder.add(InlineKeyboardButton(
            text="⬅️ Back",
            callback_data="main_menu"
        ))
        
        builder.adjust(2, 2, 2)
        return builder.as_markup()
    
    async def start_background_tasks(self):
        """Start background monitoring tasks"""
        # Resource price updates
        async def update_resource_prices():
            while True:
                try:
                    self.resource_manager.update_prices()
                    await asyncio.sleep(300)  # Every 5 minutes
                except Exception as e:
                    self.logger.error(f"Error updating resource prices: {e}")
                    await asyncio.sleep(300)
        
        # Performance monitoring
        async def monitor_performance():
            while True:
                try:
                    self.performance_monitor.collect_system_metrics()
                    await asyncio.sleep(60)  # Every minute
                except Exception as e:
                    self.logger.error(f"Error monitoring performance: {e}")
                    await asyncio.sleep(60)
        
        # Start tasks
        self.background_tasks.append(asyncio.create_task(update_resource_prices()))
        self.background_tasks.append(asyncio.create_task(monitor_performance()))
    
    async def start(self):
        """Start the enhanced bot"""
        try:
            # Start background tasks
            await self.start_background_tasks()
            
            # Start polling
            await self.dp.start_polling(self.bot)
            
        except Exception as e:
            self.logger.error(f"Error starting bot: {e}")
        finally:
            # Cleanup
            for task in self.background_tasks:
                task.cancel()
    
    async def stop(self):
        """Stop the enhanced bot"""
        try:
            # Stop background tasks
            for task in self.background_tasks:
                task.cancel()
            
            # Stop bot
            await self.bot.session.close()
            
        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}")

# Example usage
if __name__ == "__main__":
    import json
    
    # Load configuration
    with open("config.json", "r") as f:
        config = json.load(f)
    
    # Create enhanced bot
    bot = EnhancedWorldWarBot(config["bot"]["token"], config)
    
    # Start bot
    asyncio.run(bot.start())