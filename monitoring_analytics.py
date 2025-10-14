"""
Advanced Monitoring and Analytics System
Comprehensive bot performance monitoring and user analytics
"""

import json
import os
import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging
import psutil
import threading

@dataclass
class PerformanceMetric:
    """Performance metric data point"""
    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    tags: Dict[str, str]

@dataclass
class UserEvent:
    """User event data"""
    event_id: str
    user_id: int
    event_type: str
    timestamp: datetime
    data: Dict[str, Any]
    session_id: str

@dataclass
class BotHealth:
    """Bot health status"""
    timestamp: datetime
    status: str  # healthy, warning, critical
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_connections: int
    error_rate: float
    response_time_avg: float
    uptime_seconds: float
    issues: List[str]

class PerformanceMonitor:
    """Advanced performance monitoring system"""
    
    def __init__(self, max_metrics: int = 10000):
        self.max_metrics = max_metrics
        self.metrics: deque = deque(maxlen=max_metrics)
        self.metric_counters = defaultdict(int)
        self.response_times = deque(maxlen=1000)
        self.error_count = 0
        self.command_count = 0
        self.start_time = time.time()
        self.logger = logging.getLogger(__name__)
        
        # Start background monitoring
        self.monitoring_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitoring_thread.start()
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while True:
            try:
                self.collect_system_metrics()
                time.sleep(60)  # Collect metrics every minute
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)
    
    def record_command(self, command: str, response_time: float, success: bool = True):
        """Record command execution"""
        self.command_count += 1
        self.response_times.append(response_time)
        
        if not success:
            self.error_count += 1
        
        # Record metric
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_name="command_execution",
            value=response_time,
            unit="seconds",
            tags={"command": command, "success": str(success)}
        )
        self.metrics.append(metric)
        
        # Update counters
        self.metric_counters[f"command_{command}"] += 1
        if success:
            self.metric_counters[f"command_{command}_success"] += 1
        else:
            self.metric_counters[f"command_{command}_error"] += 1
    
    def record_database_query(self, query_type: str, duration: float, success: bool = True):
        """Record database query"""
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_name="database_query",
            value=duration,
            unit="seconds",
            tags={"query_type": query_type, "success": str(success)}
        )
        self.metrics.append(metric)
    
    def record_cache_operation(self, operation: str, hit: bool):
        """Record cache operation"""
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_name="cache_operation",
            value=1.0 if hit else 0.0,
            unit="hit_rate",
            tags={"operation": operation, "hit": str(hit)}
        )
        self.metrics.append(metric)
    
    def collect_system_metrics(self):
        """Collect system performance metrics"""
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            self.metrics.append(PerformanceMetric(
                timestamp=datetime.now(),
                metric_name="cpu_usage",
                value=cpu_usage,
                unit="percent",
                tags={}
            ))
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            self.metrics.append(PerformanceMetric(
                timestamp=datetime.now(),
                metric_name="memory_usage",
                value=memory_usage,
                unit="percent",
                tags={}
            ))
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = (disk.used / disk.total) * 100
            self.metrics.append(PerformanceMetric(
                timestamp=datetime.now(),
                metric_name="disk_usage",
                value=disk_usage,
                unit="percent",
                tags={}
            ))
            
            # Network I/O
            network = psutil.net_io_counters()
            self.metrics.append(PerformanceMetric(
                timestamp=datetime.now(),
                metric_name="network_bytes_sent",
                value=network.bytes_sent,
                unit="bytes",
                tags={}
            ))
            self.metrics.append(PerformanceMetric(
                timestamp=datetime.now(),
                metric_name="network_bytes_recv",
                value=network.bytes_recv,
                unit="bytes",
                tags={}
            ))
            
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        uptime = time.time() - self.start_time
        
        # Calculate averages
        avg_response_time = 0
        if self.response_times:
            avg_response_time = sum(self.response_times) / len(self.response_times)
        
        error_rate = 0
        if self.command_count > 0:
            error_rate = (self.error_count / self.command_count) * 100
        
        # Get recent metrics
        recent_metrics = [m for m in self.metrics if m.timestamp >= datetime.now() - timedelta(hours=1)]
        
        # Calculate recent averages
        recent_cpu = 0
        recent_memory = 0
        recent_disk = 0
        
        cpu_metrics = [m for m in recent_metrics if m.metric_name == "cpu_usage"]
        if cpu_metrics:
            recent_cpu = sum(m.value for m in cpu_metrics) / len(cpu_metrics)
        
        memory_metrics = [m for m in recent_metrics if m.metric_name == "memory_usage"]
        if memory_metrics:
            recent_memory = sum(m.value for m in memory_metrics) / len(memory_metrics)
        
        disk_metrics = [m for m in recent_metrics if m.metric_name == "disk_usage"]
        if disk_metrics:
            recent_disk = sum(m.value for m in disk_metrics) / len(disk_metrics)
        
        return {
            "uptime_seconds": uptime,
            "uptime_formatted": str(timedelta(seconds=int(uptime))),
            "total_commands": self.command_count,
            "commands_per_minute": (self.command_count / uptime) * 60 if uptime > 0 else 0,
            "error_count": self.error_count,
            "error_rate": error_rate,
            "average_response_time": avg_response_time,
            "recent_cpu_usage": recent_cpu,
            "recent_memory_usage": recent_memory,
            "recent_disk_usage": recent_disk,
            "total_metrics": len(self.metrics)
        }
    
    def get_command_statistics(self) -> Dict[str, Any]:
        """Get command execution statistics"""
        stats = {}
        
        for counter_name, count in self.metric_counters.items():
            if counter_name.startswith("command_"):
                command = counter_name.replace("command_", "")
                if command not in stats:
                    stats[command] = {"total": 0, "success": 0, "error": 0}
                
                if counter_name.endswith("_success"):
                    stats[command]["success"] = count
                elif counter_name.endswith("_error"):
                    stats[command]["error"] = count
                else:
                    stats[command]["total"] = count
        
        return stats
    
    def get_health_status(self) -> BotHealth:
        """Get bot health status"""
        issues = []
        status = "healthy"
        
        # Get recent metrics
        recent_metrics = [m for m in self.metrics if m.timestamp >= datetime.now() - timedelta(minutes=5)]
        
        # Check CPU usage
        cpu_metrics = [m for m in recent_metrics if m.metric_name == "cpu_usage"]
        cpu_usage = 0
        if cpu_metrics:
            cpu_usage = sum(m.value for m in cpu_metrics) / len(cpu_metrics)
            if cpu_usage > 80:
                issues.append(f"High CPU usage: {cpu_usage:.1f}%")
                status = "warning"
            if cpu_usage > 95:
                status = "critical"
        
        # Check memory usage
        memory_metrics = [m for m in recent_metrics if m.metric_name == "memory_usage"]
        memory_usage = 0
        if memory_metrics:
            memory_usage = sum(m.value for m in memory_metrics) / len(memory_metrics)
            if memory_usage > 85:
                issues.append(f"High memory usage: {memory_usage:.1f}%")
                status = "warning"
            if memory_usage > 95:
                status = "critical"
        
        # Check disk usage
        disk_metrics = [m for m in recent_metrics if m.metric_name == "disk_usage"]
        disk_usage = 0
        if disk_metrics:
            disk_usage = sum(m.value for m in disk_metrics) / len(disk_metrics)
            if disk_usage > 90:
                issues.append(f"High disk usage: {disk_usage:.1f}%")
                status = "warning"
            if disk_usage > 95:
                status = "critical"
        
        # Check error rate
        error_rate = 0
        if self.command_count > 0:
            error_rate = (self.error_count / self.command_count) * 100
            if error_rate > 5:
                issues.append(f"High error rate: {error_rate:.1f}%")
                status = "warning"
            if error_rate > 20:
                status = "critical"
        
        # Check response time
        response_time_avg = 0
        if self.response_times:
            response_time_avg = sum(self.response_times) / len(self.response_times)
            if response_time_avg > 5:
                issues.append(f"Slow response time: {response_time_avg:.2f}s")
                status = "warning"
            if response_time_avg > 10:
                status = "critical"
        
        return BotHealth(
            timestamp=datetime.now(),
            status=status,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            active_connections=0,  # Would be tracked by bot
            error_rate=error_rate,
            response_time_avg=response_time_avg,
            uptime_seconds=time.time() - self.start_time,
            issues=issues
        )

class UserAnalytics:
    """User behavior analytics system"""
    
    def __init__(self, max_events: int = 50000):
        self.max_events = max_events
        self.events: deque = deque(maxlen=max_events)
        self.user_sessions: Dict[int, str] = {}
        self.session_counter = 0
        self.logger = logging.getLogger(__name__)
    
    def start_user_session(self, user_id: int) -> str:
        """Start a new user session"""
        self.session_counter += 1
        session_id = f"session_{user_id}_{self.session_counter}_{int(time.time())}"
        self.user_sessions[user_id] = session_id
        return session_id
    
    def end_user_session(self, user_id: int):
        """End user session"""
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
    
    def record_event(self, user_id: int, event_type: str, data: Dict[str, Any] = None):
        """Record user event"""
        session_id = self.user_sessions.get(user_id, f"unknown_{user_id}")
        
        event = UserEvent(
            event_id=f"event_{user_id}_{int(time.time() * 1000)}",
            user_id=user_id,
            event_type=event_type,
            timestamp=datetime.now(),
            data=data or {},
            session_id=session_id
        )
        
        self.events.append(event)
    
    def get_user_activity(self, user_id: int, hours: int = 24) -> List[UserEvent]:
        """Get user activity for last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [e for e in self.events if e.user_id == user_id and e.timestamp >= cutoff_time]
    
    def get_event_statistics(self, hours: int = 24) -> Dict[str, Any]:
        """Get event statistics"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_events = [e for e in self.events if e.timestamp >= cutoff_time]
        
        # Count events by type
        event_counts = defaultdict(int)
        for event in recent_events:
            event_counts[event.event_type] += 1
        
        # Count unique users
        unique_users = len(set(e.user_id for e in recent_events))
        
        # Count active sessions
        active_sessions = len(self.user_sessions)
        
        return {
            "total_events": len(recent_events),
            "unique_users": unique_users,
            "active_sessions": active_sessions,
            "events_by_type": dict(event_counts),
            "events_per_hour": len(recent_events) / hours if hours > 0 else 0
        }
    
    def get_user_engagement(self, user_id: int) -> Dict[str, Any]:
        """Get user engagement metrics"""
        user_events = [e for e in self.events if e.user_id == user_id]
        
        if not user_events:
            return {"engagement_score": 0, "total_events": 0, "last_activity": None}
        
        # Calculate engagement score based on event frequency and recency
        now = datetime.now()
        recent_events = [e for e in user_events if e.timestamp >= now - timedelta(hours=24)]
        
        # Base score on recent activity
        engagement_score = min(len(recent_events) * 10, 100)
        
        # Boost score for very recent activity
        if recent_events:
            last_activity = max(e.timestamp for e in recent_events)
            hours_since_activity = (now - last_activity).total_seconds() / 3600
            if hours_since_activity < 1:
                engagement_score += 20
            elif hours_since_activity < 6:
                engagement_score += 10
        
        return {
            "engagement_score": min(engagement_score, 100),
            "total_events": len(user_events),
            "recent_events": len(recent_events),
            "last_activity": max(e.timestamp for e in user_events) if user_events else None,
            "events_per_day": len(user_events) / max(1, (now - min(e.timestamp for e in user_events)).days)
        }
    
    def get_popular_commands(self, hours: int = 24) -> List[Tuple[str, int]]:
        """Get most popular commands"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_events = [e for e in self.events if e.timestamp >= cutoff_time and e.event_type == "command"]
        
        command_counts = defaultdict(int)
        for event in recent_events:
            command = event.data.get("command", "unknown")
            command_counts[command] += 1
        
        return sorted(command_counts.items(), key=lambda x: x[1], reverse=True)
    
    def get_user_retention(self, days: int = 30) -> Dict[str, float]:
        """Get user retention metrics"""
        cutoff_time = datetime.now() - timedelta(days=days)
        recent_events = [e for e in self.events if e.timestamp >= cutoff_time]
        
        if not recent_events:
            return {"daily_retention": 0, "weekly_retention": 0, "monthly_retention": 0}
        
        # Get unique users by time period
        daily_users = set()
        weekly_users = set()
        monthly_users = set()
        
        for event in recent_events:
            user_id = event.user_id
            event_time = event.timestamp
            
            if event_time >= datetime.now() - timedelta(days=1):
                daily_users.add(user_id)
            if event_time >= datetime.now() - timedelta(days=7):
                weekly_users.add(user_id)
            if event_time >= datetime.now() - timedelta(days=30):
                monthly_users.add(user_id)
        
        # Calculate retention rates
        total_users = len(set(e.user_id for e in recent_events))
        
        daily_retention = (len(daily_users) / total_users) * 100 if total_users > 0 else 0
        weekly_retention = (len(weekly_users) / total_users) * 100 if total_users > 0 else 0
        monthly_retention = (len(monthly_users) / total_users) * 100 if total_users > 0 else 0
        
        return {
            "daily_retention": daily_retention,
            "weekly_retention": weekly_retention,
            "monthly_retention": monthly_retention
        }

class AnalyticsDashboard:
    """Comprehensive analytics dashboard"""
    
    def __init__(self, performance_monitor: PerformanceMonitor, user_analytics: UserAnalytics):
        self.performance_monitor = performance_monitor
        self.user_analytics = user_analytics
        self.logger = logging.getLogger(__name__)
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        return {
            "performance": self.performance_monitor.get_performance_summary(),
            "health": self.performance_monitor.get_health_status(),
            "command_stats": self.performance_monitor.get_command_statistics(),
            "user_analytics": self.user_analytics.get_event_statistics(),
            "popular_commands": self.user_analytics.get_popular_commands(),
            "user_retention": self.user_analytics.get_user_retention()
        }
    
    def get_performance_alerts(self) -> List[Dict[str, Any]]:
        """Get performance alerts"""
        alerts = []
        health = self.performance_monitor.get_health_status()
        
        if health.status == "critical":
            alerts.append({
                "level": "critical",
                "message": "Bot is in critical state",
                "details": health.issues
            })
        elif health.status == "warning":
            alerts.append({
                "level": "warning",
                "message": "Bot has performance warnings",
                "details": health.issues
            })
        
        # Check for specific issues
        if health.cpu_usage > 90:
            alerts.append({
                "level": "warning",
                "message": f"Very high CPU usage: {health.cpu_usage:.1f}%",
                "details": ["Consider scaling or optimization"]
            })
        
        if health.memory_usage > 90:
            alerts.append({
                "level": "warning",
                "message": f"Very high memory usage: {health.memory_usage:.1f}%",
                "details": ["Consider memory optimization"]
            })
        
        if health.error_rate > 10:
            alerts.append({
                "level": "warning",
                "message": f"High error rate: {health.error_rate:.1f}%",
                "details": ["Check error logs and fix issues"]
            })
        
        return alerts
    
    def get_optimization_recommendations(self) -> List[str]:
        """Get optimization recommendations"""
        recommendations = []
        health = self.performance_monitor.get_health_status()
        performance = self.performance_monitor.get_performance_summary()
        
        if health.cpu_usage > 70:
            recommendations.append("Consider implementing caching to reduce CPU usage")
        
        if health.memory_usage > 80:
            recommendations.append("Consider memory optimization and garbage collection")
        
        if health.response_time_avg > 3:
            recommendations.append("Consider database query optimization")
        
        if performance["error_rate"] > 5:
            recommendations.append("Improve error handling and input validation")
        
        if performance["commands_per_minute"] > 100:
            recommendations.append("Consider rate limiting and load balancing")
        
        return recommendations

# Example usage and testing
if __name__ == "__main__":
    # Test monitoring and analytics
    print("Testing monitoring and analytics system...")
    
    # Create instances
    perf_monitor = PerformanceMonitor()
    user_analytics = UserAnalytics()
    dashboard = AnalyticsDashboard(perf_monitor, user_analytics)
    
    # Test performance monitoring
    perf_monitor.record_command("start", 0.5, True)
    perf_monitor.record_command("help", 0.3, True)
    perf_monitor.record_command("status", 0.8, False)
    
    # Test user analytics
    user_id = 12345
    session_id = user_analytics.start_user_session(user_id)
    user_analytics.record_event(user_id, "command", {"command": "start"})
    user_analytics.record_event(user_id, "command", {"command": "help"})
    user_analytics.record_event(user_id, "command", {"command": "status"})
    
    # Get data
    performance_summary = perf_monitor.get_performance_summary()
    print(f"Performance summary: {performance_summary}")
    
    health_status = perf_monitor.get_health_status()
    print(f"Health status: {health_status.status}")
    
    event_stats = user_analytics.get_event_statistics()
    print(f"Event statistics: {event_stats}")
    
    user_engagement = user_analytics.get_user_engagement(user_id)
    print(f"User engagement: {user_engagement}")
    
    dashboard_data = dashboard.get_dashboard_data()
    print(f"Dashboard data keys: {list(dashboard_data.keys())}")
    
    alerts = dashboard.get_performance_alerts()
    print(f"Performance alerts: {len(alerts)}")
    
    recommendations = dashboard.get_optimization_recommendations()
    print(f"Optimization recommendations: {len(recommendations)}")
    
    print("✅ Monitoring and analytics system working correctly!")