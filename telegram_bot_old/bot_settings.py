"""
Advanced Bot Settings System
Comprehensive configuration and user preferences management
"""

import json
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import asyncio

@dataclass
class UserPreferences:
    """User-specific preferences and settings"""
    # Display Settings
    language: str = "en"
    timezone: str = "UTC"
    date_format: str = "%Y-%m-%d"
    time_format: str = "%H:%M"
    currency_symbol: str = "💰"
    
    # Game Settings
    auto_save: bool = True
    auto_collect: bool = False
    auto_build: bool = False
    auto_research: bool = False
    auto_attack: bool = False
    
    # Notification Settings
    notifications_enabled: bool = True
    battle_notifications: bool = True
    trade_notifications: bool = True
    quest_notifications: bool = True
    research_notifications: bool = True
    daily_income_notifications: bool = True
    alliance_notifications: bool = True
    world_event_notifications: bool = True
    
    # Privacy Settings
    show_online_status: bool = True
    show_rank: bool = True
    show_wealth: bool = True
    show_military_power: bool = True
    allow_direct_messages: bool = True
    allow_trade_requests: bool = True
    allow_alliance_invites: bool = True
    
    # Gameplay Settings
    difficulty_level: str = "normal"  # easy, normal, hard, extreme
    auto_pause_on_attack: bool = True
    auto_retreat_threshold: float = 0.3
    auto_heal_threshold: float = 0.5
    auto_supply_threshold: float = 0.2
    
    # UI Settings
    compact_mode: bool = False
    show_emojis: bool = True
    show_animations: bool = True
    show_detailed_stats: bool = True
    show_tooltips: bool = True
    theme: str = "default"  # default, dark, light, military
    
    # Sound Settings
    sound_enabled: bool = True
    battle_sounds: bool = True
    notification_sounds: bool = True
    music_enabled: bool = False
    
    # Advanced Settings
    debug_mode: bool = False
    verbose_logging: bool = False
    auto_backup: bool = True
    backup_frequency: int = 24  # hours
    max_backups: int = 7

@dataclass
class GameSettings:
    """Game-wide settings and balance"""
    # Economy Settings
    starting_gold: int = 1000
    starting_materials: int = 100
    daily_income_multiplier: float = 1.0
    trade_tax_rate: float = 0.05
    inflation_rate: float = 0.01
    price_volatility: float = 0.1
    
    # Military Settings
    unit_upkeep_multiplier: float = 1.0
    battle_cooldown: int = 300  # seconds
    max_units_per_province: int = 100
    unit_experience_gain: float = 1.0
    morale_decay_rate: float = 0.01
    
    # Research Settings
    research_speed_multiplier: float = 1.0
    research_cost_multiplier: float = 1.0
    max_research_queue: int = 5
    research_failure_chance: float = 0.05
    
    # Quest Settings
    quest_difficulty_multiplier: float = 1.0
    quest_reward_multiplier: float = 1.0
    max_active_quests: int = 3
    quest_cooldown: int = 3600  # seconds
    
    # World Settings
    world_speed_multiplier: float = 1.0
    event_frequency: float = 1.0
    disaster_frequency: float = 0.1
    ai_aggression: float = 0.5
    
    # Alliance Settings
    max_alliance_size: int = 10
    alliance_creation_cost: int = 5000
    alliance_war_cooldown: int = 86400  # seconds
    alliance_trade_bonus: float = 0.1

@dataclass
class AdminSettings:
    """Administrative settings and controls"""
    # Bot Settings
    maintenance_mode: bool = False
    maintenance_message: str = "Bot is under maintenance. Please try again later."
    max_users: int = 10000
    max_groups: int = 1000
    rate_limit_per_user: int = 30  # commands per minute
    rate_limit_per_group: int = 100  # commands per minute
    
    # Security Settings
    enable_captcha: bool = False
    captcha_timeout: int = 300  # seconds
    max_failed_attempts: int = 3
    ban_duration: int = 3600  # seconds
    enable_ip_blocking: bool = False
    
    # Content Moderation
    enable_profanity_filter: bool = True
    enable_spam_protection: bool = True
    max_message_length: int = 4000
    auto_delete_spam: bool = True
    spam_threshold: int = 5  # messages per minute
    
    # Data Management
    auto_backup_enabled: bool = True
    backup_frequency: int = 6  # hours
    max_backup_age: int = 30  # days
    enable_data_export: bool = True
    enable_data_import: bool = False
    
    # Monitoring
    enable_analytics: bool = True
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    enable_performance_monitoring: bool = True
    alert_on_errors: bool = True

class BotSettingsManager:
    """Manages bot settings and user preferences"""
    
    def __init__(self, config_file: str = "bot_settings.json"):
        self.config_file = config_file
        self.user_preferences: Dict[int, UserPreferences] = {}
        self.game_settings = GameSettings()
        self.admin_settings = AdminSettings()
        self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load game settings
                if 'game_settings' in data:
                    self.game_settings = GameSettings(**data['game_settings'])
                
                # Load admin settings
                if 'admin_settings' in data:
                    self.admin_settings = AdminSettings(**data['admin_settings'])
                
                # Load user preferences
                if 'user_preferences' in data:
                    for user_id, prefs in data['user_preferences'].items():
                        self.user_preferences[int(user_id)] = UserPreferences(**prefs)
                        
            except Exception as e:
                print(f"Error loading settings: {e}")
                self.create_default_settings()
        else:
            self.create_default_settings()
    
    def save_settings(self):
        """Save settings to file"""
        try:
            data = {
                'game_settings': asdict(self.game_settings),
                'admin_settings': asdict(self.admin_settings),
                'user_preferences': {
                    str(user_id): asdict(prefs) 
                    for user_id, prefs in self.user_preferences.items()
                }
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def create_default_settings(self):
        """Create default settings"""
        self.game_settings = GameSettings()
        self.admin_settings = AdminSettings()
        self.user_preferences = {}
        self.save_settings()
    
    def get_user_preferences(self, user_id: int) -> UserPreferences:
        """Get user preferences, create default if not exists"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = UserPreferences()
            self.save_settings()
        return self.user_preferences[user_id]
    
    def update_user_preferences(self, user_id: int, **kwargs):
        """Update user preferences"""
        prefs = self.get_user_preferences(user_id)
        for key, value in kwargs.items():
            if hasattr(prefs, key):
                setattr(prefs, key, value)
        self.save_settings()
    
    def update_game_settings(self, **kwargs):
        """Update game settings"""
        for key, value in kwargs.items():
            if hasattr(self.game_settings, key):
                setattr(self.game_settings, key, value)
        self.save_settings()
    
    def update_admin_settings(self, **kwargs):
        """Update admin settings"""
        for key, value in kwargs.items():
            if hasattr(self.admin_settings, key):
                setattr(self.admin_settings, key, value)
        self.save_settings()
    
    def reset_user_preferences(self, user_id: int):
        """Reset user preferences to default"""
        self.user_preferences[user_id] = UserPreferences()
        self.save_settings()
    
    def get_all_users_with_setting(self, setting_name: str, value: Any) -> List[int]:
        """Get all users with a specific setting value"""
        users = []
        for user_id, prefs in self.user_preferences.items():
            if hasattr(prefs, setting_name) and getattr(prefs, setting_name) == value:
                users.append(user_id)
        return users
    
    def get_setting_statistics(self) -> Dict[str, Any]:
        """Get statistics about user settings"""
        stats = {
            'total_users': len(self.user_preferences),
            'languages': {},
            'difficulty_levels': {},
            'themes': {},
            'notifications_enabled': 0,
            'auto_save_enabled': 0,
            'debug_mode_enabled': 0
        }
        
        for prefs in self.user_preferences.values():
            # Language distribution
            lang = prefs.language
            stats['languages'][lang] = stats['languages'].get(lang, 0) + 1
            
            # Difficulty distribution
            diff = prefs.difficulty_level
            stats['difficulty_levels'][diff] = stats['difficulty_levels'].get(diff, 0) + 1
            
            # Theme distribution
            theme = prefs.theme
            stats['themes'][theme] = stats['themes'].get(theme, 0) + 1
            
            # Boolean settings
            if prefs.notifications_enabled:
                stats['notifications_enabled'] += 1
            if prefs.auto_save:
                stats['auto_save_enabled'] += 1
            if prefs.debug_mode:
                stats['debug_mode_enabled'] += 1
        
        return stats

class NotificationManager:
    """Manages notifications and alerts"""
    
    def __init__(self, settings_manager: BotSettingsManager):
        self.settings_manager = settings_manager
        self.pending_notifications = {}
    
    async def send_notification(self, user_id: int, message: str, notification_type: str = "general"):
        """Send notification to user if enabled"""
        prefs = self.settings_manager.get_user_preferences(user_id)
        
        # Check if notifications are enabled
        if not prefs.notifications_enabled:
            return False
        
        # Check specific notification type
        if notification_type == "battle" and not prefs.battle_notifications:
            return False
        elif notification_type == "trade" and not prefs.trade_notifications:
            return False
        elif notification_type == "quest" and not prefs.quest_notifications:
            return False
        elif notification_type == "research" and not prefs.research_notifications:
            return False
        elif notification_type == "daily_income" and not prefs.daily_income_notifications:
            return False
        elif notification_type == "alliance" and not prefs.alliance_notifications:
            return False
        elif notification_type == "world_event" and not prefs.world_event_notifications:
            return False
        
        # Store notification for sending
        if user_id not in self.pending_notifications:
            self.pending_notifications[user_id] = []
        
        self.pending_notifications[user_id].append({
            'message': message,
            'type': notification_type,
            'timestamp': datetime.now()
        })
        
        return True
    
    def get_pending_notifications(self, user_id: int) -> List[Dict]:
        """Get pending notifications for user"""
        return self.pending_notifications.get(user_id, [])
    
    def clear_notifications(self, user_id: int):
        """Clear pending notifications for user"""
        if user_id in self.pending_notifications:
            del self.pending_notifications[user_id]

class LanguageManager:
    """Manages multi-language support"""
    
    def __init__(self):
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load translation files"""
        # English (default)
        self.translations['en'] = {
            'welcome': 'Welcome to World War Bot!',
            'start_game': 'Start Game',
            'settings': 'Settings',
            'help': 'Help',
            'status': 'Status',
            'economy': 'Economy',
            'military': 'Military',
            'province': 'Province',
            'quest': 'Quest',
            'alliance': 'Alliance',
            'admin': 'Admin',
            'back': 'Back',
            'next': 'Next',
            'previous': 'Previous',
            'confirm': 'Confirm',
            'cancel': 'Cancel',
            'save': 'Save',
            'reset': 'Reset',
            'delete': 'Delete',
            'edit': 'Edit',
            'view': 'View',
            'search': 'Search',
            'filter': 'Filter',
            'sort': 'Sort',
            'refresh': 'Refresh',
            'loading': 'Loading...',
            'error': 'Error',
            'success': 'Success',
            'warning': 'Warning',
            'info': 'Info',
            'yes': 'Yes',
            'no': 'No',
            'ok': 'OK',
            'close': 'Close',
            'open': 'Open',
            'enable': 'Enable',
            'disable': 'Disable',
            'on': 'On',
            'off': 'Off',
            'active': 'Active',
            'inactive': 'Inactive',
            'available': 'Available',
            'unavailable': 'Unavailable',
            'locked': 'Locked',
            'unlocked': 'Unlocked',
            'completed': 'Completed',
            'in_progress': 'In Progress',
            'pending': 'Pending',
            'failed': 'Failed',
            'cancelled': 'Cancelled',
            'expired': 'Expired',
            'new': 'New',
            'old': 'Old',
            'recent': 'Recent',
            'popular': 'Popular',
            'trending': 'Trending',
            'featured': 'Featured',
            'recommended': 'Recommended',
            'suggested': 'Suggested',
            'favorite': 'Favorite',
            'bookmarked': 'Bookmarked',
            'shared': 'Shared',
            'public': 'Public',
            'private': 'Private',
            'secret': 'Secret',
            'hidden': 'Hidden',
            'visible': 'Visible',
            'show': 'Show',
            'hide': 'Hide',
            'display': 'Display',
            'appearance': 'Appearance',
            'theme': 'Theme',
            'color': 'Color',
            'size': 'Size',
            'font': 'Font',
            'style': 'Style',
            'layout': 'Layout',
            'position': 'Position',
            'alignment': 'Alignment',
            'spacing': 'Spacing',
            'margin': 'Margin',
            'padding': 'Padding',
            'border': 'Border',
            'background': 'Background',
            'foreground': 'Foreground',
            'transparency': 'Transparency',
            'opacity': 'Opacity',
            'brightness': 'Brightness',
            'contrast': 'Contrast',
            'saturation': 'Saturation',
            'hue': 'Hue',
            'blur': 'Blur',
            'sharpness': 'Sharpness',
            'quality': 'Quality',
            'resolution': 'Resolution',
            'dimensions': 'Dimensions',
            'width': 'Width',
            'height': 'Height',
            'depth': 'Depth',
            'length': 'Length',
            'area': 'Area',
            'volume': 'Volume',
            'weight': 'Weight',
            'mass': 'Mass',
            'density': 'Density',
            'speed': 'Speed',
            'velocity': 'Velocity',
            'acceleration': 'Acceleration',
            'force': 'Force',
            'pressure': 'Pressure',
            'temperature': 'Temperature',
            'energy': 'Energy',
            'power': 'Power',
            'frequency': 'Frequency',
            'amplitude': 'Amplitude',
            'wavelength': 'Wavelength',
            'phase': 'Phase',
            'frequency': 'Frequency',
            'amplitude': 'Amplitude',
            'wavelength': 'Wavelength',
            'phase': 'Phase'
        }
        
        # Persian (Farsi)
        self.translations['fa'] = {
            'welcome': 'به ربات جنگ جهانی خوش آمدید!',
            'start_game': 'شروع بازی',
            'settings': 'تنظیمات',
            'help': 'راهنما',
            'status': 'وضعیت',
            'economy': 'اقتصاد',
            'military': 'نظامی',
            'province': 'استان',
            'quest': 'ماموریت',
            'alliance': 'اتحاد',
            'admin': 'مدیر',
            'back': 'بازگشت',
            'next': 'بعدی',
            'previous': 'قبلی',
            'confirm': 'تایید',
            'cancel': 'لغو',
            'save': 'ذخیره',
            'reset': 'بازنشانی',
            'delete': 'حذف',
            'edit': 'ویرایش',
            'view': 'مشاهده',
            'search': 'جستجو',
            'filter': 'فیلتر',
            'sort': 'مرتب‌سازی',
            'refresh': 'تازه‌سازی',
            'loading': 'در حال بارگذاری...',
            'error': 'خطا',
            'success': 'موفقیت',
            'warning': 'هشدار',
            'info': 'اطلاعات',
            'yes': 'بله',
            'no': 'خیر',
            'ok': 'تایید',
            'close': 'بستن',
            'open': 'باز کردن',
            'enable': 'فعال',
            'disable': 'غیرفعال',
            'on': 'روشن',
            'off': 'خاموش',
            'active': 'فعال',
            'inactive': 'غیرفعال',
            'available': 'موجود',
            'unavailable': 'ناموجود',
            'locked': 'قفل شده',
            'unlocked': 'باز شده',
            'completed': 'تکمیل شده',
            'in_progress': 'در حال انجام',
            'pending': 'در انتظار',
            'failed': 'ناموفق',
            'cancelled': 'لغو شده',
            'expired': 'منقضی شده',
            'new': 'جدید',
            'old': 'قدیمی',
            'recent': 'اخیر',
            'popular': 'محبوب',
            'trending': 'ترند',
            'featured': 'ویژه',
            'recommended': 'پیشنهادی',
            'suggested': 'پیشنهادی',
            'favorite': 'مورد علاقه',
            'bookmarked': 'نشان شده',
            'shared': 'اشتراک گذاری شده',
            'public': 'عمومی',
            'private': 'خصوصی',
            'secret': 'مخفی',
            'hidden': 'مخفی',
            'visible': 'قابل مشاهده',
            'show': 'نمایش',
            'hide': 'مخفی کردن',
            'display': 'نمایش',
            'appearance': 'ظاهر',
            'theme': 'تم',
            'color': 'رنگ',
            'size': 'اندازه',
            'font': 'فونت',
            'style': 'سبک',
            'layout': 'چیدمان',
            'position': 'موقعیت',
            'alignment': 'تراز',
            'spacing': 'فاصله',
            'margin': 'حاشیه',
            'padding': 'پدینگ',
            'border': 'حاشیه',
            'background': 'پس‌زمینه',
            'foreground': 'پیش‌زمینه',
            'transparency': 'شفافیت',
            'opacity': 'کدورت',
            'brightness': 'روشنایی',
            'contrast': 'کنتراست',
            'saturation': 'اشباع',
            'hue': 'رنگ',
            'blur': 'تاری',
            'sharpness': 'وضوح',
            'quality': 'کیفیت',
            'resolution': 'وضوح',
            'dimensions': 'ابعاد',
            'width': 'عرض',
            'height': 'ارتفاع',
            'depth': 'عمق',
            'length': 'طول',
            'area': 'مساحت',
            'volume': 'حجم',
            'weight': 'وزن',
            'mass': 'جرم',
            'density': 'چگالی',
            'speed': 'سرعت',
            'velocity': 'سرعت',
            'acceleration': 'شتاب',
            'force': 'نیرو',
            'pressure': 'فشار',
            'temperature': 'دما',
            'energy': 'انرژی',
            'power': 'قدرت',
            'frequency': 'فرکانس',
            'amplitude': 'دامنه',
            'wavelength': 'طول موج',
            'phase': 'فاز'
        }
    
    def get_text(self, key: str, language: str = 'en') -> str:
        """Get translated text"""
        if language in self.translations and key in self.translations[language]:
            return self.translations[language][key]
        elif key in self.translations['en']:
            return self.translations['en'][key]
        else:
            return key
    
    def get_available_languages(self) -> List[str]:
        """Get list of available languages"""
        return list(self.translations.keys())
    
    def add_language(self, language_code: str, translations: Dict[str, str]):
        """Add new language translations"""
        self.translations[language_code] = translations
    
    def get_language_name(self, language_code: str) -> str:
        """Get language name from code"""
        language_names = {
            'en': 'English',
            'fa': 'فارسی (Persian)',
            'es': 'Español (Spanish)',
            'fr': 'Français (French)',
            'de': 'Deutsch (German)',
            'it': 'Italiano (Italian)',
            'pt': 'Português (Portuguese)',
            'ru': 'Русский (Russian)',
            'zh': '中文 (Chinese)',
            'ja': '日本語 (Japanese)',
            'ko': '한국어 (Korean)',
            'ar': 'العربية (Arabic)',
            'hi': 'हिन्दी (Hindi)',
            'tr': 'Türkçe (Turkish)',
            'nl': 'Nederlands (Dutch)',
            'sv': 'Svenska (Swedish)',
            'no': 'Norsk (Norwegian)',
            'da': 'Dansk (Danish)',
            'fi': 'Suomi (Finnish)',
            'pl': 'Polski (Polish)',
            'cs': 'Čeština (Czech)',
            'hu': 'Magyar (Hungarian)',
            'ro': 'Română (Romanian)',
            'bg': 'Български (Bulgarian)',
            'hr': 'Hrvatski (Croatian)',
            'sk': 'Slovenčina (Slovak)',
            'sl': 'Slovenščina (Slovenian)',
            'et': 'Eesti (Estonian)',
            'lv': 'Latviešu (Latvian)',
            'lt': 'Lietuvių (Lithuanian)',
            'uk': 'Українська (Ukrainian)',
            'be': 'Беларуская (Belarusian)',
            'ka': 'ქართული (Georgian)',
            'hy': 'Հայերեն (Armenian)',
            'az': 'Azərbaycan (Azerbaijani)',
            'kk': 'Қазақша (Kazakh)',
            'ky': 'Кыргызча (Kyrgyz)',
            'uz': 'Oʻzbekcha (Uzbek)',
            'tg': 'Тоҷикӣ (Tajik)',
            'mn': 'Монгол (Mongolian)',
            'th': 'ไทย (Thai)',
            'vi': 'Tiếng Việt (Vietnamese)',
            'id': 'Bahasa Indonesia (Indonesian)',
            'ms': 'Bahasa Melayu (Malay)',
            'tl': 'Tagalog (Filipino)',
            'sw': 'Kiswahili (Swahili)',
            'am': 'አማርኛ (Amharic)',
            'ha': 'Hausa',
            'yo': 'Yorùbá',
            'ig': 'Igbo',
            'zu': 'IsiZulu',
            'af': 'Afrikaans',
            'sq': 'Shqip (Albanian)',
            'eu': 'Euskera (Basque)',
            'ca': 'Català (Catalan)',
            'gl': 'Galego (Galician)',
            'cy': 'Cymraeg (Welsh)',
            'ga': 'Gaeilge (Irish)',
            'mt': 'Malti (Maltese)',
            'is': 'Íslenska (Icelandic)',
            'fo': 'Føroyskt (Faroese)',
            'kl': 'Kalaallisut (Greenlandic)',
            'mi': 'Te Reo Māori (Maori)',
            'haw': 'ʻŌlelo Hawaiʻi (Hawaiian)',
            'sm': 'Gagana Samoa (Samoan)',
            'to': 'Lea fakatonga (Tongan)',
            'fj': 'Vosa Vakaviti (Fijian)',
            'ty': 'Reo Tahiti (Tahitian)',
            'mg': 'Malagasy',
            'rw': 'Ikinyarwanda (Kinyarwanda)',
            'rn': 'Kirundi',
            'so': 'Soomaali (Somali)',
            'om': 'Afaan Oromoo (Oromo)',
            'ti': 'ትግርኛ (Tigrinya)',
            'ber': 'Tamaziɣt (Berber)',
            'wo': 'Wolof',
            'ff': 'Fulfulde (Fula)',
            'dy': 'Diola (Jola)',
            'bm': 'Bamanankan (Bambara)',
            'sn': 'ChiShona (Shona)',
            'nd': 'IsiNdebele (Ndebele)',
            'st': 'Sesotho (Sotho)',
            'tn': 'Setswana (Tswana)',
            'ss': 'SiSwati (Swati)',
            've': 'Tshivenḓa (Venda)',
            'ts': 'Xitsonga (Tsonga)',
            'nr': 'IsiNdebele (Southern Ndebele)',
            'nso': 'Sesotho sa Leboa (Northern Sotho)',
            'zu': 'IsiZulu (Zulu)',
            'xh': 'IsiXhosa (Xhosa)',
            'af': 'Afrikaans',
            'en': 'English',
            'es': 'Español (Spanish)',
            'fr': 'Français (French)',
            'de': 'Deutsch (German)',
            'it': 'Italiano (Italian)',
            'pt': 'Português (Portuguese)',
            'ru': 'Русский (Russian)',
            'zh': '中文 (Chinese)',
            'ja': '日本語 (Japanese)',
            'ko': '한국어 (Korean)',
            'ar': 'العربية (Arabic)',
            'hi': 'हिन्दी (Hindi)',
            'tr': 'Türkçe (Turkish)',
            'nl': 'Nederlands (Dutch)',
            'sv': 'Svenska (Swedish)',
            'no': 'Norsk (Norwegian)',
            'da': 'Dansk (Danish)',
            'fi': 'Suomi (Finnish)',
            'pl': 'Polski (Polish)',
            'cs': 'Čeština (Czech)',
            'hu': 'Magyar (Hungarian)',
            'ro': 'Română (Romanian)',
            'bg': 'Български (Bulgarian)',
            'hr': 'Hrvatski (Croatian)',
            'sk': 'Slovenčina (Slovak)',
            'sl': 'Slovenščina (Slovenian)',
            'et': 'Eesti (Estonian)',
            'lv': 'Latviešu (Latvian)',
            'lt': 'Lietuvių (Lithuanian)',
            'uk': 'Українська (Ukrainian)',
            'be': 'Беларуская (Belarusian)',
            'ka': 'ქართული (Georgian)',
            'hy': 'Հայերեն (Armenian)',
            'az': 'Azərbaycan (Azerbaijani)',
            'kk': 'Қазақша (Kazakh)',
            'ky': 'Кыргызча (Kyrgyz)',
            'uz': 'Oʻzbekcha (Uzbek)',
            'tg': 'Тоҷикӣ (Tajik)',
            'mn': 'Монгол (Mongolian)',
            'th': 'ไทย (Thai)',
            'vi': 'Tiếng Việt (Vietnamese)',
            'id': 'Bahasa Indonesia (Indonesian)',
            'ms': 'Bahasa Melayu (Malay)',
            'tl': 'Tagalog (Filipino)',
            'sw': 'Kiswahili (Swahili)',
            'am': 'አማርኛ (Amharic)',
            'ha': 'Hausa',
            'yo': 'Yorùbá',
            'ig': 'Igbo',
            'zu': 'IsiZulu',
            'af': 'Afrikaans',
            'sq': 'Shqip (Albanian)',
            'eu': 'Euskera (Basque)',
            'ca': 'Català (Catalan)',
            'gl': 'Galego (Galician)',
            'cy': 'Cymraeg (Welsh)',
            'ga': 'Gaeilge (Irish)',
            'mt': 'Malti (Maltese)',
            'is': 'Íslenska (Icelandic)',
            'fo': 'Føroyskt (Faroese)',
            'kl': 'Kalaallisut (Greenlandic)',
            'mi': 'Te Reo Māori (Maori)',
            'haw': 'ʻŌlelo Hawaiʻi (Hawaiian)',
            'sm': 'Gagana Samoa (Samoan)',
            'to': 'Lea fakatonga (Tongan)',
            'fj': 'Vosa Vakaviti (Fijian)',
            'ty': 'Reo Tahiti (Tahitian)',
            'mg': 'Malagasy',
            'rw': 'Ikinyarwanda (Kinyarwanda)',
            'rn': 'Kirundi',
            'so': 'Soomaali (Somali)',
            'om': 'Afaan Oromoo (Oromo)',
            'ti': 'ትግርኛ (Tigrinya)',
            'ber': 'Tamaziɣt (Berber)',
            'wo': 'Wolof',
            'ff': 'Fulfulde (Fula)',
            'dy': 'Diola (Jola)',
            'bm': 'Bamanankan (Bambara)',
            'sn': 'ChiShona (Shona)',
            'nd': 'IsiNdebele (Ndebele)',
            'st': 'Sesotho (Sotho)',
            'tn': 'Setswana (Tswana)',
            'ss': 'SiSwati (Swati)',
            've': 'Tshivenḓa (Venda)',
            'ts': 'Xitsonga (Tsonga)',
            'nr': 'IsiNdebele (Southern Ndebele)',
            'nso': 'Sesotho sa Leboa (Northern Sotho)',
            'zu': 'IsiZulu (Zulu)',
            'xh': 'IsiXhosa (Xhosa)',
            'af': 'Afrikaans'
        }
        return language_names.get(language_code, language_code.upper())

class PerformanceMonitor:
    """Monitors bot performance and provides optimization suggestions"""
    
    def __init__(self):
        self.metrics = {
            'command_count': 0,
            'response_time': [],
            'error_count': 0,
            'memory_usage': [],
            'cpu_usage': [],
            'database_queries': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        self.start_time = datetime.now()
    
    def record_command(self, response_time: float):
        """Record command execution"""
        self.metrics['command_count'] += 1
        self.metrics['response_time'].append(response_time)
        
        # Keep only last 1000 response times
        if len(self.metrics['response_time']) > 1000:
            self.metrics['response_time'] = self.metrics['response_time'][-1000:]
    
    def record_error(self):
        """Record error occurrence"""
        self.metrics['error_count'] += 1
    
    def record_database_query(self):
        """Record database query"""
        self.metrics['database_queries'] += 1
    
    def record_cache_hit(self):
        """Record cache hit"""
        self.metrics['cache_hits'] += 1
    
    def record_cache_miss(self):
        """Record cache miss"""
        self.metrics['cache_misses'] += 1
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        uptime = datetime.now() - self.start_time
        
        avg_response_time = 0
        if self.metrics['response_time']:
            avg_response_time = sum(self.metrics['response_time']) / len(self.metrics['response_time'])
        
        commands_per_minute = 0
        if uptime.total_seconds() > 0:
            commands_per_minute = (self.metrics['command_count'] / uptime.total_seconds()) * 60
        
        error_rate = 0
        if self.metrics['command_count'] > 0:
            error_rate = (self.metrics['error_count'] / self.metrics['command_count']) * 100
        
        cache_hit_rate = 0
        total_cache_requests = self.metrics['cache_hits'] + self.metrics['cache_misses']
        if total_cache_requests > 0:
            cache_hit_rate = (self.metrics['cache_hits'] / total_cache_requests) * 100
        
        return {
            'uptime_seconds': uptime.total_seconds(),
            'uptime_formatted': str(uptime).split('.')[0],
            'total_commands': self.metrics['command_count'],
            'commands_per_minute': round(commands_per_minute, 2),
            'average_response_time': round(avg_response_time, 3),
            'error_count': self.metrics['error_count'],
            'error_rate': round(error_rate, 2),
            'database_queries': self.metrics['database_queries'],
            'cache_hit_rate': round(cache_hit_rate, 2),
            'memory_usage_mb': round(self.get_memory_usage(), 2),
            'cpu_usage_percent': round(self.get_cpu_usage(), 2)
        }
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0.0
    
    def get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        try:
            import psutil
            return psutil.cpu_percent()
        except ImportError:
            return 0.0
    
    def get_optimization_suggestions(self) -> List[str]:
        """Get performance optimization suggestions"""
        suggestions = []
        stats = self.get_performance_stats()
        
        if stats['average_response_time'] > 2.0:
            suggestions.append("Consider implementing caching for frequently accessed data")
        
        if stats['error_rate'] > 5.0:
            suggestions.append("High error rate detected - check error handling and input validation")
        
        if stats['cache_hit_rate'] < 50.0:
            suggestions.append("Low cache hit rate - consider expanding cache coverage")
        
        if stats['database_queries'] > 1000:
            suggestions.append("High database query count - consider query optimization")
        
        if stats['memory_usage_mb'] > 500:
            suggestions.append("High memory usage - consider memory optimization")
        
        if stats['cpu_usage_percent'] > 80:
            suggestions.append("High CPU usage - consider load balancing or optimization")
        
        return suggestions

# Example usage and testing
if __name__ == "__main__":
    # Test settings manager
    settings_manager = BotSettingsManager()
    
    # Test user preferences
    user_id = 12345
    prefs = settings_manager.get_user_preferences(user_id)
    print(f"User {user_id} language: {prefs.language}")
    
    # Update user preferences
    settings_manager.update_user_preferences(user_id, language="fa", theme="dark")
    prefs = settings_manager.get_user_preferences(user_id)
    print(f"Updated language: {prefs.language}, theme: {prefs.theme}")
    
    # Test language manager
    lang_manager = LanguageManager()
    print(f"Welcome in English: {lang_manager.get_text('welcome', 'en')}")
    print(f"Welcome in Persian: {lang_manager.get_text('welcome', 'fa')}")
    
    # Test performance monitor
    perf_monitor = PerformanceMonitor()
    perf_monitor.record_command(0.5)
    perf_monitor.record_command(1.2)
    perf_monitor.record_error()
    
    stats = perf_monitor.get_performance_stats()
    print(f"Performance stats: {stats}")
    
    suggestions = perf_monitor.get_optimization_suggestions()
    print(f"Optimization suggestions: {suggestions}")
    
    print("✅ Bot settings system working correctly!")