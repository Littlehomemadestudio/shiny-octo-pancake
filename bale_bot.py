import os
import time
import random
import asyncio
from datetime import datetime, timedelta
from bale import Bot, Message, User, Chat, ChatMember

# -------------------- CONFIGURATION --------------------
TOKEN = "1014684452:DsvPJv7fND2xZcx7C4VfydXiJDfDnBhvL1nitb4S"

# Initialize bot
bot = Bot(token=TOKEN)

# -------------------- GAME CONFIGURATION --------------------
# Real-life military assets with costs, power, and names
MILITARY_ASSETS = {
    # Tanks
    "abrams": {"cost": 50, "power": 5, "name": "تانک آبرامز"},
    "t90": {"cost": 100, "power": 10, "name": "تانک تی-90"},
    "leopard": {"cost": 200, "power": 20, "name": "تانک لئوپارد 2"},
    "merkava": {"cost": 500, "power": 50, "name": "تانک مرکاوا"},
    
    # Aircraft
    "f16": {"cost": 100, "power": 15, "name": "اف-16"},
    "su27": {"cost": 250, "power": 35, "name": "سوخو-27"},
    "b2": {"cost": 500, "power": 70, "name": "بمب افکن بی-2"},
    "predator": {"cost": 150, "power": 25, "name": "پهپاد پردیتور"},
    
    # Missiles
    "tomahawk": {"cost": 300, "power": 60, "name": "موشک توماهاوک"},
    "scud": {"cost": 1000, "power": 200, "name": "موشک اسکاد"},
    "patriot": {"cost": 800, "power": 150, "name": "موشک پاتریوت"},
    
    # Navy
    "destroyer": {"cost": 1200, "power": 250, "name": "ناوشکن"},
    "submarine": {"cost": 1500, "power": 300, "name": "زیردریایی"},
    "carrier": {"cost": 5000, "power": 1000, "name": "ناو هواپیمابر"},
    
    # Infantry
    "soldier": {"cost": 10, "power": 1, "name": "سرباز"},
    "marine": {"cost": 100, "power": 15, "name": "تفنگدار دریایی"},
    
    # Artillery
    "howitzer": {"cost": 300, "power": 55, "name": "هویتزر"},
    "mlrs": {"cost": 400, "power": 70, "name": "سامانه راکتی چندلول"},
    
    # Defense Systems
    "sam": {"cost": 350, "power": 60, "name": "سامانه ضدهوایی"},
    "radar": {"cost": 200, "power": 10, "name": "سیستم رادار"},
}

BASE_POINTS_PER_MESSAGE = 2000
COOLDOWN_MINUTES = 0

# -------------------- IN-MEMORY DATA STORAGE --------------------
group_data = {}
message_history = {}  # Store message IDs for cleanup

def get_chat_data(chat_id):
    """دریافت یا ایجاد داده برای یک چت خاص"""
    chat_id_str = str(chat_id)
    if chat_id_str not in group_data:
        group_data[chat_id_str] = {
            "owner_id": None,
            "rules": "قوانین گروه هنوز تنظیم نشده است.",
            "welcome_message": "به گروه خوش آمدید! 🎉",
            "users": {},
            "alliances": {}
        }
    return group_data[chat_id_str]

def get_user_data(chat_id, user_id):
    """دریافت یا ایجاد داده برای یک کاربر خاص"""
    chat_data = get_chat_data(chat_id)
    user_id_str = str(user_id)
    
    if user_id_str not in chat_data["users"]:
        chat_data["users"][user_id_str] = {
            "points": 0,
            "last_message_time": 0,
            "military": {asset: 0 for asset in MILITARY_ASSETS},
            "battles_won": 0,
            "battles_lost": 0,
            "alliance": None
        }
    
    return chat_data["users"][user_id_str]

def add_message_to_history(chat_id, message_id):
    """Add message to cleanup history"""
    chat_id_str = str(chat_id)
    if chat_id_str not in message_history:
        message_history[chat_id_str] = []
    
    message_history[chat_id_str].append({
        "message_id": message_id,
        "timestamp": time.time()
    })
    
    # Keep only last 100 messages
    if len(message_history[chat_id_str]) > 100:
        message_history[chat_id_str] = message_history[chat_id_str][-100:]

# -------------------- HELPER FUNCTIONS --------------------
def is_owner(user_id, chat_id):
    """بررسی آیا کاربر صاحب گروه است"""
    chat_data = get_chat_data(chat_id)
    return chat_data["owner_id"] == user_id

async def is_creator(user_id, chat_id):
    """بررسی آیا کاربر سازنده گروه است"""
    try:
        chat_member = await bot.get_chat_member(chat_id, user_id)
        return chat_member.status == "creator"
    except:
        return False

async def delete_message_safe(message, delay=0):
    """حذف ایمن پیام پس از تاخیر"""
    try:
        await asyncio.sleep(delay)
        await message.delete()
    except:
        pass

def calculate_total_power(user_data):
    """محاسبه قدرت کل نظامی کاربر"""
    total_power = 0
    for asset_type, count in user_data["military"].items():
        if asset_type in MILITARY_ASSETS and count > 0:
            asset_power = MILITARY_ASSETS[asset_type]["power"]
            total_power += asset_power * count
    return total_power

# -------------------- BOT EVENTS --------------------
@bot.event
async def on_ready():
    """هندلر راه‌اندازی ربات"""
    print(f"✅ {bot.user.username} is ready!")

@bot.event
async def on_message(message: Message):
    """مدیریت پیام‌های دریافتی"""
    try:
        if message.author.is_bot:
            return

        chat_id = message.chat.id
        user_id = message.author.user_id
        text = message.content or ""
        
        # Track message for cleanup
        add_message_to_history(chat_id, message.message_id)
        
        # Award points for activity
        await handle_points(message, chat_id, user_id)
        
        # Handle commands
        if text.startswith("/"):
            await handle_command(message, text.lower(), chat_id, user_id)
            
    except Exception as e:
        print(f"Error in on_message: {e}")

@bot.event
async def on_chat_join(chat_member: ChatMember):
    """مدیریت ورود عضو جدید"""
    try:
        chat_id = chat_member.chat.id
        user = chat_member.user
        chat_data = get_chat_data(chat_id)
        welcome_msg = chat_data["welcome_message"]
        await bot.send_message(chat_id, f"👋 {user.first_name} {welcome_msg}")
    except Exception as e:
        print(f"Error in on_chat_join: {e}")

# -------------------- COMMAND HANDLERS --------------------
async def handle_points(message, chat_id, user_id):
    """اعطای امتیاز به کاربر"""
    try:
        user_data = get_user_data(chat_id, user_id)
        current_time = time.time()
        
        if current_time - user_data["last_message_time"] >= COOLDOWN_MINUTES * 60:
            user_data["points"] += BASE_POINTS_PER_MESSAGE
            user_data["last_message_time"] = current_time
    except Exception as e:
        print(f"Error in handle_points: {e}")

async def handle_command(message, command, chat_id, user_id):
    """پردازش دستورات ربات"""
    try:
        # General commands
        if command == "/start":
            reply = await message.reply("🤖 ربات نظامی بله فعال است!\n\n"
                              "دستورات:\n"
                              "/help - راهنمایی\n"
                              "/game_help - راهنمای بازی\n"
                              "/clean - پاکسازی پیام‌های ربات")
            add_message_to_history(chat_id, reply.message_id)
        
        elif command == "/help":
            await show_help(message, chat_id)
        
        elif command == "/rules":
            await show_rules(message, chat_id)
        
        elif command == "/info":
            await user_info(message, chat_id)
        
        elif command == "/game_help":
            await game_help(message, chat_id)
        
        elif command == "/clean":
            await clean_messages(message, chat_id, user_id)
        
        # Game commands
        elif command == "/points":
            await show_points(message, chat_id, user_id)
        
        elif command == "/military":
            await show_military(message, chat_id, user_id)
        
        elif command.startswith("/buy"):
            await buy_asset(message, chat_id, user_id)
        
        elif command.startswith("/attack"):
            await attack_user(message, chat_id, user_id)
        
        # Alliance commands
        elif command.startswith("/alliance"):
            await handle_alliance_command(message, chat_id, user_id)
        
        # Owner commands
        elif command.startswith("/setowner") and await is_creator(user_id, chat_id):
            await set_owner(message, chat_id)
        
        elif command.startswith("/setrules") and is_owner(user_id, chat_id):
            await set_rules(message, chat_id)
        
        elif command.startswith("/setwelcome") and is_owner(user_id, chat_id):
            await set_welcome(message, chat_id)
        
        elif command.startswith("/ban") and is_owner(user_id, chat_id):
            await ban_user(message, chat_id)
        
        else:
            reply = await message.reply("❌ دستور نامعتبر یا عدم دسترسی!")
            add_message_to_history(chat_id, reply.message_id)
            await delete_message_safe(message, 3)
            await delete_message_safe(reply, 3)
    
    except Exception as e:
        print(f"Error in handle_command: {e}")

# -------------------- CLEAN COMMAND --------------------
async def clean_messages(message, chat_id, user_id):
    """پاکسازی پیام‌های ربات و کامندهای کاربر"""
    try:
        chat_id_str = str(chat_id)
        
        if chat_id_str not in message_history:
            reply = await message.reply("⚠️ هیچ پیامی برای پاکسازی وجود ندارد!")
            add_message_to_history(chat_id, reply.message_id)
            await delete_message_safe(reply, 3)
            return
        
        deleted_count = 0
        messages_to_delete = message_history[chat_id_str].copy()
        
        for msg_data in messages_to_delete:
            try:
                # Try to delete each message
                await bot.delete_message(chat_id, msg_data["message_id"])
                deleted_count += 1
                await asyncio.sleep(0.1)  # Small delay to avoid rate limits
            except:
                pass
        
        # Clear history
        message_history[chat_id_str] = []
        
        # Delete the clean command itself
        await delete_message_safe(message, 0)
        
        # Send confirmation and auto-delete
        confirmation = await bot.send_message(chat_id, f"✅ {deleted_count} پیام پاکسازی شد!")
        await delete_message_safe(confirmation, 3)
        
    except Exception as e:
        print(f"Error in clean_messages: {e}")
        reply = await message.reply("⚠️ خطا در پاکسازی پیام‌ها!")
        await delete_message_safe(reply, 3)

# -------------------- GAME COMMANDS --------------------
async def game_help(message, chat_id):
    """نمایش راهنمای بازی"""
    help_text = """
🎮 راهنمای بازی نظامی:

💰 انواع تجهیزات:
**تانک‌ها:**
• abrams - تانک آبرامز (50 امتیاز)
• t90 - تانک تی-90 (100 امتیاز)
• leopard - لئوپارد 2 (200 امتیاز)
• merkava - مرکاوا (500 امتیاز)

**هواپیماها:**
• f16 - اف-16 (100 امتیاز)
• su27 - سوخو-27 (250 امتیاز)
• b2 - بمب افکن بی-2 (500 امتیاز)
• predator - پهپاد پردیتور (150 امتیاز)

**موشک‌ها:**
• tomahawk - توماهاوک (300 امتیاز)
• scud - اسکاد (1000 امتیاز)
• patriot - پاتریوت (800 امتیاز)

**نیروی دریایی:**
• destroyer - ناوشکن (1200 امتیاز)
• submarine - زیردریایی (1500 امتیاز)
• carrier - ناو هواپیمابر (5000 امتیاز)

**دیگر:**
• soldier - سرباز (10 امتیاز)
• marine - تفنگدار دریایی (100 امتیاز)
• howitzer - هویتزر (300 امتیاز)
• mlrs - راکتی چندلول (400 امتیاز)
• sam - ضدهوایی (350 امتیاز)
• radar - رادار (200 امتیاز)

📝 دستورات:
/points - امتیازات شما
/military - نیروی نظامی
/buy [نوع] [تعداد] - خرید تجهیزات
/attack [reply] - حمله به کاربر
/alliance_create [نام] - ایجاد اتحاد
/alliance_join [نام] - پیوستن به اتحاد
/clean - پاکسازی پیام‌ها

💡 با ارسال پیام امتیاز کسب کنید!
    """
    reply = await message.reply(help_text)
    add_message_to_history(chat_id, reply.message_id)

async def show_points(message, chat_id, user_id):
    """نمایش امتیازات کاربر"""
    try:
        user_data = get_user_data(chat_id, user_id)
        reply = await message.reply(f"💰 امتیازات شما: {user_data['points']}")
        add_message_to_history(chat_id, reply.message_id)
        await delete_message_safe(message, 10)
        await delete_message_safe(reply, 10)
    except Exception as e:
        print(f"Error in show_points: {e}")

async def show_military(message, chat_id, user_id):
    """نمایش نیروی نظامی کاربر"""
    try:
        user_data = get_user_data(chat_id, user_id)
        
        military_text = "🎖 نیروی نظامی شما:\n\n"
        
        categories = {
            "🚜 تانک‌ها": ["abrams", "t90", "leopard", "merkava"],
            "✈️ هواپیماها": ["f16", "su27", "b2", "predator"],
            "🚀 موشک‌ها": ["tomahawk", "scud", "patriot"],
            "⚓ نیروی دریایی": ["destroyer", "submarine", "carrier"],
            "👥 پیاده نظام": ["soldier", "marine"],
            "💣 توپخانه": ["howitzer", "mlrs"],
            "🛡 دفاعی": ["sam", "radar"]
        }
        
        for category_name, asset_types in categories.items():
            category_assets = []
            for asset_type in asset_types:
                count = user_data["military"][asset_type]
                if count > 0:
                    asset_name = MILITARY_ASSETS[asset_type]["name"]
                    category_assets.append(f"  • {asset_name}: {count}")
            
            if category_assets:
                military_text += f"{category_name}:\n" + "\n".join(category_assets) + "\n\n"
        
        total_power = calculate_total_power(user_data)
        battle_stats = f"💪 قدرت کل: {total_power}\n🏆 برد: {user_data['battles_won']} | 💀 باخت: {user_data['battles_lost']}"
        
        response = f"{military_text}\n{battle_stats}"
        reply = await message.reply(response)
        add_message_to_history(chat_id, reply.message_id)
        await delete_message_safe(message, 15)
        await delete_message_safe(reply, 15)
    except Exception as e:
        print(f"Error in show_military: {e}")

async def buy_asset(message, chat_id, user_id):
    """خرید تجهیزات نظامی"""
    try:
        parts = message.content.split()
        if len(parts) < 3:
            reply = await message.reply("⚠️ فرمت: /buy [نوع] [تعداد]\nمثال: /buy abrams 5")
            add_message_to_history(chat_id, reply.message_id)
            await delete_message_safe(reply, 5)
            return
        
        asset_type = parts[1].lower()
        try:
            quantity = int(parts[2])
            if quantity <= 0:
                raise ValueError
        except ValueError:
            reply = await message.reply("⚠️ تعداد باید عدد مثبت باشد!")
            add_message_to_history(chat_id, reply.message_id)
            await delete_message_safe(reply, 3)
            return
        
        if asset_type not in MILITARY_ASSETS:
            reply = await message.reply("⚠️ نوع تجهیز نامعتبر! از /game_help استفاده کنید.")
            add_message_to_history(chat_id, reply.message_id)
            await delete_message_safe(reply, 5)
            return
        
        user_data = get_user_data(chat_id, user_id)
        asset_cost = MILITARY_ASSETS[asset_type]["cost"]
        total_cost = asset_cost * quantity
        
        if user_data["points"] < total_cost:
            reply = await message.reply(f"⚠️ امتیاز کافی ندارید!\nنیاز: {total_cost} | دارید: {user_data['points']}")
            add_message_to_history(chat_id, reply.message_id)
            await delete_message_safe(reply, 5)
            return
        
        user_data["points"] -= total_cost
        user_data["military"][asset_type] += quantity
        
        asset_name = MILITARY_ASSETS[asset_type]["name"]
        response = f"✅ {quantity} عدد {asset_name} خریداری شد!\n💰 امتیاز باقیمانده: {user_data['points']}"
        reply = await message.reply(response)
        add_message_to_history(chat_id, reply.message_id)
        
        await delete_message_safe(message, 3)
        await delete_message_safe(reply, 10)
        
    except Exception as e:
        print(f"Error in buy_asset: {e}")

async def attack_user(message, chat_id, user_id):
    """حمله به کاربر دیگر"""
    try:
        if not message.reply_to_message:
            reply = await message.reply("⚠️ به پیام کاربر مورد نظر ریپلای کنید!")
            add_message_to_history(chat_id, reply.message_id)
            await delete_message_safe(reply, 3)
            return
        
        target_user = message.reply_to_message.author
        if target_user.user_id == user_id:
            reply = await message.reply("😅 نمی‌توانید به خودتان حمله کنید!")
            add_message_to_history(chat_id, reply.message_id)
            await delete_message_safe(reply, 3)
            return
        
        attacker_data = get_user_data(chat_id, user_id)
        defender_data = get_user_data(chat_id, target_user.user_id)
        
        attacker_power = calculate_total_power(attacker_data)
        if attacker_power == 0:
            reply = await message.reply("⚠️ شما نیروی نظامی ندارید!")
            add_message_to_history(chat_id, reply.message_id)
            await delete_message_safe(reply, 3)
            return
        
        defender_power = calculate_total_power(defender_data)
        if defender_power == 0:
            reply = await message.reply("⚠️ کاربر مورد نظر نیروی نظامی ندارد!")
            add_message_to_history(chat_id, reply.message_id)
            await delete_message_safe(reply, 3)
            return
        
        # Battle calculation
        attack_strength = attacker_power * random.uniform(0.8, 1.2)
        defense_strength = defender_power * random.uniform(0.8, 1.2)
        
        if attack_strength > defense_strength:
            damage_ratio = min(0.3, (attack_strength - defense_strength) / attack_strength * 0.5)
            stolen_points = int(defender_data["points"] * damage_ratio)
            
            attacker_data["points"] += stolen_points
            defender_data["points"] = max(0, defender_data["points"] - stolen_points)
            attacker_data["battles_won"] += 1
            defender_data["battles_lost"] += 1
            
            result_text = (f"⚔️ {message.author.first_name} به {target_user.first_name} حمله کرد و برنده شد!\n"
                          f"💰 غنیمت: {stolen_points} امتیاز")
        else:
            damage_ratio = min(0.2, (defense_strength - attack_strength) / defense_strength * 0.3)
            lost_points = int(attacker_data["points"] * damage_ratio)
            
            attacker_data["points"] = max(0, attacker_data["points"] - lost_points)
            attacker_data["battles_lost"] += 1
            defender_data["battles_won"] += 1
            
            result_text = (f"🛡 {message.author.first_name} به {target_user.first_name} حمله کرد اما شکست خورد!\n"
                          f"💸 ضرر: {lost_points} امتیاز")
        
        reply = await message.reply(result_text)
        add_message_to_history(chat_id, reply.message_id)
        
    except Exception as e:
        print(f"Error in attack_user: {e}")

# -------------------- ALLIANCE COMMANDS --------------------
async def handle_alliance_command(message, chat_id, user_id):
    """مدیریت دستورات اتحاد"""
    parts = message.content.split()
    if len(parts) < 2:
        reply = await message.reply("⚠️ فرمت نادرست! از /game_help استفاده کنید.")
        add_message_to_history(chat_id, reply.message_id)
        return
    
    subcommand = parts[1].lower()
    
    if subcommand == "create" and len(parts) >= 3:
        await alliance_create(message, chat_id, user_id, " ".join(parts[2:]))
    elif subcommand == "join" and len(parts) >= 3:
        await alliance_join(message, chat_id, user_id, " ".join(parts[2:]))
    elif subcommand == "leave":
        await alliance_leave(message, chat_id, user_id)
    elif subcommand == "list":
        await alliance_list(message, chat_id)
    else:
        reply = await message.reply("⚠️ دستور اتحاد نامعتبر!")
        add_message_to_history(chat_id, reply.message_id)

async def alliance_create(message, chat_id, user_id, alliance_name):
    """ایجاد اتحاد جدید"""
    try:
        chat_data = get_chat_data(chat_id)
        user_data = get_user_data(chat_id, user_id)
        
        if user_data["alliance"]:
            reply = await message.reply("⚠️ شما قبلاً در یک اتحاد هستید!")
            add_message_to_history(chat_id, reply.message_id)
            return
        
        if alliance_name in chat_data["alliances"]:
            reply = await message.reply("⚠️ این نام قبلاً استفاده شده!")
            add_message_to_history(chat_id, reply.message_id)
            return
        
        chat_data["alliances"][alliance_name] = {
            "creator": user_id,
            "members": [user_id]
        }
        user_data["alliance"] = alliance_name
        
        reply = await message.reply(f"✅ اتحاد '{alliance_name}' ایجاد شد!")
        add_message_to_history(chat_id, reply.message_id)
    except Exception as e:
        print(f"Error in alliance_create: {e}")

async def alliance_join(message, chat_id, user_id, alliance_name):
    """پیوستن به اتحاد"""
    try:
        chat_data = get_chat_data(chat_id)
        user_data = get_user_data(chat_id, user_id)
        
        if user_data["alliance"]:
            reply = await message.reply("⚠️ شما قبلاً در یک اتحاد هستید!")
            add_message_to_history(chat_id, reply.message_id)
            return
        
        if alliance_name not in chat_data["alliances"]:
            reply = await message.reply("⚠️ این اتحاد وجود ندارد!")
            add_message_to_history(chat_id, reply.message_id)
            return
        
        chat_data["alliances"][alliance_name]["members"].append(user_id)
        user_data["alliance"] = alliance_name
        
        reply = await message.reply(f"✅ به اتحاد '{alliance_name}' پیوستید!")
        add_message_to_history(chat_id, reply.message_id)
    except Exception as e:
        print(f"Error in alliance_join: {e}")

async def alliance_leave(message, chat_id, user_id):
    """ترک اتحاد"""
    try:
        chat_data = get_chat_data(chat_id)
        user_data = get_user_data(chat_id, user_id)
        
        if not user_data["alliance"]:
            reply = await message.reply("⚠️ شما در هیچ اتحادی نیستید!")
            add_message_to_history(chat_id, reply.message_id)
            return
        
        alliance_name = user_data["alliance"]
        alliance = chat_data["alliances"][alliance_name]
        
        if user_id in alliance["members"]:
            alliance["members"].remove(user_id)
        
        if not alliance["members"]:
            del chat_data["alliances"][alliance_name]
        
        user_data["alliance"] = None
        
        reply = await message.reply(f"✅ از اتحاد '{alliance_name}' خارج شدید!")
        add_message_to_history(chat_id, reply.message_id)
    except Exception as e:
        print(f"Error in alliance_leave: {e}")

async def alliance_list(message, chat_id):
    """لیست اتحادها"""
    try:
        chat_data = get_chat_data(chat_id)
        
        if not chat_data["alliances"]:
            reply = await message.reply("⚠️ هیچ اتحادی وجود ندارد!")
            add_message_to_history(chat_id, reply.message_id)
            return
        
        alliances_text = "🤝 لیست اتحادها:\n\n"
        for name, data in chat_data["alliances"].items():
            member_count = len(data["members"])
            alliances_text += f"• {name} ({member_count} عضو)\n"
        
        reply = await message.reply(alliances_text)
        add_message_to_history(chat_id, reply.message_id)
    except Exception as e:
        print(f"Error in alliance_list: {e}")

# -------------------- OTHER COMMANDS --------------------
async def show_help(message, chat_id):
    """نمایش راهنما"""
    help_text = """
🤖 راهنمای ربات:

📋 دستورات عمومی:
/start - شروع
/help - راهنما
/rules - قوانین
/info - اطلاعات شما
/game_help - راهنمای بازی
/clean - پاکسازی پیام‌ها

🎮 دستورات بازی:
/points - امتیازات
/military - نیروی نظامی
/buy [نوع] [تعداد] - خرید
/attack [reply] - حمله

🤝 دستورات اتحاد:
/alliance_create [نام] - ایجاد
/alliance_join [نام] - پیوستن
/alliance_leave - ترک
/alliance_list - لیست

🛡 دستورات مدیریت (فقط مالک):
/setowner - تنظیم مالک
/setrules [متن] - تنظیم قوانین
/setwelcome [متن] - پیام خوشآمد
/ban [reply] - اخراج کاربر
    """
    reply = await message.reply(help_text)
    add_message_to_history(chat_id, reply.message_id)

async def show_rules(message, chat_id):
    """نمایش قوانین"""
    chat_data = get_chat_data(chat_id)
    reply = await message.reply(f"📜 قوانین گروه:\n\n{chat_data['rules']}")
    add_message_to_history(chat_id, reply.message_id)

async def user_info(message, chat_id):
    """نمایش اطلاعات کاربر"""
    user = message.author
    user_data = get_user_data(chat_id, user.user_id)
    
    alliance_info = f"🤝 اتحاد: {user_data['alliance']}\n" if user_data["alliance"] else ""
    
    info_text = (f"👤 اطلاعات کاربر:\n\n"
                f"نام: {user.first_name}\n"
                f"آیدی: {user.user_id}\n"
                f"{alliance_info}"
                f"💰 امتیاز: {user_data['points']}\n"
                f"💪 قدرت: {calculate_total_power(user_data)}")
    
    reply = await message.reply(info_text)
    add_message_to_history(chat_id, reply.message_id)

async def set_owner(message, chat_id):
    """تنظیم مالک گروه"""
    if not message.reply_to_message:
        reply = await message.reply("⚠️ به پیام کاربر ریپلای کنید!")
        add_message_to_history(chat_id, reply.message_id)
        return
    
    new_owner_id = message.reply_to_message.author.user_id
    chat_data = get_chat_data(chat_id)
    chat_data["owner_id"] = new_owner_id
    
    reply = await message.reply("✅ مالک گروه تنظیم شد!")
    add_message_to_history(chat_id, reply.message_id)

async def set_rules(message, chat_id):
    """تنظیم قوانین"""
    new_rules = message.content.replace("/setrules", "").strip()
    if not new_rules:
        reply = await message.reply("⚠️ متن قوانین را وارد کنید!")
        add_message_to_history(chat_id, reply.message_id)
        return
    
    chat_data = get_chat_data(chat_id)
    chat_data["rules"] = new_rules
    
    reply = await message.reply("✅ قوانین به روز شد!")
    add_message_to_history(chat_id, reply.message_id)

async def set_welcome(message, chat_id):
    """تنظیم پیام خوشآمد"""
    new_welcome = message.content.replace("/setwelcome", "").strip()
    if not new_welcome:
        reply = await message.reply("⚠️ متن پیام را وارد کنید!")
        add_message_to_history(chat_id, reply.message_id)
        return
    
    chat_data = get_chat_data(chat_id)
    chat_data["welcome_message"] = new_welcome
    
    reply = await message.reply("✅ پیام خوشآمد به روز شد!")
    add_message_to_history(chat_id, reply.message_id)

async def ban_user(message, chat_id):
    """اخراج کاربر"""
    if not message.reply_to_message:
        reply = await message.reply("⚠️ به پیام کاربر ریپلای کنید!")
        add_message_to_history(chat_id, reply.message_id)
        return
    
    target_user = message.reply_to_message.author
    try:
        await bot.ban_chat_member(chat_id, target_user.user_id)
        reply = await message.reply(f"🚫 {target_user.first_name} از گروه اخراج شد!")
        add_message_to_history(chat_id, reply.message_id)
    except Exception as e:
        print(f"Error banning user: {e}")
        reply = await message.reply("⚠️ خطا در اخراج کاربر!")
        add_message_to_history(chat_id, reply.message_id)

# -------------------- RUN BOT --------------------
if __name__ == "__main__":
    print("🚀 Starting Bale bot...")
    bot.run()
