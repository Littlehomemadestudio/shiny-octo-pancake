"""
Bale Bot for World War Strategy Game
All functions from Telegram bot with global purchase sync feature
"""
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from bale import Bot, Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, UpdatesFilter
from bale.handlers import MessageHandler, CallbackQueryHandler, CommandHandler

from bale_storage import BaleStorage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaleWorldWarBot:
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.bot = Bot(token=self.config["bot"]["token"])
        
        # Initialize storage with global purchase sync
        self.storage = BaleStorage()
        
        # Game state
        self.player_cooldowns = {}
        
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all bot command and callback handlers"""
        
        # Basic commands
        self.bot.add_handler(CommandHandler("start", self.start_command))
        self.bot.add_handler(CommandHandler("help", self.help_command))
        self.bot.add_handler(CommandHandler("status", self.status_command))
        self.bot.add_handler(CommandHandler("profile", self.profile_command))
        
        # Economy commands
        self.bot.add_handler(CommandHandler("economy", self.economy_command))
        self.bot.add_handler(CommandHandler("trade", self.trade_command))
        self.bot.add_handler(CommandHandler("materials", self.materials_command))
        self.bot.add_handler(CommandHandler("buy", self.buy_command))
        
        # Military commands
        self.bot.add_handler(CommandHandler("military", self.military_command))
        self.bot.add_handler(CommandHandler("attack", self.attack_command))
        self.bot.add_handler(CommandHandler("build", self.build_units_command))
        
        # Quest commands
        self.bot.add_handler(CommandHandler("quest", self.quest_command))
        self.bot.add_handler(CommandHandler("missions", self.missions_command))
        
        # Global purchase sync feature
        self.bot.add_handler(CommandHandler("globalpurchases", self.global_purchases_command))
        self.bot.add_handler(CommandHandler("recentbuys", self.recent_buys_command))
        
        # Callback handlers
        self.bot.add_handler(CallbackQueryHandler(self.handle_callback, filters=UpdatesFilter.regex("game_")))
    
    async def start_command(self, message: Message):
        """Handle /start command"""
        user_id = message.author.user_id
        
        # Check if user exists
        player = self.storage.load_player(user_id)
        
        if not player:
            # Create new player
            player = {
                'bale_id': user_id,
                'username': message.author.username or "Unknown",
                'first_name': message.author.first_name or "Unknown",
                'last_name': message.author.last_name or "",
                'level': 1,
                'experience': 0,
                'rank': "فرمانده",
                'gold': 1000.0,
                'morale': 100.0,
                'last_active': datetime.now().isoformat(),
                'created_at': datetime.now().isoformat(),
                'is_banned': False,
                'language': 'fa'
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
🎖️ **به {self.config['game']['world_name']} خوش آمدید، فرمانده!**

شما برای رهبری یک کشور جدید در این دنیای پر از درگیری و استراتژی انتخاب شده‌اید.

**منابع اولیه شما:**
💰 طلا: 1,000
🛠️ آهن: 100
⛽ نفت: 100
🌾 غذا: 100
🥇 طلا: 100
☢️ اورانیوم: 100

**دستورات سریع:**
/status - مشاهده وضعیت کشور شما
/military - مدیریت نیروهای مسلح
/economy - تجارت و مدیریت منابع
/quest - انجام مأموریت‌ها
/buy - خرید منابع و واحدها (با همگام‌سازی جهانی!)

موفق باشید فرمانده! جهان منتظر رهبری شماست.
            """
        else:
            welcome_text = f"""
🎖️ **خوش برگشتید، {player['rank']} {player['first_name']}!**

کشور شما آماده چالش‌های جدید است.

**وضعیت فعلی:**
💰 طلا: {player['gold']:,.0f}
⭐ سطح: {player['level']}
🏆 رتبه: {player['rank']}
💪 روحیه: {player['morale']:.0f}%

از دستور /help برای مشاهده تمام دستورات استفاده کنید.
            """
        
        keyboard = self.get_main_menu_keyboard()
        await message.reply(welcome_text, components=keyboard)
    
    async def help_command(self, message: Message):
        """Handle /help command"""
        help_text = """
🎖️ **ربات استراتژی جنگ جهانی - دستورات**

**🏠 دستورات پایه:**
/start - شروع بازی یا مشاهده وضعیت
/status - وضعیت فعلی کشور شما
/profile - پروفایل کامل بازیکن
/help - نمایش این پیام راهنما

**💰 اقتصاد:**
/economy - بررسی اقتصادی و تجارت
/trade - رابط تجاری
/materials - مشاهده منابع شما
/buy - خرید منابع و واحدها

**⚔️ نظامی:**
/military - مدیریت نظامی
/attack - حمله به بازیکنان یا استان‌ها
/build - ساخت واحدهای نظامی

**🎯 مأموریت‌ها:**
/quest - مأموریت‌های موجود
/missions - مأموریت‌های فعال شما

**🌍 خریدهای جهانی (ویژگی جدید!):**
/globalpurchases - مشاهده تاریخچه خریدهای جهانی
/recentbuys - آخرین خریدهای انجام شده توسط بازیکنان

از صفحه کلیدهای شیشه‌ای برای پیمایش آسان استفاده کنید!
        """
        await message.reply(help_text)
    
    async def status_command(self, message: Message):
        """Handle /status command"""
        user_id = message.author.user_id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.reply("❌ ابتدا باید بازی را با دستور /start شروع کنید")
            return
        
        # Get player materials and units
        materials = self.storage.load_materials(user_id)
        units = self.storage.load_units(user_id)
        
        total_units = sum(units.values())
        
        status_text = f"""
🎖️ **{player['rank']} {player['first_name']}**

**📊 آمار پایه:**
💰 طلا: {player['gold']:,.0f}
⭐ سطح: {player['level']} (XP: {player['experience']:,})
💪 روحیه: {player['morale']:.0f}%
🛡️ کل واحدها: {total_units:,}

**📦 منابع:**
🛠️ آهن: {materials.get('iron', 0):,.0f}
⛽ نفت: {materials.get('oil', 0):,.0f}
🌾 غذا: {materials.get('food', 0):,.0f}
🥇 طلا: {materials.get('gold', 0):,.0f}
☢️ اورانیوم: {materials.get('uranium', 0):,.0f}
🔩 فولاد: {materials.get('steel', 0):,.0f}

**⏰ آخرین فعالیت:** {player['last_active'][:16]}
        """
        
        keyboard = self.get_status_menu_keyboard()
        await message.reply(status_text, components=keyboard)
    
    async def profile_command(self, message: Message):
        """Handle /profile command"""
        user_id = message.author.user_id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.reply("❌ ابتدا باید بازی را با دستور /start شروع کنید")
            return
        
        # Get detailed stats
        materials = self.storage.load_materials(user_id)
        units = self.storage.load_units(user_id)
        
        profile_text = f"""
👤 **پروفایل کامل - {player['rank']} {player['first_name']}**

**🎖️ رتبه نظامی:** {player['rank']}
**⭐ سطح تجربه:** {player['level']}
**💯 امتیاز تجربه:** {player['experience']:,}
**💰 خزانه:** {player['gold']:,.0f} طلا
**💪 روحیه:** {player['morale']:.0f}%

**📦 موجودی منابع:**
"""
        for material, quantity in materials.items():
            emoji = {"iron": "🛠️", "oil": "⛽", "food": "🌾", "gold": "🥇", "uranium": "☢️", "steel": "🔩"}.get(material, "📦")
            profile_text += f"{emoji} {material}: {quantity:,.0f}\n"
        
        profile_text += f"""
**⚔️ نیروهای نظامی:**
"""
        for unit_type, quantity in units.items():
            emoji = {"infantry": "👥", "tank": "🚗", "artillery": "💣", "aircraft": "✈️", "ship": "🚢"}.get(unit_type, "⚔️")
            profile_text += f"{emoji} {unit_type}: {quantity:,}\n"
        
        profile_text += f"""
**📅 عضو از:** {player['created_at'][:10]}
**⏰ آخرین فعالیت:** {player['last_active'][:16]}
        """
        
        await message.reply(profile_text)
    
    async def economy_command(self, message: Message):
        """Handle /economy command"""
        user_id = message.author.user_id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.reply("❌ ابتدا باید بازی را با دستور /start شروع کنید")
            return
        
        # Get current market prices
        prices = self.config["economy"]["materials"]
        
        economy_text = f"""
💰 **نمای کلی اقتصادی**

**📈 قیمت‌های فعلی بازار:**
"""
        for material, price_info in prices.items():
            emoji = {"iron": "🛠️", "oil": "⛽", "food": "🌾", "gold": "🥇", "uranium": "☢️", "steel": "🔩"}.get(material, "📦")
            economy_text += f"{emoji} {material}: {price_info['base_price']:.2f} طلا/واحد\n"
        
        economy_text += f"""
**💼 منابع شما:**
"""
        materials = self.storage.load_materials(user_id)
        for material, quantity in materials.items():
            emoji = {"iron": "🛠️", "oil": "⛽", "food": "🌾", "gold": "🥇", "uranium": "☢️", "steel": "🔩"}.get(material, "📦")
            economy_text += f"{emoji} {material}: {quantity:,.0f}\n"
        
        economy_text += f"""
**💰 خزانه:** {player['gold']:,.0f} طلا

از دستور /trade برای خرید و فروش منابع استفاده کنید!
از دستور /buy برای خریدهای سریع استفاده کنید (با همگام‌سازی جهانی!)
        """
        
        keyboard = self.get_economy_menu_keyboard()
        await message.reply(economy_text, components=keyboard)
    
    async def trade_command(self, message: Message):
        """Handle /trade command"""
        keyboard = self.get_trade_menu_keyboard()
        await message.reply("💼 **مرکز تجاری**\n\nانتخاب کنید چه کاری می‌خواهید انجام دهید:", components=keyboard)
    
    async def materials_command(self, message: Message):
        """Handle /materials command"""
        user_id = message.author.user_id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.reply("❌ ابتدا باید بازی را با دستور /start شروع کنید")
            return
        
        materials = self.storage.load_materials(user_id)
        
        materials_text = "📦 **موجودی منابع شما**\n\n"
        
        for material, quantity in materials.items():
            emoji = {"iron": "🛠️", "oil": "⛽", "food": "🌾", "gold": "🥇", "uranium": "☢️", "steel": "🔩"}.get(material, "📦")
            materials_text += f"{emoji} **{material}**: {quantity:,.0f} واحد\n"
        
        await message.reply(materials_text)
    
    async def buy_command(self, message: Message):
        """Handle /buy command - with global purchase sync"""
        user_id = message.author.user_id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.reply("❌ ابتدا باید بازی را با دستور /start شروع کنید")
            return
        
        # Show buy options
        buy_text = """
🛒 **مرکز خرید (با همگام‌سازی جهانی)**

هر خریدی که انجام دهید به صورت جهانی ثبت می‌شود و همه بازیکنان می‌توانند آن را ببینند!

**منابع موجود:**
🛠️ آهن - 10 طلا/واحد
⛽ نفت - 15 طلا/واحد
🌾 غذا - 5 طلا/واحد
☢️ اورانیوم - 100 طلا/واحد
🔩 فولاد - 25 طلا/واحد

**واحدهای نظامی:**
👥 پیاده نظام - 100 طلا
🚗 تانک - 500 طلا
💣 توپخانه - 300 طلا
✈️ هواپیما - 800 طلا
🚢 کشتی - 1000 طلا

برای خرید از دکمه‌های زیر استفاده کنید:
        """
        
        keyboard = self.get_buy_menu_keyboard()
        await message.reply(buy_text, components=keyboard)
    
    async def military_command(self, message: Message):
        """Handle /military command"""
        user_id = message.author.user_id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.reply("❌ ابتدا باید بازی را با دستور /start شروع کنید")
            return
        
        # Get player units
        units = self.storage.load_units(user_id)
        total_units = sum(units.values())
        
        military_text = f"""
⚔️ **نمای کلی نظامی**

**👥 کل نیروها:** {total_units:,} واحد

**📊 تفکیک واحدها:**
"""
        for unit_type, quantity in units.items():
            emoji = {"infantry": "👥", "tank": "🚗", "artillery": "💣", "aircraft": "✈️", "ship": "🚢"}.get(unit_type, "⚔️")
            military_text += f"{emoji} {unit_type}: {quantity:,}\n"
        
        if total_units == 0:
            military_text += "\n❌ شما واحد نظامی ندارید. از دستور /build برای ایجاد ارتش خود استفاده کنید!"
        else:
            military_text += f"\n💪 **روحیه:** {player['morale']:.0f}%"
        
        keyboard = self.get_military_menu_keyboard()
        await message.reply(military_text, components=keyboard)
    
    async def attack_command(self, message: Message):
        """Handle /attack command"""
        keyboard = self.get_attack_menu_keyboard()
        await message.reply("⚔️ **مرکز نبرد**\n\nهدف خود را انتخاب کنید:", components=keyboard)
    
    async def build_units_command(self, message: Message):
        """Handle /build command"""
        keyboard = self.get_build_menu_keyboard()
        await message.reply("🏭 **تولید واحد**\n\nنوع واحد را برای ساخت انتخاب کنید:", components=keyboard)
    
    async def quest_command(self, message: Message):
        """Handle /quest command"""
        keyboard = self.get_quest_menu_keyboard()
        await message.reply("🎯 **مرکز مأموریت**\n\nمأموریت‌ها را بپذیرید:", components=keyboard)
    
    async def missions_command(self, message: Message):
        """Handle /missions command"""
        user_id = message.author.user_id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.reply("❌ ابتدا باید بازی را با دستور /start شروع کنید")
            return
        
        # Get active quests
        quests = self.storage.load_quests(user_id)
        active_quests = [q for q in quests if q.get('status') == 'active']
        
        if not active_quests:
            missions_text = "🎯 **مأموریت‌های فعال**\n\n❌ شما مأموریت فعالی ندارید.\n\nاز دستور /quest برای یافتن مأموریت‌های جدید استفاده کنید!"
        else:
            missions_text = "🎯 **مأموریت‌های فعال**\n\n"
            for quest in active_quests:
                progress = quest.get('progress', 0) * 100
                missions_text += f"**{quest.get('title', 'مأموریت ناشناخته')}**\n"
                missions_text += f"پیشرفت: {progress:.0f}%\n"
                missions_text += f"نوع: {quest.get('type', 'ناشناخته')}\n\n"
        
        await message.reply(missions_text)
    
    async def global_purchases_command(self, message: Message):
        """Handle /globalpurchases command - NEW FEATURE"""
        user_id = message.author.user_id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.reply("❌ ابتدا باید بازی را با دستور /start شروع کنید")
            return
        
        purchases = self.storage.get_recent_global_purchases(limit=20)
        
        if not purchases:
            purchases_text = "🌍 **خریدهای جهانی**\n\n❌ هنوز هیچ خریدی ثبت نشده است."
        else:
            purchases_text = "🌍 **تاریخچه خریدهای جهانی**\n\n"
            for i, purchase in enumerate(purchases, 1):
                player_name = purchase.get('player_name', 'ناشناخته')
                item = purchase.get('item', 'ناشناخته')
                quantity = purchase.get('quantity', 0)
                cost = purchase.get('cost', 0)
                timestamp = purchase.get('timestamp', '')[:16]
                
                purchases_text += f"{i}. **{player_name}** خرید کرد:\n"
                purchases_text += f"   {item} × {quantity:,} (💰 {cost:,.0f} طلا)\n"
                purchases_text += f"   🕐 {timestamp}\n\n"
        
        await message.reply(purchases_text)
    
    async def recent_buys_command(self, message: Message):
        """Handle /recentbuys command - NEW FEATURE"""
        user_id = message.author.user_id
        
        player = self.storage.load_player(user_id)
        if not player:
            await message.reply("❌ ابتدا باید بازی را با دستور /start شروع کنید")
            return
        
        purchases = self.storage.get_recent_global_purchases(limit=10)
        
        if not purchases:
            purchases_text = "🌍 **آخرین خریدها**\n\n❌ هنوز هیچ خریدی ثبت نشده است."
        else:
            purchases_text = "🌍 **آخرین خریدهای بازیکنان**\n\n"
            for i, purchase in enumerate(purchases, 1):
                player_name = purchase.get('player_name', 'ناشناخته')
                item = purchase.get('item', 'ناشناخته')
                quantity = purchase.get('quantity', 0)
                
                purchases_text += f"{i}. {player_name} → {item} × {quantity:,}\n"
        
        await message.reply(purchases_text)
    
    async def handle_callback(self, callback: CallbackQuery):
        """Handle inline keyboard callbacks"""
        data = callback.data
        user_id = callback.from_user.user_id
        
        try:
            if data.startswith("game_main_"):
                await self.handle_main_menu_callback(callback)
            elif data.startswith("game_economy_"):
                await self.handle_economy_callback(callback)
            elif data.startswith("game_military_"):
                await self.handle_military_callback(callback)
            elif data.startswith("game_trade_"):
                await self.handle_trade_callback(callback)
            elif data.startswith("game_quest_"):
                await self.handle_quest_callback(callback)
            elif data.startswith("game_buy_"):
                await self.handle_buy_callback(callback)
            else:
                await callback.answer("❌ عملیات ناشناخته")
        except Exception as e:
            logger.error(f"Error handling callback {data}: {e}")
            await callback.answer("❌ خطایی رخ داد")
    
    async def handle_main_menu_callback(self, callback: CallbackQuery):
        """Handle main menu callbacks"""
        data = callback.data
        
        if data == "game_main_status":
            await self.status_command(callback.message)
        elif data == "game_main_economy":
            await self.economy_command(callback.message)
        elif data == "game_main_military":
            await self.military_command(callback.message)
        elif data == "game_main_quest":
            await self.quest_command(callback.message)
        
        await callback.answer()
    
    async def handle_economy_callback(self, callback: CallbackQuery):
        """Handle economy menu callbacks"""
        data = callback.data
        
        if data == "game_economy_trade":
            await self.trade_command(callback.message)
        elif data == "game_economy_materials":
            await self.materials_command(callback.message)
        elif data == "game_economy_prices":
            await self.economy_command(callback.message)
        elif data == "game_economy_buy":
            await self.buy_command(callback.message)
        
        await callback.answer()
    
    async def handle_military_callback(self, callback: CallbackQuery):
        """Handle military menu callbacks"""
        data = callback.data
        
        if data == "game_military_attack":
            await self.attack_command(callback.message)
        elif data == "game_military_build":
            await self.build_units_command(callback.message)
        elif data == "game_military_units":
            await self.military_command(callback.message)
        
        await callback.answer()
    
    async def handle_trade_callback(self, callback: CallbackQuery):
        """Handle trade menu callbacks"""
        data = callback.data
        
        if data == "game_trade_buy":
            await callback.message.reply("💼 **خرید منابع**\n\nاین قابلیت به زودی اضافه می‌شود! از دستور /materials برای مشاهده منابع فعلی خود استفاده کنید.")
        elif data == "game_trade_sell":
            await callback.message.reply("💼 **فروش منابع**\n\nاین قابلیت به زودی اضافه می‌شود! از دستور /materials برای مشاهده منابع فعلی خود استفاده کنید.")
        elif data == "game_trade_market":
            await callback.message.reply("📈 **نمای کلی بازار**\n\nاین قابلیت به زودی اضافه می‌شود! از دستور /economy برای مشاهده قیمت‌های فعلی استفاده کنید.")
        
        await callback.answer()
    
    async def handle_quest_callback(self, callback: CallbackQuery):
        """Handle quest menu callbacks"""
        data = callback.data
        
        if data == "game_quest_available":
            await callback.message.reply("🎯 **مأموریت‌های موجود**\n\nاین قابلیت به زودی اضافه می‌شود! برای مأموریت‌های هیجان‌انگیز بعداً بررسی کنید.")
        elif data == "game_quest_active":
            await self.missions_command(callback.message)
        
        await callback.answer()
    
    async def handle_buy_callback(self, callback: CallbackQuery):
        """Handle buy menu callbacks - with global purchase sync"""
        data = callback.data
        user_id = callback.from_user.user_id
        
        player = self.storage.load_player(user_id)
        if not player:
            await callback.answer("❌ ابتدا باید بازی را شروع کنید")
            return
        
        # Parse buy action
        item_type = data.replace("game_buy_", "")
        
        # Material purchases
        if item_type in self.config["economy"]["materials"]:
            price = self.config["economy"]["materials"][item_type]["base_price"]
            quantity = 10  # Buy 10 units at a time
            total_cost = price * quantity
            
            if player['gold'] >= total_cost:
                player['gold'] -= total_cost
                self.storage.save_player(player)
                
                materials = self.storage.load_materials(user_id)
                materials[item_type] = materials.get(item_type, 0) + quantity
                self.storage.save_materials(user_id, materials)
                
                # Add to global purchases - THIS IS THE NEW FEATURE!
                purchase_data = {
                    'player_id': user_id,
                    'player_name': player['first_name'],
                    'item': f"🛒 {item_type}",
                    'item_type': 'material',
                    'quantity': quantity,
                    'cost': total_cost
                }
                self.storage.add_global_purchase(purchase_data)
                
                await callback.message.reply(f"✅ شما {quantity} واحد {item_type} خریداری کردید!\n💰 هزینه: {total_cost:,.0f} طلا\n\n🌍 این خرید به صورت جهانی ثبت شد!")
                await callback.answer()
            else:
                await callback.answer("❌ طلای کافی ندارید!")
        
        # Unit purchases
        elif item_type in self.config["military"]["unit_types"]:
            unit_cost = self.config["military"]["unit_types"][item_type]["cost"]
            
            if player['gold'] >= unit_cost:
                player['gold'] -= unit_cost
                self.storage.save_player(player)
                
                units = self.storage.load_units(user_id)
                units[item_type] = units.get(item_type, 0) + 1
                self.storage.save_units(user_id, units)
                
                # Add to global purchases - THIS IS THE NEW FEATURE!
                purchase_data = {
                    'player_id': user_id,
                    'player_name': player['first_name'],
                    'item': f"⚔️ {item_type}",
                    'item_type': 'unit',
                    'quantity': 1,
                    'cost': unit_cost
                }
                self.storage.add_global_purchase(purchase_data)
                
                await callback.message.reply(f"✅ شما 1 واحد {item_type} خریداری کردید!\n💰 هزینه: {unit_cost:,.0f} طلا\n\n🌍 این خرید به صورت جهانی ثبت شد!")
                await callback.answer()
            else:
                await callback.answer("❌ طلای کافی ندارید!")
        else:
            await callback.answer("❌ آیتم ناشناخته")
    
    # Keyboard builders
    def get_main_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get main menu keyboard"""
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("📊 وضعیت", callback_data="game_main_status"))
        keyboard.add(InlineKeyboardButton("💰 اقتصاد", callback_data="game_main_economy"))
        keyboard.add(InlineKeyboardButton("⚔️ نظامی", callback_data="game_main_military"))
        keyboard.add(InlineKeyboardButton("🎯 مأموریت‌ها", callback_data="game_main_quest"))
        return keyboard
    
    def get_status_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get status menu keyboard"""
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("💰 اقتصاد", callback_data="game_main_economy"))
        keyboard.add(InlineKeyboardButton("⚔️ نظامی", callback_data="game_main_military"))
        keyboard.add(InlineKeyboardButton("🎯 مأموریت‌ها", callback_data="game_main_quest"))
        keyboard.add(InlineKeyboardButton("📋 پروفایل", callback_data="game_main_profile"))
        return keyboard
    
    def get_economy_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get economy menu keyboard"""
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("💼 تجارت", callback_data="game_economy_trade"))
        keyboard.add(InlineKeyboardButton("🛒 خرید سریع", callback_data="game_economy_buy"))
        keyboard.add(InlineKeyboardButton("📦 منابع", callback_data="game_economy_materials"))
        keyboard.add(InlineKeyboardButton("📈 قیمت‌ها", callback_data="game_economy_prices"))
        keyboard.add(InlineKeyboardButton("🏠 منوی اصلی", callback_data="game_main_status"))
        return keyboard
    
    def get_military_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get military menu keyboard"""
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("⚔️ حمله", callback_data="game_military_attack"))
        keyboard.add(InlineKeyboardButton("🏭 ساخت واحد", callback_data="game_military_build"))
        keyboard.add(InlineKeyboardButton("👥 واحدهای من", callback_data="game_military_units"))
        keyboard.add(InlineKeyboardButton("🏠 منوی اصلی", callback_data="game_main_status"))
        return keyboard
    
    def get_trade_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get trade menu keyboard"""
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("💰 خرید منابع", callback_data="game_trade_buy"))
        keyboard.add(InlineKeyboardButton("💸 فروش منابع", callback_data="game_trade_sell"))
        keyboard.add(InlineKeyboardButton("📈 بازار", callback_data="game_trade_market"))
        keyboard.add(InlineKeyboardButton("🏠 منوی اصلی", callback_data="game_main_economy"))
        return keyboard
    
    def get_attack_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get attack menu keyboard"""
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("👤 حمله به بازیکن", callback_data="game_attack_player"))
        keyboard.add(InlineKeyboardButton("🏰 حمله به استان", callback_data="game_attack_province"))
        keyboard.add(InlineKeyboardButton("🏠 منوی اصلی", callback_data="game_main_military"))
        return keyboard
    
    def get_build_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get build menu keyboard"""
        keyboard = InlineKeyboardMarkup()
        for unit_type in self.config["military"]["unit_types"]:
            keyboard.add(InlineKeyboardButton(f"🏭 ساخت {unit_type}", callback_data=f"game_build_{unit_type}"))
        keyboard.add(InlineKeyboardButton("🏠 منوی اصلی", callback_data="game_main_military"))
        return keyboard
    
    def get_quest_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get quest menu keyboard"""
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🎯 مأموریت‌های موجود", callback_data="game_quest_available"))
        keyboard.add(InlineKeyboardButton("📋 مأموریت‌های من", callback_data="game_quest_active"))
        keyboard.add(InlineKeyboardButton("🏠 منوی اصلی", callback_data="game_main_status"))
        return keyboard
    
    def get_buy_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get buy menu keyboard with materials and units"""
        keyboard = InlineKeyboardMarkup()
        
        # Material buttons
        keyboard.add(InlineKeyboardButton("🛠️ خرید آهن (10 واحد)", callback_data="game_buy_iron"))
        keyboard.add(InlineKeyboardButton("⛽ خرید نفت (10 واحد)", callback_data="game_buy_oil"))
        keyboard.add(InlineKeyboardButton("🌾 خرید غذا (10 واحد)", callback_data="game_buy_food"))
        keyboard.add(InlineKeyboardButton("☢️ خرید اورانیوم (10 واحد)", callback_data="game_buy_uranium"))
        keyboard.add(InlineKeyboardButton("🔩 خرید فولاد (10 واحد)", callback_data="game_buy_steel"))
        
        # Unit buttons
        keyboard.add(InlineKeyboardButton("👥 خرید پیاده نظام", callback_data="game_buy_infantry"))
        keyboard.add(InlineKeyboardButton("🚗 خرید تانک", callback_data="game_buy_tank"))
        keyboard.add(InlineKeyboardButton("💣 خرید توپخانه", callback_data="game_buy_artillery"))
        keyboard.add(InlineKeyboardButton("✈️ خرید هواپیما", callback_data="game_buy_aircraft"))
        keyboard.add(InlineKeyboardButton("🚢 خرید کشتی", callback_data="game_buy_ship"))
        
        keyboard.add(InlineKeyboardButton("🏠 منوی اصلی", callback_data="game_main_economy"))
        return keyboard
    
    async def start(self):
        """Start the bot"""
        logger.info("Starting Bale World War Bot...")
        
        # Start polling
        await self.bot.run()
    
    async def stop(self):
        """Stop the bot"""
        logger.info("Stopping Bale World War Bot...")
        await self.bot.close()

if __name__ == "__main__":
    bot = BaleWorldWarBot()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        asyncio.run(bot.stop())
