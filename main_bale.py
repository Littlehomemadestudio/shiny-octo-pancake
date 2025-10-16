"""
Main entry point for Bale World War Bot
No environment variables required - just update config.json with your Bale bot token
"""
import asyncio
import logging
import json

from bale_bot import BaleWorldWarBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bale_bot.log'),
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
                logger.error("لطفاً config.json را با توکن واقعی ربات بله خود به‌روزرسانی کنید!")
                logger.error("'YOUR_BOT_TOKEN_HERE' را با توکن ربات خود از @BotFather جایگزین کنید")
                return
                
        except FileNotFoundError:
            logger.error("فایل config.json پیدا نشد! لطفاً آن را با توکن ربات خود ایجاد کنید.")
            return
        
        # Create and start bot
        bot = BaleWorldWarBot()
        logger.info("در حال راه‌اندازی ربات بله جنگ جهانی...")
        await bot.start()
        
    except KeyboardInterrupt:
        logger.info("ربات توسط کاربر متوقف شد")
    except Exception as e:
        logger.error(f"خطا در راه‌اندازی ربات: {e}")
    finally:
        logger.info("خاموش‌سازی ربات کامل شد")

if __name__ == "__main__":
    asyncio.run(main())
