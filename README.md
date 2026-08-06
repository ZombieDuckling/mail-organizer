# 🍎 Mail Organizer Pro

A comprehensive, well-organized solution for managing and cleaning your Apple Mail inbox with intelligent unsubscribe detection and modern GUI interfaces.

## 🚀 Quick Start

### Main Application
```bash
python3 main.py
```

### GUI Interface
```bash
python3 gui/gui_launcher.py
```

### Individual Scripts
```bash
# Quick cleanup (gentle)
python3 scripts/cleanup/quick_cleanup.py

# Smart cleanup (preserves unsubscribe emails)
python3 scripts/cleanup/smart_cleanup.py

# Nuclear cleanup (aggressive)
python3 scripts/cleanup/nuclear_cleanup.py

# Mark all emails as read
python3 scripts/mark_read/mark_all_read.py

# Analyze inbox
python3 scripts/analysis/inbox_analyzer.py

# Check unsubscribe links
python3 scripts/analysis/unsubscribe_analyzer.py
```

## 🎯 Features

### 🧹 Email Cleanup
- **Quick Cleanup**: Gentle removal of promotional emails
- **Smart Cleanup**: Preserves emails with unsubscribe links for manual review
- **Nuclear Cleanup**: Aggressive cleanup for maximum inbox reduction
- **Age-based Cleanup**: Remove emails older than specified days
- **Attachment Cleanup**: Remove emails with attachments (often promotional)

### 🔍 Intelligent Analysis
- **Inbox Analysis**: Comprehensive statistics and insights
- **Unsubscribe Detection**: Find and extract unsubscribe links
- **Sender Analysis**: Group emails by sender for better organization
- **Content Analysis**: Detect promotional content patterns

### 🖥️ Modern Interfaces
- **Tkinter GUI**: Beautiful, modern desktop interface
- **Command Line**: Full-featured terminal interface
- **Web GUI**: Browser-based interface (coming soon)

### ⚙️ Automation
- **Mail Rules**: Automatic creation of Mail.app rules
- **Scheduled Cleanup**: Regular maintenance capabilities
- **Smart Preservation**: Keep important emails while cleaning spam

## 📁 Project Structure

```
mail-organizer/
├── main.py                    # Main entry point
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── config/                    # Configuration
│   ├── settings.py           # Application settings
│   └── keywords.py           # Email detection patterns
├── core/                      # Core functionality
│   ├── mail_manager.py       # Mail operations
│   ├── cleanup_engine.py     # Cleanup logic
│   ├── unsubscribe_detector.py # Unsubscribe handling
│   └── mail_rules.py         # Mail rules management
├── gui/                       # User interfaces
│   ├── tkinter_gui.py        # Desktop GUI
│   └── gui_launcher.py       # GUI launcher
├── scripts/                   # Individual scripts
│   ├── cleanup/              # Cleanup scripts
│   ├── mark_read/            # Mark as read scripts
│   └── analysis/             # Analysis scripts
├── utils/                     # Utilities
│   ├── applescript_runner.py # AppleScript execution
│   ├── logger.py             # Logging system
│   └── file_utils.py         # File operations
├── legacy/                    # Old files (backup)
└── tests/                     # Test files (future)
```

## 🛠️ Installation

1. **Clone or download** this repository
2. **Ensure Python 3.6+** is installed
3. **No external dependencies** required (uses only Python standard library)
4. **Ensure Apple Mail** is installed and accessible

## ✅ Development Checks

```bash
python3 -m compileall -q core config utils tests
python3 -m pytest tests/ -q
```

The test suite covers pure parsing and safety logic only; it does not launch Mail.app or execute AppleScript.

## 📋 Usage Examples

### Command Line Interface
```bash
# Start the main application
python3 main.py

# Choose from the interactive menu:
# 1. Quick Cleanup
# 2. Smart Cleanup  
# 3. Nuclear Cleanup
# 4. Mark All as Read
# 5. Analyze Inbox
# 6. Check Unsubscribe Links
# 7. Create Mail Rules
# 8. Launch GUI
```

### GUI Interface
```bash
# Launch the modern GUI
python3 gui/gui_launcher.py

# Or launch directly
python3 gui/tkinter_gui.py
```

### Individual Scripts
```bash
# Quick cleanup with confirmation
python3 scripts/cleanup/quick_cleanup.py

# Smart cleanup preserving unsubscribe emails
python3 scripts/cleanup/smart_cleanup.py

# Aggressive nuclear cleanup
python3 scripts/cleanup/nuclear_cleanup.py

# Mark all emails as read
python3 scripts/mark_read/mark_all_read.py

# Comprehensive inbox analysis
python3 scripts/analysis/inbox_analyzer.py

# Unsubscribe link analysis
python3 scripts/analysis/unsubscribe_analyzer.py
```

## 🔧 Configuration

### Settings
The application uses a configuration system located in `config/settings.py`:

- **Auto-refresh**: Automatically update email count
- **Refresh interval**: How often to refresh (seconds)
- **Log level**: Logging verbosity
- **Backup before cleanup**: Create backups before operations
- **Show confirmations**: Ask for confirmation before operations

### Keywords
Email detection patterns are defined in `config/keywords.py`:

- **Promotional keywords**: Subject and sender patterns
- **Unsubscribe patterns**: Link detection regex
- **Cleanup levels**: Predefined cleanup intensities
- **Age thresholds**: Time-based cleanup options

## 📊 What It Detects

### Promotional Keywords
**Subject patterns**: unsubscribe, promotional, marketing, newsletter, offers, sale, discount, deal, limited time, exclusive, special offer, clearance, save, percent off, free shipping, buy now, shop now, act now, don't miss, last chance, flash sale, daily deal, weekly special, monthly offer

**Sender patterns**: noreply, no-reply, marketing, promo, offers, deals, newsletter, notifications, alerts, updates, digest

### Unsubscribe Link Detection
- HTTP/HTTPS unsubscribe URLs
- Mailto unsubscribe links
- Various HTML link formats
- Safety validation for URLs

## ⚠️ Safety Features

- **Emails go to trash**, not permanently deleted
- **Unsubscribe emails are preserved** in smart mode
- **URL safety validation** for unsubscribe links
- **Manual review options** for unsubscribe links
- **Confirmation dialogs** for destructive operations
- **Comprehensive logging** of all operations

## 🔐 Permissions

You may need to grant Terminal permission to control Mail:
1. Go to **System Preferences** > **Security & Privacy** > **Privacy** > **Automation**
2. Add **Terminal** and allow it to control **Mail**
3. Restart Terminal if needed

## 🆘 Troubleshooting

### Permission Errors
1. Check System Preferences > Security & Privacy > Privacy > Automation
2. Ensure Terminal has permission to control Mail
3. Try running the script again

### Mail Not Responding
1. Make sure Mail is running: `open -a Mail`
2. Wait a few seconds and try again
3. Check if Mail is busy with other operations

### Python Issues
1. Ensure Python 3.6+ is installed: `python3 --version`
2. Check that all files are in the correct locations
3. Verify AppleScript support is available

## 📈 Results

After running the organizer, you'll see:
- **Number of emails deleted**
- **Number of emails with unsubscribe links found**
- **List of senders with unsubscribe options**
- **Detailed reports** (if requested)
- **Comprehensive statistics**

## 🎉 Benefits

- **Cleaner inbox**: Remove promotional emails automatically
- **Time saving**: No more manual email sorting
- **Smart preservation**: Keep important emails with unsubscribe options
- **Better organization**: Understand your email patterns
- **Automation**: Set up rules for future email management
- **Safety**: All operations are reversible

## 🔄 Migration from Old Version

If you're upgrading from the old version:
1. **Old files are preserved** in the `legacy/` directory
2. **New structure** is more organized and maintainable
3. **Same functionality** with better organization
4. **Improved error handling** and logging
5. **Modern GUI** with better user experience

## 🚀 Future Enhancements

- **Web GUI**: Browser-based interface
- **Scheduling**: Automatic cleanup scheduling
- **Advanced Rules**: More sophisticated mail rules
- **Statistics**: Long-term email statistics
- **Integration**: Integration with other email clients
- **Machine Learning**: Smart email classification

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

---

**Made with ❤️ for macOS users who want a cleaner inbox**