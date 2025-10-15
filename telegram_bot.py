import os
import json
import time
import random
import asyncio
import traceback
from datetime import datetime, timedelta
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# -------------------- CONFIGURATION --------------------
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your actual token
DATA_FILE = "group_data.json"

# -------------------- GAME CONFIGURATION --------------------
# Real-life military assets with costs, power, and names
MILITARY_ASSETS = {
    # Tanks
    "abrams_tank": {"cost": 50, "power": 5, "name": "Abrams Tank"},
    "leopard_tank": {"cost": 100, "power": 10, "name": "Leopard Tank"},
    "t90_tank": {"cost": 200, "power": 20, "name": "T-90 Tank"},
    "challenger_tank": {"cost": 500, "power": 50, "name": "Challenger Tank"},
    
    # Aircraft
    "f16_fighter": {"cost": 100, "power": 15, "name": "F-16 Fighter"},
    "f35_stealth": {"cost": 250, "power": 35, "name": "F-35 Stealth"},
    "su27_fighter": {"cost": 500, "power": 70, "name": "Su-27 Fighter"},
    "reaper_drone": {"cost": 150, "power": 25, "name": "Reaper Drone"},
    
    # Missiles
    "patriot_missile": {"cost": 300, "power": 60, "name": "Patriot Missile"},
    "tomahawk_missile": {"cost": 1000, "power": 200, "name": "Tomahawk Missile"},
    "javelin_missile": {"cost": 800, "power": 150, "name": "Javelin Missile"},
    
    # Navy
    "destroyer": {"cost": 1200, "power": 250, "name": "Destroyer"},
    "submarine": {"cost": 1500, "power": 300, "name": "Nuclear Submarine"},
    "aircraft_carrier": {"cost": 5000, "power": 1000, "name": "Aircraft Carrier"},
    
    # Infantry
    "soldier": {"cost": 10, "power": 1, "name": "Soldier"},
    "special_forces": {"cost": 100, "power": 15, "name": "Special Forces"},
    
    # Artillery
    "howitzer": {"cost": 300, "power": 55, "name": "Howitzer"},
    "mlrs": {"cost": 400, "power": 70, "name": "MLRS"},
    
    # Defense Systems
    "s400_system": {"cost": 350, "power": 60, "name": "S-400 System"},
    "radar": {"cost": 200, "power": 10, "name": "Radar System"},
}

BASE_POINTS_PER_MESSAGE = 2000
COOLDOWN_MINUTES = 0  # Cooldown between earning points from messages

# -------------------- DATA MANAGEMENT --------------------
group_data = {}

def load_data():
    """Load group data from file"""
    global group_data
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            group_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        group_data = {}
        print("No existing data file found or invalid JSON, starting with empty data")

def save_data():
    """Save group data to file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(group_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving data: {e}")

def get_chat_data(chat_id):
    """Get or create data for a specific chat"""
    chat_id_str = str(chat_id)
    if chat_id_str not in group_data:
        group_data[chat_id_str] = {
            "owner_id": None,
            "warnings": {},
            "muted_users": {},
            "rules": "Group rules have not been set yet.",
            "welcome_message": "Welcome to the group! Please read the rules.",
            "admins": [],
            "users": {},  # Store user game data
            "alliances": {}  # Store alliance data
        }
    return group_data[chat_id_str]

def get_user_data(chat_id, user_id):
    """Get or create data for a specific user in a chat"""
    chat_data = get_chat_data(chat_id)
    user_id_str = str(user_id)
    
    if user_id_str not in chat_data["users"]:
        chat_data["users"][user_id_str] = {
            "points": 0,
            "last_message_time": 0,
            "military": {},  # Unified military storage
            "battles_won": 0,
            "battles_lost": 0,
            "alliance": None  # Name of alliance user belongs to
        }
    
    # Initialize all military types if not present
    user_data = chat_data["users"][user_id_str]
    for asset_type in MILITARY_ASSETS:
        if asset_type not in user_data["military"]:
            user_data["military"][asset_type] = 0
    
    return user_data

# -------------------- HELPER FUNCTIONS --------------------
def is_owner(user_id, chat_id):
    """Check if user is group owner"""
    chat_data = get_chat_data(chat_id)
    return chat_data["owner_id"] == user_id

def format_time(seconds):
    """Format time to readable string"""
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        return f"{seconds//60} minutes"
    elif seconds < 86400:
        return f"{seconds//3600} hours"
    else:
        return f"{seconds//86400} days"

async def delete_message_safe(message, delay=0):
    """Safely delete message after delay"""
    try:
        await asyncio.sleep(delay)
        await message.delete()
    except:
        pass  # Ignore errors if we can't delete the message

def calculate_total_power(user_data):
    """Calculate total military power of user"""
    total_power = 0
    
    # Calculate power of all military assets
    for asset_type, count in user_data["military"].items():
        if asset_type in MILITARY_ASSETS and count > 0:
            asset_power = MILITARY_ASSETS[asset_type]["power"]
            total_power += asset_power * count
    
    return total_power

def get_asset_display_name(asset_type):
    """Get the display name for a military asset"""
    return MILITARY_ASSETS.get(asset_type, {}).get("name", asset_type)

def get_asset_cost(asset_type):
    """Get the cost for a military asset"""
    return MILITARY_ASSETS.get(asset_type, {}).get("cost", 0)

# -------------------- BOT COMMANDS --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    await update.message.reply_text("🤖 Group management bot is active!\n\n"
                                  "Available commands:\n"
                                  "/help - Help\n"
                                  "/rules - Show rules\n"
                                  "/info - User info\n"
                                  "/game_help - Game guide\n"
                                  "/clean - Clean bot messages")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command handler"""
    help_text = """
🤖 Group Management Bot Help:

👤 General Commands:
/help - Show this help
/rules - Show group rules
/info - User information
/game_help - Military game guide
/clean - Clean bot messages

🎮 Game Commands:
/points - Show points
/military - Show military force
/buy [type] [quantity] - Buy equipment
/attack [reply] - Attack user

🤝 Alliance Commands:
/alliance_create [name] - Create alliance
/alliance_join [name] - Join alliance
/alliance_leave - Leave alliance
/alliance_info [name] - Alliance info
/alliance_list - List alliances
/alliance_invite [reply] - Invite to alliance
/alliance_kick [reply] - Kick from alliance

🛡 Owner Commands:
/setowner - Set new owner (creator only)
/mute [time] [reason] - Mute user
/unmute - Unmute user
/ban [reason] - Ban user
/warn [reason] - Warn user
/setrules [text] - Set group rules
/setwelcome [text] - Set welcome message
/addadmin [id] - Add admin
/removeadmin [id] - Remove admin
/owner - Show group owner
    """
    await update.message.reply_text(help_text)

async def clean_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clean command to delete bot messages and user commands"""
    try:
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        
        # Check if user is owner or admin
        if not is_owner(user_id, chat_id):
            await update.message.reply_text("🚫 Only group owner can use this command!")
            return
        
        # Delete the command message
        await delete_message_safe(update.message, 1)
        
        # Send confirmation and delete it after 3 seconds
        confirmation = await update.message.reply_text("🧹 Cleaning bot messages...")
        await delete_message_safe(confirmation, 3)
        
    except Exception as e:
        print(f"Error in clean_command: {e}")
        await update.message.reply_text("⚠️ Error cleaning messages!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    try:
        # Ignore bot messages
        if update.effective_user.is_bot:
            return

        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        text = update.message.text or ""
        
        # Award points for user messages
        await handle_points(update, chat_id, user_id)
        
        # Handle commands
        if text.startswith("/"):
            await handle_command(update, text.lower(), chat_id, user_id)
            
    except Exception as e:
        print(f"Error in handle_message: {e}")
        print(traceback.format_exc())
        try:
            await update.message.reply_text("⚠️ An error occurred!")
        except:
            print("Also failed to send error message")

async def handle_points(update, chat_id, user_id):
    """Award points to user for activity"""
    try:
        user_data = get_user_data(chat_id, user_id)
        current_time = time.time()
        
        # Check cooldown
        if current_time - user_data["last_message_time"] >= COOLDOWN_MINUTES * 60:
            user_data["points"] += BASE_POINTS_PER_MESSAGE
            user_data["last_message_time"] = current_time
            save_data()
    except Exception as e:
        print(f"Error in handle_points: {e}")

async def handle_command(update, command, chat_id, user_id):
    """Process bot commands"""
    try:
        # General commands
        if command == "/start":
            await start(update, context=None)
        
        elif command == "/help":
            await help_command(update, context=None)
        
        elif command == "/rules":
            await show_rules(update, chat_id)
        
        elif command == "/info":
            await user_info(update)
        
        elif command == "/game_help":
            await game_help(update)
        
        elif command == "/clean":
            await clean_command(update, context=None)
        
        # Game commands
        elif command == "/points":
            await show_points(update, chat_id, user_id)
        
        elif command == "/military":
            await show_military(update, chat_id, user_id)
        
        elif command.startswith("/buy"):
            await buy_asset(update, chat_id, user_id)
        
        elif command.startswith("/attack"):
            await attack_user(update, chat_id, user_id)
        
        # Alliance commands
        elif command.startswith("/alliance"):
            await handle_alliance_command(update, chat_id, user_id)
        
        # Owner commands
        elif command.startswith("/setowner") and await is_creator(user_id, chat_id):
            await set_owner(update, chat_id)
        
        elif command.startswith("/mute") and is_owner(user_id, chat_id):
            await mute_user(update, chat_id)
        
        elif command.startswith("/unmute") and is_owner(user_id, chat_id):
            await unmute_user(update, chat_id)
        
        elif command.startswith("/ban") and is_owner(user_id, chat_id):
            await ban_user(update, chat_id)
        
        elif command.startswith("/warn") and is_owner(user_id, chat_id):
            await warn_user(update, chat_id)
        
        elif command.startswith("/setrules") and is_owner(user_id, chat_id):
            await set_rules(update, chat_id)
        
        elif command.startswith("/setwelcome") and is_owner(user_id, chat_id):
            await set_welcome(update, chat_id)
        
        elif command.startswith("/addadmin") and is_owner(user_id, chat_id):
            await add_admin(update, chat_id)
        
        elif command.startswith("/removeadmin") and is_owner(user_id, chat_id):
            await remove_admin(update, chat_id)
        
        elif command == "/owner" and is_owner(user_id, chat_id):
            await show_owner(update, chat_id)
        
        else:
            await update.message.reply_text("🚫 Invalid command or no access!")
    except Exception as e:
        print(f"Error in handle_command: {e}")
        print(traceback.format_exc())
        await update.message.reply_text("⚠️ Error processing command!")

async def is_creator(user_id, chat_id):
    """Check if user is group creator"""
    try:
        bot = context.bot
        chat_member = await bot.get_chat_member(chat_id, user_id)
        return chat_member.status == "creator"
    except:
        return False

# -------------------- GAME COMMAND HANDLERS --------------------
async def game_help(update):
    """Show game help"""
    help_text = """
🎮 Military Game Guide:

Game Commands:
/points - Show your points
/military - Show your military force
/buy [type] [quantity] - Buy military equipment
/attack [reply] - Attack user

💰 Available Equipment Types:
- Tanks: abrams_tank, leopard_tank, t90_tank, challenger_tank
- Aircraft: f16_fighter, f35_stealth, su27_fighter, reaper_drone
- Missiles: patriot_missile, tomahawk_missile, javelin_missile
- Navy: destroyer, submarine, aircraft_carrier
- Infantry: soldier, special_forces
- Artillery: howitzer, mlrs
- Defense Systems: s400_system, radar

🤝 Alliance Commands:
/alliance_create [name] - Create new alliance
/alliance_join [name] - Join alliance
/alliance_leave - Leave alliance
/alliance_info [name] - Alliance info
/alliance_list - List alliances
/alliance_invite [reply] - Invite user to alliance
/alliance_kick [reply] - Kick member from alliance

💡 Earn points by sending messages in the group!
    """
    await update.message.reply_text(help_text)

async def show_points(update, chat_id, user_id):
    """Show user points"""
    try:
        user_data = get_user_data(chat_id, user_id)
        await update.message.reply_text(f"💰 Your points: {user_data['points']}")
        await delete_message_safe(update.message, 10)  # Delete after 10 seconds
    except Exception as e:
        print(f"Error in show_points: {e}")
        await update.message.reply_text("⚠️ Error showing points!")

async def show_military(update, chat_id, user_id):
    """Show user military force"""
    try:
        user_data = get_user_data(chat_id, user_id)
        
        military_text = "🎖 Your Military Force:\n\n"
        
        # Group assets by category for better display
        categories = {
            "Tanks": ["abrams_tank", "leopard_tank", "t90_tank", "challenger_tank"],
            "Aircraft": ["f16_fighter", "f35_stealth", "su27_fighter", "reaper_drone"],
            "Missiles": ["patriot_missile", "tomahawk_missile", "javelin_missile"],
            "Navy": ["destroyer", "submarine", "aircraft_carrier"],
            "Infantry": ["soldier", "special_forces"],
            "Artillery": ["howitzer", "mlrs"],
            "Defense": ["s400_system", "radar"]
        }
        
        for category_name, asset_types in categories.items():
            category_assets = []
            for asset_type in asset_types:
                count = user_data["military"][asset_type]
                if count > 0:
                    asset_name = get_asset_display_name(asset_type)
                    category_assets.append(f"{asset_name}: {count}")
            
            if category_assets:
                military_text += f"**{category_name}:**\n" + "\n".join(category_assets) + "\n\n"
        
        total_power = calculate_total_power(user_data)
        battle_stats = f"💪 Total Power: {total_power}\n🏆 Won: {user_data['battles_won']} | 💀 Lost: {user_data['battles_lost']}"
        
        response = f"{military_text}\n{battle_stats}"
        await update.message.reply_text(response)
        await delete_message_safe(update.message, 15)  # Delete after 15 seconds
    except Exception as e:
        print(f"Error in show_military: {e}")
        await update.message.reply_text("⚠️ Error showing military force!")

async def buy_asset(update, chat_id, user_id):
    """Buy military equipment"""
    try:
        parts = update.message.text.split()
        if len(parts) < 3:
            await update.message.reply_text("⚠️ Invalid buy command format")
            return
        
        asset_type = parts[1].lower()
        try:
            quantity = int(parts[2])
            if quantity <= 0:
                await update.message.reply_text("⚠️ Quantity must be greater than zero!")
                return
        except ValueError:
            await update.message.reply_text("⚠️ Quantity must be a number!")
            return
        
        if asset_type not in MILITARY_ASSETS:
            await update.message.reply_text("⚠️ Invalid equipment type! Use /game_help for valid types.")
            return
        
        user_data = get_user_data(chat_id, user_id)
        asset_cost = get_asset_cost(asset_type)
        total_cost = asset_cost * quantity
        
        if user_data["points"] < total_cost:
            await update.message.reply_text(f"⚠️ Insufficient points! Need: {total_cost} points (Have: {user_data['points']})")
            return
        
        # Buy equipment
        user_data["points"] -= total_cost
        user_data["military"][asset_type] += quantity
        
        save_data()
        
        asset_name = get_asset_display_name(asset_type)
        response = f"✅ {quantity} {asset_name} purchased successfully!\nRemaining points: {user_data['points']}"
        reply_msg = await update.message.reply_text(response)
        
        # Delete messages for privacy
        await delete_message_safe(update.message, 3)  # Delete the command
        await delete_message_safe(reply_msg, 10)  # Delete the response after 10 seconds
        
    except Exception as e:
        print(f"Error in buy_asset: {e}")
        await update.message.reply_text("⚠️ Error buying equipment!")

async def attack_user(update, chat_id, user_id):
    """Attack another user"""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("⚠️ Please reply to the user you want to attack!")
            return
        
        target_user = update.message.reply_to_message.from_user
        if target_user.id == user_id:
            await update.message.reply_text("🤣⚠️ You can't attack yourself!")
            return
        
        attacker_data = get_user_data(chat_id, user_id)
        defender_data = get_user_data(chat_id, target_user.id)
        
        # Check if attacker has military force
        attacker_power = calculate_total_power(attacker_data)
        if attacker_power == 0:
            await update.message.reply_text("⚠️ You have no military force to attack!")
            return
        
        # Check if defender has military force
        defender_power = calculate_total_power(defender_data)
        if defender_power == 0:
            await update.message.reply_text("⚠️ Target user has no military force to defend!")
            return
        
        # Calculate battle result
        attack_strength = attacker_power * random.uniform(0.8, 1.2)
        defense_strength = defender_power * random.uniform(0.8, 1.2)
        
        if attack_strength > defense_strength:
            # Attacker won
            damage_ratio = min(0.3, (attack_strength - defense_strength) / attack_strength * 0.5)
            stolen_points = int(defender_data["points"] * damage_ratio)
            
            # Transfer points
            attacker_data["points"] += stolen_points
            defender_data["points"] = max(0, defender_data["points"] - stolen_points)
            
            # Record stats
            attacker_data["battles_won"] += 1
            defender_data["battles_lost"] += 1
            
            result_text = (f"⚔️ {update.effective_user.first_name} attacked {target_user.first_name} and won!\n"
                          f"💰 Loot: {stolen_points} points")
        else:
            # Defender won
            damage_ratio = min(0.2, (defense_strength - attack_strength) / defense_strength * 0.3)
            lost_points = int(attacker_data["points"] * damage_ratio)
            
            # Penalty for attacker
            attacker_data["points"] = max(0, attacker_data["points"] - lost_points)
            
            # Record stats
            attacker_data["battles_lost"] += 1
            defender_data["battles_won"] += 1
            
            result_text = (f"🛡 {update.effective_user.first_name} attacked {target_user.first_name} but lost!\n"
                          f"💸 Penalty: {lost_points} points")
        
        save_data()
        await update.message.reply_text(result_text)
        
    except Exception as e:
        print(f"Error in attack_user: {e}")
        await update.message.reply_text("⚠️ Error in attack!")

# -------------------- ALLIANCE COMMAND HANDLERS --------------------
async def handle_alliance_command(update, chat_id, user_id):
    """Process alliance commands"""
    parts = update.message.text.split()
    if len(parts) < 2:
        await update.message.reply_text("⚠️ Invalid command format. Use /game_help for guidance.")
        return
    
    subcommand = parts[1].lower()
    
    if subcommand == "create" and len(parts) >= 3:
        await alliance_create(update, chat_id, user_id, " ".join(parts[2:]))
    elif subcommand == "join" and len(parts) >= 3:
        await alliance_join(update, chat_id, user_id, " ".join(parts[2:]))
    elif subcommand == "leave":
        await alliance_leave(update, chat_id, user_id)
    elif subcommand == "info" and len(parts) >= 3:
        await alliance_info(update, chat_id, " ".join(parts[2:]))
    elif subcommand == "list":
        await alliance_list(update, chat_id)
    elif subcommand == "invite":
        await alliance_invite(update, chat_id, user_id)
    elif subcommand == "kick":
        await alliance_kick(update, chat_id, user_id)
    else:
        await update.message.reply_text("⚠️ Invalid alliance command. Use /game_help for guidance.")

async def alliance_create(update, chat_id, user_id, alliance_name):
    """Create a new alliance"""
    try:
        chat_data = get_chat_data(chat_id)
        user_data = get_user_data(chat_id, user_id)
        
        if user_data["alliance"]:
            await update.message.reply_text("⚠️ You are already in an alliance. Leave current one first.")
            return
        
        if alliance_name in chat_data["alliances"]:
            await update.message.reply_text("⚠️ An alliance with this name already exists.")
            return
        
        # Create alliance
        chat_data["alliances"][alliance_name] = {
            "creator": user_id,
            "members": [user_id],
            "created_at": datetime.now().isoformat(),
            "description": "New alliance"
        }
        
        # Add user to alliance
        user_data["alliance"] = alliance_name
        
        save_data()
        await update.message.reply_text(f"✅ Alliance '{alliance_name}' created successfully and you joined it!")
        
    except Exception as e:
        print(f"Error in alliance_create: {e}")
        await update.message.reply_text("⚠️ Error creating alliance!")

async def alliance_join(update, chat_id, user_id, alliance_name):
    """Join an existing alliance"""
    try:
        chat_data = get_chat_data(chat_id)
        user_data = get_user_data(chat_id, user_id)
        
        if user_data["alliance"]:
            await update.message.reply_text("⚠️ You are already in an alliance. Leave current one first.")
            return
        
        if alliance_name not in chat_data["alliances"]:
            await update.message.reply_text("⚠️ No alliance with this name exists.")
            return
        
        # Add user to alliance
        chat_data["alliances"][alliance_name]["members"].append(user_id)
        user_data["alliance"] = alliance_name
        
        save_data()
        await update.message.reply_text(f"✅ You successfully joined alliance '{alliance_name}'!")
        
    except Exception as e:
        print(f"Error in alliance_join: {e}")
        await update.message.reply_text("⚠️ Error joining alliance!")

async def alliance_leave(update, chat_id, user_id):
    """Leave an alliance"""
    try:
        chat_data = get_chat_data(chat_id)
        user_data = get_user_data(chat_id, user_id)
        
        if not user_data["alliance"]:
            await update.message.reply_text("⚠️ You are not in any alliance.")
            return
        
        alliance_name = user_data["alliance"]
        
        if alliance_name not in chat_data["alliances"]:
            user_data["alliance"] = None
            save_data()
            await update.message.reply_text("⚠️ Your alliance doesn't exist. Status updated.")
            return
        
        alliance = chat_data["alliances"][alliance_name]
        
        # Remove user from alliance
        if user_id in alliance["members"]:
            alliance["members"].remove(user_id)
        
        # If alliance is empty, delete it
        if not alliance["members"]:
            del chat_data["alliances"][alliance_name]
        # If creator leaves, assign new creator
        elif alliance["creator"] == user_id:
            alliance["creator"] = alliance["members"][0]
        
        user_data["alliance"] = None
        
        save_data()
        await update.message.reply_text(f"✅ You successfully left alliance '{alliance_name}'!")
        
    except Exception as e:
        print(f"Error in alliance_leave: {e}")
        await update.message.reply_text("⚠️ Error leaving alliance!")

async def alliance_info(update, chat_id, alliance_name):
    """Show information about an alliance"""
    try:
        chat_data = get_chat_data(chat_id)
        
        if alliance_name not in chat_data["alliances"]:
            await update.message.reply_text("⚠️ No alliance with this name exists.")
            return
        
        alliance = chat_data["alliances"][alliance_name]
        creator_id = alliance["creator"]
        
        # Get member count and total power
        member_count = len(alliance["members"])
        total_power = 0
        
        for member_id in alliance["members"]:
            member_data = get_user_data(chat_id, member_id)
            total_power += calculate_total_power(member_data)
        
        created_at = datetime.fromisoformat(alliance["created_at"]).strftime("%Y-%m-%d %H:%M")
        
        info_text = (
            f"🤝 Alliance '{alliance_name}' Info:\n\n"
            f"👑 Creator: User#{creator_id}\n"
            f"👥 Members: {member_count}\n"
            f"💪 Total Power: {total_power}\n"
            f"📅 Created: {created_at}\n"
            f"📝 Description: {alliance.get('description', 'No description')}"
        )
        
        await update.message.reply_text(info_text)
        
    except Exception as e:
        print(f"Error in alliance_info: {e}")
        await update.message.reply_text("⚠️ Error getting alliance info!")

async def alliance_list(update, chat_id):
    """List all alliances in the chat"""
    try:
        chat_data = get_chat_data(chat_id)
        
        if not chat_data["alliances"]:
            await update.message.reply_text("⚠️ No alliances exist in this group.")
            return
        
        alliances_text = "🤝 Group Alliances:\n\n"
        
        for alliance_name, alliance_data in chat_data["alliances"].items():
            member_count = len(alliance_data["members"])
            alliances_text += f"• {alliance_name} ({member_count} members)\n"
        
        await update.message.reply_text(alliances_text)
        
    except Exception as e:
        print(f"Error in alliance_list: {e}")
        await update.message.reply_text("⚠️ Error getting alliance list!")

async def alliance_invite(update, chat_id, user_id):
    """Invite a user to your alliance"""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("⚠️ Please reply to the user you want to invite!")
            return
        
        target_user = update.message.reply_to_message.from_user
        target_user_id = target_user.id
        
        user_data = get_user_data(chat_id, user_id)
        target_user_data = get_user_data(chat_id, target_user_id)
        chat_data = get_chat_data(chat_id)
        
        if not user_data["alliance"]:
            await update.message.reply_text("⚠️ You are not in any alliance.")
            return
        
        if target_user_data["alliance"]:
            await update.message.reply_text("⚠️ This user is already in an alliance.")
            return
        
        alliance_name = user_data["alliance"]
        alliance = chat_data["alliances"][alliance_name]
        
        # Check if user is the creator or has permission
        if user_id != alliance["creator"]:
            await update.message.reply_text("⚠️ Only alliance creator can invite new members.")
            return
        
        await update.message.reply_text(f"✅ Invitation sent to {target_user.first_name} to join {alliance_name}!")
        
    except Exception as e:
        print(f"Error in alliance_invite: {e}")
        await update.message.reply_text("⚠️ Error sending invitation!")

async def alliance_kick(update, chat_id, user_id):
    """Kick a user from your alliance"""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("⚠️ Please reply to the user you want to kick!")
            return
        
        target_user = update.message.reply_to_message.from_user
        target_user_id = target_user.id
        
        user_data = get_user_data(chat_id, user_id)
        target_user_data = get_user_data(chat_id, target_user_id)
        chat_data = get_chat_data(chat_id)
        
        if not user_data["alliance"]:
            await update.message.reply_text("⚠️ You are not in any alliance.")
            return
        
        alliance_name = user_data["alliance"]
        
        if alliance_name != target_user_data["alliance"]:
            await update.message.reply_text("⚠️ This user is not in your alliance.")
            return
        
        alliance = chat_data["alliances"][alliance_name]
        
        # Check if user is the creator or has permission
        if user_id != alliance["creator"]:
            await update.message.reply_text("⚠️ Only alliance creator can kick members.")
            return
        
        # Cannot kick yourself
        if target_user_id == user_id:
            await update.message.reply_text("⚠️ You can't kick yourself.")
            return
        
        # Remove user from alliance
        if target_user_id in alliance["members"]:
            alliance["members"].remove(target_user_id)
        
        target_user_data["alliance"] = None
        
        save_data()
        await update.message.reply_text(f"✅ User {target_user.first_name} kicked from alliance!")
        
    except Exception as e:
        print(f"Error in alliance_kick: {e}")
        await update.message.reply_text("⚠️ Error kicking user!")

# -------------------- ORIGINAL COMMAND HANDLERS --------------------
async def show_rules(update, chat_id):
    """Show group rules"""
    try:
        chat_data = get_chat_data(chat_id)
        await update.message.reply_text(f"📜 Group Rules:\n\n{chat_data['rules']}")
    except Exception as e:
        print(f"Error in show_rules: {e}")
        await update.message.reply_text("⚠️ Error showing rules!")

async def user_info(update):
    """Show user information"""
    try:
        user = update.effective_user
        user_data = get_user_data(update.effective_chat.id, user.id)
        
        alliance_info = ""
        if user_data["alliance"]:
            alliance_info = f"🤝 Alliance: {user_data['alliance']}\n"
        
        await update.message.reply_text(f"👤 User Information:\n\n"
                                      f"Name: {user.first_name}\n"
                                      f"ID: {user.id}\n"
                                      f"Username: @{user.username or 'None'}\n"
                                      f"{alliance_info}"
                                      f"💰 Points: {user_data['points']}\n"
                                      f"💪 Military Power: {calculate_total_power(user_data)}")
    except Exception as e:
        print(f"Error in user_info: {e}")
        await update.message.reply_text("⚠️ Error showing user info!")

async def set_owner(update, chat_id):
    """Set group owner"""
    try:
        if not await is_creator(update.effective_user.id, chat_id):
            await update.message.reply_text("🚫 Only group creator can set owner!")
            return
            
        if not update.message.reply_to_message:
            await update.message.reply_text("⚠️ Please reply to the user you want to set as owner!")
            return
        
        new_owner_id = update.message.reply_to_message.from_user.id
        chat_data = get_chat_data(chat_id)
        chat_data["owner_id"] = new_owner_id
        save_data()
        
        await update.message.reply_text(f"✅ Group owner set successfully!")
        
    except Exception as e:
        print(f"Error in set_owner: {e}")
        await update.message.reply_text("⚠️ Error setting owner!")

async def mute_user(update, chat_id):
    """Mute user"""
    try:
        # Extract parameters from command
        parts = update.message.text.split()
        if len(parts) < 2:
            await update.message.reply_text("⚠️ Command format: /mute [time] [reason]\nExample: /mute 1h spam")
            return
        
        # Parse mute duration
        time_str = parts[1].lower()
        if time_str.endswith("m"):
            duration = int(time_str[:-1]) * 60  # minutes
        elif time_str.endswith("h"):
            duration = int(time_str[:-1]) * 3600  # hours
        elif time_str.endswith("d"):
            duration = int(time_str[:-1]) * 86400  # days
        else:
            duration = int(time_str) * 60  # default minutes
        
        # Get reason
        reason = " ".join(parts[2:]) if len(parts) > 2 else "No reason"
        
        # Check if user is replied to
        if not update.message.reply_to_message:
            await update.message.reply_text("⚠️ Please reply to the user you want to mute!")
            return
        
        target_id = update.message.reply_to_message.from_user.id
        chat_data = get_chat_data(chat_id)
        
        # Mute user until specific time
        mute_until = datetime.now() + timedelta(seconds=duration)
        chat_data["muted_users"][str(target_id)] = mute_until.isoformat()
        save_data()
        
        await update.message.reply_text(f"🔇 User muted for {format_time(duration)}.\nReason: {reason}")
        
    except Exception as e:
        print(f"Error in mute_user: {e}")
        await update.message.reply_text("⚠️ Error executing command!")

async def unmute_user(update, chat_id):
    """Unmute user"""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("⚠️ Please reply to the user you want to unmute!")
            return
        
        target_id = update.message.reply_to_message.from_user.id
        chat_data = get_chat_data(chat_id)
        
        if str(target_id) in chat_data["muted_users"]:
            del chat_data["muted_users"][str(target_id)]
            save_data()
            await update.message.reply_text("✅ User unmuted.")
        else:
            await update.message.reply_text("⚠️ User is not muted!")
    except Exception as e:
        print(f"Error in unmute_user: {e}")
        await update.message.reply_text("⚠️ Error unmuting user!")

async def ban_user(update, chat_id):
    """Ban user from group"""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("⚠️ Please reply to the user you want to ban!")
            return
        
        # Extract reason
        parts = update.message.text.split()
        reason = " ".join(parts[1:]) if len(parts) > 1 else "No reason"
        
        target_user = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(chat_id, target_user.id)
        
        await update.message.reply_text(f"🚫 User banned from group.\nReason: {reason}")
        
    except Exception as e:
        print(f"Error in ban_user: {e}")
        await update.message.reply_text("⚠️ Error banning user!")

async def warn_user(update, chat_id):
    """Warn user"""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("⚠️ Please reply to the user you want to warn!")
            return
        
        # Extract reason
        parts = update.message.text.split()
        reason = " ".join(parts[1:]) if len(parts) > 1 else "No reason"
        
        target_id = update.message.reply_to_message.from_user.id
        chat_data = get_chat_data(chat_id)
        
        # Add warning
        if str(target_id) not in chat_data["warnings"]:
            chat_data["warnings"][str(target_id)] = []
        
        chat_data["warnings"][str(target_id)].append({
            "reason": reason,
            "time": datetime.now().isoformat(),
            "by": update.effective_user.id
        })
        save_data()
        
        warning_count = len(chat_data["warnings"][str(target_id)])
        await update.message.reply_text(f"⚠️ User warned.\nReason: {reason}\nWarning count: {warning_count}")
        
    except Exception as e:
        print(f"Error in warn_user: {e}")
        await update.message.reply_text("⚠️ Error warning user!")

async def set_rules(update, chat_id):
    """Set group rules"""
    try:
        new_rules = update.message.text.replace("/setrules", "").strip()
        if not new_rules:
            await update.message.reply_text("⚠️ Please enter the rules text!")
            return
        
        chat_data = get_chat_data(chat_id)
        chat_data["rules"] = new_rules
        save_data()
        
        await update.message.reply_text("✅ Group rules updated successfully!")
        
    except Exception as e:
        print(f"Error in set_rules: {e}")
        await update.message.reply_text("⚠️ Error saving rules!")

async def set_welcome(update, chat_id):
    """Set welcome message"""
    try:
        new_welcome = update.message.text.replace("/setwelcome", "").strip()
        if not new_welcome:
            await update.message.reply_text("⚠️ Please enter the welcome message text!")
            return
        
        chat_data = get_chat_data(chat_id)
        chat_data["welcome_message"] = new_welcome
        save_data()
        
        await update.message.reply_text("✅ Welcome message updated successfully!")
        
    except Exception as e:
        print(f"Error in set_welcome: {e}")
        await update.message.reply_text("⚠️ Error saving welcome message!")

async def add_admin(update, chat_id):
    """Add new admin"""
    try:
        parts = update.message.text.split()
        if len(parts) < 2:
            await update.message.reply_text("⚠️ Command format: /addadmin [user_id]")
            return
        
        new_admin_id = int(parts[1])
        chat_data = get_chat_data(chat_id)
        
        if new_admin_id not in chat_data["admins"]:
            chat_data["admins"].append(new_admin_id)
            save_data()
            await update.message.reply_text(f"✅ User {new_admin_id} added to admin list!")
        else:
            await update.message.reply_text("⚠️ User is already an admin!")
            
    except ValueError:
        await update.message.reply_text("⚠️ User ID must be a number!")
    except Exception as e:
        print(f"Error in add_admin: {e}")
        await update.message.reply_text("⚠️ Error adding admin!")

async def remove_admin(update, chat_id):
    """Remove admin"""
    try:
        parts = update.message.text.split()
        if len(parts) < 2:
            await update.message.reply_text("⚠️ Command format: /removeadmin [user_id]")
            return
        
        admin_id = int(parts[1])
        chat_data = get_chat_data(chat_id)
        
        if admin_id in chat_data["admins"]:
            chat_data["admins"].remove(admin_id)
            save_data()
            await update.message.reply_text(f"✅ User {admin_id} removed from admin list!")
        else:
            await update.message.reply_text("⚠️ User is not in admin list!")
            
    except ValueError:
        await update.message.reply_text("⚠️ User ID must be a number!")
    except Exception as e:
        print(f"Error in remove_admin: {e}")
        await update.message.reply_text("⚠️ Error removing admin!")

async def show_owner(update, chat_id):
    """Show group owner"""
    try:
        chat_data = get_chat_data(chat_id)
        if chat_data["owner_id"]:
            await update.message.reply_text(f"👑 Group owner: {chat_data['owner_id']}")
        else:
            await update.message.reply_text("⚠️ Group owner not set. Use /setowner to set one.")
    except Exception as e:
        print(f"Error in show_owner: {e}")
        await update.message.reply_text("⚠️ Error showing group owner!")

# -------------------- MAIN FUNCTION --------------------
def main():
    """Main function to run the bot"""
    print("Starting Telegram bot...")
    load_data()
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clean", clean_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()