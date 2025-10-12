#!/bin/bash

echo "🖥️  Creating Desktop Shortcut for Email Organizer GUI"
echo "====================================================="
echo ""

# Create desktop shortcut
DESKTOP_PATH="$HOME/Desktop"
SHORTCUT_PATH="$DESKTOP_PATH/Email Organizer Pro.command"

# Create the shortcut script
cat > "$SHORTCUT_PATH" << 'SHORTCUT_EOF'
#!/bin/bash

# Change to the mail organizer directory
cd ~/mail-organizer

# Launch the GUI launcher
./launch_gui.sh
SHORTCUT_EOF

# Make it executable
chmod +x "$SHORTCUT_PATH"

echo "✅ Desktop shortcut created: $SHORTCUT_PATH"
echo ""
echo "🖱️  You can now double-click 'Email Organizer Pro' on your Desktop to launch the GUI!"
echo ""
echo "📁 Or run from terminal:"
echo "   cd ~/mail-organizer"
echo "   ./launch_gui.sh"
