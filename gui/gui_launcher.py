#!/usr/bin/env python3
"""
GUI launcher for Mail Organizer
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gui.tkinter_gui import main as tkinter_main
from utils.logger import setup_logger

def main():
    """Main launcher function"""
    logger = setup_logger('gui_launcher')
    
    print("🍎 Mail Organizer GUI Launcher")
    print("==============================")
    print()
    
    print("Available GUI options:")
    print("1. Tkinter GUI (Recommended)")
    print("2. Web GUI (Coming Soon)")
    print()
    
    try:
        choice = input("Enter your choice (1-2): ").strip()
    except KeyboardInterrupt:
        print("\n❌ Launch cancelled.")
        return 0
    
    if choice == "1":
        print("🚀 Launching Tkinter GUI...")
        try:
            tkinter_main()
        except Exception as e:
            print(f"❌ Failed to launch Tkinter GUI: {e}")
            return 1
    
    elif choice == "2":
        print("⚠️  Web GUI is not yet implemented in the new structure.")
        print("   Please use the Tkinter GUI for now.")
        return 1
    
    else:
        print("❌ Invalid choice. Please run the launcher again.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
