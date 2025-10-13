# World War Strategy Telegram Bot

A comprehensive multiplayer strategy game bot for Telegram that simulates a complex world war scenario with economy, military, politics, and diplomacy systems.

## 🎮 Features

### Core Systems
- **Economy System**: Dynamic material trading, fluctuating prices, player-to-player trades
- **Military System**: Unit management, combat mechanics, territory control
- **Province Management**: Resource production, building construction, governance
- **Quest System**: Procedurally generated missions with rewards
- **Technology Tree**: Research system with tiered unlocks
- **Politics & Diplomacy**: Alliances, treaties, espionage
- **World Simulation**: Dynamic events, weather, AI factions

### Game Mechanics
- **Player Progression**: Leveling system with ranks (Commander → Supreme Leader)
- **Resource Management**: Iron, oil, food, gold, uranium, steel
- **Combat System**: Terrain, weather, and morale effects
- **Diplomatic Relations**: Alliances, trade agreements, wars
- **World Events**: Economic booms, natural disasters, political changes

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Telegram Bot Token

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd world-war-telegram-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Configure database**
   - Create a PostgreSQL database
   - Update `DATABASE_URL` in `.env`
   - Update `config.json` with your database URL

5. **Set up bot token**
   - Get a bot token from @BotFather
   - Add it to `.env` as `BOT_TOKEN`

6. **Run the bot**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### Environment Variables (.env)
```env
BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=postgresql://user:password@localhost/worldwar_bot
ADMIN_IDS=123456789,987654321
DEBUG=false
```

### Game Configuration (config.json)
- **Bot Settings**: Token, admin IDs, debug mode
- **Database**: Connection URL and settings
- **Game Balance**: Income rates, cooldowns, difficulty
- **Economy**: Material prices and volatility
- **Military**: Unit stats and costs
- **World**: Province count, AI factions, event frequency

## 🎯 Commands

### Basic Commands
- `/start` - Start playing or view status
- `/help` - Show all available commands
- `/status` - View your nation's current status
- `/profile` - Detailed player profile

### Economy Commands
- `/economy` - Economic overview and trading
- `/trade` - Open trading interface
- `/materials` - View your resources

### Military Commands
- `/military` - Military management
- `/attack` - Attack other players or provinces
- `/build` - Build military units

### World Commands
- `/map` - View world map
- `/province` - Manage your provinces
- `/quest` - Available quests and missions
- `/research` - Research new technologies
- `/alliance` - Alliance management

### Admin Commands
- `/admin` - Admin panel (admin only)

## 🏗️ Architecture

### Core Components
- **bot.py**: Main bot class with command handlers
- **database.py**: SQLAlchemy models and database management
- **economy.py**: Economy system with trading and price fluctuations
- **military.py**: Military units, combat, and battle simulation
- **province_manager.py**: Province management and resource production
- **quest_system.py**: Quest generation and mission management
- **technology.py**: Research tree and technology unlocks
- **world_simulation.py**: World events and AI faction simulation
- **admin.py**: Administrative functions and game management
- **ui_menus.py**: Interactive inline keyboards and UI elements

### Database Schema
- **Players**: User accounts, stats, resources
- **Nations**: Player nations with government types
- **Provinces**: World map with resources and buildings
- **Units**: Military units with stats and locations
- **Quests**: Available and active missions
- **Technologies**: Research tree and unlocks
- **Alliances**: Diplomatic relationships
- **Trades**: Player-to-player trading
- **Battles**: Combat records and history
- **World Events**: Dynamic global events

## 🎮 Gameplay

### Getting Started
1. Use `/start` to create your character
2. Build your first military units with `/build`
3. Claim provinces with `/province`
4. Start trading resources with `/trade`
5. Take on quests with `/quest`
6. Research technologies with `/research`

### Strategy Tips
- **Economy**: Trade materials when prices are high
- **Military**: Balance unit types for effective combat
- **Diplomacy**: Form alliances to protect your interests
- **Research**: Focus on technologies that match your strategy
- **Quests**: Complete missions for experience and rewards

## 🔧 Development

### Adding New Features
1. Create new modules in the project root
2. Import and integrate with the main bot class
3. Add command handlers in `bot.py`
4. Create UI elements in `ui_menus.py`
5. Update database models if needed

### Database Migrations
- Modify models in `database.py`
- Run the bot to auto-create tables
- For complex changes, create migration scripts

### Testing
- Use the debug mode in `config.json`
- Test with a small group first
- Monitor logs for errors

## 📊 Monitoring

### Logs
- Bot logs are written to `bot.log`
- Database queries are logged in debug mode
- Error handling with detailed stack traces

### Admin Tools
- `/admin` command for game statistics
- Player management and moderation
- World event creation and management
- Data backup and restore functionality

## 🚨 Troubleshooting

### Common Issues
1. **Bot not responding**: Check bot token and network connection
2. **Database errors**: Verify PostgreSQL connection and permissions
3. **Import errors**: Ensure all dependencies are installed
4. **Memory issues**: Monitor database size and optimize queries

### Support
- Check logs for error messages
- Verify configuration files
- Test with minimal setup first
- Contact developers for complex issues

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

---

**Happy Gaming! 🎖️**