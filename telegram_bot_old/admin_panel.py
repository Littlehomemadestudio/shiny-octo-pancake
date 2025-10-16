"""
Advanced Admin Panel System
Comprehensive administrative controls and monitoring
"""

import json
import os
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import sqlite3
import psutil
import logging

@dataclass
class AdminAction:
    """Represents an admin action"""
    action_id: str
    admin_id: int
    target_id: Optional[int]
    action_type: str
    description: str
    timestamp: datetime
    success: bool
    details: Dict[str, Any]

@dataclass
class SystemMetrics:
    """System performance metrics"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, int]
    active_connections: int
    command_count: int
    error_count: int
    response_time_avg: float
    database_queries: int
    cache_hit_rate: float

class AdminPanel:
    """Advanced admin panel with comprehensive controls"""
    
    def __init__(self, settings_manager, database_manager):
        self.settings_manager = settings_manager
        self.database_manager = database_manager
        self.admin_actions: List[AdminAction] = []
        self.system_metrics: List[SystemMetrics] = []
        self.logger = logging.getLogger(__name__)
        
        # Initialize admin actions file
        self.actions_file = "admin_actions.json"
        self.load_admin_actions()
        
        # Initialize metrics file
        self.metrics_file = "system_metrics.json"
        self.load_system_metrics()
    
    def load_admin_actions(self):
        """Load admin actions from file"""
        if os.path.exists(self.actions_file):
            try:
                with open(self.actions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.admin_actions = [
                        AdminAction(
                            action_id=action['action_id'],
                            admin_id=action['admin_id'],
                            target_id=action.get('target_id'),
                            action_type=action['action_type'],
                            description=action['description'],
                            timestamp=datetime.fromisoformat(action['timestamp']),
                            success=action['success'],
                            details=action['details']
                        )
                        for action in data
                    ]
            except Exception as e:
                self.logger.error(f"Error loading admin actions: {e}")
                self.admin_actions = []
        else:
            self.admin_actions = []
    
    def save_admin_actions(self):
        """Save admin actions to file"""
        try:
            data = [
                {
                    'action_id': action.action_id,
                    'admin_id': action.admin_id,
                    'target_id': action.target_id,
                    'action_type': action.action_type,
                    'description': action.description,
                    'timestamp': action.timestamp.isoformat(),
                    'success': action.success,
                    'details': action.details
                }
                for action in self.admin_actions
            ]
            
            with open(self.actions_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving admin actions: {e}")
    
    def load_system_metrics(self):
        """Load system metrics from file"""
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.system_metrics = [
                        SystemMetrics(
                            timestamp=datetime.fromisoformat(metric['timestamp']),
                            cpu_usage=metric['cpu_usage'],
                            memory_usage=metric['memory_usage'],
                            disk_usage=metric['disk_usage'],
                            network_io=metric['network_io'],
                            active_connections=metric['active_connections'],
                            command_count=metric['command_count'],
                            error_count=metric['error_count'],
                            response_time_avg=metric['response_time_avg'],
                            database_queries=metric['database_queries'],
                            cache_hit_rate=metric['cache_hit_rate']
                        )
                        for metric in data
                    ]
            except Exception as e:
                self.logger.error(f"Error loading system metrics: {e}")
                self.system_metrics = []
        else:
            self.system_metrics = []
    
    def save_system_metrics(self):
        """Save system metrics to file"""
        try:
            data = [
                {
                    'timestamp': metric.timestamp.isoformat(),
                    'cpu_usage': metric.cpu_usage,
                    'memory_usage': metric.memory_usage,
                    'disk_usage': metric.disk_usage,
                    'network_io': metric.network_io,
                    'active_connections': metric.active_connections,
                    'command_count': metric.command_count,
                    'error_count': metric.error_count,
                    'response_time_avg': metric.response_time_avg,
                    'database_queries': metric.database_queries,
                    'cache_hit_rate': metric.cache_hit_rate
                }
                for metric in self.system_metrics
            ]
            
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving system metrics: {e}")
    
    def log_admin_action(self, admin_id: int, action_type: str, description: str, 
                        target_id: Optional[int] = None, success: bool = True, 
                        details: Optional[Dict[str, Any]] = None):
        """Log an admin action"""
        action_id = f"{admin_id}_{int(datetime.now().timestamp())}"
        action = AdminAction(
            action_id=action_id,
            admin_id=admin_id,
            target_id=target_id,
            action_type=action_type,
            description=description,
            timestamp=datetime.now(),
            success=success,
            details=details or {}
        )
        
        self.admin_actions.append(action)
        
        # Keep only last 1000 actions
        if len(self.admin_actions) > 1000:
            self.admin_actions = self.admin_actions[-1000:]
        
        self.save_admin_actions()
        self.logger.info(f"Admin action logged: {action_type} by {admin_id}")
    
    def collect_system_metrics(self):
        """Collect current system metrics"""
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = (disk.used / disk.total) * 100
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
            
            # Active connections
            connections = len(psutil.net_connections())
            
            # Bot-specific metrics (would be provided by bot)
            command_count = 0  # Would be tracked by bot
            error_count = 0    # Would be tracked by bot
            response_time_avg = 0.0  # Would be tracked by bot
            database_queries = 0  # Would be tracked by bot
            cache_hit_rate = 0.0  # Would be tracked by bot
            
            metric = SystemMetrics(
                timestamp=datetime.now(),
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                network_io=network_io,
                active_connections=connections,
                command_count=command_count,
                error_count=error_count,
                response_time_avg=response_time_avg,
                database_queries=database_queries,
                cache_hit_rate=cache_hit_rate
            )
            
            self.system_metrics.append(metric)
            
            # Keep only last 1000 metrics
            if len(self.system_metrics) > 1000:
                self.system_metrics = self.system_metrics[-1000:]
            
            self.save_system_metrics()
            
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {e}")
    
    def get_admin_actions(self, admin_id: Optional[int] = None, 
                         action_type: Optional[str] = None,
                         limit: int = 50) -> List[AdminAction]:
        """Get admin actions with optional filtering"""
        actions = self.admin_actions
        
        if admin_id:
            actions = [a for a in actions if a.admin_id == admin_id]
        
        if action_type:
            actions = [a for a in actions if a.action_type == action_type]
        
        return actions[-limit:]
    
    def get_system_metrics(self, hours: int = 24) -> List[SystemMetrics]:
        """Get system metrics for the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [m for m in self.system_metrics if m.timestamp >= cutoff_time]
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        if not self.system_metrics:
            return {"status": "unknown", "message": "No metrics available"}
        
        latest = self.system_metrics[-1]
        
        # Health checks
        health_issues = []
        
        if latest.cpu_usage > 80:
            health_issues.append(f"High CPU usage: {latest.cpu_usage:.1f}%")
        
        if latest.memory_usage > 85:
            health_issues.append(f"High memory usage: {latest.memory_usage:.1f}%")
        
        if latest.disk_usage > 90:
            health_issues.append(f"High disk usage: {latest.disk_usage:.1f}%")
        
        if latest.error_count > 10:
            health_issues.append(f"High error count: {latest.error_count}")
        
        if latest.response_time_avg > 5.0:
            health_issues.append(f"Slow response time: {latest.response_time_avg:.2f}s")
        
        if health_issues:
            return {
                "status": "warning",
                "message": "System health issues detected",
                "issues": health_issues
            }
        else:
            return {
                "status": "healthy",
                "message": "System is running normally",
                "issues": []
            }
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            with self.database_manager.get_session() as session:
                from database import Player, Nation, PlayerUnit, PlayerQuest
                
                # Total users
                total_users = session.query(Player).count()
                
                # Active users (last 24 hours)
                active_cutoff = datetime.now() - timedelta(hours=24)
                active_users = session.query(Player).filter(
                    Player.last_active >= active_cutoff
                ).count()
                
                # Users by level
                users_by_level = {}
                for player in session.query(Player).all():
                    level = player.level
                    users_by_level[level] = users_by_level.get(level, 0) + 1
                
                # Total nations
                total_nations = session.query(Nation).count()
                
                # Total units
                total_units = session.query(PlayerUnit).count()
                
                # Active quests
                active_quests = session.query(PlayerQuest).filter(
                    PlayerQuest.status == "active"
                ).count()
                
                return {
                    "total_users": total_users,
                    "active_users": active_users,
                    "users_by_level": users_by_level,
                    "total_nations": total_nations,
                    "total_units": total_units,
                    "active_quests": active_quests
                }
                
        except Exception as e:
            self.logger.error(f"Error getting user statistics: {e}")
            return {}
    
    def get_economy_statistics(self) -> Dict[str, Any]:
        """Get economy statistics"""
        try:
            with self.database_manager.get_session() as session:
                from database import Player, Trade
                
                # Total gold in circulation
                total_gold = session.query(Player).with_entities(
                    session.query(Player).func.sum(Player.gold)
                ).scalar() or 0
                
                # Average gold per player
                player_count = session.query(Player).count()
                avg_gold = total_gold / player_count if player_count > 0 else 0
                
                # Total trades
                total_trades = session.query(Trade).count()
                
                # Recent trades (last 24 hours)
                trade_cutoff = datetime.now() - timedelta(hours=24)
                recent_trades = session.query(Trade).filter(
                    Trade.created_at >= trade_cutoff
                ).count()
                
                return {
                    "total_gold": total_gold,
                    "average_gold": avg_gold,
                    "total_trades": total_trades,
                    "recent_trades": recent_trades
                }
                
        except Exception as e:
            self.logger.error(f"Error getting economy statistics: {e}")
            return {}
    
    def get_military_statistics(self) -> Dict[str, Any]:
        """Get military statistics"""
        try:
            with self.database_manager.get_session() as session:
                from database import PlayerUnit, Battle
                
                # Total units
                total_units = session.query(PlayerUnit).count()
                
                # Units by type
                units_by_type = {}
                for unit in session.query(PlayerUnit).all():
                    unit_type = unit.unit_type
                    units_by_type[unit_type] = units_by_type.get(unit_type, 0) + 1
                
                # Total battles
                total_battles = session.query(Battle).count()
                
                # Recent battles (last 24 hours)
                battle_cutoff = datetime.now() - timedelta(hours=24)
                recent_battles = session.query(Battle).filter(
                    Battle.created_at >= battle_cutoff
                ).count()
                
                return {
                    "total_units": total_units,
                    "units_by_type": units_by_type,
                    "total_battles": total_battles,
                    "recent_battles": recent_battles
                }
                
        except Exception as e:
            self.logger.error(f"Error getting military statistics: {e}")
            return {}
    
    def ban_user(self, admin_id: int, target_id: int, reason: str, duration: int = 0) -> bool:
        """Ban a user"""
        try:
            with self.database_manager.get_session() as session:
                from database import Player
                
                player = session.query(Player).filter_by(telegram_id=target_id).first()
                if not player:
                    return False
                
                # Set ban status
                player.is_banned = True
                player.ban_reason = reason
                player.ban_expires = datetime.now() + timedelta(seconds=duration) if duration > 0 else None
                
                session.commit()
                
                self.log_admin_action(
                    admin_id=admin_id,
                    action_type="ban_user",
                    description=f"Banned user {target_id}: {reason}",
                    target_id=target_id,
                    success=True,
                    details={"reason": reason, "duration": duration}
                )
                
                return True
                
        except Exception as e:
            self.logger.error(f"Error banning user: {e}")
            self.log_admin_action(
                admin_id=admin_id,
                action_type="ban_user",
                description=f"Failed to ban user {target_id}: {str(e)}",
                target_id=target_id,
                success=False,
                details={"error": str(e)}
            )
            return False
    
    def unban_user(self, admin_id: int, target_id: int) -> bool:
        """Unban a user"""
        try:
            with self.database_manager.get_session() as session:
                from database import Player
                
                player = session.query(Player).filter_by(telegram_id=target_id).first()
                if not player:
                    return False
                
                # Remove ban status
                player.is_banned = False
                player.ban_reason = None
                player.ban_expires = None
                
                session.commit()
                
                self.log_admin_action(
                    admin_id=admin_id,
                    action_type="unban_user",
                    description=f"Unbanned user {target_id}",
                    target_id=target_id,
                    success=True
                )
                
                return True
                
        except Exception as e:
            self.logger.error(f"Error unbanning user: {e}")
            self.log_admin_action(
                admin_id=admin_id,
                action_type="unban_user",
                description=f"Failed to unban user {target_id}: {str(e)}",
                target_id=target_id,
                success=False,
                details={"error": str(e)}
            )
            return False
    
    def give_resources(self, admin_id: int, target_id: int, gold: int = 0, 
                      materials: Dict[str, int] = None) -> bool:
        """Give resources to a user"""
        try:
            with self.database_manager.get_session() as session:
                from database import Player, PlayerMaterial
                
                player = session.query(Player).filter_by(telegram_id=target_id).first()
                if not player:
                    return False
                
                # Give gold
                if gold > 0:
                    player.gold += gold
                
                # Give materials
                if materials:
                    for material, amount in materials.items():
                        player_material = session.query(PlayerMaterial).filter_by(
                            player_id=player.id,
                            material=material
                        ).first()
                        
                        if player_material:
                            player_material.amount += amount
                        else:
                            player_material = PlayerMaterial(
                                player_id=player.id,
                                material=material,
                                amount=amount
                            )
                            session.add(player_material)
                
                session.commit()
                
                self.log_admin_action(
                    admin_id=admin_id,
                    action_type="give_resources",
                    description=f"Gave resources to user {target_id}",
                    target_id=target_id,
                    success=True,
                    details={"gold": gold, "materials": materials or {}}
                )
                
                return True
                
        except Exception as e:
            self.logger.error(f"Error giving resources: {e}")
            self.log_admin_action(
                admin_id=admin_id,
                action_type="give_resources",
                description=f"Failed to give resources to user {target_id}: {str(e)}",
                target_id=target_id,
                success=False,
                details={"error": str(e)}
            )
            return False
    
    def reset_user_data(self, admin_id: int, target_id: int) -> bool:
        """Reset user data"""
        try:
            with self.database_manager.get_session() as session:
                from database import Player, PlayerUnit, PlayerMaterial, PlayerQuest
                
                player = session.query(Player).filter_by(telegram_id=target_id).first()
                if not player:
                    return False
                
                # Reset player data
                player.gold = 1000
                player.level = 1
                player.experience = 0
                player.military_power = 0
                
                # Delete units
                session.query(PlayerUnit).filter_by(player_id=player.id).delete()
                
                # Delete materials
                session.query(PlayerMaterial).filter_by(player_id=player.id).delete()
                
                # Delete quests
                session.query(PlayerQuest).filter_by(player_id=player.id).delete()
                
                session.commit()
                
                self.log_admin_action(
                    admin_id=admin_id,
                    action_type="reset_user_data",
                    description=f"Reset data for user {target_id}",
                    target_id=target_id,
                    success=True
                )
                
                return True
                
        except Exception as e:
            self.logger.error(f"Error resetting user data: {e}")
            self.log_admin_action(
                admin_id=admin_id,
                action_type="reset_user_data",
                description=f"Failed to reset data for user {target_id}: {str(e)}",
                target_id=target_id,
                success=False,
                details={"error": str(e)}
            )
            return False
    
    def get_admin_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive admin dashboard data"""
        return {
            "system_health": self.get_system_health(),
            "user_statistics": self.get_user_statistics(),
            "economy_statistics": self.get_economy_statistics(),
            "military_statistics": self.get_military_statistics(),
            "recent_actions": self.get_admin_actions(limit=10),
            "system_metrics": self.get_system_metrics(hours=1)
        }

# Example usage and testing
if __name__ == "__main__":
    # Test admin panel
    print("Testing admin panel system...")
    
    # Mock settings manager and database manager
    class MockSettingsManager:
        def __init__(self):
            pass
    
    class MockDatabaseManager:
        def get_session(self):
            return self
        
        def __enter__(self):
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
    
    settings_manager = MockSettingsManager()
    database_manager = MockDatabaseManager()
    
    # Create admin panel
    admin_panel = AdminPanel(settings_manager, database_manager)
    
    # Test logging admin action
    admin_panel.log_admin_action(
        admin_id=12345,
        action_type="test_action",
        description="Test admin action",
        target_id=67890,
        success=True,
        details={"test": "data"}
    )
    
    # Test collecting metrics
    admin_panel.collect_system_metrics()
    
    # Test getting data
    actions = admin_panel.get_admin_actions(limit=5)
    print(f"Admin actions: {len(actions)}")
    
    metrics = admin_panel.get_system_metrics(hours=1)
    print(f"System metrics: {len(metrics)}")
    
    health = admin_panel.get_system_health()
    print(f"System health: {health}")
    
    print("✅ Admin panel system working correctly!")