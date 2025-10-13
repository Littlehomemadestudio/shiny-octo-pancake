# Enhanced Quran Reader App

A comprehensive desktop application for daily Quran reading with advanced features including statistics tracking, achievements, community chat, and more.

## Features

### Core Reading Features
- **Daily Reading Tracker**: Track your daily Quran reading progress
- **Reading Timer**: Built-in timer to track reading sessions
- **Progress Tracking**: Visual progress bars and statistics
- **Page Navigation**: Easy navigation through Quran pages
- **Reading Streaks**: Track consecutive days of reading

### Advanced Features
- **SQLite Database**: Persistent data storage for all user data
- **Achievement System**: Unlock achievements based on reading milestones
- **Statistics Dashboard**: Comprehensive reading analytics
- **Bookmark System**: Save and manage bookmarks with notes
- **Community Chat**: Connect with other readers (simulated)
- **Settings Management**: Customizable user preferences
- **Logging System**: Detailed logging for debugging and monitoring

### User Interface
- **Modern Design**: Clean, responsive interface with Islamic color scheme
- **Scrollable Content**: Handle large amounts of content efficiently
- **Real-time Updates**: Live updates of statistics and progress
- **Settings Panel**: Easy access to user preferences

## Installation

1. **Clone or download the application files**
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python improved_quran_app.py
   ```

## Usage

### Getting Started
1. Launch the application
2. The app will automatically create a database and load your data
3. Click "Start Reading" to begin a reading session
4. Read for at least 5 minutes to unlock the "Next Page" button
5. Use the "Next Page" button to advance and earn points

### Features Guide

#### Reading Sessions
- **Start Reading**: Begin a timed reading session
- **Pause/Resume**: Pause and resume your reading session
- **Next Page**: Advance to the next page (unlocked after 5 minutes of reading)
- **Reading Timer**: Track your session duration

#### Statistics & Progress
- **Progress Bar**: Visual representation of your overall progress
- **Daily Goals**: Set and track daily reading goals
- **Streak Counter**: Track consecutive days of reading
- **Points System**: Earn points for reading sessions
- **Detailed Statistics**: View comprehensive reading analytics

#### Bookmarks
- **Add Bookmarks**: Bookmark any page with optional notes
- **View Bookmarks**: Access your bookmarked pages
- **Bookmark Management**: Organize and manage your bookmarks

#### Community Features
- **Chat System**: Connect with other readers (simulated)
- **Message History**: Persistent chat message storage
- **Real-time Updates**: Live chat updates

#### Settings
- **Username**: Set your display name
- **Daily Goals**: Configure daily reading targets
- **Font Size**: Adjust text size for better readability
- **Auto-save**: Automatic data saving

#### Achievements
The app includes several achievements that unlock automatically:
- **First Steps**: Read your first page
- **Weekly Warrior**: Maintain a 7-day reading streak
- **Monthly Master**: Maintain a 30-day reading streak
- **Century Reader**: Read 100 pages
- **Halfway Hero**: Read 500 pages
- **Quran Master**: Complete the entire Quran
- **Time Master**: Spend 100 hours reading

## Database Schema

The application uses SQLite with the following tables:
- `user_data`: User progress and statistics
- `reading_sessions`: Individual reading session records
- `bookmarks`: User bookmarks with notes
- `chat_messages`: Community chat messages
- `achievements`: Achievement definitions and unlock status

## File Structure

```
quran_app/
├── improved_quran_app.py    # Main application file
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── quran_app.db           # SQLite database (created automatically)
├── settings.json          # User settings (created automatically)
└── quran_app.log          # Application logs (created automatically)
```

## Technical Features

### Error Handling
- Comprehensive error handling throughout the application
- Graceful handling of database errors
- User-friendly error messages
- Detailed logging for debugging

### Data Persistence
- SQLite database for reliable data storage
- Automatic data saving
- Backup and recovery capabilities
- Data integrity checks

### Performance
- Efficient database queries
- Optimized UI updates
- Memory management
- Responsive interface

### Security
- Input validation
- SQL injection prevention
- Safe file handling
- Error logging without sensitive data exposure

## Customization

### Adding New Achievements
Edit the `AchievementSystem` class to add new achievements:

```python
self.achievements = {
    'new_achievement': {
        'name': 'Achievement Name',
        'description': 'Achievement description',
        'points_required': 0
    }
}
```

### Modifying UI Colors
Update the color scheme in the `create_widgets` methods:

```python
# Example: Change header color
header_frame = tk.Frame(parent, bg='#your_color')
```

### Adding New Statistics
Extend the `get_reading_stats` method in `DatabaseManager`:

```python
def get_reading_stats(self) -> Dict:
    # Add your new statistics here
    pass
```

## Troubleshooting

### Common Issues

1. **Database Errors**: Delete `quran_app.db` to reset the database
2. **Settings Issues**: Delete `settings.json` to reset settings
3. **UI Problems**: Check the log file `quran_app.log` for errors
4. **Performance Issues**: Restart the application

### Log Files
Check `quran_app.log` for detailed error information and debugging data.

## Future Enhancements

Potential improvements for future versions:
- Audio recitation support
- Verse highlighting and commentary
- Multi-language support
- Cloud synchronization
- Mobile app version
- Real-time community features
- Advanced analytics and insights
- Integration with Islamic calendar
- Prayer time reminders

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions:
1. Check the troubleshooting section
2. Review the log files
3. Create an issue in the project repository

---

**May Allah accept our efforts in spreading the knowledge of the Quran. Ameen.**