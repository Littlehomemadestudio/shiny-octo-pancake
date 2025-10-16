# Migration Notes: Telegram Bot → Bale Bot

## تغییرات انجام شده / Changes Made

### 1. ایجاد ربات بله جدید / Created New Bale Bot
- ✅ `bale_bot.py` - منطق اصلی ربات با API بله
- ✅ `bale_storage.py` - سیستم ذخیره‌سازی با قابلیت همگام‌سازی جهانی
- ✅ `main_bale.py` - نقطه ورود اصلی برای ربات بله
- ✅ `README_BALE.md` - مستندات کامل فارسی/انگلیسی

### 2. فایل‌های قدیمی تلگرام / Old Telegram Files
همه فایل‌های ربات تلگرام به پوشه `telegram_bot_old/` منتقل شدند:
- ✅ main.py
- ✅ simple_bot.py
- ✅ simple_storage.py
- ✅ database.py
- ✅ economy.py
- ✅ military.py
- ✅ و تمام فایل‌های دیگر...

### 3. ویژگی جدید: همگام‌سازی جهانی خریدها / New Feature: Global Purchase Sync

#### چگونه کار می‌کند / How It Works

هنگامی که یک بازیکن در PV (چت خصوصی) ربات خریدی انجام می‌دهد:

1. **ثبت خرید / Purchase Recording**:
   ```python
   purchase_data = {
       'player_id': user_id,
       'player_name': player['first_name'],
       'item': f"🛒 {item_type}",
       'item_type': 'material',
       'quantity': quantity,
       'cost': total_cost,
       'timestamp': datetime.now().isoformat()
   }
   self.storage.add_global_purchase(purchase_data)
   ```

2. **ذخیره‌سازی جهانی / Global Storage**:
   - تمام خریدها در `data/global_purchases.json` ذخیره می‌شوند
   - هر بازیکن می‌تواند تاریخچه را مشاهده کند

3. **دستورات جدید / New Commands**:
   - `/globalpurchases` - نمایش 20 خرید اخیر با جزئیات کامل
   - `/recentbuys` - نمایش 10 خرید اخیر (خلاصه)

#### مثال خروجی / Example Output

```
🌍 تاریخچه خریدهای جهانی

1. علی خرید کرد:
   🛒 iron × 10 (💰 100 طلا)
   🕐 2025-10-16 12:30

2. مریم خرید کرد:
   ⚔️ tank × 1 (💰 500 طلا)
   🕐 2025-10-16 12:28

3. حسین خرید کرد:
   🛒 oil × 10 (💰 150 طلا)
   🕐 2025-10-16 12:25
```

### 4. تغییرات API / API Changes

#### تلگرام (قدیمی) / Telegram (Old)
```python
from aiogram import Bot, Dispatcher, types
bot = Bot(token=token)
dp = Dispatcher(storage=MemoryStorage())
```

#### بله (جدید) / Bale (New)
```python
from bale import Bot, Message, CallbackQuery
bot = Bot(token=token)
bot.add_handler(CommandHandler("start", start_command))
```

### 5. تغییرات زبان / Language Changes

- تمام متن‌های رابط کاربری به **فارسی** تبدیل شدند
- دستورات همچنان به انگلیسی هستند (مثل `/start`, `/buy`)
- پیام‌ها و منوها فارسی شدند

### 6. فایل‌های پیکربندی / Configuration Files

#### requirements.txt
```txt
# نسخه قدیمی (تلگرام)
aiogram==3.2.0
sqlalchemy==2.0.23
...

# نسخه جدید (بله)
python-bale-bot>=1.0.0
asyncio>=3.4.3
aiofiles>=23.2.1
```

#### config.json
همان فایل config.json برای هر دو نسخه استفاده می‌شود، فقط توکن باید تغییر کند:
```json
{
  "bot": {
    "token": "YOUR_BALE_BOT_TOKEN_HERE"
  }
}
```

## نحوه استفاده / How to Use

### اجرای ربات بله / Run Bale Bot
```bash
python main_bale.py
```

### اجرای ربات تلگرام (قدیمی) / Run Telegram Bot (Old)
```bash
cd telegram_bot_old
python main.py
```

## تست‌ها / Tests

برای تست ویژگی همگام‌سازی جهانی:

1. دو یا سه کاربر ربات را استارت کنند (`/start`)
2. یک کاربر چیزی بخرد (`/buy`)
3. کاربر دیگر `/globalpurchases` را اجرا کند
4. باید خرید کاربر اول را ببیند!

## ساختار داده / Data Structure

### global_purchases.json
```json
[
  {
    "player_id": 123456789,
    "player_name": "علی",
    "item": "🛒 iron",
    "item_type": "material",
    "quantity": 10,
    "cost": 100,
    "timestamp": "2025-10-16T12:30:45.123456"
  }
]
```

## نکات مهم / Important Notes

1. **فایل‌های داده / Data Files**: 
   - ربات بله از همان سیستم ذخیره‌سازی فایل استفاده می‌کند
   - داده‌های تلگرام و بله **جدا** هستند (مگر اینکه ID کاربران یکسان باشد)

2. **کدهای قدیمی / Old Code**:
   - تمام کدهای تلگرام در `telegram_bot_old/` محفوظ هستند
   - می‌توانید در هر زمان به آن‌ها مراجعه کنید

3. **ویژگی‌های نگه داشته شده / Preserved Features**:
   - ✅ سیستم اقتصادی کامل
   - ✅ سیستم نظامی
   - ✅ سیستم مأموریت
   - ✅ مدیریت منابع
   - ✅ صفحه کلیدهای شیشه‌ای

4. **ویژگی‌های جدید / New Features**:
   - ✅ همگام‌سازی جهانی خریدها
   - ✅ رابط کاربری فارسی
   - ✅ بهینه‌سازی برای بله

## مشکلات احتمالی / Potential Issues

### اگر ربات کار نکرد / If Bot Doesn't Work

1. **بررسی توکن / Check Token**:
   ```bash
   # در config.json
   "token": "YOUR_ACTUAL_BALE_TOKEN"
   ```

2. **نصب کتابخانه / Install Library**:
   ```bash
   pip install python-bale-bot
   ```

3. **بررسی لاگ‌ها / Check Logs**:
   ```bash
   cat bale_bot.log
   ```

### اگر کتابخانه python-bale-bot وجود نداشت / If python-bale-bot Doesn't Exist

باید از API مستقیم بله استفاده کنید:
```python
import requests

def send_message(chat_id, text):
    url = f"https://tapi.bale.ai/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    return requests.post(url, json=data)
```

## خلاصه / Summary

- ✅ ربات تلگرام به بله تبدیل شد
- ✅ تمام قابلیت‌ها حفظ شدند
- ✅ ویژگی جدید همگام‌سازی جهانی اضافه شد
- ✅ فایل‌های قدیمی در `telegram_bot_old/` نگهداری شدند
- ✅ مستندات کامل ایجاد شد

## نسخه / Version

- **Telegram Bot Version**: v1.0 (archived in telegram_bot_old/)
- **Bale Bot Version**: v2.0 (current)
- **Migration Date**: 2025-10-16
