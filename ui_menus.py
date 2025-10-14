"""
UI Menu Manager for World War Telegram Bot
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class UIManager:
    def __init__(self):
        self.emoji_map = {
            "status": "📊",
            "economy": "💰",
            "military": "⚔️",
            "quest": "🎯",
            "research": "🔬",
            "alliance": "🤝",
            "admin": "⚙️",
            "trade": "💼",
            "materials": "📦",
            "attack": "⚔️",
            "build": "🏭",
            "province": "🗺️",
            "map": "🗺️",
            "diplomacy": "🌍",
            "back": "⬅️",
            "close": "❌"
        }
    
    def get_main_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get main menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['status']} Status",
            callback_data="game_main_status"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['economy']} Economy",
            callback_data="game_main_economy"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['military']} Military",
            callback_data="game_main_military"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['quest']} Quests",
            callback_data="game_main_quest"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['research']} Research",
            callback_data="game_main_research"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['alliance']} Alliance",
            callback_data="game_main_alliance"
        ))
        
        builder.adjust(2, 2, 2)
        return builder.as_markup()
    
    def get_status_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get status menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['profile']} Profile",
            callback_data="game_status_profile"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['materials']} Materials",
            callback_data="game_status_materials"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['military']} Military",
            callback_data="game_status_military"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_main_menu"
        ))
        
        builder.adjust(2, 2)
        return builder.as_markup()
    
    def get_economy_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get economy menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['trade']} Trade",
            callback_data="game_economy_trade"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['materials']} Materials",
            callback_data="game_economy_materials"
        ))
        builder.add(InlineKeyboardButton(
            text="📈 Market Prices",
            callback_data="game_economy_prices"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_main_menu"
        ))
        
        builder.adjust(2, 2)
        return builder.as_markup()
    
    def get_trade_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get trade menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        # Buy buttons
        materials = ["iron", "oil", "food", "gold", "uranium", "steel"]
        for material in materials:
            emoji = {"iron": "🛠️", "oil": "⛽", "food": "🌾", "gold": "🥇", "uranium": "☢️", "steel": "🔩"}.get(material, "📦")
            builder.add(InlineKeyboardButton(
                text=f"Buy {emoji} {material.title()}",
                callback_data=f"game_trade_buy_{material}"
            ))
        
        builder.add(InlineKeyboardButton(
            text="📈 Market Overview",
            callback_data="game_trade_market"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_economy_menu"
        ))
        
        builder.adjust(2, 2, 2, 1, 1)
        return builder.as_markup()
    
    def get_military_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get military menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['attack']} Attack",
            callback_data="game_military_attack"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['build']} Build Units",
            callback_data="game_military_build"
        ))
        builder.add(InlineKeyboardButton(
            text="👥 View Units",
            callback_data="game_military_units"
        ))
        builder.add(InlineKeyboardButton(
            text="🎖️ Assets Database",
            callback_data="game_military_assets"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_main_menu"
        ))
        
        builder.adjust(2, 2, 1)
        return builder.as_markup()
    
    def get_attack_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get attack menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="🎯 Attack Player",
            callback_data="game_attack_player"
        ))
        builder.add(InlineKeyboardButton(
            text="🏰 Attack Province",
            callback_data="game_attack_province"
        ))
        builder.add(InlineKeyboardButton(
            text="🤖 Attack AI Faction",
            callback_data="game_attack_ai"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_military_menu"
        ))
        
        builder.adjust(2, 2)
        return builder.as_markup()
    
    def get_build_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get build menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        unit_types = ["infantry", "tank", "artillery", "aircraft", "ship"]
        for unit_type in unit_types:
            emoji = {"infantry": "👥", "tank": "🚗", "artillery": "💣", "aircraft": "✈️", "ship": "🚢"}.get(unit_type, "⚔️")
            builder.add(InlineKeyboardButton(
                text=f"Build {emoji} {unit_type.title()}",
                callback_data=f"game_build_{unit_type}"
            ))
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_military_menu"
        ))
        
        builder.adjust(2, 2, 1, 1)
        return builder.as_markup()
    
    def get_assets_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get assets menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        categories = ["infantry", "armor", "aircraft", "naval", "missile", "defense"]
        for category in categories:
            emoji = {"infantry": "👥", "armor": "🚗", "aircraft": "✈️", "naval": "🚢", "missile": "🚀", "defense": "🛡️"}.get(category, "⚔️")
            builder.add(InlineKeyboardButton(
                text=f"{emoji} {category.title()}",
                callback_data=f"game_assets_{category}"
            ))
        
        builder.add(InlineKeyboardButton(
            text="🔍 Search Assets",
            callback_data="game_assets_search"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_military_menu"
        ))
        
        builder.adjust(2, 2, 2, 1, 1)
        return builder.as_markup()
    
    def get_province_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get province menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="🏰 My Provinces",
            callback_data="game_province_my"
        ))
        builder.add(InlineKeyboardButton(
            text="🏗️ Build",
            callback_data="game_province_build"
        ))
        builder.add(InlineKeyboardButton(
            text="📊 Manage",
            callback_data="game_province_manage"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_main_menu"
        ))
        
        builder.adjust(2, 2)
        return builder.as_markup()
    
    def get_map_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get map menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="🗺️ World Map",
            callback_data="game_map_world"
        ))
        builder.add(InlineKeyboardButton(
            text="🏰 Provinces",
            callback_data="game_map_provinces"
        ))
        builder.add(InlineKeyboardButton(
            text="⚔️ Conflicts",
            callback_data="game_map_conflicts"
        ))
        builder.add(InlineKeyboardButton(
            text="📊 Statistics",
            callback_data="game_map_stats"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_main_menu"
        ))
        
        builder.adjust(2, 2, 1)
        return builder.as_markup()
    
    def get_quest_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get quest menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="🎯 Available Quests",
            callback_data="game_quest_available"
        ))
        builder.add(InlineKeyboardButton(
            text="📋 Active Missions",
            callback_data="game_quest_active"
        ))
        builder.add(InlineKeyboardButton(
            text="🏆 Completed",
            callback_data="game_quest_completed"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_main_menu"
        ))
        
        builder.adjust(2, 2)
        return builder.as_markup()
    
    def get_research_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get research menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="🔬 Available Research",
            callback_data="game_research_available"
        ))
        builder.add(InlineKeyboardButton(
            text="⏳ Active Research",
            callback_data="game_research_active"
        ))
        builder.add(InlineKeyboardButton(
            text="🌳 Tech Tree",
            callback_data="game_research_tree"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_main_menu"
        ))
        
        builder.adjust(2, 2)
        return builder.as_markup()
    
    def get_tech_tree_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get tech tree menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="⚔️ Military Tech",
            callback_data="game_tech_military"
        ))
        builder.add(InlineKeyboardButton(
            text="💰 Economic Tech",
            callback_data="game_tech_economic"
        ))
        builder.add(InlineKeyboardButton(
            text="🔬 Research Tech",
            callback_data="game_tech_research"
        ))
        builder.add(InlineKeyboardButton(
            text="🏗️ Infrastructure",
            callback_data="game_tech_infrastructure"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_research_menu"
        ))
        
        builder.adjust(2, 2, 1)
        return builder.as_markup()
    
    def get_alliance_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get alliance menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="🤝 My Alliances",
            callback_data="game_alliance_list"
        ))
        builder.add(InlineKeyboardButton(
            text="➕ Create Alliance",
            callback_data="game_alliance_create"
        ))
        builder.add(InlineKeyboardButton(
            text="📨 Requests",
            callback_data="game_alliance_requests"
        ))
        builder.add(InlineKeyboardButton(
            text="🌍 Diplomacy",
            callback_data="game_alliance_diplomacy"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_main_menu"
        ))
        
        builder.adjust(2, 2, 1)
        return builder.as_markup()
    
    def get_diplomacy_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get diplomacy menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="🌍 Nations",
            callback_data="game_diplomacy_nations"
        ))
        builder.add(InlineKeyboardButton(
            text="📊 Relations",
            callback_data="game_diplomacy_relations"
        ))
        builder.add(InlineKeyboardButton(
            text="📜 Treaties",
            callback_data="game_diplomacy_treaties"
        ))
        builder.add(InlineKeyboardButton(
            text="🕵️ Espionage",
            callback_data="game_diplomacy_espionage"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_alliance_menu"
        ))
        
        builder.adjust(2, 2, 1)
        return builder.as_markup()
    
    def get_admin_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get admin menu keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="📊 Game Stats",
            callback_data="game_admin_stats"
        ))
        builder.add(InlineKeyboardButton(
            text="🔄 Reset Game",
            callback_data="game_admin_reset"
        ))
        builder.add(InlineKeyboardButton(
            text="🚫 Ban Player",
            callback_data="game_admin_ban"
        ))
        builder.add(InlineKeyboardButton(
            text="⚙️ Settings",
            callback_data="game_admin_settings"
        ))
        builder.add(InlineKeyboardButton(
            text="💾 Backup",
            callback_data="game_admin_backup"
        ))
        builder.add(InlineKeyboardButton(
            text="📈 Economy",
            callback_data="game_admin_economy"
        ))
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['back']} Back",
            callback_data="game_main_menu"
        ))
        
        builder.adjust(2, 2, 2, 1)
        return builder.as_markup()
    
    def get_confirmation_keyboard(self, action: str, data: str = "") -> InlineKeyboardMarkup:
        """Get confirmation keyboard for actions"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text="✅ Confirm",
            callback_data=f"game_confirm_{action}_{data}"
        ))
        builder.add(InlineKeyboardButton(
            text="❌ Cancel",
            callback_data="game_cancel"
        ))
        
        builder.adjust(2)
        return builder.as_markup()
    
    def get_pagination_keyboard(self, current_page: int, total_pages: int, prefix: str) -> InlineKeyboardMarkup:
        """Get pagination keyboard"""
        builder = InlineKeyboardBuilder()
        
        if current_page > 1:
            builder.add(InlineKeyboardButton(
                text="⬅️ Previous",
                callback_data=f"{prefix}_page_{current_page - 1}"
            ))
        
        builder.add(InlineKeyboardButton(
            text=f"Page {current_page}/{total_pages}",
            callback_data="game_noop"
        ))
        
        if current_page < total_pages:
            builder.add(InlineKeyboardButton(
                text="Next ➡️",
                callback_data=f"{prefix}_page_{current_page + 1}"
            ))
        
        builder.adjust(3)
        return builder.as_markup()
    
    def get_close_keyboard(self) -> InlineKeyboardMarkup:
        """Get simple close keyboard"""
        builder = InlineKeyboardBuilder()
        
        builder.add(InlineKeyboardButton(
            text=f"{self.emoji_map['close']} Close",
            callback_data="game_close"
        ))
        
        return builder.as_markup()