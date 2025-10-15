"""
Enhanced Bot with Advanced Settings System
Integration of all settings, monitoring, and admin features
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Import our custom modules
from bot_settings import BotSettingsManager, NotificationManager, LanguageManager, PerformanceMonitor
from settings_ui import SettingsUIManager
from admin_panel import AdminPanel
from monitoring_analytics import UserAnalytics, AnalyticsDashboard
from database import DatabaseManager
from military_assets import MilitaryAssetsDatabase

class EnhancedWorldWarBot:
    """Enhanced bot with comprehensive settings and monitoring"""
    
    def __init__(self, bot_token: str, config: Dict[str, Any]):
        self.bot = Bot(token=bot_token)
        self.dp = Dispatcher()
        self.config = config
        
        # Initialize core systems
        self.db_manager = DatabaseManager(config["database"]["url"])
        
        # Initialize settings system
        self.settings_manager = BotSettingsManager()
        self.notification_manager = NotificationManager(self.settings_manager)
        self.language_manager = LanguageManager()
        
        # Initialize UI managers
        self.settings_ui = SettingsUIManager(self.settings_manager)
        
        # Initialize monitoring
        self.performance_monitor = PerformanceMonitor()
        self.user_analytics = UserAnalytics()
        self.analytics_dashboard = AnalyticsDashboard(self.performance_monitor, self.user_analytics)
        
        # Initialize admin panel
        self.admin_panel = AdminPanel(self.settings_manager, self.db_manager)
        
        # Initialize game systems
        self.military_assets = MilitaryAssetsDatabase()
        
        # Setup logging
        self.setup_logging()
        
        # Register handlers
        self.register_handlers()
        
        # Start background tasks
        self.background_tasks = []
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bot.log'),
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
        
        # Game commands
        self.dp.message.register(self.economy_command, Command("economy"))
        self.dp.message.register(self.military_command, Command("military"))
        self.dp.message.register(self.province_command, Command("province"))
        self.dp.message.register(self.quest_command, Command("quest"))
        self.dp.message.register(self.alliance_command, Command("alliance"))
        
        # Callback handlers
        self.dp.callback_query.register(self.handle_main_callback, lambda c: c.data.startswith("main_"))
        self.dp.callback_query.register(self.handle_settings_callback, lambda c: c.data.startswith("settings_"))
        self.dp.callback_query.register(self.handle_admin_callback, lambda c: c.data.startswith("admin_"))
        self.dp.callback_query.register(self.handle_toggle_callback, lambda c: c.data.startswith("toggle_"))
        self.dp.callback_query.register(self.handle_change_callback, lambda c: c.data.startswith("change_"))
        self.dp.callback_query.register(self.handle_set_callback, lambda c: c.data.startswith("set_"))
    
    async def start_command(self, message: Message):
        """Enhanced start command with user session tracking"""
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
            text += f"🎮 **World War Strategy Bot**\n"
            text += f"🌐 Language: {prefs.language.upper()}\n"
            text += f"🎭 Theme: {prefs.theme.title()}\n"
            text += f"🎯 Difficulty: {prefs.difficulty_level.title()}\n\n"
            text += f"Use /help to see all commands!\n"
            text += f"Use /settings to customize your experience!"
            
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
    
    async def help_command(self, message: Message):
        """Enhanced help command with localization"""
        user_id = message.from_user.id
        start_time = time.time()
        
        try:
            prefs = self.settings_manager.get_user_preferences(user_id)
            self.user_analytics.record_event(user_id, "command", {"command": "help"})
            
            help_text = self.language_manager.get_text("help", prefs.language)
            
            text = f"📚 **{help_text}**\n\n"
            text += f"**🎮 Game Commands:**\n"
            text += f"• /start - Start the game\n"
            text += f"• /status - View your status\n"
            text += f"• /economy - Economy management\n"
            text += f"• /military - Military management\n"
            text += f"• /province - Province management\n"
            text += f"• /quest - Quest system\n"
            text += f"• /alliance - Alliance system\n\n"
            text += f"**⚙️ Settings Commands:**\n"
            text += f"• /settings - User settings\n"
            text += f"• /admin - Admin panel (admin only)\n"
            text += f"• /analytics - Analytics dashboard\n\n"
            text += f"**🌐 Language:** {prefs.language.upper()}\n"
            text += f"**🎭 Theme:** {prefs.theme.title()}\n"
            text += f"**🎯 Difficulty:** {prefs.difficulty_level.title()}\n\n"
            text += f"Use the buttons below for quick access!"
            
            keyboard = self.get_main_menu_keyboard()
            await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
            
        except Exception as e:
            self.logger.error(f"Error in help command: {e}")
            await message.answer("❌ An error occurred. Please try again.")
        finally:
            response_time = time.time() - start_time
            self.performance_monitor.record_command("help", response_time, True)
    
    async def settings_command(self, message: Message):
        """Settings command with comprehensive options"""
        user_id = message.from_user.id
        start_time = time.time()
        
        try:
            self.user_analytics.record_event(user_id, "command", {"command": "settings"})
            
            # Get settings summary
            summary_text = self.settings_ui.get_settings_summary_text(user_id)
            keyboard = self.settings_ui.get_main_settings_keyboard()
            
            await message.answer(summary_text, reply_markup=keyboard, parse_mode="Markdown")
            
        except Exception as e:
            self.logger.error(f"Error in settings command: {e}")
            await message.answer("❌ An error occurred. Please try again.")
        finally:
            response_time = time.time() - start_time
            self.performance_monitor.record_command("settings", response_time, True)
    
    async def admin_command(self, message: Message):
        """Admin command with comprehensive admin panel"""
        user_id = message.from_user.id
        start_time = time.time()
        
        try:
            # Check if user is admin
            admin_ids = self.config["bot"]["admin_ids"]
            if user_id not in admin_ids:
                await message.answer("❌ Access denied. Admin only.")
                return
            
            self.user_analytics.record_event(user_id, "command", {"command": "admin"})
            
            # Get admin dashboard data
            dashboard_data = self.admin_panel.get_admin_dashboard_data()
            
            text = "👑 **Admin Dashboard**\n\n"
            text += f"**🔧 System Health:** {dashboard_data['system_health']['status'].upper()}\n"
            text += f"**👥 Total Users:** {dashboard_data['user_statistics'].get('total_users', 0)}\n"
            text += f"**💰 Total Gold:** {dashboard_data['economy_statistics'].get('total_gold', 0)}\n"
            text += f"**⚔️ Total Units:** {dashboard_data['military_statistics'].get('total_units', 0)}\n"
            text += f"**📊 Recent Actions:** {len(dashboard_data['recent_actions'])}\n\n"
            text += f"Use the buttons below to manage the bot!"
            
            keyboard = self.settings_ui.get_admin_settings_keyboard(user_id)
            await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
            
        except Exception as e:
            self.logger.error(f"Error in admin command: {e}")
            await message.answer("❌ An error occurred. Please try again.")
        finally:
            response_time = time.time() - start_time
            self.performance_monitor.record_command("admin", response_time, True)
    
    async def analytics_command(self, message: Message):
        """Analytics command with comprehensive metrics"""
        user_id = message.from_user.id
        start_time = time.time()
        
        try:
            # Check if user is admin
            admin_ids = self.config["bot"]["admin_ids"]
            if user_id not in admin_ids:
                await message.answer("❌ Access denied. Admin only.")
                return
            
            self.user_analytics.record_event(user_id, "command", {"command": "analytics"})
            
            # Get dashboard data
            dashboard_data = self.analytics_dashboard.get_dashboard_data()
            
            text = "📊 **Analytics Dashboard**\n\n"
            text += f"**⚡ Performance:**\n"
            text += f"• Uptime: {dashboard_data['performance']['uptime_formatted']}\n"
            text += f"• Commands/min: {dashboard_data['performance']['commands_per_minute']:.1f}\n"
            text += f"• Avg Response: {dashboard_data['performance']['average_response_time']:.2f}s\n"
            text += f"• Error Rate: {dashboard_data['performance']['error_rate']:.1f}%\n\n"
            text += f"**👥 User Analytics:**\n"
            text += f"• Total Events: {dashboard_data['user_analytics']['total_events']}\n"
            text += f"• Unique Users: {dashboard_data['user_analytics']['unique_users']}\n"
            text += f"• Active Sessions: {dashboard_data['user_analytics']['active_sessions']}\n"
            text += f"• Events/hour: {dashboard_data['user_analytics']['events_per_hour']:.1f}\n\n"
            text += f"**🔥 Popular Commands:**\n"
            for command, count in dashboard_data['popular_commands'][:5]:
                text += f"• {command}: {count}\n"
            
            await message.answer(text, parse_mode="Markdown")
            
        except Exception as e:
            self.logger.error(f"Error in analytics command: {e}")
            await message.answer("❌ An error occurred. Please try again.")
        finally:
            response_time = time.time() - start_time
            self.performance_monitor.record_command("analytics", response_time, True)
    
    async def handle_settings_callback(self, callback_query: CallbackQuery):
        """Handle settings callback queries"""
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        try:
            if data == "settings_user":
                keyboard = self.settings_ui.get_user_settings_keyboard(user_id)
                await callback_query.message.answer("👤 **User Settings**\n\nCustomize your gameplay experience:", reply_markup=keyboard, parse_mode="Markdown")
            
            elif data == "settings_notifications":
                keyboard = self.settings_ui.get_notification_settings_keyboard(user_id)
                await callback_query.message.answer("🔔 **Notification Settings**\n\nConfigure what notifications you receive:", reply_markup=keyboard, parse_mode="Markdown")
            
            elif data == "settings_privacy":
                keyboard = self.settings_ui.get_privacy_settings_keyboard(user_id)
                await callback_query.message.answer("🔒 **Privacy Settings**\n\nControl your privacy and visibility:", reply_markup=keyboard, parse_mode="Markdown")
            
            elif data == "settings_display":
                keyboard = self.settings_ui.get_display_settings_keyboard(user_id)
                await callback_query.message.answer("🎨 **Display Settings**\n\nCustomize the appearance:", reply_markup=keyboard, parse_mode="Markdown")
            
            elif data == "settings_sound":
                keyboard = self.settings_ui.get_sound_settings_keyboard(user_id)
                await callback_query.message.answer("🔊 **Sound Settings**\n\nConfigure audio preferences:", reply_markup=keyboard, parse_mode="Markdown")
            
            elif data == "settings_language":
                keyboard = self.settings_ui.get_language_settings_keyboard(user_id)
                await callback_query.message.answer("🌐 **Language Settings**\n\nChoose your preferred language:", reply_markup=keyboard, parse_mode="Markdown")
            
            elif data == "settings_theme":
                keyboard = self.settings_ui.get_theme_settings_keyboard(user_id)
                await callback_query.message.answer("🎭 **Theme Settings**\n\nSelect your preferred theme:", reply_markup=keyboard, parse_mode="Markdown")
            
            elif data == "settings_main":
                summary_text = self.settings_ui.get_settings_summary_text(user_id)
                keyboard = self.settings_ui.get_main_settings_keyboard()
                await callback_query.message.answer(summary_text, reply_markup=keyboard, parse_mode="Markdown")
            
        except Exception as e:
            self.logger.error(f"Error handling settings callback: {e}")
            await callback_query.message.answer("❌ An error occurred. Please try again.")
        
        await callback_query.answer()
    
    async def handle_toggle_callback(self, callback_query: CallbackQuery):
        """Handle toggle callback queries"""
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        try:
            # Parse toggle action
            toggle_action = data.replace("toggle_", "")
            
            # Get current preferences
            prefs = self.settings_manager.get_user_preferences(user_id)
            
            # Toggle the setting
            if hasattr(prefs, toggle_action):
                current_value = getattr(prefs, toggle_action)
                setattr(prefs, toggle_action, not current_value)
                
                # Update in settings manager
                self.settings_manager.update_user_preferences(user_id, **{toggle_action: not current_value})
                
                # Record event
                self.user_analytics.record_event(user_id, "setting_changed", {
                    "setting": toggle_action,
                    "new_value": not current_value
                })
                
                # Send confirmation
                status = "enabled" if not current_value else "disabled"
                await callback_query.message.answer(f"✅ Setting '{toggle_action}' {status}!")
            else:
                await callback_query.message.answer(f"❌ Unknown setting: {toggle_action}")
        
        except Exception as e:
            self.logger.error(f"Error handling toggle callback: {e}")
            await callback_query.message.answer("❌ An error occurred. Please try again.")
        
        await callback_query.answer()
    
    async def handle_change_callback(self, callback_query: CallbackQuery):
        """Handle change callback queries"""
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        try:
            # Parse change action
            change_action = data.replace("change_", "")
            
            if change_action == "difficulty":
                keyboard = self.settings_ui.get_difficulty_settings_keyboard(user_id)
                await callback_query.message.answer("🎯 **Difficulty Settings**\n\nChoose your difficulty level:", reply_markup=keyboard, parse_mode="Markdown")
            else:
                await callback_query.message.answer(f"❌ Unknown change action: {change_action}")
        
        except Exception as e:
            self.logger.error(f"Error handling change callback: {e}")
            await callback_query.message.answer("❌ An error occurred. Please try again.")
        
        await callback_query.answer()
    
    async def handle_set_callback(self, callback_query: CallbackQuery):
        """Handle set callback queries"""
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        try:
            # Parse set action
            parts = data.split("_")
            if len(parts) >= 3:
                action_type = parts[1]  # language, theme, difficulty, etc.
                value = parts[2]  # the value to set
                
                if action_type == "language":
                    self.settings_manager.update_user_preferences(user_id, language=value)
                    await callback_query.message.answer(f"✅ Language set to {value.upper()}!")
                
                elif action_type == "theme":
                    self.settings_manager.update_user_preferences(user_id, theme=value)
                    await callback_query.message.answer(f"✅ Theme set to {value.title()}!")
                
                elif action_type == "difficulty":
                    self.settings_manager.update_user_preferences(user_id, difficulty_level=value)
                    await callback_query.message.answer(f"✅ Difficulty set to {value.title()}!")
                
                else:
                    await callback_query.message.answer(f"❌ Unknown set action: {action_type}")
                
                # Record event
                self.user_analytics.record_event(user_id, "setting_changed", {
                    "setting": action_type,
                    "new_value": value
                })
            else:
                await callback_query.message.answer("❌ Invalid set action format")
        
        except Exception as e:
            self.logger.error(f"Error handling set callback: {e}")
            await callback_query.message.answer("❌ An error occurred. Please try again.")
        
        await callback_query.answer()
    
    def get_main_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get main menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="🎮 Start Game",
            callback_data="main_start"
        ))
        builder.add(InlineKeyboardButton(
            text="📊 Status",
            callback_data="main_status"
        ))
        builder.add(InlineKeyboardButton(
            text="💰 Economy",
            callback_data="main_economy"
        ))
        builder.add(InlineKeyboardButton(
            text="⚔️ Military",
            callback_data="main_military"
        ))
        builder.add(InlineKeyboardButton(
            text="🗺️ Province",
            callback_data="main_province"
        ))
        builder.add(InlineKeyboardButton(
            text="🎯 Quest",
            callback_data="main_quest"
        ))
        builder.add(InlineKeyboardButton(
            text="🤝 Alliance",
            callback_data="main_alliance"
        ))
        builder.add(InlineKeyboardButton(
            text="⚙️ Settings",
            callback_data="main_settings"
        ))
        builder.add(InlineKeyboardButton(
            text="❓ Help",
            callback_data="main_help"
        ))
        
        builder.adjust(3, 3, 3)
        return builder.as_markup()
    
    async def start_background_tasks(self):
        """Start background monitoring tasks"""
        # System metrics collection
        async def collect_metrics():
            while True:
                try:
                    self.admin_panel.collect_system_metrics()
                    await asyncio.sleep(300)  # Every 5 minutes
                except Exception as e:
                    self.logger.error(f"Error collecting metrics: {e}")
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
        self.background_tasks.append(asyncio.create_task(collect_metrics()))
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
    # Load configuration
    import json
    with open("config.json", "r") as f:
        config = json.load(f)
    
    # Create enhanced bot
    bot = EnhancedWorldWarBot(config["bot"]["token"], config)
    
    # Start bot
    asyncio.run(bot.start())