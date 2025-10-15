# Simple World War Strategy Bot

A simplified Telegram bot for a World War strategy game that requires no environment variables, no admin setup, and uses simple text file storage instead of a database.

## Features

- 🎖️ **No Environment Variables**: Just update config.json with your bot token
- 🚫 **No Admin Requirements**: All users can play immediately
- 📁 **Simple Storage**: Uses text files instead of complex databases
- 🎮 **Core Game Features**: Economy, military, quests, and more
- 📱 **Easy Setup**: Just run and play!

## Quick Start

1. **Get a Bot Token**:
   - Message @BotFather on Telegram
   - Create a new bot with `/newbot`
   - Copy your bot token

2. **Update Configuration**:
   - Open `config.json`
   - Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token

3. **Install Dependencies**:
   ```bash
   pip install -r requirements_simple.txt
   ```

4. **Run the Bot**:
   ```bash
   python main.py
   ```

## Configuration

The bot uses a simple `config.json` file for configuration:

```json
{
  "bot": {
    "token": "YOUR_BOT_TOKEN_HERE",
    "debug": false
  },
  "game": {
    "world_name": "Terra Nova",
    "daily_income_base": 1000,
    "battle_cooldown": 300,
    "trade_cooldown": 60
  },
  "economy": {
    "materials": {
      "iron": {"base_price": 10},
      "oil": {"base_price": 15},
      "food": {"base_price": 5},
      "gold": {"base_price": 50},
      "uranium": {"base_price": 100},
      "steel": {"base_price": 25}
    }
  },
  "military": {
    "unit_types": {
      "infantry": {"cost": 100, "upkeep": 10, "attack": 5, "defense": 3},
      "tank": {"cost": 500, "upkeep": 50, "attack": 15, "defense": 10},
      "artillery": {"cost": 300, "upkeep": 30, "attack": 20, "defense": 2},
      "aircraft": {"cost": 800, "upkeep": 80, "attack": 25, "defense": 5},
      "ship": {"cost": 1000, "upkeep": 100, "attack": 30, "defense": 15}
    }
  }
}
```

## Game Commands

- `/start` - Start playing or view status
- `/status` - View your nation's current status
- `/profile` - Detailed player profile
- `/economy` - Economic overview and trading
- `/military` - Military management
- `/quest` - Available quests and missions
- `/help` - Show all available commands

## Data Storage

Player data is stored in simple JSON files in the `data/` directory:
- `player_[user_id].json` - Player profile and stats
- `materials_[user_id].json` - Player resources
- `units_[user_id].json` - Player military units
- `quests_[user_id].json` - Player quests and missions

## File Structure

```
├── main.py                 # Main entry point
├── simple_bot.py          # Simplified bot implementation
├── simple_storage.py      # Text file storage system
├── config.json            # Bot configuration
├── requirements_simple.txt # Dependencies
├── data/                  # Player data storage
└── quran_files/          # Quran-related applications
```

## No Security Required

This simplified version is designed for casual gaming and doesn't include:
- Admin restrictions
- User authentication
- Complex security measures
- Database requirements

Perfect for personal use, testing, or small group games!

## Troubleshooting

**Bot not responding?**
- Check that your bot token is correct in `config.json`
- Make sure the bot is running (check console output)
- Verify the bot is not blocked by Telegram

**Data not saving?**
- Check that the `data/` directory exists and is writable
- Look for error messages in the console

**Commands not working?**
- Make sure you've started the bot with `/start` first
- Check the console for error messages

## Support

This is a simplified version for easy setup and use. For advanced features, refer to the original complex bot implementation.