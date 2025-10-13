import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, simpledialog
import datetime
import json
import os
import sqlite3
import requests
import threading
import time
import logging
from PIL import Image, ImageTk, ImageFont, ImageStat
import random
import re
import numpy as np
from typing import Dict, List, Tuple, Optional

class QuranApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quran Reader Pro - Advanced Islamic Study Platform")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2a2a2a')
        self.root.minsize(1200, 800)
        
        # Modern color scheme with gray background
        self.colors = {
            'primary': '#16213e',
            'secondary': '#0f3460', 
            'accent': '#e94560',
            'success': '#4caf50',
            'warning': '#ff9800',
            'background': '#2a2a2a',  # Gray background
            'surface': '#3a3a3a',     # Lighter gray for surfaces
            'text': '#ffffff',
            'text_secondary': '#b0b0b0',
            'arabic_text': '#2d5a27',
            'arabic_bg': '#f8f9fa'
        }
        
        # Initialize database
        self.init_database()
        
        # User data
        self.user_data = self.load_user_data()
        self.current_page = self.user_data.get('current_page', 1)
        self.current_surah = self.user_data.get('current_surah', 1)
        self.current_ayah = self.user_data.get('current_ayah', 1)
        self.total_pages = 604
        self.streak = self.user_data.get('streak', 0)
        self.points = self.user_data.get('points', 0)
        self.last_read_date = self.user_data.get('last_read_date')
        self.bookmarks = self.user_data.get('bookmarks', [])
        self.notes = self.user_data.get('notes', {})
        self.achievements = self.user_data.get('achievements', [])
        
        # Timer and reading tracking
        self.reading_time = 0
        self.timer_running = False
        self.daily_goal = 30  # minutes
        self.reading_history = self.user_data.get('reading_history', {})
        
        # Dynamic viewing time based on page content analysis
        self.base_viewing_time = 120  # Base 2 minutes
        self.viewing_time_required = self.base_viewing_time
        self.current_page_viewing_time = 0
        self.page_start_time = time.time()
        self.can_advance = False
        self.page_complexity_score = 0.5  # Default complexity (0.5 = normal)
        
        # Page analysis settings
        self.min_reading_time = 60   # Minimum 1 minute
        self.max_reading_time = 300  # Maximum 5 minutes
        self.ink_density_threshold = 0.15  # Threshold for considering text density
        
        # User profile
        self.user_profile = self.user_data.get('user_profile', {
            'username': 'User',
            'bio': 'Quran reader',
            'join_date': datetime.date.today().strftime('%Y-%m-%d'),
            'total_pages_read': 0,
            'total_reading_time': 0,
            'achievements': [],
            'level': 1,
            'experience': 0
        })
        
        # Online sync settings
        self.online_sync_enabled = self.user_data.get('online_sync_enabled', False)
        self.api_endpoint = "https://api.quranreader.com"  # Placeholder API
        self.user_id = self.user_data.get('user_id', None)
        
        # Quran data
        self.quran_data = {}
        self.surah_names = {}
        self.quran_pages_dir = r"C:\Users\Littl\Downloads\quranpages\114"
        self.load_quran_data()
        
        # UI state
        self.dark_mode = self.user_data.get('dark_mode', True)
        self.font_size = self.user_data.get('font_size', 16)
        self.show_arabic = self.user_data.get('show_arabic', True)
        self.show_translation = self.user_data.get('show_translation', True)
        
        # Create modern GUI
        self.create_modern_widgets()
        
        # Initialize viewing time
        self.reset_page_viewing_time()
        
        # Check streak and achievements
        self.check_streak()
        self.check_achievements()
        
        # Update display
        self.update_display()
        
        # Load initial content
        self.load_current_content()
        
    def init_database(self):
        """Initialize SQLite database for Quran data and user progress"""
        self.conn = sqlite3.connect('quran_app.db')
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS quran_verses (
                id INTEGER PRIMARY KEY,
                surah_number INTEGER,
                ayah_number INTEGER,
                arabic_text TEXT,
                translation TEXT,
                page_number INTEGER
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS surah_info (
                surah_number INTEGER PRIMARY KEY,
                name_arabic TEXT,
                name_english TEXT,
                total_ayahs INTEGER,
                revelation_place TEXT
            )
        ''')
        
        self.conn.commit()
    
    def load_quran_data(self):
        """Load Quran data from API or local file"""
        # Sample Quran data structure
        self.surah_names = {
            1: {"name": "", "ayahs": 7, "place": "Makkah"},
            2: {"name": "", "ayahs": 200, "place": "Madinah"},
            4: {"name": "", "ayahs": 176, "place": "Madinah"},
            5: {"name": "", "ayahs": 120, "place": "Madinah"},
        }
        
        # Sample verses for demonstration
        self.quran_data = {
            1: {
                1: {
                    "arabic": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                    "translation": "In the name of Allah, the Entirely Merciful, the Especially Merciful."
                },
                2: {
                    "arabic": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
                    "translation": "[All] praise is [due] to Allah, Lord of the worlds."
                },
                3: {
                    "arabic": "الرَّحْمَٰنِ الرَّحِيمِ",
                    "translation": "The Entirely Merciful, the Especially Merciful."
                }
            }
        }

    def create_modern_widgets(self):
        """Create modern, responsive GUI with advanced features"""
        # Configure style
        self.setup_styles()
        
        # Create main container
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True)
        
        # Create header with modern design
        self.create_header(main_container)
        
        # Create main content area with sidebar
        content_container = tk.Frame(main_container, bg=self.colors['background'])
        content_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left sidebar
        self.create_sidebar(content_container)
        
        # Main reading area
        self.create_reading_area(content_container)
        
        # Right panel for notes and bookmarks
        self.create_right_panel(content_container)
        
        # Status bar
        self.create_status_bar(main_container)

    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Modern.TFrame', background=self.colors['surface'])
        style.configure('Card.TFrame', background=self.colors['surface'], relief='raised', borderwidth=1)
        style.configure('Modern.TButton', 
                       background=self.colors['accent'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        style.configure('Modern.TLabel', 
                       background=self.colors['surface'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10))
        style.configure('Header.TLabel',
                       background=self.colors['primary'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 16, 'bold'))

    def create_header(self, parent):
        """Create modern header with stats and controls"""
        header = tk.Frame(parent, bg=self.colors['primary'], height=80)
        header.pack(fill='x', padx=0, pady=(0, 5))
        header.pack_propagate(False)
        
        # User profile section
        profile_frame = tk.Frame(header, bg=self.colors['primary'])
        profile_frame.pack(side='left', padx=20, pady=15)
        
        # User avatar and info
        avatar_frame = tk.Frame(profile_frame, bg=self.colors['primary'])
        avatar_frame.pack(side='left', padx=(0, 15))
        
        self.avatar_label = tk.Label(avatar_frame, text="👤", 
                                    font=('Segoe UI', 24),
                                    fg=self.colors['text'], bg=self.colors['primary'])
        self.avatar_label.pack()
        
        user_info_frame = tk.Frame(profile_frame, bg=self.colors['primary'])
        user_info_frame.pack(side='left')
        
        self.username_label = tk.Label(user_info_frame, text=self.user_profile['username'], 
                                      font=('Segoe UI', 16, 'bold'),
                                      fg=self.colors['text'], bg=self.colors['primary'])
        self.username_label.pack(anchor='w')
        
        level_info = f"Level {self.user_profile['level']} • {self.user_profile['total_pages_read']} pages read"
        self.level_label = tk.Label(user_info_frame, text=level_info, 
                                   font=('Segoe UI', 10),
                                   fg=self.colors['text_secondary'], bg=self.colors['primary'])
        self.level_label.pack(anchor='w')
        
        # Title section
        title_frame = tk.Frame(header, bg=self.colors['primary'])
        title_frame.pack(side='left', padx=20, pady=15)
        
        title_label = tk.Label(title_frame, text="Quran Reader Pro", 
                              font=('Segoe UI', 18, 'bold'),
                              fg=self.colors['text'], bg=self.colors['primary'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_frame, text="Advanced Islamic Study Platform", 
                                 font=('Segoe UI', 9),
                                 fg=self.colors['text_secondary'], bg=self.colors['primary'])
        subtitle_label.pack(anchor='w')
        
        # Stats panel
        stats_frame = tk.Frame(header, bg=self.colors['primary'])
        stats_frame.pack(side='right', padx=20, pady=10)
        
        # Streak counter
        streak_frame = tk.Frame(stats_frame, bg=self.colors['accent'], relief='raised', bd=2)
        streak_frame.pack(side='right', padx=5)
        
        self.streak_label = tk.Label(streak_frame, text=f"{self.streak}", 
                                    font=('Segoe UI', 18, 'bold'),
                                    fg=self.colors['text'], bg=self.colors['accent'])
        self.streak_label.pack(padx=15, pady=5)
        
        streak_text = tk.Label(streak_frame, text="Day Streak", 
                              font=('Segoe UI', 8),
                              fg=self.colors['text'], bg=self.colors['accent'])
        streak_text.pack()
        
        # Points counter
        points_frame = tk.Frame(stats_frame, bg=self.colors['success'], relief='raised', bd=2)
        points_frame.pack(side='right', padx=5)
        
        self.points_label = tk.Label(points_frame, text=f"{self.points}", 
                                    font=('Segoe UI', 18, 'bold'),
                                    fg=self.colors['text'], bg=self.colors['success'])
        self.points_label.pack(padx=15, pady=5)
        
        points_text = tk.Label(points_frame, text="Points", 
                              font=('Segoe UI', 8),
                              fg=self.colors['text'], bg=self.colors['success'])
        points_text.pack()
        
        # Control buttons
        controls_frame = tk.Frame(header, bg=self.colors['primary'])
        controls_frame.pack(side='right', padx=10, pady=20)
        
        leaderboard_btn = tk.Button(controls_frame, text="🏆", font=('Segoe UI', 14),
                                   bg=self.colors['primary'], fg=self.colors['text'],
                                   relief='flat', command=self.show_leaderboard,
                                   width=3, height=1)
        leaderboard_btn.pack(side='right', padx=5)
        
        profile_btn = tk.Button(controls_frame, text="👤", font=('Segoe UI', 14),
                               bg=self.colors['primary'], fg=self.colors['text'],
                               relief='flat', command=self.open_profile,
                               width=3, height=1)
        profile_btn.pack(side='right', padx=5)
        
        settings_btn = tk.Button(controls_frame, text="⚙", font=('Segoe UI', 14),
                                bg=self.colors['primary'], fg=self.colors['text'],
                                relief='flat', command=self.open_settings,
                                width=3, height=1)
        settings_btn.pack(side='right', padx=5)

    def create_sidebar(self, parent):
        """Create navigation sidebar"""
        sidebar = tk.Frame(parent, bg=self.colors['surface'], width=250)
        sidebar.pack(side='left', fill='y', padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Navigation header
        nav_header = tk.Label(sidebar, text="Navigation", 
                             font=('Segoe UI', 14, 'bold'),
                             bg=self.colors['surface'], fg=self.colors['text'])
        nav_header.pack(pady=10)
        
        # Viewing progress
        viewing_frame = tk.LabelFrame(sidebar, text="Viewing Progress", 
                                     bg=self.colors['surface'], fg=self.colors['text'],
                                     font=('Segoe UI', 10, 'bold'))
        viewing_frame.pack(fill='x', padx=10, pady=5)
        
        self.viewing_time_label = tk.Label(viewing_frame, text="00:00 / 02:00", 
                                          font=('Segoe UI', 14, 'bold'),
                                          bg=self.colors['surface'], fg=self.colors['accent'])
        self.viewing_time_label.pack(pady=5)
        
        self.viewing_progress = ttk.Progressbar(viewing_frame, orient='horizontal', 
                                               length=200, mode='determinate',
                                               maximum=self.viewing_time_required)
        self.viewing_progress.pack(padx=10, pady=5)
        self.viewing_progress['value'] = 0
        
        self.advance_status = tk.Label(viewing_frame, text="⏳ Reading required to advance", 
                                      font=('Segoe UI', 9),
                                      bg=self.colors['surface'], fg=self.colors['warning'])
        self.advance_status.pack(pady=5)
        
        # Page complexity indicator
        self.complexity_label = tk.Label(viewing_frame, text="Page complexity: Analyzing...", 
                                        font=('Segoe UI', 8),
                                        bg=self.colors['surface'], fg=self.colors['text_secondary'])
        self.complexity_label.pack(pady=2)
        
        # Quick navigation
        nav_buttons_frame = tk.Frame(sidebar, bg=self.colors['surface'])
        nav_buttons_frame.pack(fill='x', padx=10, pady=10)
        
        self.prev_button = tk.Button(nav_buttons_frame, text="⏮ Previous", command=self.previous_page,
                                    bg=self.colors['secondary'], fg=self.colors['text'],
                                    font=('Segoe UI', 10), relief='flat')
        self.prev_button.pack(fill='x', pady=2)
        
        self.next_button = tk.Button(nav_buttons_frame, text="⏭ Next", command=self.next_page,
                                    bg=self.colors['secondary'], fg=self.colors['text'],
                                    font=('Segoe UI', 10), relief='flat', state='disabled')
        self.next_button.pack(fill='x', pady=2)
        
        tk.Button(nav_buttons_frame, text="🔖 Bookmarks", command=self.show_bookmarks,
                 bg=self.colors['warning'], fg=self.colors['text'],
                 font=('Segoe UI', 10), relief='flat').pack(fill='x', pady=2)
        
        # Skip button (no points)
        self.skip_button = tk.Button(nav_buttons_frame, text="⏩ Skip (No Points)", command=self.skip_page,
                                    bg=self.colors['accent'], fg=self.colors['text'],
                                    font=('Segoe UI', 10), relief='flat')
        self.skip_button.pack(fill='x', pady=2)
        
        # Progress section
        progress_frame = tk.LabelFrame(sidebar, text="Progress", 
                                      bg=self.colors['surface'], fg=self.colors['text'],
                                      font=('Segoe UI', 10, 'bold'))
        progress_frame.pack(fill='x', padx=10, pady=5)
        
        self.progress_label = tk.Label(progress_frame, text=f"Page {self.current_page}/{self.total_pages}", 
                                      bg=self.colors['surface'], fg=self.colors['text'])
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', 
                                           length=200, mode='determinate',
                                           maximum=self.total_pages)
        self.progress_bar.pack(padx=10, pady=5)
        self.progress_bar['value'] = self.current_page
        
        # Reading timer
        timer_frame = tk.LabelFrame(sidebar, text="Reading Timer", 
                                   bg=self.colors['surface'], fg=self.colors['text'],
                                   font=('Segoe UI', 10, 'bold'))
        timer_frame.pack(fill='x', padx=10, pady=5)
        
        self.timer_label = tk.Label(timer_frame, text="00:00:00", 
                                   font=('Segoe UI', 16, 'bold'),
                                   bg=self.colors['surface'], fg=self.colors['accent'])
        self.timer_label.pack(pady=5)
        
        timer_buttons = tk.Frame(timer_frame, bg=self.colors['surface'])
        timer_buttons.pack(pady=5)
        
        self.start_button = tk.Button(timer_buttons, text="▶ Start", 
                                     command=self.start_reading,
                                     bg=self.colors['success'], fg=self.colors['text'],
                                     font=('Segoe UI', 10), relief='flat', width=8)
        self.start_button.pack(side='left', padx=2)
        
        tk.Button(timer_buttons, text="⏸ Pause", 
                 command=self.pause_reading,
                 bg=self.colors['warning'], fg=self.colors['text'],
                 font=('Segoe UI', 10), relief='flat', width=8).pack(side='left', padx=2)

    def create_reading_area(self, parent):
        """Create main reading area with Quran content"""
        reading_frame = tk.Frame(parent, bg=self.colors['background'])
        reading_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        # Quran content display
        content_frame = tk.Frame(reading_frame, bg=self.colors['surface'], relief='raised', bd=2)
        content_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Header with surah info
        header_frame = tk.Frame(content_frame, bg=self.colors['primary'])
        header_frame.pack(fill='x', padx=10, pady=10)
        
        self.surah_title = tk.Label(header_frame, text="Surah Al-Fatiha", 
                                   font=('Segoe UI', 18, 'bold'),
                                   bg=self.colors['primary'], fg=self.colors['text'])
        self.surah_title.pack(side='left')
        
        self.ayah_info = tk.Label(header_frame, text="Ayah 1 of 7", 
                                 font=('Segoe UI', 12),
                                 bg=self.colors['primary'], fg=self.colors['text_secondary'])
        self.ayah_info.pack(side='right')
        
        # Quran page image display
        self.page_frame = tk.Frame(content_frame, bg=self.colors['arabic_bg'])
        self.page_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Page image label
        self.page_image_label = tk.Label(self.page_frame, text="Loading Quran Page...", 
                                        font=('Segoe UI', 16),
                                        bg=self.colors['arabic_bg'], fg=self.colors['arabic_text'])
        self.page_image_label.pack(expand=True)
        
        # Arabic text display (hidden by default)
        self.arabic_frame = tk.Frame(content_frame, bg=self.colors['arabic_bg'])
        
        self.arabic_text = tk.Label(self.arabic_frame, text="", 
                                   font=('Arabic Typesetting', 20),
                                   bg=self.colors['arabic_bg'], fg=self.colors['arabic_text'],
                                   justify='right', wraplength=600)
        self.arabic_text.pack(pady=10)
        
        # Translation display (hidden by default)
        self.translation_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        
        self.translation_text = tk.Label(self.translation_frame, text="", 
                                        font=('Segoe UI', 14),
                                        bg=self.colors['surface'], fg=self.colors['text'],
                                        justify='left', wraplength=600)
        self.translation_text.pack(pady=10)
        
        # Initialize page view mode
        self.page_view_mode = True
        
        # Controls
        controls_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        controls_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(controls_frame, text="🔖 Bookmark", command=self.bookmark_current,
                 bg=self.colors['warning'], fg=self.colors['text'],
                 font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="📝 Add Note", command=self.add_note,
                 bg=self.colors['secondary'], fg=self.colors['text'],
                 font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="🔍 Search", command=self.open_search,
                 bg=self.colors['accent'], fg=self.colors['text'],
                 font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="🖼️ Page View", command=self.toggle_page_view,
                 bg=self.colors['success'], fg=self.colors['text'],
                 font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)

    def create_right_panel(self, parent):
        """Create right panel for notes and bookmarks"""
        right_panel = tk.Frame(parent, bg=self.colors['surface'], width=300)
        right_panel.pack(side='right', fill='y', padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Notes section
        notes_frame = tk.LabelFrame(right_panel, text="Notes", 
                                   bg=self.colors['surface'], fg=self.colors['text'],
                                   font=('Segoe UI', 12, 'bold'))
        notes_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=10, 
                                                   bg='#2a2a2a', fg=self.colors['text'],
                                                   font=('Segoe UI', 10), wrap='word')
        self.notes_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        notes_buttons = tk.Frame(notes_frame, bg=self.colors['surface'])
        notes_buttons.pack(fill='x', padx=5, pady=5)
        
        tk.Button(notes_buttons, text="Save Note", command=self.save_note,
                 bg=self.colors['success'], fg=self.colors['text'],
                 font=('Segoe UI', 9), relief='flat').pack(side='left')
        
        tk.Button(notes_buttons, text="Clear", command=self.clear_note,
                 bg=self.colors['accent'], fg=self.colors['text'],
                 font=('Segoe UI', 9), relief='flat').pack(side='right')
        
        # Bookmarks section
        bookmarks_frame = tk.LabelFrame(right_panel, text="Bookmarks", 
                                       bg=self.colors['surface'], fg=self.colors['text'],
                                       font=('Segoe UI', 12, 'bold'))
        bookmarks_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.bookmarks_listbox = tk.Listbox(bookmarks_frame, height=6, 
                                           bg='#2a2a2a', fg=self.colors['text'],
                                           font=('Segoe UI', 9))
        self.bookmarks_listbox.pack(fill='x', padx=5, pady=5)
        self.bookmarks_listbox.bind('<Double-Button-1>', self.go_to_bookmark)

    def create_status_bar(self, parent):
        """Create status bar at bottom"""
        status_frame = tk.Frame(parent, bg=self.colors['primary'], height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Ready", 
                                    bg=self.colors['primary'], fg=self.colors['text'],
                                    font=('Segoe UI', 9))
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Daily goal progress
        self.goal_text = tk.Label(status_frame, text=f"Daily Goal: {self.reading_time//60}/{self.daily_goal} min", 
                            bg=self.colors['primary'], fg=self.colors['text_secondary'],
                            font=('Segoe UI', 9))
        self.goal_text.pack(side='right', padx=10, pady=5)

    def load_current_content(self):
        """Load current verse content"""
        if self.page_view_mode:
            self.load_quran_page()
        else:
            self.load_verse_content()
        
        # Update header info
        surah_name = self.surah_names.get(self.current_surah, {}).get('name', 'Unknown')
        total_ayahs = self.surah_names.get(self.current_surah, {}).get('ayahs', 1)
        
        self.surah_title.config(text=f"Surah {surah_name}")
        self.ayah_info.config(text=f"Ayah {self.current_ayah} of {total_ayahs}")
        
        # Load notes for current verse
        self.load_notes()
        
        # Update status
        self.status_label.config(text=f"Loaded: Surah {surah_name}, Ayah {self.current_ayah}")

    def analyze_page_complexity(self, image_path):
        """Analyze page complexity based on ink density/darkness"""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Convert to grayscale for analysis
            gray_image = image.convert('L')
            
            # Convert to numpy array
            img_array = np.array(gray_image)
            
            # Calculate ink density (percentage of dark pixels)
            # Dark pixels are those with value < 128 (out of 255)
            dark_pixels = np.sum(img_array < 128)
            total_pixels = img_array.size
            ink_density = dark_pixels / total_pixels
            
            # Calculate text density in different regions
            height, width = img_array.shape
            
            # Divide image into regions for analysis
            top_region = img_array[:height//3, :]
            middle_region = img_array[height//3:2*height//3, :]
            bottom_region = img_array[2*height//3:, :]
            
            # Calculate density for each region
            regions = [top_region, middle_region, bottom_region]
            region_densities = []
            
            for region in regions:
                region_dark = np.sum(region < 128)
                region_total = region.size
                region_density = region_dark / region_total if region_total > 0 else 0
                region_densities.append(region_density)
            
            # Calculate complexity score (0.0 to 2.0)
            # Base score from overall ink density
            complexity_score = ink_density * 2.0
            
            # Add variation bonus if regions have different densities (more text variety)
            density_variance = np.var(region_densities)
            variation_bonus = min(density_variance * 0.5, 0.3)  # Max 0.3 bonus
            complexity_score += variation_bonus
            
            # Ensure score is within bounds
            complexity_score = max(0.2, min(complexity_score, 2.0))
            
            return {
                'ink_density': ink_density,
                'complexity_score': complexity_score,
                'region_densities': region_densities,
                'has_text': ink_density > self.ink_density_threshold
            }
            
        except Exception as e:
            logging.error(f"Error analyzing page complexity: {e}")
            return {
                'ink_density': 0.3,  # Default moderate density
                'complexity_score': 0.5,
                'region_densities': [0.3, 0.3, 0.3],
                'has_text': True
            }

    def calculate_reading_time(self, complexity_data):
        """Calculate reading time based on page complexity"""
        complexity_score = complexity_data['complexity_score']
        ink_density = complexity_data['ink_density']
        
        # Base time calculation
        # More complex pages = more reading time
        time_multiplier = 0.5 + complexity_score  # Range: 0.7 to 2.5
        
        # Adjust for very low density (mostly empty pages)
        if ink_density < 0.05:  # Very sparse pages
            time_multiplier = 0.3
        elif ink_density < 0.1:  # Sparse pages
            time_multiplier = 0.5
        
        # Calculate final reading time
        reading_time = int(self.base_viewing_time * time_multiplier)
        
        # Ensure within bounds
        reading_time = max(self.min_reading_time, min(reading_time, self.max_reading_time))
        
        return reading_time

    def load_quran_page(self):
        """Load Quran page image and analyze complexity"""
        try:
            # Try to load page image from directory with new naming convention
            page_filename = f"quran-{self.current_page}-fa.jpg"
            page_path = os.path.join(self.quran_pages_dir, page_filename)
            
            if os.path.exists(page_path):
                # Analyze page complexity first
                complexity_data = self.analyze_page_complexity(page_path)
                self.page_complexity_score = complexity_data['complexity_score']
                
                # Calculate dynamic reading time
                self.viewing_time_required = self.calculate_reading_time(complexity_data)
                
                # Update UI to show new reading time
                minutes = self.viewing_time_required // 60
                seconds = self.viewing_time_required % 60
                self.viewing_time_label.config(text=f"00:00 / {minutes:02d}:{seconds:02d}")
                self.viewing_progress.config(maximum=self.viewing_time_required)
                self.viewing_progress['value'] = 0
                
                # Update status with complexity info
                complexity_info = f"Page complexity: {self.page_complexity_score:.2f}, Ink density: {complexity_data['ink_density']:.1%}"
                self.status_label.config(text=complexity_info)
                
                # Update complexity label in sidebar
                complexity_text = f"Complexity: {self.page_complexity_score:.2f} ({complexity_data['ink_density']:.1%} ink)"
                self.complexity_label.config(text=complexity_text)
                
                # Load and resize image
                image = Image.open(page_path)
                
                # Resize image to fit the display area
                display_width = 600
                display_height = 800
                image.thumbnail((display_width, display_height), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Update the label with the image
                self.page_image_label.config(image=photo, text="")
                self.page_image_label.image = photo  # Keep a reference
                
            else:
                # Show placeholder if image not found
                self.page_image_label.config(
                    text=f"Quran Page {self.current_page}\n\n[Page image not found]\n\nLooking for: {page_filename}",
                    image=""
                )
                # Reset to default reading time
                self.viewing_time_required = self.base_viewing_time
                
        except Exception as e:
            # Show error message
            self.page_image_label.config(
                text=f"Error loading page {self.current_page}:\n{str(e)}",
                image=""
            )
            # Reset to default reading time
            self.viewing_time_required = self.base_viewing_time

    def load_verse_content(self):
        """Load verse content in text mode"""
        if self.current_surah in self.quran_data and self.current_ayah in self.quran_data[self.current_surah]:
            verse_data = self.quran_data[self.current_surah][self.current_ayah]
            
            # Display Arabic text
            
            # Display translation
            if self.show_translation:
                self.translation_text.config(text=verse_data['translation'])
            else:
                self.translation_text.config(text="")

    def toggle_page_view(self):
        """Toggle between page view and verse view"""
        self.page_view_mode = not self.page_view_mode
        
        if self.page_view_mode:
            # Show page view, hide text view
            self.page_frame.pack(fill='both', expand=True, padx=10, pady=5)
            self.arabic_frame.pack_forget()
            self.translation_frame.pack_forget()
            self.load_quran_page()
        else:
            # Show text view, hide page view
            self.page_frame.pack_forget()
            if self.show_arabic:
                self.arabic_frame.pack(fill='x', padx=10, pady=5)
            if self.show_translation:
                self.translation_frame.pack(fill='x', padx=10, pady=5)
            self.load_verse_content()

    def on_surah_change(self, event=None):
        """Handle surah selection change (placeholder for future use)"""
        pass  # This method is no longer needed since we removed surah selection

    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.reset_page_viewing_time()
            self.load_current_content()
            self.update_display()

    def next_page(self):
        """Go to next page (requires viewing time)"""
        if not self.can_advance:
            minutes = self.viewing_time_required // 60
            seconds = self.viewing_time_required % 60
            messagebox.showwarning("Viewing Time Required", 
                                 f"Please read for {minutes} minutes and {seconds} seconds before advancing to the next page.\n\nCurrent page complexity: {self.page_complexity_score:.2f}")
            return
            
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.reset_page_viewing_time()
            self.load_current_content()
            self.update_display()
            
            # Award points for progression (already awarded when viewing time completed)
            self.user_profile['total_pages_read'] += 1
            self.update_user_profile()
            
            # Check achievements
            self.check_achievements()
            
            # Sync online if enabled
            if self.online_sync_enabled:
                self.sync_online()
        else:
            messagebox.showinfo("Congratulations", "You've completed reading the entire Quran!")

    def skip_page(self):
        """Skip to next page without earning points"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.reset_page_viewing_time()
            self.load_current_content()
            self.update_display()
            
            self.status_label.config(text="Page skipped - no points earned")
        else:
            messagebox.showinfo("Congratulations", "You've completed reading the entire Quran!")

    def reset_page_viewing_time(self):
        """Reset viewing time for new page"""
        self.current_page_viewing_time = 0
        self.can_advance = False
        self.page_start_time = time.time()
        
        # Update UI elements with current reading time requirement
        minutes = self.viewing_time_required // 60
        seconds = self.viewing_time_required % 60
        self.viewing_time_label.config(text=f"00:00 / {minutes:02d}:{seconds:02d}")
        self.viewing_progress.config(maximum=self.viewing_time_required)
        self.viewing_progress['value'] = 0
        self.next_button.config(state='disabled', bg=self.colors['secondary'])
        self.advance_status.config(text="⏳ Reading required to advance", fg=self.colors['warning'])
        
    def start_reading(self):
        """Start reading timer"""
        if not self.timer_running:
            self.timer_running = True
            self.start_button.config(text="⏸ Pause", bg=self.colors['warning'])
            self.update_timer()
            self.status_label.config(text="Reading in progress...")

    def pause_reading(self):
        """Pause reading timer"""
        self.timer_running = False
        self.start_button.config(text="▶ Resume", bg=self.colors['success'])
        self.status_label.config(text="Reading paused")
    
    def update_timer(self):
        """Update reading timer and viewing progress"""
        if self.timer_running:
            self.reading_time += 1
            self.current_page_viewing_time += 1
            
            # Update main timer display
            hours = self.reading_time // 3600
            minutes = (self.reading_time % 3600) // 60
            seconds = self.reading_time % 60
            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            
            # Update viewing progress
            viewing_minutes = self.current_page_viewing_time // 60
            viewing_seconds = self.current_page_viewing_time % 60
            required_minutes = self.viewing_time_required // 60
            required_seconds = self.viewing_time_required % 60
            self.viewing_time_label.config(text=f"{viewing_minutes:02d}:{viewing_seconds:02d} / {required_minutes:02d}:{required_seconds:02d}")
            self.viewing_progress['value'] = self.current_page_viewing_time
            
            # Check if can advance to next page
            if self.current_page_viewing_time >= self.viewing_time_required and not self.can_advance:
                self.can_advance = True
                self.next_button.config(state='normal', bg=self.colors['success'])
                self.advance_status.config(text="✅ Ready to advance!", fg=self.colors['success'])
                # Award points for completing viewing time
                self.points += 25
                self.points_label.config(text=f"{self.points}")
                self.update_user_profile()
            
            # Update daily goal progress
            current_minutes = self.reading_time // 60
            self.goal_text.config(text=f"Daily Goal: {current_minutes}/{self.daily_goal} min")
            
            # Award bonus points for reading time
            if self.reading_time % 300 == 0:  # Every 5 minutes
                self.points += 10
                self.points_label.config(text=f"{self.points}")
            
            # Schedule next update
            self.root.after(1000, self.update_timer)
    
    def bookmark_current(self):
        """Bookmark current page"""
        bookmark_key = f"Page {self.current_page}"
        
        if bookmark_key not in self.bookmarks:
            self.bookmarks.append(bookmark_key)
            self.update_bookmarks_display()
            self.save_user_data()
            self.status_label.config(text=f"Bookmarked: {bookmark_key}")
            messagebox.showinfo("Bookmark Added", f"Bookmarked {bookmark_key}")
        else:
            messagebox.showinfo("Already Bookmarked", "This page is already bookmarked")

    def update_bookmarks_display(self):
        """Update bookmarks listbox"""
        self.bookmarks_listbox.delete(0, tk.END)
        for bookmark in self.bookmarks:
            self.bookmarks_listbox.insert(tk.END, bookmark)

    def go_to_bookmark(self, event=None):
        """Go to selected bookmark"""
        selection = self.bookmarks_listbox.curselection()
        if selection:
            bookmark = self.bookmarks[selection[0]]
            # Parse bookmark to extract page number
            page_num = int(bookmark.split(' ')[1])  # Extract page number
            
            self.current_page = page_num
            
            self.load_current_content()
            self.update_display()
            self.status_label.config(text=f"Navigated to {bookmark}")

    def add_note(self):
        """Add note to current page"""
        note_key = f"Page {self.current_page}"
        
        if note_key in self.notes:
            self.notes_text.delete(1.0, tk.END)
            self.notes_text.insert(1.0, self.notes[note_key])
        
        self.notes_text.focus()

    def save_note(self):
        """Save note for current page"""
        note_key = f"Page {self.current_page}"
        note_content = self.notes_text.get(1.0, tk.END).strip()
        
        if note_content:
            self.notes[note_key] = note_content
            self.save_user_data()
            self.status_label.config(text=f"Note saved for {note_key}")
        else:
            if note_key in self.notes:
                del self.notes[note_key]
                self.save_user_data()
                self.status_label.config(text="Note cleared")

    def clear_note(self):
        """Clear current note"""
        self.notes_text.delete(1.0, tk.END)

    def load_notes(self):
        """Load notes for current page"""
        note_key = f"Page {self.current_page}"
        
        self.notes_text.delete(1.0, tk.END)
        if note_key in self.notes:
            self.notes_text.insert(1.0, self.notes[note_key])

    def open_search(self):
        """Open search dialog"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Quran")
        search_window.geometry("600x400")
        search_window.configure(bg=self.colors['background'])
        
        # Search input
        search_frame = tk.Frame(search_window, bg=self.colors['background'])
        search_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(search_frame, text="Search in Quran:", 
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['background'], fg=self.colors['text']).pack(anchor='w')
        
        search_entry = tk.Entry(search_frame, font=('Segoe UI', 12), width=50)
        search_entry.pack(fill='x', pady=10)
        
        # Results
        results_frame = tk.Frame(search_window, bg=self.colors['background'])
        results_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        results_text = scrolledtext.ScrolledText(results_frame, height=15,
                                                bg='#2a2a2a', fg=self.colors['text'],
                                                font=('Segoe UI', 10))
        results_text.pack(fill='both', expand=True)
        
        def perform_search():
            query = search_entry.get().lower()
            results_text.delete(1.0, tk.END)
            
            found_verses = []
            for surah_num, surah_data in self.quran_data.items():
                for ayah_num, verse_data in surah_data.items():
                    if (query in verse_data['translation'].lower() or 
                        query in verse_data['arabic']):
                        found_verses.append((surah_num, ayah_num, verse_data))
            
            if found_verses:
                for surah_num, ayah_num, verse_data in found_verses:
                    surah_name = self.surah_names.get(surah_num, {}).get('name', 'Unknown')
                    results_text.insert(tk.END, f"Surah {surah_name} ({surah_num}:{ayah_num})\n")
                    results_text.insert(tk.END, f"Translation: {verse_data['translation']}\n\n")
            else:
                results_text.insert(tk.END, "No verses found matching your search.")
        
        search_entry.bind('<Return>', lambda e: perform_search())
        tk.Button(search_frame, text="Search", command=perform_search,
                 bg=self.colors['accent'], fg=self.colors['text'],
                 font=('Segoe UI', 10)).pack(pady=10)

    def toggle_page_view(self):
        """Toggle between page view and verse view"""
        self.page_view_mode = not self.page_view_mode
        
        if self.page_view_mode:
            # Show page view, hide text view
            self.page_frame.pack(fill='both', expand=True, padx=10, pady=5)
            self.arabic_frame.pack_forget()
            self.translation_frame.pack_forget()
            self.load_quran_page()
        else:
            # Show text view, hide page view
            self.page_frame.pack_forget()
            if self.show_arabic:
                self.arabic_frame.pack(fill='x', padx=10, pady=5)
            if self.show_translation:
                self.translation_frame.pack(fill='x', padx=10, pady=5)
            self.load_verse_content()

    def open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.configure(bg=self.colors['background'])
        
        # Settings content
        settings_frame = tk.Frame(settings_window, bg=self.colors['background'])
        settings_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Theme settings
        theme_frame = tk.LabelFrame(settings_frame, text="Appearance", 
                                   bg=self.colors['surface'], fg=self.colors['text'],
                                   font=('Segoe UI', 12, 'bold'))
        theme_frame.pack(fill='x', pady=10)
        
        # Dark mode toggle
        self.dark_mode_var = tk.BooleanVar(value=self.dark_mode)
        dark_mode_check = tk.Checkbutton(theme_frame, text="Dark Mode", 
                                        variable=self.dark_mode_var,
                                        bg=self.colors['surface'], fg=self.colors['text'],
                                        font=('Segoe UI', 10))
        dark_mode_check.pack(anchor='w', padx=10, pady=5)
        
        # Font size
        tk.Label(theme_frame, text="Font Size:", 
                bg=self.colors['surface'], fg=self.colors['text'],
                font=('Segoe UI', 10)).pack(anchor='w', padx=10, pady=(10, 0))
        
        self.font_size_var = tk.IntVar(value=self.font_size)
        font_size_scale = tk.Scale(theme_frame, from_=12, to=24, orient='horizontal',
                                  variable=self.font_size_var,
                                  bg=self.colors['surface'], fg=self.colors['text'])
        font_size_scale.pack(fill='x', padx=10, pady=5)
        
        # Display options
        display_frame = tk.LabelFrame(settings_frame, text="Display Options", 
                                     bg=self.colors['surface'], fg=self.colors['text'],
                                     font=('Segoe UI', 12, 'bold'))
        display_frame.pack(fill='x', pady=10)
        
        self.show_arabic_var = tk.BooleanVar(value=self.show_arabic)
        arabic_check = tk.Checkbutton(display_frame, text="Show Arabic Text", 
                                     variable=self.show_arabic_var,
                                     bg=self.colors['surface'], fg=self.colors['text'],
                                     font=('Segoe UI', 10))
        arabic_check.pack(anchor='w', padx=10, pady=5)
        
        self.show_translation_var = tk.BooleanVar(value=self.show_translation)
        translation_check = tk.Checkbutton(display_frame, text="Show Translation", 
                                          variable=self.show_translation_var,
                                          bg=self.colors['surface'], fg=self.colors['text'],
                                          font=('Segoe UI', 10))
        translation_check.pack(anchor='w', padx=10, pady=5)
        
        # Daily goal
        goal_frame = tk.LabelFrame(settings_frame, text="Reading Goals", 
                                  bg=self.colors['surface'], fg=self.colors['text'],
                                  font=('Segoe UI', 12, 'bold'))
        goal_frame.pack(fill='x', pady=10)
        
        tk.Label(goal_frame, text="Daily Reading Goal (minutes):", 
                bg=self.colors['surface'], fg=self.colors['text'],
                font=('Segoe UI', 10)).pack(anchor='w', padx=10, pady=(10, 0))
        
        self.daily_goal_var = tk.IntVar(value=self.daily_goal)
        goal_scale = tk.Scale(goal_frame, from_=10, to=120, orient='horizontal',
                             variable=self.daily_goal_var,
                             bg=self.colors['surface'], fg=self.colors['text'])
        goal_scale.pack(fill='x', padx=10, pady=5)
        
        # Save button
        def save_settings():
            self.dark_mode = self.dark_mode_var.get()
            self.font_size = self.font_size_var.get()
            self.show_arabic = self.show_arabic_var.get()
            self.show_translation = self.show_translation_var.get()
            self.daily_goal = self.daily_goal_var.get()
            
            self.save_user_data()
            self.load_current_content()  # Refresh display
            settings_window.destroy()
            self.status_label.config(text="Settings saved successfully!")
        
        tk.Button(settings_frame, text="Save Settings", command=save_settings,
                 bg=self.colors['success'], fg=self.colors['text'],
                 font=('Segoe UI', 12, 'bold')).pack(pady=20)

    def check_achievements(self):
        """Check and award achievements"""
        new_achievements = []
        
        # Reading streak achievements
        if self.streak >= 7 and "week_streak" not in self.achievements:
            new_achievements.append("week_streak")
            self.achievements.append("week_streak")
        
        if self.streak >= 30 and "month_streak" not in self.achievements:
            new_achievements.append("month_streak")
            self.achievements.append("month_streak")
        
        # Points achievements
        if self.points >= 1000 and "points_1000" not in self.achievements:
            new_achievements.append("points_1000")
            self.achievements.append("points_1000")
        
        # Reading time achievements
        total_minutes = self.reading_time // 60
        if total_minutes >= 60 and "reading_hour" not in self.achievements:
            new_achievements.append("reading_hour")
            self.achievements.append("reading_hour")
        
        # Show new achievements
        if new_achievements:
            self.show_achievement_notification(new_achievements)
            self.save_user_data()

    def show_achievement_notification(self, achievements):
        """Show achievement notification"""
        achievement_names = {
            "week_streak": "7 Day Streak! 🔥",
            "month_streak": "30 Day Streak! 🏆",
            "points_1000": "1000 Points! ⭐",
            "reading_hour": "1 Hour Reading! 📚"
        }
        
        message = "New Achievement(s) Unlocked!\n\n"
        for achievement in achievements:
            message += f"• {achievement_names.get(achievement, achievement)}\n"
        
        messagebox.showinfo("Achievement Unlocked!", message)

    def show_bookmarks(self):
        """Show bookmarks window"""
        if not self.bookmarks:
            messagebox.showinfo("Bookmarks", "No bookmarks found. Add bookmarks by clicking the bookmark button while reading.")
            return
        
        bookmarks_window = tk.Toplevel(self.root)
        bookmarks_window.title("Bookmarks")
        bookmarks_window.geometry("500x400")
        bookmarks_window.configure(bg=self.colors['background'])
        
        # Bookmarks list
        bookmarks_frame = tk.Frame(bookmarks_window, bg=self.colors['background'])
        bookmarks_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        bookmarks_listbox = tk.Listbox(bookmarks_frame, 
                                      bg='#2a2a2a', fg=self.colors['text'],
                                      font=('Segoe UI', 12))
        bookmarks_listbox.pack(fill='both', expand=True)
        
        for bookmark in self.bookmarks:
            bookmarks_listbox.insert(tk.END, bookmark)
        
        def go_to_selected():
            selection = bookmarks_listbox.curselection()
            if selection:
                bookmark = self.bookmarks[selection[0]]
                page_num = int(bookmark.split(' ')[1])
                
                self.current_page = page_num
                
                self.load_current_content()
                self.update_display()
                bookmarks_window.destroy()
        
        tk.Button(bookmarks_frame, text="Go to Bookmark", command=go_to_selected,
                 bg=self.colors['accent'], fg=self.colors['text'],
                 font=('Segoe UI', 10)).pack(pady=10)

    def open_profile(self):
        """Open user profile window"""
        profile_window = tk.Toplevel(self.root)
        profile_window.title("User Profile")
        profile_window.geometry("600x500")
        profile_window.configure(bg=self.colors['background'])
        
        # Profile header
        header_frame = tk.Frame(profile_window, bg=self.colors['primary'], height=100)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        # Avatar and basic info
        avatar_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        avatar_frame.pack(side='left', padx=20, pady=20)
        
        tk.Label(avatar_frame, text="👤", font=('Segoe UI', 32),
                bg=self.colors['primary'], fg=self.colors['text']).pack()
        
        info_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        info_frame.pack(side='left', fill='both', expand=True, padx=20, pady=20)
        
        self.profile_username = tk.Label(info_frame, text=self.user_profile['username'], 
                                        font=('Segoe UI', 20, 'bold'),
                                        bg=self.colors['primary'], fg=self.colors['text'])
        self.profile_username.pack(anchor='w')
        
        level_info = f"Level {self.user_profile['level']} • {self.user_profile['total_pages_read']} pages read"
        tk.Label(info_frame, text=level_info, font=('Segoe UI', 12),
                bg=self.colors['primary'], fg=self.colors['text_secondary']).pack(anchor='w')
        
        # Profile content
        content_frame = tk.Frame(profile_window, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Stats section
        stats_frame = tk.LabelFrame(content_frame, text="Statistics", 
                                   bg=self.colors['surface'], fg=self.colors['text'],
                                   font=('Segoe UI', 12, 'bold'))
        stats_frame.pack(fill='x', padx=10, pady=10)
        
        stats_grid = tk.Frame(stats_frame, bg=self.colors['surface'])
        stats_grid.pack(fill='x', padx=10, pady=10)
        
        # Create stats labels
        stats_data = [
            ("Total Pages Read:", str(self.user_profile['total_pages_read'])),
            ("Current Streak:", f"{self.streak} days"),
            ("Total Points:", str(self.points)),
            ("Level:", str(self.user_profile['level'])),
            ("Experience:", str(self.user_profile['experience'])),
            ("Join Date:", self.user_profile['join_date'])
        ]
        
        for i, (label, value) in enumerate(stats_data):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(stats_grid, text=label, font=('Segoe UI', 10),
                    bg=self.colors['surface'], fg=self.colors['text_secondary']).grid(row=row, column=col, sticky='w', padx=(0, 10))
            tk.Label(stats_grid, text=value, font=('Segoe UI', 10, 'bold'),
                    bg=self.colors['surface'], fg=self.colors['text']).grid(row=row, column=col+1, sticky='w')
        
        # Bio section
        bio_frame = tk.LabelFrame(content_frame, text="Bio", 
                                 bg=self.colors['surface'], fg=self.colors['text'],
                                 font=('Segoe UI', 12, 'bold'))
        bio_frame.pack(fill='x', padx=10, pady=10)
        
        self.bio_text = scrolledtext.ScrolledText(bio_frame, height=4, 
                                                 bg='#2a2a2a', fg=self.colors['text'],
                                                 font=('Segoe UI', 10), wrap='word')
        self.bio_text.pack(fill='x', padx=10, pady=10)
        self.bio_text.insert(1.0, self.user_profile['bio'])
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors['background'])
        button_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(button_frame, text="Save Profile", command=lambda: self.save_profile(profile_window),
                 bg=self.colors['success'], fg=self.colors['text'],
                 font=('Segoe UI', 10)).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Edit Username", command=self.edit_username,
                 bg=self.colors['accent'], fg=self.colors['text'],
                 font=('Segoe UI', 10)).pack(side='left', padx=5)

    def edit_username(self):
        """Edit username dialog"""
        new_username = simpledialog.askstring("Edit Username", "Enter new username:", 
                                             initialvalue=self.user_profile['username'])
        if new_username and new_username.strip():
            self.user_profile['username'] = new_username.strip()
            self.username_label.config(text=new_username.strip())
            self.save_user_data()
            self.status_label.config(text="Username updated!")

    def save_profile(self, window):
        """Save profile changes"""
        self.user_profile['bio'] = self.bio_text.get(1.0, tk.END).strip()
        self.save_user_data()
        window.destroy()
        self.status_label.config(text="Profile saved!")

    def update_user_profile(self):
        """Update user profile with new stats"""
        # Calculate level based on experience
        new_level = (self.user_profile['experience'] // 100) + 1
        if new_level > self.user_profile['level']:
            self.user_profile['level'] = new_level
            messagebox.showinfo("Level Up!", f"Congratulations! You've reached level {new_level}!")
        
        # Update UI
        self.level_label.config(text=f"Level {self.user_profile['level']} • {self.user_profile['total_pages_read']} pages read")
        
        # Save changes
        self.save_user_data()

    def show_leaderboard(self):
        """Show leaderboard window"""
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Leaderboard")
        leaderboard_window.geometry("700x600")
        leaderboard_window.configure(bg=self.colors['background'])
        
        # Header
        header_frame = tk.Frame(leaderboard_window, bg=self.colors['primary'], height=60)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🏆 Global Leaderboard", 
                font=('Segoe UI', 18, 'bold'),
                bg=self.colors['primary'], fg=self.colors['text']).pack(expand=True)
        
        # Leaderboard content
        content_frame = tk.Frame(leaderboard_window, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Local leaderboard (simulated)
        local_frame = tk.LabelFrame(content_frame, text="Local Rankings", 
                                   bg=self.colors['surface'], fg=self.colors['text'],
                                   font=('Segoe UI', 12, 'bold'))
        local_frame.pack(fill='x', padx=10, pady=10)
        
        # Simulated leaderboard data
        leaderboard_data = [
            ("1st", "QuranMaster", "Level 15", "2,450 pages", "45,230 pts"),
            ("2nd", "FaithfulReader", "Level 12", "1,890 pages", "32,100 pts"),
            ("3rd", "DailyQuran", "Level 10", "1,500 pages", "28,750 pts"),
            ("4th", self.user_profile['username'], f"Level {self.user_profile['level']}", 
             f"{self.user_profile['total_pages_read']} pages", f"{self.points} pts"),
            ("5th", "PeacefulSoul", "Level 8", "1,200 pages", "22,500 pts")
        ]
        
        for rank, name, level, pages, points in leaderboard_data:
            rank_frame = tk.Frame(local_frame, bg=self.colors['surface'])
            rank_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(rank_frame, text=rank, font=('Segoe UI', 12, 'bold'),
                    bg=self.colors['surface'], fg=self.colors['accent'], width=5).pack(side='left')
            tk.Label(rank_frame, text=name, font=('Segoe UI', 11, 'bold'),
                    bg=self.colors['surface'], fg=self.colors['text'], width=15).pack(side='left')
            tk.Label(rank_frame, text=level, font=('Segoe UI', 10),
                    bg=self.colors['surface'], fg=self.colors['text_secondary'], width=10).pack(side='left')
            tk.Label(rank_frame, text=pages, font=('Segoe UI', 10),
                    bg=self.colors['surface'], fg=self.colors['text_secondary'], width=15).pack(side='left')
            tk.Label(rank_frame, text=points, font=('Segoe UI', 10, 'bold'),
                    bg=self.colors['surface'], fg=self.colors['success'], width=15).pack(side='left')
        
        # Online sync section
        sync_frame = tk.LabelFrame(content_frame, text="Online Sync", 
                                  bg=self.colors['surface'], fg=self.colors['text'],
                                  font=('Segoe UI', 12, 'bold'))
        sync_frame.pack(fill='x', padx=10, pady=10)
        
        sync_info = tk.Label(sync_frame, 
                            text="Enable online sync to participate in global leaderboards and sync your progress across devices.",
                            font=('Segoe UI', 10), bg=self.colors['surface'], fg=self.colors['text_secondary'],
                            wraplength=600)
        sync_info.pack(padx=10, pady=10)
        
        button_frame = tk.Frame(sync_frame, bg=self.colors['surface'])
        button_frame.pack(fill='x', padx=10, pady=10)
        
        sync_status = "Enabled" if self.online_sync_enabled else "Disabled"
        sync_color = self.colors['success'] if self.online_sync_enabled else self.colors['warning']
        
        self.sync_status_label = tk.Label(button_frame, text=f"Status: {sync_status}", 
                                         font=('Segoe UI', 10, 'bold'),
                                         bg=self.colors['surface'], fg=sync_color)
        self.sync_status_label.pack(side='left')
        
        toggle_text = "Disable Sync" if self.online_sync_enabled else "Enable Sync"
        toggle_command = self.disable_online_sync if self.online_sync_enabled else self.enable_online_sync
        
        tk.Button(button_frame, text=toggle_text, command=toggle_command,
                 bg=self.colors['accent'], fg=self.colors['text'],
                 font=('Segoe UI', 10)).pack(side='right')

    def enable_online_sync(self):
        """Enable online sync"""
        self.online_sync_enabled = True
        self.save_user_data()
        
        # Show setup dialog
        messagebox.showinfo("Online Sync", "Online sync enabled! Your progress will be synced to the cloud.")
        self.status_label.config(text="Online sync enabled")

    def disable_online_sync(self):
        """Disable online sync"""
        self.online_sync_enabled = False
        self.save_user_data()
        self.status_label.config(text="Online sync disabled")

    def sync_online(self):
        """Sync user data online"""
        if not self.online_sync_enabled:
            return
        
        try:
            # Simulate API call
            sync_data = {
                'user_id': self.user_id,
                'username': self.user_profile['username'],
                'total_pages_read': self.user_profile['total_pages_read'],
                'points': self.points,
                'streak': self.streak,
                'level': self.user_profile['level'],
                'last_sync': datetime.datetime.now().isoformat()
            }
            
            # In a real app, this would make an HTTP request
            # response = requests.post(f"{self.api_endpoint}/sync", json=sync_data)
            
            self.status_label.config(text="Data synced online")
            
        except Exception as e:
            self.status_label.config(text="Sync failed - check connection")
            logging.error(f"Online sync failed: {e}")
    
    def update_display(self):
        """Update display elements"""
        self.progress_label.config(text=f"Page {self.current_page}/{self.total_pages}")
        self.progress_bar['value'] = self.current_page
        
        # Update user profile display in header
        level_info = f"Level {self.user_profile['level']} • {self.user_profile['total_pages_read']} pages read"
        self.level_label.config(text=level_info)
    
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
        else:
            # First time reading
            self.streak = 1
        
        # Update last read date to today
        self.last_read_date = today.strftime("%Y-%m-%d")
        self.streak_label.config(text=f"{self.streak}")
    
    def load_user_data(self):
        """Load user data from JSON file"""
        try:
            with open('user_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_user_data(self):
        """Save user data to JSON file"""
        data = {
            'current_page': self.current_page,
            'current_surah': self.current_surah,
            'current_ayah': self.current_ayah,
            'streak': self.streak,
            'points': self.points,
            'last_read_date': self.last_read_date,
            'bookmarks': self.bookmarks,
            'notes': self.notes,
            'achievements': self.achievements,
            'dark_mode': self.dark_mode,
            'font_size': self.font_size,
            'show_arabic': self.show_arabic,
            'show_translation': self.show_translation,
            'reading_history': self.reading_history,
            'user_profile': self.user_profile,
            'online_sync_enabled': self.online_sync_enabled,
            'user_id': self.user_id
        }
        
        with open('user_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def on_closing(self):
        """Handle application closing"""
        self.save_user_data()
        if hasattr(self, 'conn'):
            self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuranApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
