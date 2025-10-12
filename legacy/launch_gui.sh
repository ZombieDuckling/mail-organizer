#!/bin/bash

echo "🍎 Email Organizer GUI Launcher"
echo "==============================="
echo ""

echo "Choose your GUI version:"
echo "1. Simple GUI (email_organizer_gui.py)"
echo "2. Advanced GUI (advanced_gui.py)"
echo ""

read -p "Enter your choice (1-2): " choice

case $choice in
    1)
        echo "🚀 Launching Simple GUI..."
        python3 email_organizer_gui.py
        ;;
    2)
        echo "🚀 Launching Advanced GUI..."
        python3 advanced_gui.py
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
