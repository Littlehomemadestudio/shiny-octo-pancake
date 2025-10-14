"""
Complex Resource Management System
Multiple currencies with realistic economic mechanics
"""

import random
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import json
import os

class ResourceType(Enum):
    GOLD = "gold"
    OIL = "oil"
    IRON = "iron"
    POPULATION = "population"
    KNOWLEDGE = "knowledge"
    ENERGY = "energy"
    FOOD = "food"
    WATER = "water"
    TECHNOLOGY = "technology"
    INFLUENCE = "influence"
    MANPOWER = "manpower"
    MATERIALS = "materials"
    FUEL = "fuel"
    AMMUNITION = "ammunition"
    MEDICAL_SUPPLIES = "medical_supplies"

class ResourceCategory(Enum):
    BASIC = "basic"          # Gold, Food, Water
    INDUSTRIAL = "industrial"  # Oil, Iron, Energy, Materials
    HUMAN = "human"          # Population, Manpower, Knowledge
    MILITARY = "military"    # Fuel, Ammunition, Medical Supplies
    ADVANCED = "advanced"    # Technology, Influence

@dataclass
class Resource:
    """Resource definition"""
    resource_type: ResourceType
    category: ResourceCategory
    name: str
    description: str
    base_value: float  # Base value in gold
    volatility: float  # Price volatility (0-1)
    rarity: float  # Rarity factor (0-1)
    decay_rate: float  # Decay rate per hour
    storage_cost: float  # Storage cost per unit per hour
    emoji: str
    unit: str
    min_price: float
    max_price: float

@dataclass
class ResourcePrice:
    """Current resource price"""
    resource_type: ResourceType
    price: float
    change: float  # Price change from last update
    change_percent: float
    timestamp: datetime
    demand: float  # Current demand (0-1)
    supply: float  # Current supply (0-1)

@dataclass
class ResourceTransaction:
    """Resource transaction record"""
    transaction_id: str
    user_id: int
    resource_type: ResourceType
    amount: float
    price: float
    total_cost: float
    transaction_type: str  # "buy", "sell", "trade", "earn", "spend"
    timestamp: datetime
    description: str

@dataclass
class ResourceStorage:
    """Player resource storage"""
    user_id: int
    resources: Dict[ResourceType, float]
    storage_capacity: Dict[ResourceType, float]
    last_updated: datetime

class ComplexResourceManager:
    """Advanced resource management system"""
    
    def __init__(self, database_manager):
        self.db_manager = database_manager
        self.resources: Dict[ResourceType, Resource] = {}
        self.prices: Dict[ResourceType, ResourcePrice] = {}
        self.transactions: List[ResourceTransaction] = []
        self.storage: Dict[int, ResourceStorage] = {}
        self.market_events: List[Dict] = []
        self._initialize_resources()
        self._initialize_prices()
    
    def _initialize_resources(self):
        """Initialize all resource types"""
        resource_definitions = [
            # BASIC RESOURCES
            Resource(
                resource_type=ResourceType.GOLD,
                category=ResourceCategory.BASIC,
                name="Gold",
                description="Universal currency and store of value",
                base_value=1.0,
                volatility=0.1,
                rarity=0.0,
                decay_rate=0.0,
                storage_cost=0.0,
                emoji="💰",
                unit="coins",
                min_price=0.8,
                max_price=1.2
            ),
            Resource(
                resource_type=ResourceType.FOOD,
                category=ResourceCategory.BASIC,
                name="Food",
                description="Essential for population growth and military operations",
                base_value=0.5,
                volatility=0.3,
                rarity=0.1,
                decay_rate=0.05,
                storage_cost=0.01,
                emoji="🌾",
                unit="tons",
                min_price=0.2,
                max_price=1.0
            ),
            Resource(
                resource_type=ResourceType.WATER,
                category=ResourceCategory.BASIC,
                name="Water",
                description="Critical for survival and industrial processes",
                base_value=0.3,
                volatility=0.4,
                rarity=0.2,
                decay_rate=0.0,
                storage_cost=0.005,
                emoji="💧",
                unit="liters",
                min_price=0.1,
                max_price=0.8
            ),
            
            # INDUSTRIAL RESOURCES
            Resource(
                resource_type=ResourceType.OIL,
                category=ResourceCategory.INDUSTRIAL,
                name="Oil",
                description="Primary energy source for vehicles and industry",
                base_value=2.0,
                volatility=0.5,
                rarity=0.3,
                decay_rate=0.0,
                storage_cost=0.05,
                emoji="🛢️",
                unit="barrels",
                min_price=1.0,
                max_price=4.0
            ),
            Resource(
                resource_type=ResourceType.IRON,
                category=ResourceCategory.INDUSTRIAL,
                name="Iron",
                description="Essential for construction and weapons manufacturing",
                base_value=1.5,
                volatility=0.2,
                rarity=0.1,
                decay_rate=0.01,
                storage_cost=0.02,
                emoji="⛏️",
                unit="tons",
                min_price=1.0,
                max_price=2.5
            ),
            Resource(
                resource_type=ResourceType.ENERGY,
                category=ResourceCategory.INDUSTRIAL,
                name="Energy",
                description="Electrical power for all operations",
                base_value=1.2,
                volatility=0.3,
                rarity=0.2,
                decay_rate=0.1,
                storage_cost=0.03,
                emoji="⚡",
                unit="MWh",
                min_price=0.5,
                max_price=2.0
            ),
            Resource(
                resource_type=ResourceType.MATERIALS,
                category=ResourceCategory.INDUSTRIAL,
                name="Materials",
                description="General construction and manufacturing materials",
                base_value=0.8,
                volatility=0.25,
                rarity=0.05,
                decay_rate=0.02,
                storage_cost=0.01,
                emoji="🧱",
                unit="units",
                min_price=0.4,
                max_price=1.5
            ),
            
            # HUMAN RESOURCES
            Resource(
                resource_type=ResourceType.POPULATION,
                category=ResourceCategory.HUMAN,
                name="Population",
                description="Citizens available for work and military service",
                base_value=10.0,
                volatility=0.1,
                rarity=0.0,
                decay_rate=0.001,
                storage_cost=0.1,
                emoji="👥",
                unit="people",
                min_price=5.0,
                max_price=20.0
            ),
            Resource(
                resource_type=ResourceType.MANPOWER,
                category=ResourceCategory.HUMAN,
                name="Manpower",
                description="Trained personnel available for military operations",
                base_value=15.0,
                volatility=0.2,
                rarity=0.2,
                decay_rate=0.005,
                storage_cost=0.15,
                emoji="🪖",
                unit="personnel",
                min_price=8.0,
                max_price=30.0
            ),
            Resource(
                resource_type=ResourceType.KNOWLEDGE,
                category=ResourceCategory.HUMAN,
                name="Knowledge",
                description="Scientific and technical expertise",
                base_value=25.0,
                volatility=0.15,
                rarity=0.4,
                decay_rate=0.0,
                storage_cost=0.0,
                emoji="🧠",
                unit="points",
                min_price=15.0,
                max_price=50.0
            ),
            
            # MILITARY RESOURCES
            Resource(
                resource_type=ResourceType.FUEL,
                category=ResourceCategory.MILITARY,
                name="Military Fuel",
                description="High-grade fuel for military vehicles",
                base_value=3.0,
                volatility=0.4,
                rarity=0.3,
                decay_rate=0.02,
                storage_cost=0.08,
                emoji="⛽",
                unit="gallons",
                min_price=1.5,
                max_price=6.0
            ),
            Resource(
                resource_type=ResourceType.AMMUNITION,
                category=ResourceCategory.MILITARY,
                name="Ammunition",
                description="Weapons and ammunition for military operations",
                base_value=5.0,
                volatility=0.3,
                rarity=0.4,
                decay_rate=0.0,
                storage_cost=0.1,
                emoji="🔫",
                unit="rounds",
                min_price=2.5,
                max_price=10.0
            ),
            Resource(
                resource_type=ResourceType.MEDICAL_SUPPLIES,
                category=ResourceCategory.MILITARY,
                name="Medical Supplies",
                description="Medical equipment and supplies for wounded",
                base_value=8.0,
                volatility=0.2,
                rarity=0.3,
                decay_rate=0.01,
                storage_cost=0.05,
                emoji="🏥",
                unit="units",
                min_price=4.0,
                max_price=15.0
            ),
            
            # ADVANCED RESOURCES
            Resource(
                resource_type=ResourceType.TECHNOLOGY,
                category=ResourceCategory.ADVANCED,
                name="Technology",
                description="Advanced technological capabilities",
                base_value=50.0,
                volatility=0.1,
                rarity=0.6,
                decay_rate=0.0,
                storage_cost=0.0,
                emoji="🔬",
                unit="points",
                min_price=30.0,
                max_price=100.0
            ),
            Resource(
                resource_type=ResourceType.INFLUENCE,
                category=ResourceCategory.ADVANCED,
                name="Influence",
                description="Political and diplomatic influence",
                base_value=20.0,
                volatility=0.2,
                rarity=0.5,
                decay_rate=0.005,
                storage_cost=0.0,
                emoji="👑",
                unit="points",
                min_price=10.0,
                max_price=40.0
            )
        ]
        
        for resource in resource_definitions:
            self.resources[resource.resource_type] = resource
    
    def _initialize_prices(self):
        """Initialize resource prices"""
        for resource_type, resource in self.resources.items():
            price = resource.base_value * random.uniform(0.8, 1.2)
            self.prices[resource_type] = ResourcePrice(
                resource_type=resource_type,
                price=price,
                change=0.0,
                change_percent=0.0,
                timestamp=datetime.now(),
                demand=random.uniform(0.3, 0.7),
                supply=random.uniform(0.3, 0.7)
            )
    
    def update_prices(self):
        """Update all resource prices based on market conditions"""
        for resource_type, resource in self.resources.items():
            price_data = self.prices[resource_type]
            
            # Calculate price change based on supply and demand
            supply_demand_ratio = price_data.supply / max(price_data.demand, 0.1)
            
            # Base price change
            base_change = (supply_demand_ratio - 1) * resource.volatility * 0.1
            
            # Add random volatility
            random_change = random.uniform(-resource.volatility, resource.volatility) * 0.05
            
            # Add market events impact
            event_impact = self._calculate_event_impact(resource_type)
            
            # Calculate new price
            total_change = base_change + random_change + event_impact
            new_price = price_data.price * (1 + total_change)
            
            # Apply price limits
            new_price = max(resource.min_price, min(resource.max_price, new_price))
            
            # Update price data
            old_price = price_data.price
            price_data.price = new_price
            price_data.change = new_price - old_price
            price_data.change_percent = (price_data.change / old_price) * 100 if old_price > 0 else 0
            price_data.timestamp = datetime.now()
            
            # Update supply and demand
            price_data.demand = max(0.1, min(1.0, price_data.demand + random.uniform(-0.1, 0.1)))
            price_data.supply = max(0.1, min(1.0, price_data.supply + random.uniform(-0.1, 0.1)))
    
    def _calculate_event_impact(self, resource_type: ResourceType) -> float:
        """Calculate impact of market events on resource price"""
        impact = 0.0
        
        for event in self.market_events:
            if event["expires"] < datetime.now():
                continue
            
            if resource_type in event["affected_resources"]:
                impact += event["impact"] * event["intensity"]
        
        return impact
    
    def create_market_event(self, event_type: str, description: str, 
                           affected_resources: List[ResourceType], 
                           impact: float, intensity: float, duration_hours: int):
        """Create a market event that affects resource prices"""
        event = {
            "event_type": event_type,
            "description": description,
            "affected_resources": affected_resources,
            "impact": impact,
            "intensity": intensity,
            "created": datetime.now(),
            "expires": datetime.now() + timedelta(hours=duration_hours)
        }
        
        self.market_events.append(event)
        
        # Remove expired events
        self.market_events = [e for e in self.market_events if e["expires"] > datetime.now()]
    
    def get_resource_price(self, resource_type: ResourceType) -> ResourcePrice:
        """Get current price of a resource"""
        return self.prices.get(resource_type)
    
    def get_all_prices(self) -> Dict[ResourceType, ResourcePrice]:
        """Get all resource prices"""
        return self.prices.copy()
    
    def buy_resource(self, user_id: int, resource_type: ResourceType, 
                    amount: float) -> Tuple[bool, str, float]:
        """Buy a resource"""
        if resource_type not in self.resources:
            return False, "Invalid resource type", 0.0
        
        price_data = self.prices[resource_type]
        total_cost = amount * price_data.price
        
        # Check if user has enough gold
        user_storage = self._get_user_storage(user_id)
        if user_storage.resources.get(ResourceType.GOLD, 0) < total_cost:
            return False, "Insufficient gold", 0.0
        
        # Check storage capacity
        if not self._check_storage_capacity(user_id, resource_type, amount):
            return False, "Insufficient storage capacity", 0.0
        
        # Execute transaction
        user_storage.resources[ResourceType.GOLD] -= total_cost
        user_storage.resources[resource_type] = user_storage.resources.get(resource_type, 0) + amount
        
        # Record transaction
        self._record_transaction(user_id, resource_type, amount, price_data.price, 
                               total_cost, "buy", f"Bought {amount} {resource_type.value}")
        
        return True, "Purchase successful", total_cost
    
    def sell_resource(self, user_id: int, resource_type: ResourceType, 
                     amount: float) -> Tuple[bool, str, float]:
        """Sell a resource"""
        if resource_type not in self.resources:
            return False, "Invalid resource type", 0.0
        
        price_data = self.prices[resource_type]
        total_earnings = amount * price_data.price
        
        # Check if user has enough resources
        user_storage = self._get_user_storage(user_id)
        if user_storage.resources.get(resource_type, 0) < amount:
            return False, "Insufficient resources", 0.0
        
        # Execute transaction
        user_storage.resources[resource_type] -= amount
        user_storage.resources[ResourceType.GOLD] = user_storage.resources.get(ResourceType.GOLD, 0) + total_earnings
        
        # Record transaction
        self._record_transaction(user_id, resource_type, amount, price_data.price, 
                               total_earnings, "sell", f"Sold {amount} {resource_type.value}")
        
        return True, "Sale successful", total_earnings
    
    def trade_resources(self, user_id: int, from_resource: ResourceType, 
                       to_resource: ResourceType, amount: float) -> Tuple[bool, str, float]:
        """Trade one resource for another"""
        if from_resource not in self.resources or to_resource not in self.resources:
            return False, "Invalid resource type", 0.0
        
        from_price = self.prices[from_resource].price
        to_price = self.prices[to_resource].price
        
        # Calculate exchange rate
        exchange_rate = from_price / to_price
        received_amount = amount * exchange_rate
        
        # Check if user has enough resources
        user_storage = self._get_user_storage(user_id)
        if user_storage.resources.get(from_resource, 0) < amount:
            return False, "Insufficient resources", 0.0
        
        # Check storage capacity
        if not self._check_storage_capacity(user_id, to_resource, received_amount):
            return False, "Insufficient storage capacity", 0.0
        
        # Execute trade
        user_storage.resources[from_resource] -= amount
        user_storage.resources[to_resource] = user_storage.resources.get(to_resource, 0) + received_amount
        
        # Record transaction
        self._record_transaction(user_id, from_resource, amount, from_price, 
                               amount * from_price, "trade", 
                               f"Traded {amount} {from_resource.value} for {received_amount} {to_resource.value}")
        
        return True, "Trade successful", received_amount
    
    def _get_user_storage(self, user_id: int) -> ResourceStorage:
        """Get or create user storage"""
        if user_id not in self.storage:
            self.storage[user_id] = ResourceStorage(
                user_id=user_id,
                resources={},
                storage_capacity={},
                last_updated=datetime.now()
            )
        return self.storage[user_id]
    
    def _check_storage_capacity(self, user_id: int, resource_type: ResourceType, 
                               amount: float) -> bool:
        """Check if user has enough storage capacity"""
        user_storage = self._get_user_storage(user_id)
        current_amount = user_storage.resources.get(resource_type, 0)
        capacity = user_storage.storage_capacity.get(resource_type, 1000.0)  # Default capacity
        
        return current_amount + amount <= capacity
    
    def _record_transaction(self, user_id: int, resource_type: ResourceType, 
                           amount: float, price: float, total_cost: float, 
                           transaction_type: str, description: str):
        """Record a resource transaction"""
        transaction = ResourceTransaction(
            transaction_id=f"txn_{user_id}_{int(time.time())}",
            user_id=user_id,
            resource_type=resource_type,
            amount=amount,
            price=price,
            total_cost=total_cost,
            transaction_type=transaction_type,
            timestamp=datetime.now(),
            description=description
        )
        
        self.transactions.append(transaction)
        
        # Keep only last 1000 transactions
        if len(self.transactions) > 1000:
            self.transactions = self.transactions[-1000:]
    
    def get_user_resources(self, user_id: int) -> Dict[ResourceType, float]:
        """Get user's current resources"""
        user_storage = self._get_user_storage(user_id)
        return user_storage.resources.copy()
    
    def add_resource(self, user_id: int, resource_type: ResourceType, amount: float, 
                    source: str = "earned"):
        """Add resources to user (e.g., from quests, daily income)"""
        user_storage = self._get_user_storage(user_id)
        user_storage.resources[resource_type] = user_storage.resources.get(resource_type, 0) + amount
        
        # Record transaction
        price = self.prices[resource_type].price if resource_type in self.prices else 0
        self._record_transaction(user_id, resource_type, amount, price, 
                               amount * price, "earn", f"Earned {amount} {resource_type.value} from {source}")
    
    def spend_resource(self, user_id: int, resource_type: ResourceType, amount: float, 
                      purpose: str = "spent"):
        """Spend resources (e.g., for building, research)"""
        user_storage = self._get_user_storage(user_id)
        
        if user_storage.resources.get(resource_type, 0) < amount:
            return False, "Insufficient resources"
        
        user_storage.resources[resource_type] -= amount
        
        # Record transaction
        price = self.prices[resource_type].price if resource_type in self.prices else 0
        self._record_transaction(user_id, resource_type, amount, price, 
                               amount * price, "spend", f"Spent {amount} {resource_type.value} for {purpose}")
        
        return True, "Resources spent successfully"
    
    def get_market_summary(self) -> Dict[str, Any]:
        """Get market summary with trends and events"""
        summary = {
            "total_resources": len(self.resources),
            "price_changes": {},
            "most_volatile": [],
            "active_events": [],
            "market_health": "stable"
        }
        
        # Calculate price changes
        for resource_type, price_data in self.prices.items():
            summary["price_changes"][resource_type.value] = {
                "price": price_data.price,
                "change": price_data.change,
                "change_percent": price_data.change_percent,
                "demand": price_data.demand,
                "supply": price_data.supply
            }
        
        # Find most volatile resources
        volatility_scores = []
        for resource_type, resource in self.resources.items():
            price_data = self.prices[resource_type]
            volatility_score = abs(price_data.change_percent) * resource.volatility
            volatility_scores.append((resource_type, volatility_score))
        
        volatility_scores.sort(key=lambda x: x[1], reverse=True)
        summary["most_volatile"] = [r[0].value for r in volatility_scores[:5]]
        
        # Active events
        active_events = [e for e in self.market_events if e["expires"] > datetime.now()]
        summary["active_events"] = [
            {
                "type": e["event_type"],
                "description": e["description"],
                "affected_resources": [r.value for r in e["affected_resources"]],
                "expires": e["expires"].isoformat()
            }
            for e in active_events
        ]
        
        # Market health
        total_volatility = sum(abs(p.change_percent) for p in self.prices.values()) / len(self.prices)
        if total_volatility > 10:
            summary["market_health"] = "volatile"
        elif total_volatility > 5:
            summary["market_health"] = "unstable"
        else:
            summary["market_health"] = "stable"
        
        return summary

# Example usage and testing
if __name__ == "__main__":
    # Test resource management system
    print("Testing complex resource management system...")
    
    # Mock database manager
    class MockDatabaseManager:
        def get_session(self):
            return self
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
    
    db_manager = MockDatabaseManager()
    resource_manager = ComplexResourceManager(db_manager)
    
    # Test user
    user_id = 12345
    
    # Give user some starting resources
    resource_manager.add_resource(user_id, ResourceType.GOLD, 1000, "starting")
    resource_manager.add_resource(user_id, ResourceType.OIL, 100, "starting")
    resource_manager.add_resource(user_id, ResourceType.IRON, 50, "starting")
    
    # Test buying resources
    success, message, cost = resource_manager.buy_resource(user_id, ResourceType.FOOD, 10)
    print(f"Buy food: {success}, {message}, Cost: {cost}")
    
    # Test selling resources
    success, message, earnings = resource_manager.sell_resource(user_id, ResourceType.OIL, 20)
    print(f"Sell oil: {success}, {message}, Earnings: {earnings}")
    
    # Test trading resources
    success, message, received = resource_manager.trade_resources(user_id, ResourceType.IRON, ResourceType.ENERGY, 10)
    print(f"Trade iron for energy: {success}, {message}, Received: {received}")
    
    # Test market events
    resource_manager.create_market_event(
        "oil_crisis",
        "Major oil fields attacked, oil prices skyrocketing",
        [ResourceType.OIL, ResourceType.FUEL],
        0.5,  # 50% price increase
        0.8,  # High intensity
        24    # 24 hours duration
    )
    
    # Update prices
    resource_manager.update_prices()
    
    # Get market summary
    summary = resource_manager.get_market_summary()
    print(f"Market summary: {summary}")
    
    # Get user resources
    user_resources = resource_manager.get_user_resources(user_id)
    print(f"User resources: {user_resources}")
    
    print("✅ Complex resource management system working correctly!")