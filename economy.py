"""
Economy System for World War Telegram Bot
"""
import asyncio
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import DatabaseManager, Player, PlayerMaterial, Trade

class EconomyManager:
    def __init__(self, config: Dict):
        self.config = config
        self.materials = config["materials"]
        self.price_update_interval = config["price_update_interval"]
        self.base_prices = {material: data["base_price"] for material, data in self.materials.items()}
        self.volatilities = {material: data["volatility"] for material, data in self.materials.items()}
        self.current_prices = self.base_prices.copy()
        self.price_history = {material: [] for material in self.materials.keys()}
        self.is_running = False
    
    def get_current_prices(self) -> Dict[str, Dict]:
        """Get current market prices with volatility info"""
        prices = {}
        for material, base_price in self.base_prices.items():
            current_price = self.current_prices[material]
            volatility = self.volatilities[material]
            change = ((current_price - base_price) / base_price) * 100
            
            prices[material] = {
                "price": current_price,
                "base_price": base_price,
                "volatility": volatility,
                "change_percent": change,
                "trend": "up" if change > 0 else "down" if change < 0 else "stable"
            }
        
        return prices
    
    def update_prices(self):
        """Update material prices based on supply and demand"""
        for material in self.materials.keys():
            base_price = self.base_prices[material]
            volatility = self.volatilities[material]
            
            # Random walk with mean reversion
            current_price = self.current_prices[material]
            change = random.gauss(0, volatility * base_price)
            
            # Mean reversion factor
            mean_reversion = (base_price - current_price) * 0.1
            
            new_price = current_price + change + mean_reversion
            
            # Ensure price doesn't go below 10% of base price
            min_price = base_price * 0.1
            max_price = base_price * 5.0
            
            new_price = max(min_price, min(max_price, new_price))
            
            self.current_prices[material] = new_price
            
            # Store price history
            self.price_history[material].append({
                "timestamp": datetime.utcnow(),
                "price": new_price
            })
            
            # Keep only last 100 price points
            if len(self.price_history[material]) > 100:
                self.price_history[material] = self.price_history[material][-100:]
    
    async def update_prices_loop(self):
        """Background task to update prices periodically"""
        self.is_running = True
        while self.is_running:
            try:
                self.update_prices()
                await asyncio.sleep(self.price_update_interval)
            except Exception as e:
                print(f"Error updating prices: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    def stop(self):
        """Stop the price update loop"""
        self.is_running = False
    
    def calculate_trade_cost(self, material: str, quantity: float) -> float:
        """Calculate cost for trading a material"""
        if material not in self.current_prices:
            return 0.0
        
        price_per_unit = self.current_prices[material]
        return price_per_unit * quantity
    
    def get_material_value(self, materials: Dict[str, float]) -> float:
        """Calculate total value of materials"""
        total_value = 0.0
        for material, quantity in materials.items():
            if material in self.current_prices:
                total_value += self.current_prices[material] * quantity
        return total_value
    
    def apply_market_impact(self, material: str, quantity: float, trade_type: str):
        """Apply market impact for large trades"""
        if material not in self.current_prices:
            return
        
        # Large trades affect prices
        impact_factor = min(quantity / 1000.0, 0.1)  # Max 10% impact
        
        if trade_type == "buy":
            # Buying increases price
            price_increase = self.current_prices[material] * impact_factor
            self.current_prices[material] += price_increase
        elif trade_type == "sell":
            # Selling decreases price
            price_decrease = self.current_prices[material] * impact_factor
            self.current_prices[material] = max(
                self.current_prices[material] - price_decrease,
                self.base_prices[material] * 0.1
            )

class TradeManager:
    def __init__(self, db_manager: DatabaseManager, economy_manager: EconomyManager):
        self.db = db_manager
        self.economy = economy_manager
    
    def create_trade(self, seller_id: int, material: str, quantity: float, 
                    price_per_unit: float, buyer_id: Optional[int] = None) -> Trade:
        """Create a new trade"""
        with self.db.get_session() as session:
            trade = Trade(
                seller_id=seller_id,
                buyer_id=buyer_id,
                material_type=material,
                quantity=quantity,
                price_per_unit=price_per_unit,
                total_price=price_per_unit * quantity,
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            session.add(trade)
            session.commit()
            return trade
    
    def get_available_trades(self, material: Optional[str] = None) -> List[Trade]:
        """Get available trades, optionally filtered by material"""
        with self.db.get_session() as session:
            query = session.query(Trade).filter(Trade.status == "open")
            if material:
                query = query.filter(Trade.material_type == material)
            return query.all()
    
    def execute_trade(self, trade_id: int, buyer_id: int) -> bool:
        """Execute a trade between players"""
        with self.db.get_session() as session:
            trade = session.query(Trade).filter_by(id=trade_id).first()
            if not trade or trade.status != "open":
                return False
            
            seller = session.query(Player).filter_by(id=trade.seller_id).first()
            buyer = session.query(Player).filter_by(id=buyer_id).first()
            
            if not seller or not buyer:
                return False
            
            # Check if buyer has enough gold
            if buyer.gold < trade.total_price:
                return False
            
            # Check if seller has enough materials
            seller_material = session.query(PlayerMaterial).filter_by(
                player_id=seller.id,
                material_type=trade.material_type
            ).first()
            
            if not seller_material or seller_material.quantity < trade.quantity:
                return False
            
            # Execute the trade
            seller_material.quantity -= trade.quantity
            seller.gold += trade.total_price
            
            # Give materials to buyer
            buyer_material = session.query(PlayerMaterial).filter_by(
                player_id=buyer.id,
                material_type=trade.material_type
            ).first()
            
            if buyer_material:
                buyer_material.quantity += trade.quantity
            else:
                buyer_material = PlayerMaterial(
                    player_id=buyer.id,
                    material_type=trade.material_type,
                    quantity=trade.quantity
                )
                session.add(buyer_material)
            
            buyer.gold -= trade.total_price
            
            # Update trade status
            trade.buyer_id = buyer_id
            trade.status = "completed"
            trade.completed_at = datetime.utcnow()
            
            # Apply market impact
            self.economy.apply_market_impact(trade.material_type, trade.quantity, "buy")
            
            session.commit()
            return True
    
    def cancel_trade(self, trade_id: int, player_id: int) -> bool:
        """Cancel a trade (only by seller)"""
        with self.db.get_session() as session:
            trade = session.query(Trade).filter_by(id=trade_id).first()
            if not trade or trade.seller_id != player_id or trade.status != "open":
                return False
            
            trade.status = "cancelled"
            session.commit()
            return True
    
    def get_player_trades(self, player_id: int) -> List[Trade]:
        """Get all trades for a player"""
        with self.db.get_session() as session:
            return session.query(Trade).filter(
                (Trade.seller_id == player_id) | (Trade.buyer_id == player_id)
            ).order_by(Trade.created_at.desc()).all()

class DailyIncomeManager:
    def __init__(self, db_manager: DatabaseManager, config: Dict):
        self.db = db_manager
        self.config = config
        self.daily_income_base = config["daily_income_base"]
        self.tax_rate = config["tax_rate"]
        self.inflation_rate = config["inflation_rate"]
    
    def calculate_daily_income(self, player: Player) -> float:
        """Calculate daily income for a player"""
        base_income = self.daily_income_base
        
        # Level bonus
        level_bonus = player.level * 50
        
        # Morale bonus/penalty
        morale_factor = player.morale / 100.0
        
        # Nation bonus (if player has a nation)
        nation_bonus = 0
        if player.nation:
            nation_bonus = player.nation.gdp * 0.001  # 0.1% of nation GDP
        
        total_income = (base_income + level_bonus + nation_bonus) * morale_factor
        
        # Apply taxes
        tax_amount = total_income * self.tax_rate
        net_income = total_income - tax_amount
        
        return max(0, net_income)
    
    def process_daily_income(self):
        """Process daily income for all players"""
        with self.db.get_session() as session:
            players = session.query(Player).filter(Player.is_banned == False).all()
            
            for player in players:
                income = self.calculate_daily_income(player)
                player.gold += income
                
                # Update last active
                player.last_active = datetime.utcnow()
            
            session.commit()
    
    def apply_inflation(self):
        """Apply inflation to base prices"""
        # This would be called periodically to increase base prices
        # For now, we'll just update the economy manager's base prices
        pass

class MarketAnalysis:
    def __init__(self, economy_manager: EconomyManager):
        self.economy = economy_manager
    
    def get_market_trends(self) -> Dict[str, Dict]:
        """Get market trend analysis"""
        trends = {}
        
        for material in self.economy.materials.keys():
            history = self.economy.price_history[material]
            if len(history) < 2:
                continue
            
            # Calculate trend over last 10 price points
            recent_prices = [p["price"] for p in history[-10:]]
            if len(recent_prices) < 2:
                continue
            
            # Simple trend calculation
            price_change = recent_prices[-1] - recent_prices[0]
            percent_change = (price_change / recent_prices[0]) * 100
            
            # Volatility calculation
            if len(recent_prices) > 1:
                price_changes = [recent_prices[i] - recent_prices[i-1] for i in range(1, len(recent_prices))]
                volatility = (sum([abs(change) for change in price_changes]) / len(price_changes)) / recent_prices[0] * 100
            else:
                volatility = 0
            
            trends[material] = {
                "trend": "up" if percent_change > 1 else "down" if percent_change < -1 else "stable",
                "change_percent": percent_change,
                "volatility": volatility,
                "recommendation": self._get_trading_recommendation(percent_change, volatility)
            }
        
        return trends
    
    def _get_trading_recommendation(self, change_percent: float, volatility: float) -> str:
        """Get trading recommendation based on trend and volatility"""
        if change_percent > 5 and volatility < 10:
            return "Strong Buy"
        elif change_percent > 1 and volatility < 15:
            return "Buy"
        elif change_percent < -5 and volatility < 10:
            return "Strong Sell"
        elif change_percent < -1 and volatility < 15:
            return "Sell"
        elif volatility > 20:
            return "High Risk"
        else:
            return "Hold"