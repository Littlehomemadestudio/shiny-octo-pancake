"""
Main entry point for World War Telegram Bot
"""
import asyncio
import logging
import os
from dotenv import load_dotenv
from bot import WorldWarBot

# Load environment variables
load_dotenv()

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
        # Check for required environment variables
        bot_token = os.getenv('BOT_TOKEN')
        if not bot_token:
            logger.error("BOT_TOKEN not found in environment variables")
            return
        
        # Create and start bot
        bot = WorldWarBot()
        logger.info("Starting World War Bot...")
        await bot.start()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())