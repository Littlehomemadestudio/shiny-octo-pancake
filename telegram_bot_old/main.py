"""
Main entry point for Simple World War Telegram Bot
No environment variables required - just update config.json with your bot token
"""
import asyncio
import logging
import json

from simple_bot import SimpleWorldWarBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to start the bot"""
    try:
        # Check if config file exists and has token
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            if config.get('bot', {}).get('token') == 'YOUR_BOT_TOKEN_HERE':
                logger.error("Please update config.json with your actual bot token!")
                logger.error("Replace 'YOUR_BOT_TOKEN_HERE' with your bot token from @BotFather")
                return
                
        except FileNotFoundError:
            logger.error("config.json not found! Please create it with your bot token.")
            return
        
        # Create and start bot
        bot = SimpleWorldWarBot()
        logger.info("Starting Simple World War Bot...")
        await bot.start()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())