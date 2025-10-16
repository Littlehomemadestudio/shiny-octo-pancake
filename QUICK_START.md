# راهنمای شروع سریع / Quick Start Guide

## برای شروع در 3 مرحله / Start in 3 Steps

### 1️⃣ نصب وابستگی‌ها / Install Dependencies

```bash
pip install python-bale-bot aiofiles asyncio
```

یا:

```bash
pip install -r requirements.txt
```

### 2️⃣ تنظیم توکن / Configure Token

فایل `config.json` را ویرایش کنید:

```json
{
  "bot": {
    "token": "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz",
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

### 3️⃣ اجرای ربات / Run the Bot

```bash
python main_bale.py
```

## تست ویژگی جدید / Test New Feature

### همگام‌سازی جهانی خریدها / Global Purchase Sync

1. **شروع بازی / Start Game**:
   ```
   /start
   ```

2. **خرید چیزی / Buy Something**:
   ```
   /buy
   ```
   سپس روی یکی از دکمه‌ها کلیک کنید (مثلاً "خرید آهن")

3. **مشاهده خریدهای جهانی / View Global Purchases**:
   ```
   /globalpurchases
   ```
   یا
   ```
   /recentbuys
   ```

4. **با کاربر دیگر تست کنید / Test with Another User**:
   - کاربر دوم هم `/start` کند
   - کاربر دوم `/globalpurchases` کند
   - باید خرید کاربر اول را ببیند! 🎉

## دستورات مفید / Useful Commands

```
/start          - شروع بازی
/help           - راهنما
/status         - وضعیت من
/profile        - پروفایل کامل

/economy        - اقتصاد
/buy            - خرید سریع (با همگام‌سازی جهانی!)
/trade          - تجارت
/materials      - مشاهده منابع

/military       - نمای نظامی
/attack         - حمله
/build          - ساخت واحد

/quest          - مأموریت‌ها
/missions       - مأموریت‌های فعال

/globalpurchases - تاریخچه خریدهای جهانی (ویژگی جدید!)
/recentbuys      - آخرین خریدها (ویژگی جدید!)
```

## مشکلات رایج / Common Issues

### خطا: ModuleNotFoundError: No module named 'bale'

```bash
pip install python-bale-bot
```

### خطا: توکن نامعتبر / Invalid Token

- مطمئن شوید توکن را از @BotFather دریافت کرده‌اید
- توکن را در `config.json` قرار دهید
- فرمت توکن: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### ربات پاسخ نمی‌دهد / Bot Not Responding

1. بررسی کنید ربات در حال اجرا باشد:
   ```bash
   ps aux | grep python
   ```

2. لاگ‌ها را بررسی کنید:
   ```bash
   tail -f bale_bot.log
   ```

3. دیباگ را فعال کنید:
   ```json
   {
     "bot": {
       "debug": true
     }
   }
   ```

## ساختار پروژه / Project Structure

```
📁 Project Root
├── 📄 main_bale.py           # ← شروع از اینجا / Start here
├── 📄 bale_bot.py            # منطق ربات / Bot logic
├── 📄 bale_storage.py        # ذخیره‌سازی / Storage
├── 📄 config.json            # ← تنظیمات / Settings
├── 📄 requirements.txt       # وابستگی‌ها / Dependencies
├── 📄 README_BALE.md         # مستندات کامل / Full docs
├── 📄 MIGRATION_NOTES.md     # یادداشت‌های مهاجرت / Migration notes
├── 📄 QUICK_START.md         # این فایل / This file
├── 📁 data/                  # داده‌های بازی / Game data
│   ├── player_*.json
│   ├── materials_*.json
│   ├── units_*.json
│   ├── quests_*.json
│   └── global_purchases.json # ← خریدهای جهانی / Global purchases
└── 📁 telegram_bot_old/      # فایل‌های قدیمی / Old files
    └── ...
```

## نکات مهم / Important Notes

1. **ویژگی جدید**: همگام‌سازی جهانی خریدها - هر خریدی که در PV ربات انجام دهید برای همه قابل مشاهده است!

2. **زبان**: رابط کاربری فارسی است، اما دستورات انگلیسی

3. **داده‌ها**: در پوشه `data/` ذخیره می‌شوند (فایل‌های JSON)

4. **فایل‌های قدیمی**: تمام فایل‌های ربات تلگرام در `telegram_bot_old/` هستند

## کمک بیشتر / More Help

- 📖 مستندات کامل: `README_BALE.md`
- 📝 یادداشت‌های مهاجرت: `MIGRATION_NOTES.md`
- 🔍 کد منبع: `bale_bot.py`, `bale_storage.py`

## موفق باشید! / Good Luck!

ربات شما آماده است! از ویژگی جدید **همگام‌سازی جهانی خریدها** لذت ببرید! 🎮🌍

---

ساخته شده با ❤️ برای جامعه بله ایران
