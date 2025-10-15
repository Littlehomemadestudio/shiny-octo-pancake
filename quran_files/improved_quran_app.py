import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import json
import os
import sqlite3
import logging
from PIL import Image, ImageTk
import random
import threading
import time
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quran_app.log'),
        logging.StreamHandler()
    ]
)

class DatabaseManager:
    """Handles all database operations for the Quran app"""
    
    def __init__(self, db_path: str = "quran_app.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                current_page INTEGER DEFAULT 1,
                streak INTEGER DEFAULT 0,
                points INTEGER DEFAULT 0,
                last_read_date TEXT,
                total_reading_time INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Reading sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reading_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_number INTEGER,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration_seconds INTEGER,
                points_earned INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bookmarks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_number INTEGER,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chat messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Achievements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT,
                points_required INTEGER,
                unlocked_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully")
    
    def get_user_data(self) -> Dict:
        """Get user data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'current_page': row[1],
                'streak': row[2],
                'points': row[3],
                'last_read_date': row[4],
                'total_reading_time': row[5]
            }
        return {}
    
    def save_user_data(self, data: Dict):
        """Save user data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user data exists
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        
        if count > 0:
            cursor.execute('''
                UPDATE user_data SET 
                current_page = ?, streak = ?, points = ?, 
                last_read_date = ?, total_reading_time = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = (SELECT id FROM user_data ORDER BY id DESC LIMIT 1)
            ''', (data['current_page'], data['streak'], data['points'], 
                  data['last_read_date'], data['total_reading_time']))
        else:
            cursor.execute('''
                INSERT INTO user_data (current_page, streak, points, last_read_date, total_reading_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['current_page'], data['streak'], data['points'], 
                  data['last_read_date'], data['total_reading_time']))
        
        conn.commit()
        conn.close()
        logging.info("User data saved successfully")
    
    def add_reading_session(self, page_number: int, duration: int, points: int):
        """Add a reading session to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reading_sessions (page_number, start_time, end_time, duration_seconds, points_earned)
            VALUES (?, datetime('now', '-{} seconds'), datetime('now'), ?, ?)
        '''.format(duration), (page_number, duration, points))
        conn.commit()
        conn.close()
    
    def get_reading_stats(self) -> Dict:
        """Get reading statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total reading time
        cursor.execute("SELECT SUM(duration_seconds) FROM reading_sessions")
        total_time = cursor.fetchone()[0] or 0
        
        # Sessions this week
        cursor.execute('''
            SELECT COUNT(*) FROM reading_sessions 
            WHERE created_at >= datetime('now', '-7 days')
        ''')
        weekly_sessions = cursor.fetchone()[0]
        
        # Pages read this month
        cursor.execute('''
            SELECT COUNT(DISTINCT page_number) FROM reading_sessions 
            WHERE created_at >= datetime('now', '-30 days')
        ''')
        monthly_pages = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_time': total_time,
            'weekly_sessions': weekly_sessions,
            'monthly_pages': monthly_pages
        }
    
    def add_bookmark(self, page_number: int, note: str = ""):
        """Add a bookmark"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookmarks (page_number, note) VALUES (?, ?)
        ''', (page_number, note))
        conn.commit()
        conn.close()
    
    def get_bookmarks(self) -> List[Tuple]:
        """Get all bookmarks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT page_number, note, created_at FROM bookmarks 
            ORDER BY created_at DESC
        ''')
        bookmarks = cursor.fetchall()
        conn.close()
        return bookmarks
    
    def save_chat_message(self, username: str, message: str):
        """Save chat message"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chat_messages (username, message) VALUES (?, ?)
        ''', (username, message))
        conn.commit()
        conn.close()
    
    def get_chat_messages(self, limit: int = 50) -> List[Tuple]:
        """Get recent chat messages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT username, message, created_at FROM chat_messages 
            ORDER BY created_at DESC LIMIT ?
        ''', (limit,))
        messages = cursor.fetchall()
        conn.close()
        return messages

class AchievementSystem:
    """Handles achievement tracking and unlocking"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.achievements = {
            'first_page': {'name': 'First Steps', 'description': 'Read your first page', 'points_required': 0},
            'week_streak': {'name': 'Weekly Warrior', 'description': 'Maintain a 7-day reading streak', 'points_required': 0},
            'month_streak': {'name': 'Monthly Master', 'description': 'Maintain a 30-day reading streak', 'points_required': 0},
            'hundred_pages': {'name': 'Century Reader', 'description': 'Read 100 pages', 'points_required': 0},
            'five_hundred_pages': {'name': 'Halfway Hero', 'description': 'Read 500 pages', 'points_required': 0},
            'quran_complete': {'name': 'Quran Master', 'description': 'Complete the entire Quran', 'points_required': 0},
            'time_master': {'name': 'Time Master', 'description': 'Spend 100 hours reading', 'points_required': 0}
        }
        self.init_achievements()
    
    def init_achievements(self):
        """Initialize achievements in database"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        for achievement_id, achievement in self.achievements.items():
            cursor.execute('''
                INSERT OR IGNORE INTO achievements (name, description, points_required)
                VALUES (?, ?, ?)
            ''', (achievement['name'], achievement['description'], achievement['points_required']))
        
        conn.commit()
        conn.close()
    
    def check_achievements(self, user_data: Dict, reading_stats: Dict) -> List[str]:
        """Check and unlock new achievements"""
        unlocked = []
        
        # First page achievement
        if user_data.get('current_page', 0) >= 1:
            if self.unlock_achievement('first_page'):
                unlocked.append('First Steps')
        
        # Streak achievements
        if user_data.get('streak', 0) >= 7:
            if self.unlock_achievement('week_streak'):
                unlocked.append('Weekly Warrior')
        
        if user_data.get('streak', 0) >= 30:
            if self.unlock_achievement('month_streak'):
                unlocked.append('Monthly Master')
        
        # Page count achievements
        if user_data.get('current_page', 0) >= 100:
            if self.unlock_achievement('hundred_pages'):
                unlocked.append('Century Reader')
        
        if user_data.get('current_page', 0) >= 500:
            if self.unlock_achievement('five_hundred_pages'):
                unlocked.append('Halfway Hero')
        
        if user_data.get('current_page', 0) >= 604:
            if self.unlock_achievement('quran_complete'):
                unlocked.append('Quran Master')
        
        # Time achievement (100 hours = 360000 seconds)
        if reading_stats.get('total_time', 0) >= 360000:
            if self.unlock_achievement('time_master'):
                unlocked.append('Time Master')
        
        return unlocked
    
    def unlock_achievement(self, achievement_id: str) -> bool:
        """Unlock an achievement if not already unlocked"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        # Check if already unlocked
        cursor.execute('''
            SELECT unlocked_at FROM achievements WHERE name = ?
        ''', (self.achievements[achievement_id]['name'],))
        result = cursor.fetchone()
        
        if result and result[0]:
            conn.close()
            return False
        
        # Unlock achievement
        cursor.execute('''
            UPDATE achievements SET unlocked_at = CURRENT_TIMESTAMP 
            WHERE name = ?
        ''', (self.achievements[achievement_id]['name'],))
        
        conn.commit()
        conn.close()
        return True

class QuranApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quran Reader - Enhanced Daily Reading App")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f8ff')
        
        # Initialize database and systems
        self.db_manager = DatabaseManager()
        self.achievement_system = AchievementSystem(self.db_manager)
        
        # Load user data
        self.user_data = self.db_manager.get_user_data()
        self.current_page = self.user_data.get('current_page', 1)
        self.total_pages = 604
        self.streak = self.user_data.get('streak', 0)
        self.points = self.user_data.get('points', 0)
        self.last_read_date = self.user_data.get('last_read_date')
        self.total_reading_time = self.user_data.get('total_reading_time', 0)
        
        # Timer variables
        self.reading_time = 0
        self.timer_running = False
        self.session_start_time = None
        
        # Settings
        self.settings = self.load_settings()
        
        # Create GUI
        self.create_widgets()
        
        # Check streak and achievements
        self.check_streak()
        self.check_achievements()
        
        # Update display
        self.update_display()
        
        # Load chat history
        self.load_chat_history()
        
        logging.info("Quran App initialized successfully")
    
    def load_settings(self) -> Dict:
        """Load user settings"""
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'username': 'User' + str(random.randint(100, 999)),
                'theme': 'light',
                'font_size': 14,
                'auto_save': True,
                'reading_goal': 1  # pages per day
            }
    
    def save_settings(self):
        """Save user settings"""
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)
    
    def create_widgets(self):
        """Create the main GUI"""
        # Create main container with scrollbar
        main_container = tk.Frame(self.root, bg='#f0f8ff')
        main_container.pack(fill='both', expand=True)
        
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(main_container, bg='#f0f8ff')
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f8ff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        self.create_header(scrollable_frame)
        
        # Main content area
        self.create_main_content(scrollable_frame)
        
        # Statistics panel
        self.create_statistics_panel(scrollable_frame)
        
        # Chat area
        self.create_chat_area(scrollable_frame)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg='#2e7d32', height=100)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        # Title and subtitle
        title_frame = tk.Frame(header_frame, bg='#2e7d32')
        title_frame.pack(side='left', padx=20, pady=10)
        
        title_label = tk.Label(title_frame, text="Quran Reader", 
                              font=('Arial', 28, 'bold'), fg='white', bg='#2e7d32')
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_frame, text="Enhanced Daily Reading Experience", 
                                 font=('Arial', 12), fg='#e8f5e8', bg='#2e7d32')
        subtitle_label.pack(anchor='w')
        
        # User stats
        stats_frame = tk.Frame(header_frame, bg='#2e7d32')
        stats_frame.pack(side='right', padx=20, pady=10)
        
        self.streak_label = tk.Label(stats_frame, text=f"Streak: {self.streak} days", 
                                    font=('Arial', 14, 'bold'), fg='white', bg='#2e7d32')
        self.streak_label.pack(anchor='e')
        
        self.points_label = tk.Label(stats_frame, text=f"Points: {self.points}", 
                                    font=('Arial', 14, 'bold'), fg='white', bg='#2e7d32')
        self.points_label.pack(anchor='e')
        
        # Settings button
        settings_button = tk.Button(stats_frame, text="⚙️", font=('Arial', 16),
                                   bg='#4caf50', fg='white', command=self.open_settings,
                                   width=3, height=1)
        settings_button.pack(anchor='e', pady=(5, 0))
    
    def create_main_content(self, parent):
        """Create the main content area"""
        main_frame = tk.Frame(parent, bg='#f0f8ff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Quran page display
        page_frame = tk.Frame(main_frame, bg='#f5f5f5', relief='raised', bd=3)
        page_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Page header
        page_header = tk.Frame(page_frame, bg='#e8f5e8', height=50)
        page_header.pack(fill='x')
        page_header.pack_propagate(False)
        
        self.page_label = tk.Label(page_header, text=f"Page {self.current_page} of {self.total_pages}", 
                                  font=('Arial', 18, 'bold'), bg='#e8f5e8', fg='#2e7d32')
        self.page_label.pack(pady=10)
        
        # Page content
        content_frame = tk.Frame(page_frame, bg='#f5f5f5')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.content_label = tk.Label(content_frame, 
                                     text="[Quran Page Content Would Appear Here]\n\nIn a real implementation, this would display the actual Quran text with proper Arabic formatting, verse numbers, and beautiful typography.",
                                     font=('Arial', 16), bg='#f5f5f5', fg='#333333', 
                                     justify='center', wraplength=800)
        self.content_label.pack(expand=True, fill='both')
        
        # Reading timer and controls
        self.create_reading_controls(main_frame)
        
        # Progress section
        self.create_progress_section(main_frame)
    
    def create_reading_controls(self, parent):
        """Create reading timer and control buttons"""
        controls_frame = tk.Frame(parent, bg='#f0f8ff')
        controls_frame.pack(fill='x', pady=15)
        
        # Timer display
        timer_frame = tk.Frame(controls_frame, bg='#f0f8ff')
        timer_frame.pack(pady=10)
        
        self.timer_label = tk.Label(timer_frame, text="Reading Time: 00:00", 
                                   font=('Arial', 16, 'bold'), bg='#f0f8ff', fg='#2e7d32')
        self.timer_label.pack()
        
        # Control buttons
        button_frame = tk.Frame(controls_frame, bg='#f0f8ff')
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(button_frame, text="Start Reading", 
                                     font=('Arial', 14, 'bold'), bg='#4caf50', fg='white',
                                     command=self.start_reading, width=18, height=2)
        self.start_button.pack(side='left', padx=(0, 10))
        
        self.next_button = tk.Button(button_frame, text="Next Page", 
                                    font=('Arial', 14, 'bold'), bg='#2196f3', fg='white',
                                    command=self.next_page, width=18, height=2, state='disabled')
        self.next_button.pack(side='left', padx=(0, 10))
        
        self.bookmark_button = tk.Button(button_frame, text="Bookmark", 
                                        font=('Arial', 14, 'bold'), bg='#ff9800', fg='white',
                                        command=self.add_bookmark, width=18, height=2)
        self.bookmark_button.pack(side='left', padx=(0, 10))
        
        self.stats_button = tk.Button(button_frame, text="Statistics", 
                                     font=('Arial', 14, 'bold'), bg='#9c27b0', fg='white',
                                     command=self.show_statistics, width=18, height=2)
        self.stats_button.pack(side='left')
    
    def create_progress_section(self, parent):
        """Create progress tracking section"""
        progress_frame = tk.Frame(parent, bg='#f0f8ff')
        progress_frame.pack(fill='x', pady=15)
        
        # Progress info
        self.progress_label = tk.Label(progress_frame, 
                                      text=f"Progress: {self.current_page}/{self.total_pages} pages ({self.current_page/self.total_pages*100:.1f}%)", 
                                      font=('Arial', 14, 'bold'), bg='#f0f8ff', fg='#2e7d32')
        self.progress_label.pack(pady=5)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', 
                                           length=800, mode='determinate',
                                           maximum=self.total_pages)
        self.progress_bar.pack(pady=5)
        self.progress_bar['value'] = self.current_page
        
        # Daily goal progress
        goal_frame = tk.Frame(progress_frame, bg='#f0f8ff')
        goal_frame.pack(pady=10)
        
        self.goal_label = tk.Label(goal_frame, 
                                  text=f"Daily Goal: 0/{self.settings.get('reading_goal', 1)} pages", 
                                  font=('Arial', 12), bg='#f0f8ff', fg='#666666')
        self.goal_label.pack()
        
        self.goal_progress = ttk.Progressbar(goal_frame, orient='horizontal', 
                                            length=400, mode='determinate',
                                            maximum=self.settings.get('reading_goal', 1))
        self.goal_progress.pack(pady=5)
    
    def create_statistics_panel(self, parent):
        """Create statistics and achievements panel"""
        stats_panel = tk.Frame(parent, bg='#e8f5e9', relief='raised', bd=2)
        stats_panel.pack(fill='x', pady=15)
        
        # Panel header
        stats_header = tk.Frame(stats_panel, bg='#4caf50', height=40)
        stats_header.pack(fill='x')
        stats_header.pack_propagate(False)
        
        stats_title = tk.Label(stats_header, text="📊 Reading Statistics & Achievements", 
                              font=('Arial', 16, 'bold'), fg='white', bg='#4caf50')
        stats_title.pack(pady=8)
        
        # Stats content
        stats_content = tk.Frame(stats_panel, bg='#e8f5e9')
        stats_content.pack(fill='x', padx=20, pady=15)
        
        # Create stats grid
        stats_grid = tk.Frame(stats_content, bg='#e8f5e9')
        stats_grid.pack(fill='x')
        
        # Get reading statistics
        reading_stats = self.db_manager.get_reading_stats()
        
        # Stats labels
        stats_data = [
            ("Total Reading Time", f"{reading_stats['total_time'] // 3600}h {(reading_stats['total_time'] % 3600) // 60}m"),
            ("Weekly Sessions", str(reading_stats['weekly_sessions'])),
            ("Monthly Pages", str(reading_stats['monthly_pages'])),
            ("Current Streak", f"{self.streak} days"),
            ("Total Points", str(self.points)),
            ("Pages Read", f"{self.current_page - 1}")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            row = i // 3
            col = i % 3
            
            stat_frame = tk.Frame(stats_grid, bg='white', relief='raised', bd=1)
            stat_frame.grid(row=row, column=col, padx=10, pady=5, sticky='ew')
            
            tk.Label(stat_frame, text=label, font=('Arial', 10), 
                   bg='white', fg='#666666').pack()
            tk.Label(stat_frame, text=value, font=('Arial', 14, 'bold'), 
                   bg='white', fg='#2e7d32').pack()
        
        # Configure grid weights
        for i in range(3):
            stats_grid.columnconfigure(i, weight=1)
    
    def create_chat_area(self, parent):
        """Create the chat area"""
        chat_frame = tk.Frame(parent, bg='#e8f5e9', relief='raised', bd=2)
        chat_frame.pack(fill='both', expand=True, pady=15)
        
        # Chat header
        chat_header = tk.Frame(chat_frame, bg='#4caf50', height=40)
        chat_header.pack(fill='x')
        chat_header.pack_propagate(False)
        
        chat_title = tk.Label(chat_header, text="💬 Community Chat", 
                             font=('Arial', 16, 'bold'), fg='white', bg='#4caf50')
        chat_title.pack(pady=8)
        
        # Chat display
        chat_display_frame = tk.Frame(chat_frame, bg='#e8f5e9')
        chat_display_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.chat_display = tk.Text(chat_display_frame, height=8, font=('Arial', 11), 
                                   bg='white', state='disabled', wrap='word')
        self.chat_display.pack(fill='both', expand=True)
        
        # Chat input
        chat_input_frame = tk.Frame(chat_frame, bg='#e8f5e9')
        chat_input_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.chat_entry = tk.Entry(chat_input_frame, font=('Arial', 12), width=50)
        self.chat_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.chat_entry.bind('<Return>', self.send_chat_message)
        
        chat_send_button = tk.Button(chat_input_frame, text="Send", font=('Arial', 12, 'bold'),
                                    bg='#4caf50', fg='white', command=self.send_chat_message,
                                    width=10)
        chat_send_button.pack(side='right')
    
    def start_reading(self):
        """Start or pause reading session"""
        if not self.timer_running:
            self.timer_running = True
            self.session_start_time = time.time()
            self.start_button.config(text="Pause Reading", bg='#ff9800')
            self.update_timer()
            logging.info("Reading session started")
        else:
            self.timer_running = False
            self.start_button.config(text="Resume Reading", bg='#4caf50')
            logging.info("Reading session paused")
    
    def update_timer(self):
        """Update the reading timer"""
        if self.timer_running:
            self.reading_time += 1
            minutes = self.reading_time // 60
            seconds = self.reading_time % 60
            self.timer_label.config(text=f"Reading Time: {minutes:02d}:{seconds:02d}")
            
            # Enable next page button after 5 minutes (300 seconds) instead of 15
            if self.reading_time >= 300:
                self.next_button.config(state='normal')
            
            # Schedule the next update
            self.root.after(1000, self.update_timer)
    
    def next_page(self):
        """Move to the next page"""
        if self.current_page < self.total_pages:
            # Calculate session duration and points
            session_duration = self.reading_time
            points_earned = min(20, max(10, session_duration // 60 * 2))  # 10-20 points based on time
            
            # Add reading session to database
            self.db_manager.add_reading_session(self.current_page, session_duration, points_earned)
            
            # Update user data
            self.current_page += 1
            self.points += points_earned
            self.total_reading_time += session_duration
            
            # Update display
            self.update_display()
            
            # Reset timer
            self.timer_running = False
            self.reading_time = 0
            self.timer_label.config(text="Reading Time: 00:00")
            self.start_button.config(text="Start Reading", bg='#4caf50')
            self.next_button.config(state='disabled')
            
            # Save user data
            self.save_user_data()
            
            # Check for achievements
            self.check_achievements()
            
            logging.info(f"Advanced to page {self.current_page}, earned {points_earned} points")
        else:
            messagebox.showinfo("Congratulations!", 
                              "🎉 You've completed the entire Quran! May Allah accept your efforts.")
    
    def add_bookmark(self):
        """Add a bookmark for the current page"""
        note = simpledialog.askstring("Add Bookmark", 
                                     f"Add a note for page {self.current_page} (optional):")
        if note is not None:  # User didn't cancel
            self.db_manager.add_bookmark(self.current_page, note or "")
            messagebox.showinfo("Bookmark Added", f"Page {self.current_page} has been bookmarked!")
            logging.info(f"Bookmark added for page {self.current_page}")
    
    def show_statistics(self):
        """Show detailed statistics window"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Detailed Statistics")
        stats_window.geometry("600x500")
        stats_window.configure(bg='#f0f8ff')
        
        # Get comprehensive stats
        reading_stats = self.db_manager.get_reading_stats()
        bookmarks = self.db_manager.get_bookmarks()
        
        # Create scrollable frame
        canvas = tk.Canvas(stats_window, bg='#f0f8ff')
        scrollbar = ttk.Scrollbar(stats_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f8ff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Statistics content
        tk.Label(scrollable_frame, text="📊 Detailed Statistics", 
                font=('Arial', 20, 'bold'), bg='#f0f8ff', fg='#2e7d32').pack(pady=20)
        
        # Reading statistics
        stats_frame = tk.Frame(scrollable_frame, bg='#e8f5e9', relief='raised', bd=2)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(stats_frame, text="Reading Statistics", 
                font=('Arial', 16, 'bold'), bg='#e8f5e9', fg='#2e7d32').pack(pady=10)
        
        stats_data = [
            ("Total Reading Time", f"{reading_stats['total_time'] // 3600} hours {(reading_stats['total_time'] % 3600) // 60} minutes"),
            ("Current Page", f"{self.current_page} of {self.total_pages}"),
            ("Pages Read", f"{self.current_page - 1}"),
            ("Completion Percentage", f"{(self.current_page - 1) / self.total_pages * 100:.1f}%"),
            ("Current Streak", f"{self.streak} days"),
            ("Total Points", f"{self.points}"),
            ("Weekly Sessions", f"{reading_stats['weekly_sessions']}"),
            ("Monthly Pages", f"{reading_stats['monthly_pages']}")
        ]
        
        for label, value in stats_data:
            stat_row = tk.Frame(stats_frame, bg='#e8f5e9')
            stat_row.pack(fill='x', padx=10, pady=2)
            
            tk.Label(stat_row, text=label, font=('Arial', 12), 
                   bg='#e8f5e9', fg='#333333', width=20, anchor='w').pack(side='left')
            tk.Label(stat_row, text=value, font=('Arial', 12, 'bold'), 
                   bg='#e8f5e9', fg='#2e7d32').pack(side='right')
        
        # Bookmarks section
        if bookmarks:
            bookmarks_frame = tk.Frame(scrollable_frame, bg='#e8f5e9', relief='raised', bd=2)
            bookmarks_frame.pack(fill='x', padx=20, pady=10)
            
            tk.Label(bookmarks_frame, text="📚 Bookmarks", 
                    font=('Arial', 16, 'bold'), bg='#e8f5e9', fg='#2e7d32').pack(pady=10)
            
            for page, note, created_at in bookmarks[:10]:  # Show last 10 bookmarks
                bookmark_row = tk.Frame(bookmarks_frame, bg='#e8f5e9')
                bookmark_row.pack(fill='x', padx=10, pady=2)
                
                tk.Label(bookmark_row, text=f"Page {page}", font=('Arial', 12, 'bold'), 
                       bg='#e8f5e9', fg='#2e7d32').pack(side='left')
                if note:
                    tk.Label(bookmark_row, text=f"- {note}", font=('Arial', 10), 
                           bg='#e8f5e9', fg='#666666').pack(side='left', padx=(5, 0))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg='#f0f8ff')
        
        tk.Label(settings_window, text="⚙️ Settings", 
                font=('Arial', 18, 'bold'), bg='#f0f8ff', fg='#2e7d32').pack(pady=20)
        
        # Username setting
        username_frame = tk.Frame(settings_window, bg='#f0f8ff')
        username_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(username_frame, text="Username:", font=('Arial', 12), 
                bg='#f0f8ff').pack(side='left')
        
        username_entry = tk.Entry(username_frame, font=('Arial', 12))
        username_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        username_entry.insert(0, self.settings.get('username', ''))
        
        # Daily goal setting
        goal_frame = tk.Frame(settings_window, bg='#f0f8ff')
        goal_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(goal_frame, text="Daily Goal (pages):", font=('Arial', 12), 
                bg='#f0f8ff').pack(side='left')
        
        goal_var = tk.StringVar(value=str(self.settings.get('reading_goal', 1)))
        goal_spinbox = tk.Spinbox(goal_frame, from_=1, to=10, textvariable=goal_var, 
                                 font=('Arial', 12), width=10)
        goal_spinbox.pack(side='right')
        
        # Font size setting
        font_frame = tk.Frame(settings_window, bg='#f0f8ff')
        font_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(font_frame, text="Font Size:", font=('Arial', 12), 
                bg='#f0f8ff').pack(side='left')
        
        font_var = tk.StringVar(value=str(self.settings.get('font_size', 14)))
        font_spinbox = tk.Spinbox(font_frame, from_=10, to=20, textvariable=font_var, 
                                 font=('Arial', 12), width=10)
        font_spinbox.pack(side='right')
        
        # Save button
        def save_settings():
            self.settings['username'] = username_entry.get()
            self.settings['reading_goal'] = int(goal_var.get())
            self.settings['font_size'] = int(font_var.get())
            self.save_settings()
            self.update_display()
            settings_window.destroy()
            messagebox.showinfo("Settings Saved", "Your settings have been saved!")
        
        save_button = tk.Button(settings_window, text="Save Settings", 
                               font=('Arial', 12, 'bold'), bg='#4caf50', fg='white',
                               command=save_settings, width=20)
        save_button.pack(pady=20)
    
    def update_display(self):
        """Update the display with current data"""
        self.page_label.config(text=f"Page {self.current_page} of {self.total_pages}")
        self.content_label.config(text=f"[Quran Page Content Would Appear Here]\n\nPage {self.current_page} of the Holy Quran\n\nIn a real implementation, this would display the actual Quran text with proper Arabic formatting, verse numbers, and beautiful typography.")
        
        # Update progress
        progress_percent = (self.current_page / self.total_pages) * 100
        self.progress_label.config(text=f"Progress: {self.current_page}/{self.total_pages} pages ({progress_percent:.1f}%)")
        self.progress_bar['value'] = self.current_page
        
        # Update daily goal progress
        daily_pages = 1  # This would be calculated based on today's reading
        self.goal_label.config(text=f"Daily Goal: {daily_pages}/{self.settings.get('reading_goal', 1)} pages")
        self.goal_progress['value'] = daily_pages
        
        # Update stats
        self.streak_label.config(text=f"Streak: {self.streak} days")
        self.points_label.config(text=f"Points: {self.points}")
    
    def check_streak(self):
        """Check and update reading streak"""
        today = datetime.date.today()
        
        if self.last_read_date:
            last_date = datetime.datetime.strptime(self.last_read_date, "%Y-%m-%d").date()
            delta = today - last_date
            
            if delta.days == 1:
                # Consecutive day
                self.streak += 1
            elif delta.days > 1:
                # Streak broken
                self.streak = 1
            # If same day, streak remains the same
        else:
            # First time reading
            self.streak = 1
        
        # Update last read date to today
        self.last_read_date = today.strftime("%Y-%m-%d")
        self.streak_label.config(text=f"Streak: {self.streak} days")
    
    def check_achievements(self):
        """Check for new achievements"""
        reading_stats = self.db_manager.get_reading_stats()
        unlocked = self.achievement_system.check_achievements(self.user_data, reading_stats)
        
        if unlocked:
            achievement_text = "🏆 New Achievement Unlocked!\n\n" + "\n".join(unlocked)
            messagebox.showinfo("Achievement Unlocked!", achievement_text)
            logging.info(f"Unlocked achievements: {unlocked}")
    
    def send_chat_message(self, event=None):
        """Send a chat message"""
        message = self.chat_entry.get().strip()
        if message:
            username = self.settings.get('username', 'User')
            self.display_chat_message(username, message)
            self.chat_entry.delete(0, tk.END)
            
            # Save message to database
            self.db_manager.save_chat_message(username, message)
            
            # Simulate responses
            self.root.after(1000, self.simulate_chat_response)
    
    def display_chat_message(self, user, message):
        """Display a chat message"""
        self.chat_display.config(state='normal')
        timestamp = datetime.datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"[{timestamp}] {user}: {message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
    
    def simulate_chat_response(self):
        """Simulate chat responses from other users"""
        responses = [
            "MashaAllah! Keep going!",
            "The Quran is a guidance for mankind.",
            "May Allah accept our efforts.",
            f"I'm on page {random.randint(1, 604)} today!",
            "The recitation is so beautiful.",
            "Don't forget to reflect on the meanings.",
            "SubhanAllah, this verse is so profound.",
            "May Allah bless your reading journey.",
            "I love the community aspect of this app!",
            "The daily reminders help me stay consistent."
        ]
        response = random.choice(responses)
        username = f"User{random.randint(100, 999)}"
        self.display_chat_message(username, response)
        self.db_manager.save_chat_message(username, response)
    
    def load_chat_history(self):
        """Load recent chat messages"""
        messages = self.db_manager.get_chat_messages(20)
        for username, message, created_at in reversed(messages):
            self.display_chat_message(username, message)
    
    def save_user_data(self):
        """Save user data to database"""
        data = {
            'current_page': self.current_page,
            'streak': self.streak,
            'points': self.points,
            'last_read_date': self.last_read_date,
            'total_reading_time': self.total_reading_time
        }
        self.db_manager.save_user_data(data)
        self.user_data = data
    
    def on_closing(self):
        """Handle application closing"""
        if self.timer_running:
            # Save current session
            session_duration = self.reading_time
            if session_duration > 0:
                self.db_manager.add_reading_session(self.current_page, session_duration, 0)
        
        self.save_user_data()
        self.save_settings()
        logging.info("Application closing, data saved")
        self.root.destroy()

def main():
    """Main function to run the application"""
    try:
        root = tk.Tk()
        app = QuranApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    except Exception as e:
        logging.error(f"Application error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    main()