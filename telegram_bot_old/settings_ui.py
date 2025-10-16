"""
Advanced Settings UI System
Comprehensive user interface for bot settings and preferences
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_settings import BotSettingsManager, UserPreferences, GameSettings, AdminSettings
from typing import Dict, List, Any

class SettingsUIManager:
    """Manages settings UI and user interactions"""
    
    def __init__(self, settings_manager: BotSettingsManager):
        self.settings_manager = settings_manager
        self.emoji_map = {
            'settings': '⚙️',
            'user': '👤',
            'game': '🎮',
            'admin': '👑',
            'notification': '🔔',
            'privacy': '🔒',
            'display': '🎨',
            'sound': '🔊',
            'language': '🌐',
            'theme': '🎭',
            'back': '⬅️',
            'next': '➡️',
            'save': '💾',
            'reset': '🔄',
            'delete': '🗑️',
            'edit': '✏️',
            'view': '👁️',
            'search': '🔍',
            'filter': '🔽',
            'sort': '🔀',
            'refresh': '🔄',
            'loading': '⏳',
            'error': '❌',
            'success': '✅',
            'warning': '⚠️',
            'info': 'ℹ️',
            'yes': '✅',
            'no': '❌',
            'ok': '👌',
            'close': '❌',
            'open': '🔓',
            'enable': '✅',
            'disable': '❌',
            'on': '🟢',
            'off': '🔴',
            'active': '🟢',
            'inactive': '🔴',
            'available': '✅',
            'unavailable': '❌',
            'locked': '🔒',
            'unlocked': '🔓',
            'completed': '✅',
            'in_progress': '⏳',
            'pending': '⏸️',
            'failed': '❌',
            'cancelled': '⏹️',
            'expired': '⏰',
            'new': '🆕',
            'old': '🕰️',
            'recent': '🕐',
            'popular': '🔥',
            'trending': '📈',
            'featured': '⭐',
            'recommended': '💡',
            'suggested': '💭',
            'favorite': '❤️',
            'bookmarked': '🔖',
            'shared': '📤',
            'public': '🌐',
            'private': '🔒',
            'secret': '🤫',
            'hidden': '👻',
            'visible': '👁️',
            'show': '👁️',
            'hide': '🙈',
            'display': '🖥️',
            'appearance': '🎨',
            'color': '🎨',
            'size': '📏',
            'font': '🔤',
            'style': '💄',
            'layout': '📐',
            'position': '📍',
            'alignment': '↔️',
            'spacing': '↕️',
            'margin': '📏',
            'padding': '📦',
            'border': '🔲',
            'background': '🖼️',
            'foreground': '🎨',
            'transparency': '👻',
            'opacity': '🌫️',
            'brightness': '☀️',
            'contrast': '🌓',
            'saturation': '🌈',
            'hue': '🎨',
            'blur': '🌫️',
            'sharpness': '🔍',
            'quality': '⭐',
            'resolution': '📺',
            'dimensions': '📐',
            'width': '↔️',
            'height': '↕️',
            'depth': '🔽',
            'length': '📏',
            'area': '📐',
            'volume': '📦',
            'weight': '⚖️',
            'mass': '⚖️',
            'density': '🔢',
            'speed': '🏃',
            'velocity': '🏃',
            'acceleration': '🚀',
            'force': '💪',
            'pressure': '💨',
            'temperature': '🌡️',
            'energy': '⚡',
            'power': '💪',
            'frequency': '📡',
            'amplitude': '📊',
            'wavelength': '🌊',
            'phase': '🔄'
        }
    
    def get_main_settings_keyboard(self) -> InlineKeyboardMarkup:
        """Get main settings menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['user']} User Settings",
            callback_data="settings_user"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['game']} Game Settings",
            callback_data="settings_game"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['notification']} Notifications",
            callback_data="settings_notifications"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['privacy']} Privacy",
            callback_data="settings_privacy"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['display']} Display",
            callback_data="settings_display"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['sound']} Sound",
            callback_data="settings_sound"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['language']} Language",
            callback_data="settings_language"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['theme']} Theme",
            callback_data="settings_theme"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back to Main Menu",
            callback_data="main_menu"
        ))
        
        builder.adjust(2, 2, 2, 2, 1)
        return builder.as_markup()
    
    def get_user_settings_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Get user settings keyboard"""
        builder = InlineKeyboardBuilder()
        prefs = self.settings_manager.get_user_preferences(user_id)
        
        # Auto-save setting
        auto_save_text = f"{self.emoji_map['enable'] if prefs.auto_save else self.emoji_map['disable']} Auto Save"
        builder.add(InlineKeyboardButton(
            text=auto_save_text,
            callback_data="toggle_auto_save"
        ))
        
        # Auto-collect setting
        auto_collect_text = f"{self.emoji_map['enable'] if prefs.auto_collect else self.emoji_map['disable']} Auto Collect"
        builder.add(InlineKeyboardButton(
            text=auto_collect_text,
            callback_data="toggle_auto_collect"
        ))
        
        # Auto-build setting
        auto_build_text = f"{self.emoji_map['enable'] if prefs.auto_build else self.emoji_map['disable']} Auto Build"
        builder.add(InlineKeyboardButton(
            text=auto_build_text,
            callback_data="toggle_auto_build"
        ))
        
        # Auto-research setting
        auto_research_text = f"{self.emoji_map['enable'] if prefs.auto_research else self.emoji_map['disable']} Auto Research"
        builder.add(InlineKeyboardButton(
            text=auto_research_text,
            callback_data="toggle_auto_research"
        ))
        
        # Auto-attack setting
        auto_attack_text = f"{self.emoji_map['enable'] if prefs.auto_attack else self.emoji_map['disable']} Auto Attack"
        builder.add(InlineKeyboardButton(
            text=auto_attack_text,
            callback_data="toggle_auto_attack"
        ))
        
        # Difficulty level
        difficulty_text = f"🎯 Difficulty: {prefs.difficulty_level.title()}"
        builder.add(InlineKeyboardButton(
            text=difficulty_text,
            callback_data="change_difficulty"
        ))
        
        # Auto-pause on attack
        auto_pause_text = f"{self.emoji_map['enable'] if prefs.auto_pause_on_attack else self.emoji_map['disable']} Auto Pause on Attack"
        builder.add(InlineKeyboardButton(
            text=auto_pause_text,
            callback_data="toggle_auto_pause"
        ))
        
        # Auto-retreat threshold
        retreat_text = f"🏃 Retreat Threshold: {int(prefs.auto_retreat_threshold * 100)}%"
        builder.add(InlineKeyboardButton(
            text=retreat_text,
            callback_data="change_retreat_threshold"
        ))
        
        # Auto-heal threshold
        heal_text = f"💊 Heal Threshold: {int(prefs.auto_heal_threshold * 100)}%"
        builder.add(InlineKeyboardButton(
            text=heal_text,
            callback_data="change_heal_threshold"
        ))
        
        # Auto-supply threshold
        supply_text = f"📦 Supply Threshold: {int(prefs.auto_supply_threshold * 100)}%"
        builder.add(InlineKeyboardButton(
            text=supply_text,
            callback_data="change_supply_threshold"
        ))
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['reset']} Reset to Defaults",
            callback_data="reset_user_settings"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back to Settings",
            callback_data="settings_main"
        ))
        
        builder.adjust(2, 2, 2, 2, 2, 1, 1)
        return builder.as_markup()
    
    def get_notification_settings_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Get notification settings keyboard"""
        builder = InlineKeyboardBuilder()
        prefs = self.settings_manager.get_user_preferences(user_id)
        
        # Main notifications toggle
        notifications_text = f"{self.emoji_map['enable'] if prefs.notifications_enabled else self.emoji_map['disable']} All Notifications"
        builder.add(InlineKeyboardButton(
            text=notifications_text,
            callback_data="toggle_notifications"
        ))
        
        # Battle notifications
        battle_text = f"{self.emoji_map['enable'] if prefs.battle_notifications else self.emoji_map['disable']} Battle Notifications"
        builder.add(InlineKeyboardButton(
            text=battle_text,
            callback_data="toggle_battle_notifications"
        ))
        
        # Trade notifications
        trade_text = f"{self.emoji_map['enable'] if prefs.trade_notifications else self.emoji_map['disable']} Trade Notifications"
        builder.add(InlineKeyboardButton(
            text=trade_text,
            callback_data="toggle_trade_notifications"
        ))
        
        # Quest notifications
        quest_text = f"{self.emoji_map['enable'] if prefs.quest_notifications else self.emoji_map['disable']} Quest Notifications"
        builder.add(InlineKeyboardButton(
            text=quest_text,
            callback_data="toggle_quest_notifications"
        ))
        
        # Research notifications
        research_text = f"{self.emoji_map['enable'] if prefs.research_notifications else self.emoji_map['disable']} Research Notifications"
        builder.add(InlineKeyboardButton(
            text=research_text,
            callback_data="toggle_research_notifications"
        ))
        
        # Daily income notifications
        income_text = f"{self.emoji_map['enable'] if prefs.daily_income_notifications else self.emoji_map['disable']} Daily Income Notifications"
        builder.add(InlineKeyboardButton(
            text=income_text,
            callback_data="toggle_income_notifications"
        ))
        
        # Alliance notifications
        alliance_text = f"{self.emoji_map['enable'] if prefs.alliance_notifications else self.emoji_map['disable']} Alliance Notifications"
        builder.add(InlineKeyboardButton(
            text=alliance_text,
            callback_data="toggle_alliance_notifications"
        ))
        
        # World event notifications
        world_text = f"{self.emoji_map['enable'] if prefs.world_event_notifications else self.emoji_map['disable']} World Event Notifications"
        builder.add(InlineKeyboardButton(
            text=world_text,
            callback_data="toggle_world_notifications"
        ))
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back to Settings",
            callback_data="settings_main"
        ))
        
        builder.adjust(2, 2, 2, 2, 1)
        return builder.as_markup()
    
    def get_privacy_settings_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Get privacy settings keyboard"""
        builder = InlineKeyboardBuilder()
        prefs = self.settings_manager.get_user_preferences(user_id)
        
        # Show online status
        online_text = f"{self.emoji_map['enable'] if prefs.show_online_status else self.emoji_map['disable']} Show Online Status"
        builder.add(InlineKeyboardButton(
            text=online_text,
            callback_data="toggle_online_status"
        ))
        
        # Show rank
        rank_text = f"{self.emoji_map['enable'] if prefs.show_rank else self.emoji_map['disable']} Show Rank"
        builder.add(InlineKeyboardButton(
            text=rank_text,
            callback_data="toggle_show_rank"
        ))
        
        # Show wealth
        wealth_text = f"{self.emoji_map['enable'] if prefs.show_wealth else self.emoji_map['disable']} Show Wealth"
        builder.add(InlineKeyboardButton(
            text=wealth_text,
            callback_data="toggle_show_wealth"
        ))
        
        # Show military power
        military_text = f"{self.emoji_map['enable'] if prefs.show_military_power else self.emoji_map['disable']} Show Military Power"
        builder.add(InlineKeyboardButton(
            text=military_text,
            callback_data="toggle_show_military"
        ))
        
        # Allow direct messages
        dm_text = f"{self.emoji_map['enable'] if prefs.allow_direct_messages else self.emoji_map['disable']} Allow Direct Messages"
        builder.add(InlineKeyboardButton(
            text=dm_text,
            callback_data="toggle_direct_messages"
        ))
        
        # Allow trade requests
        trade_text = f"{self.emoji_map['enable'] if prefs.allow_trade_requests else self.emoji_map['disable']} Allow Trade Requests"
        builder.add(InlineKeyboardButton(
            text=trade_text,
            callback_data="toggle_trade_requests"
        ))
        
        # Allow alliance invites
        alliance_text = f"{self.emoji_map['enable'] if prefs.allow_alliance_invites else self.emoji_map['disable']} Allow Alliance Invites"
        builder.add(InlineKeyboardButton(
            text=alliance_text,
            callback_data="toggle_alliance_invites"
        ))
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back to Settings",
            callback_data="settings_main"
        ))
        
        builder.adjust(2, 2, 2, 1)
        return builder.as_markup()
    
    def get_display_settings_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Get display settings keyboard"""
        builder = InlineKeyboardBuilder()
        prefs = self.settings_manager.get_user_preferences(user_id)
        
        # Compact mode
        compact_text = f"{self.emoji_map['enable'] if prefs.compact_mode else self.emoji_map['disable']} Compact Mode"
        builder.add(InlineKeyboardButton(
            text=compact_text,
            callback_data="toggle_compact_mode"
        ))
        
        # Show emojis
        emoji_text = f"{self.emoji_map['enable'] if prefs.show_emojis else self.emoji_map['disable']} Show Emojis"
        builder.add(InlineKeyboardButton(
            text=emoji_text,
            callback_data="toggle_show_emojis"
        ))
        
        # Show animations
        animation_text = f"{self.emoji_map['enable'] if prefs.show_animations else self.emoji_map['disable']} Show Animations"
        builder.add(InlineKeyboardButton(
            text=animation_text,
            callback_data="toggle_show_animations"
        ))
        
        # Show detailed stats
        stats_text = f"{self.emoji_map['enable'] if prefs.show_detailed_stats else self.emoji_map['disable']} Show Detailed Stats"
        builder.add(InlineKeyboardButton(
            text=stats_text,
            callback_data="toggle_detailed_stats"
        ))
        
        # Show tooltips
        tooltip_text = f"{self.emoji_map['enable'] if prefs.show_tooltips else self.emoji_map['disable']} Show Tooltips"
        builder.add(InlineKeyboardButton(
            text=tooltip_text,
            callback_data="toggle_show_tooltips"
        ))
        
        # Theme selection
        theme_text = f"🎭 Theme: {prefs.theme.title()}"
        builder.add(InlineKeyboardButton(
            text=theme_text,
            callback_data="change_theme"
        ))
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back to Settings",
            callback_data="settings_main"
        ))
        
        builder.adjust(2, 2, 2, 1)
        return builder.as_markup()
    
    def get_sound_settings_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Get sound settings keyboard"""
        builder = InlineKeyboardBuilder()
        prefs = self.settings_manager.get_user_preferences(user_id)
        
        # Sound enabled
        sound_text = f"{self.emoji_map['enable'] if prefs.sound_enabled else self.emoji_map['disable']} Sound Effects"
        builder.add(InlineKeyboardButton(
            text=sound_text,
            callback_data="toggle_sound"
        ))
        
        # Battle sounds
        battle_text = f"{self.emoji_map['enable'] if prefs.battle_sounds else self.emoji_map['disable']} Battle Sounds"
        builder.add(InlineKeyboardButton(
            text=battle_text,
            callback_data="toggle_battle_sounds"
        ))
        
        # Notification sounds
        notification_text = f"{self.emoji_map['enable'] if prefs.notification_sounds else self.emoji_map['disable']} Notification Sounds"
        builder.add(InlineKeyboardButton(
            text=notification_text,
            callback_data="toggle_notification_sounds"
        ))
        
        # Music
        music_text = f"{self.emoji_map['enable'] if prefs.music_enabled else self.emoji_map['disable']} Background Music"
        builder.add(InlineKeyboardButton(
            text=music_text,
            callback_data="toggle_music"
        ))
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back to Settings",
            callback_data="settings_main"
        ))
        
        builder.adjust(2, 2, 1)
        return builder.as_markup()
    
    def get_language_settings_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Get language settings keyboard"""
        builder = InlineKeyboardBuilder()
        prefs = self.settings_manager.get_user_preferences(user_id)
        
        # Current language
        current_lang = prefs.language.upper()
        lang_text = f"🌐 Current: {current_lang}"
        builder.add(InlineKeyboardButton(
            text=lang_text,
            callback_data="current_language"
        ))
        
        # Language options
        languages = [
            ("en", "🇺🇸 English"),
            ("fa", "🇮🇷 فارسی (Persian)"),
            ("es", "🇪🇸 Español"),
            ("fr", "🇫🇷 Français"),
            ("de", "🇩🇪 Deutsch"),
            ("it", "🇮🇹 Italiano"),
            ("pt", "🇵🇹 Português"),
            ("ru", "🇷🇺 Русский"),
            ("zh", "🇨🇳 中文"),
            ("ja", "🇯🇵 日本語"),
            ("ko", "🇰🇷 한국어"),
            ("ar", "🇸🇦 العربية"),
            ("hi", "🇮🇳 हिन्दी"),
            ("tr", "🇹🇷 Türkçe"),
            ("nl", "🇳🇱 Nederlands")
        ]
        
        for lang_code, lang_name in languages:
            builder.add(InlineKeyboardButton(
                text=lang_name,
                callback_data=f"set_language_{lang_code}"
            ))
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back to Settings",
            callback_data="settings_main"
        ))
        
        builder.adjust(2, 2, 2, 2, 2, 2, 2, 2, 1)
        return builder.as_markup()
    
    def get_theme_settings_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Get theme settings keyboard"""
        builder = InlineKeyboardBuilder()
        prefs = self.settings_manager.get_user_preferences(user_id)
        
        # Current theme
        current_theme = prefs.theme.title()
        theme_text = f"🎭 Current: {current_theme}"
        builder.add(InlineKeyboardButton(
            text=theme_text,
            callback_data="current_theme"
        ))
        
        # Theme options
        themes = [
            ("default", "🎨 Default"),
            ("dark", "🌙 Dark"),
            ("light", "☀️ Light"),
            ("military", "🎖️ Military"),
            ("cyber", "💻 Cyber"),
            ("space", "🚀 Space"),
            ("magical", "🧙 Magical"),
            ("retro", "📺 Retro"),
            ("minimal", "⚪ Minimal"),
            ("colorful", "🌈 Colorful")
        ]
        
        for theme_code, theme_name in themes:
            builder.add(InlineKeyboardButton(
                text=theme_name,
                callback_data=f"set_theme_{theme_code}"
            ))
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back to Settings",
            callback_data="settings_main"
        ))
        
        builder.adjust(2, 2, 2, 2, 2, 1)
        return builder.as_markup()
    
    def get_difficulty_settings_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Get difficulty settings keyboard"""
        builder = InlineKeyboardBuilder()
        prefs = self.settings_manager.get_user_preferences(user_id)
        
        # Current difficulty
        current_diff = prefs.difficulty_level.title()
        diff_text = f"🎯 Current: {current_diff}"
        builder.add(InlineKeyboardButton(
            text=diff_text,
            callback_data="current_difficulty"
        ))
        
        # Difficulty options
        difficulties = [
            ("easy", "🟢 Easy"),
            ("normal", "🟡 Normal"),
            ("hard", "🟠 Hard"),
            ("extreme", "🔴 Extreme"),
            ("nightmare", "💀 Nightmare"),
            ("impossible", "👹 Impossible")
        ]
        
        for diff_code, diff_name in difficulties:
            builder.add(InlineKeyboardButton(
                text=diff_name,
                callback_data=f"set_difficulty_{diff_code}"
            ))
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back to User Settings",
            callback_data="settings_user"
        ))
        
        builder.adjust(2, 2, 2, 1)
        return builder.as_markup()
    
    def get_admin_settings_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Get admin settings keyboard (admin only)"""
        builder = InlineKeyboardBuilder()
        admin_settings = self.settings_manager.admin_settings
        
        # Maintenance mode
        maintenance_text = f"{self.emoji_map['enable'] if admin_settings.maintenance_mode else self.emoji_map['disable']} Maintenance Mode"
        builder.add(InlineKeyboardButton(
            text=maintenance_text,
            callback_data="toggle_maintenance"
        ))
        
        # Rate limiting
        rate_limit_text = f"⏱️ Rate Limit: {admin_settings.rate_limit_per_user}/min"
        builder.add(InlineKeyboardButton(
            text=rate_limit_text,
            callback_data="change_rate_limit"
        ))
        
        # Captcha
        captcha_text = f"{self.emoji_map['enable'] if admin_settings.enable_captcha else self.emoji_map['disable']} Captcha"
        builder.add(InlineKeyboardButton(
            text=captcha_text,
            callback_data="toggle_captcha"
        ))
        
        # Profanity filter
        profanity_text = f"{self.emoji_map['enable'] if admin_settings.enable_profanity_filter else self.emoji_map['disable']} Profanity Filter"
        builder.add(InlineKeyboardButton(
            text=profanity_text,
            callback_data="toggle_profanity_filter"
        ))
        
        # Spam protection
        spam_text = f"{self.emoji_map['enable'] if admin_settings.enable_spam_protection else self.emoji_map['disable']} Spam Protection"
        builder.add(InlineKeyboardButton(
            text=spam_text,
            callback_data="toggle_spam_protection"
        ))
        
        # Auto backup
        backup_text = f"{self.emoji_map['enable'] if admin_settings.auto_backup_enabled else self.emoji_map['disable']} Auto Backup"
        builder.add(InlineKeyboardButton(
            text=backup_text,
            callback_data="toggle_auto_backup"
        ))
        
        # Analytics
        analytics_text = f"{self.emoji_map['enable'] if admin_settings.enable_analytics else self.emoji_map['disable']} Analytics"
        builder.add(InlineKeyboardButton(
            text=analytics_text,
            callback_data="toggle_analytics"
        ))
        
        # Performance monitoring
        perf_text = f"{self.emoji_map['enable'] if admin_settings.enable_performance_monitoring else self.emoji_map['disable']} Performance Monitoring"
        builder.add(InlineKeyboardButton(
            text=perf_text,
            callback_data="toggle_performance_monitoring"
        ))
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back to Settings",
            callback_data="settings_main"
        ))
        
        builder.adjust(2, 2, 2, 2, 1)
        return builder.as_markup()
    
    def get_settings_summary_text(self, user_id: int) -> str:
        """Get settings summary text"""
        prefs = self.settings_manager.get_user_preferences(user_id)
        
        text = f"⚙️ **Settings Summary**\n\n"
        text += f"**👤 User Settings:**\n"
        text += f"• Language: {prefs.language.upper()}\n"
        text += f"• Theme: {prefs.theme.title()}\n"
        text += f"• Difficulty: {prefs.difficulty_level.title()}\n"
        text += f"• Auto Save: {self.emoji_map['enable'] if prefs.auto_save else self.emoji_map['disable']}\n"
        text += f"• Notifications: {self.emoji_map['enable'] if prefs.notifications_enabled else self.emoji_map['disable']}\n\n"
        
        text += f"**🔔 Notifications:**\n"
        text += f"• Battle: {self.emoji_map['enable'] if prefs.battle_notifications else self.emoji_map['disable']}\n"
        text += f"• Trade: {self.emoji_map['enable'] if prefs.trade_notifications else self.emoji_map['disable']}\n"
        text += f"• Quest: {self.emoji_map['enable'] if prefs.quest_notifications else self.emoji_map['disable']}\n"
        text += f"• Research: {self.emoji_map['enable'] if prefs.research_notifications else self.emoji_map['disable']}\n\n"
        
        text += f"**🔒 Privacy:**\n"
        text += f"• Show Online Status: {self.emoji_map['enable'] if prefs.show_online_status else self.emoji_map['disable']}\n"
        text += f"• Show Rank: {self.emoji_map['enable'] if prefs.show_rank else self.emoji_map['disable']}\n"
        text += f"• Show Wealth: {self.emoji_map['enable'] if prefs.show_wealth else self.emoji_map['disable']}\n"
        text += f"• Allow DMs: {self.emoji_map['enable'] if prefs.allow_direct_messages else self.emoji_map['disable']}\n\n"
        
        text += f"**🎨 Display:**\n"
        text += f"• Compact Mode: {self.emoji_map['enable'] if prefs.compact_mode else self.emoji_map['disable']}\n"
        text += f"• Show Emojis: {self.emoji_map['enable'] if prefs.show_emojis else self.emoji_map['disable']}\n"
        text += f"• Show Animations: {self.emoji_map['enable'] if prefs.show_animations else self.emoji_map['disable']}\n"
        text += f"• Detailed Stats: {self.emoji_map['enable'] if prefs.show_detailed_stats else self.emoji_map['disable']}\n\n"
        
        text += f"**🔊 Sound:**\n"
        text += f"• Sound Effects: {self.emoji_map['enable'] if prefs.sound_enabled else self.emoji_map['disable']}\n"
        text += f"• Battle Sounds: {self.emoji_map['enable'] if prefs.battle_sounds else self.emoji_map['disable']}\n"
        text += f"• Notification Sounds: {self.emoji_map['enable'] if prefs.notification_sounds else self.emoji_map['disable']}\n"
        text += f"• Background Music: {self.emoji_map['enable'] if prefs.music_enabled else self.emoji_map['disable']}\n\n"
        
        text += f"**🎮 Gameplay:**\n"
        text += f"• Auto Pause on Attack: {self.emoji_map['enable'] if prefs.auto_pause_on_attack else self.emoji_map['disable']}\n"
        text += f"• Auto Retreat Threshold: {int(prefs.auto_retreat_threshold * 100)}%\n"
        text += f"• Auto Heal Threshold: {int(prefs.auto_heal_threshold * 100)}%\n"
        text += f"• Auto Supply Threshold: {int(prefs.auto_supply_threshold * 100)}%\n\n"
        
        text += f"**🔧 Advanced:**\n"
        text += f"• Debug Mode: {self.emoji_map['enable'] if prefs.debug_mode else self.emoji_map['disable']}\n"
        text += f"• Verbose Logging: {self.emoji_map['enable'] if prefs.verbose_logging else self.emoji_map['disable']}\n"
        text += f"• Auto Backup: {self.emoji_map['enable'] if prefs.auto_backup else self.emoji_map['disable']}\n"
        text += f"• Backup Frequency: Every {prefs.backup_frequency} hours\n"
        text += f"• Max Backups: {prefs.max_backups}\n\n"
        
        text += f"Use the buttons below to modify any setting!"
        
        return text

# Example usage and testing
if __name__ == "__main__":
    # Test settings UI manager
    settings_manager = BotSettingsManager()
    ui_manager = SettingsUIManager(settings_manager)
    
    # Test user ID
    user_id = 12345
    
    # Test various keyboards
    print("Testing settings keyboards...")
    
    # Main settings
    main_kb = ui_manager.get_main_settings_keyboard()
    print(f"Main settings keyboard: {len(main_kb.inline_keyboard)} rows")
    
    # User settings
    user_kb = ui_manager.get_user_settings_keyboard(user_id)
    print(f"User settings keyboard: {len(user_kb.inline_keyboard)} rows")
    
    # Notification settings
    notif_kb = ui_manager.get_notification_settings_keyboard(user_id)
    print(f"Notification settings keyboard: {len(notif_kb.inline_keyboard)} rows")
    
    # Privacy settings
    privacy_kb = ui_manager.get_privacy_settings_keyboard(user_id)
    print(f"Privacy settings keyboard: {len(privacy_kb.inline_keyboard)} rows")
    
    # Display settings
    display_kb = ui_manager.get_display_settings_keyboard(user_id)
    print(f"Display settings keyboard: {len(display_kb.inline_keyboard)} rows")
    
    # Sound settings
    sound_kb = ui_manager.get_sound_settings_keyboard(user_id)
    print(f"Sound settings keyboard: {len(sound_kb.inline_keyboard)} rows")
    
    # Language settings
    lang_kb = ui_manager.get_language_settings_keyboard(user_id)
    print(f"Language settings keyboard: {len(lang_kb.inline_keyboard)} rows")
    
    # Theme settings
    theme_kb = ui_manager.get_theme_settings_keyboard(user_id)
    print(f"Theme settings keyboard: {len(theme_kb.inline_keyboard)} rows")
    
    # Difficulty settings
    diff_kb = ui_manager.get_difficulty_settings_keyboard(user_id)
    print(f"Difficulty settings keyboard: {len(diff_kb.inline_keyboard)} rows")
    
    # Admin settings
    admin_kb = ui_manager.get_admin_settings_keyboard(user_id)
    print(f"Admin settings keyboard: {len(admin_kb.inline_keyboard)} rows")
    
    # Settings summary
    summary_text = ui_manager.get_settings_summary_text(user_id)
    print(f"Settings summary text length: {len(summary_text)} characters")
    
    print("✅ Settings UI system working correctly!")