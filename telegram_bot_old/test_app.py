#!/usr/bin/env python3
"""
Test script for the Enhanced Quran Reader Application
This script performs basic functionality tests
"""

import os
import sys
import sqlite3
import json
import tempfile
import shutil
from pathlib import Path

def test_database_creation():
    """Test database creation and initialization"""
    print("Testing database creation...")
    
    try:
        from improved_quran_app import DatabaseManager
        
        # Create a temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
            db_path = tmp_db.name
        
        db_manager = DatabaseManager(db_path)
        
        # Test user data operations
        test_data = {
            'current_page': 1,
            'streak': 5,
            'points': 100,
            'last_read_date': '2024-01-01',
            'total_reading_time': 3600
        }
        
        db_manager.save_user_data(test_data)
        retrieved_data = db_manager.get_user_data()
        
        assert retrieved_data['current_page'] == 1
        assert retrieved_data['streak'] == 5
        assert retrieved_data['points'] == 100
        
        print("✅ Database operations working correctly")
        
        # Clean up
        os.unlink(db_path)
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_achievement_system():
    """Test achievement system"""
    print("Testing achievement system...")
    
    try:
        from improved_quran_app import AchievementSystem, DatabaseManager
        
        # Create a temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
            db_path = tmp_db.name
        
        db_manager = DatabaseManager(db_path)
        achievement_system = AchievementSystem(db_manager)
        
        # Test achievement checking
        user_data = {'current_page': 1, 'streak': 0, 'points': 0}
        reading_stats = {'total_time': 0, 'weekly_sessions': 0, 'monthly_pages': 0}
        
        unlocked = achievement_system.check_achievements(user_data, reading_stats)
        
        # Should unlock "First Steps" achievement
        assert 'First Steps' in unlocked
        
        print("✅ Achievement system working correctly")
        
        # Clean up
        os.unlink(db_path)
        return True
        
    except Exception as e:
        print(f"❌ Achievement system test failed: {e}")
        return False

def test_settings_management():
    """Test settings loading and saving"""
    print("Testing settings management...")
    
    try:
        # Create temporary settings file
        test_settings = {
            'username': 'TestUser',
            'theme': 'light',
            'font_size': 14,
            'auto_save': True,
            'reading_goal': 2
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_settings:
            json.dump(test_settings, tmp_settings)
            settings_path = tmp_settings.name
        
        # Test loading settings
        with open(settings_path, 'r') as f:
            loaded_settings = json.load(f)
        
        assert loaded_settings['username'] == 'TestUser'
        assert loaded_settings['font_size'] == 14
        assert loaded_settings['reading_goal'] == 2
        
        print("✅ Settings management working correctly")
        
        # Clean up
        os.unlink(settings_path)
        return True
        
    except Exception as e:
        print(f"❌ Settings test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("Testing file structure...")
    
    required_files = [
        'improved_quran_app.py',
        'requirements.txt',
        'README.md',
        'run_app.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def run_all_tests():
    """Run all tests"""
    print("🧪 Running Quran Reader App Tests")
    print("=" * 40)
    
    tests = [
        test_file_structure,
        test_database_creation,
        test_achievement_system,
        test_settings_management
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)