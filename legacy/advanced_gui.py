#!/usr/bin/env python3
"""
Advanced Email Organizer GUI
A modern, feature-rich graphical interface for the email organizer toolkit
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import threading
import os
import time
import json
from datetime import datetime

class AdvancedEmailOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🍎 Email Organizer Pro - Advanced")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.current_count = 0
        self.is_running = False
        self.settings = self.load_settings()
        
        self.setup_ui()
        self.update_email_count()
        
    def load_settings(self):
        """Load settings from file"""
        settings_file = os.path.join(os.path.dirname(__file__), 'settings.json')
        default_settings = {
            'auto_refresh': True,
            'refresh_interval': 30,
            'log_level': 'INFO',
            'backup_before_cleanup': True,
            'show_confirmation': True
        }
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    return json.load(f)
            except:
                return default_settings
        return default_settings
        
    def save_settings(self):
        """Save settings to file"""
        settings_file = os.path.join(os.path.dirname(__file__), 'settings.json')
        with open(settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
            
    def setup_ui(self):
        # Create main container
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_container)
        
        # Main content area
        content_frame = tk.Frame(main_container, bg='#2c3e50')
        content_frame.pack(fill='both', expand=True, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(content_frame, bg='#34495e', relief='raised', bd=2)
        left_panel.pack(side='left', fill='y', padx=(0, 5))
        
        # Right panel - Log and status
        right_panel = tk.Frame(content_frame, bg='#34495e', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        self.create_control_panel(left_panel)
        self.create_log_panel(right_panel)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg='#2c3e50')
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Title
        title_label = tk.Label(header_frame, text="🍎 Email Organizer Pro", 
                              font=('Arial', 28, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(side='left')
        
        # Email count display
        count_frame = tk.Frame(header_frame, bg='#2c3e50')
        count_frame.pack(side='right')
        
        self.count_label = tk.Label(count_frame, text="📊 Loading...", 
                                   font=('Arial', 16, 'bold'), bg='#2c3e50', fg='#27ae60')
        self.count_label.pack()
        
        # Refresh button
        refresh_btn = tk.Button(count_frame, text="🔄", command=self.update_email_count,
                               font=('Arial', 12), bg='#3498db', fg='white',
                               relief='flat', cursor='hand2', width=3)
        refresh_btn.pack(pady=(5, 0))
        
    def create_control_panel(self, parent):
        """Create control panel"""
        # Title
        title_label = tk.Label(parent, text="🎛️ Controls", 
                              font=('Arial', 16, 'bold'), bg='#34495e', fg='#ecf0f1')
        title_label.pack(pady=10)
        
        # Quick actions
        quick_frame = tk.LabelFrame(parent, text="🚀 Quick Actions", 
                                   font=('Arial', 12, 'bold'), bg='#34495e', fg='#ecf0f1')
        quick_frame.pack(fill='x', padx=10, pady=5)
        
        # Quick cleanup
        self.quick_btn = tk.Button(quick_frame, text="🚀 Quick Cleanup", 
                                  command=self.quick_cleanup, font=('Arial', 11, 'bold'),
                                  bg='#3498db', fg='white', padx=15, pady=8,
                                  relief='flat', cursor='hand2')
        self.quick_btn.pack(fill='x', padx=5, pady=5)
        
        # Smart cleanup
        self.smart_btn = tk.Button(quick_frame, text="🧠 Smart Cleanup", 
                                  command=self.smart_cleanup, font=('Arial', 11, 'bold'),
                                  bg='#9b59b6', fg='white', padx=15, pady=8,
                                  relief='flat', cursor='hand2')
        self.smart_btn.pack(fill='x', padx=5, pady=5)
        
        # Nuclear cleanup
        self.nuclear_btn = tk.Button(quick_frame, text="💥 Nuclear Cleanup", 
                                    command=self.nuclear_cleanup, font=('Arial', 11, 'bold'),
                                    bg='#e74c3c', fg='white', padx=15, pady=8,
                                    relief='flat', cursor='hand2')
        self.nuclear_btn.pack(fill='x', padx=5, pady=5)
        
        # Mark as read
        self.mark_read_btn = tk.Button(quick_frame, text="📧 Mark All Read", 
                                      command=self.mark_all_read, font=('Arial', 11, 'bold'),
                                      bg='#27ae60', fg='white', padx=15, pady=8,
                                      relief='flat', cursor='hand2')
        self.mark_read_btn.pack(fill='x', padx=5, pady=5)
        
        # Advanced tools
        advanced_frame = tk.LabelFrame(parent, text="🔧 Advanced Tools", 
                                      font=('Arial', 12, 'bold'), bg='#34495e', fg='#ecf0f1')
        advanced_frame.pack(fill='x', padx=10, pady=5)
        
        # Analyze
        self.analyze_btn = tk.Button(advanced_frame, text="🔍 Analyze Inbox", 
                                    command=self.analyze_inbox, font=('Arial', 10),
                                    bg='#f39c12', fg='white', padx=10, pady=5,
                                    relief='flat', cursor='hand2')
        self.analyze_btn.pack(fill='x', padx=5, pady=2)
        
        # Unsubscribe check
        self.unsubscribe_btn = tk.Button(advanced_frame, text="📧 Unsubscribe Check", 
                                        command=self.check_unsubscribe, font=('Arial', 10),
                                        bg='#1abc9c', fg='white', padx=10, pady=5,
                                        relief='flat', cursor='hand2')
        self.unsubscribe_btn.pack(fill='x', padx=5, pady=2)
        
        # Create rules
        self.rules_btn = tk.Button(advanced_frame, text="⚙️ Create Rules", 
                                  command=self.create_rules, font=('Arial', 10),
                                  bg='#34495e', fg='white', padx=10, pady=5,
                                  relief='flat', cursor='hand2')
        self.rules_btn.pack(fill='x', padx=5, pady=2)
        
        # Mass delete
        self.mass_delete_btn = tk.Button(advanced_frame, text="💀 Mass Delete", 
                                        command=self.mass_delete, font=('Arial', 10),
                                        bg='#c0392b', fg='white', padx=10, pady=5,
                                        relief='flat', cursor='hand2')
        self.mass_delete_btn.pack(fill='x', padx=5, pady=2)
        
        # Custom cleanup
        custom_frame = tk.LabelFrame(parent, text="🎯 Custom Cleanup", 
                                    font=('Arial', 12, 'bold'), bg='#34495e', fg='#ecf0f1')
        custom_frame.pack(fill='x', padx=10, pady=5)
        
        # Keyword input
        tk.Label(custom_frame, text="Keywords:", font=('Arial', 10), 
                bg='#34495e', fg='#ecf0f1').pack(anchor='w', padx=5)
        
        self.keyword_entry = tk.Entry(custom_frame, font=('Arial', 10))
        self.keyword_entry.pack(fill='x', padx=5, pady=2)
        self.keyword_entry.insert(0, "newsletter, promotional, marketing")
        
        # Custom cleanup button
        self.custom_btn = tk.Button(custom_frame, text="🎯 Custom Cleanup", 
                                   command=self.custom_cleanup, font=('Arial', 10),
                                   bg='#8e44ad', fg='white', padx=10, pady=5,
                                   relief='flat', cursor='hand2')
        self.custom_btn.pack(fill='x', padx=5, pady=5)
        
        # Progress bar
        progress_frame = tk.Frame(parent, bg='#34495e')
        progress_frame.pack(fill='x', padx=10, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=200)
        self.progress_bar.pack(fill='x')
        
        self.progress_label = tk.Label(progress_frame, text="Ready", 
                                      font=('Arial', 9), bg='#34495e', fg='#bdc3c7')
        self.progress_label.pack()
        
    def create_log_panel(self, parent):
        """Create log panel"""
        # Title
        title_label = tk.Label(parent, text="📋 Activity Log", 
                              font=('Arial', 16, 'bold'), bg='#34495e', fg='#ecf0f1')
        title_label.pack(pady=10)
        
        # Log controls
        log_controls = tk.Frame(parent, bg='#34495e')
        log_controls.pack(fill='x', padx=10, pady=5)
        
        clear_btn = tk.Button(log_controls, text="🗑️ Clear", command=self.clear_log,
                             font=('Arial', 9), bg='#e74c3c', fg='white',
                             relief='flat', cursor='hand2')
        clear_btn.pack(side='left')
        
        save_btn = tk.Button(log_controls, text="💾 Save Log", command=self.save_log,
                            font=('Arial', 9), bg='#27ae60', fg='white',
                            relief='flat', cursor='hand2')
        save_btn.pack(side='left', padx=5)
        
        # Log text
        self.log_text = scrolledtext.ScrolledText(parent, height=20, font=('Courier', 9),
                                                 bg='#2c3e50', fg='#ecf0f1', 
                                                 insertbackground='white',
                                                 selectbackground='#3498db')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=5)
        
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = tk.Frame(parent, bg='#34495e', relief='raised', bd=1)
        status_frame.pack(fill='x', pady=(10, 0))
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = tk.Label(status_frame, textvariable=self.status_var, 
                               font=('Arial', 10), bg='#34495e', fg='#ecf0f1', anchor='w')
        status_label.pack(side='left', padx=10, pady=5)
        
        # Time display
        self.time_var = tk.StringVar()
        time_label = tk.Label(status_frame, textvariable=self.time_var, 
                             font=('Arial', 10), bg='#34495e', fg='#bdc3c7')
        time_label.pack(side='right', padx=10, pady=5)
        
        # Update time
        self.update_time()
        
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_var.set(current_time)
        self.root.after(1000, self.update_time)
        
    def log_message(self, message, level="INFO"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_map = {
            "INFO": "#ecf0f1",
            "SUCCESS": "#27ae60",
            "WARNING": "#f39c12",
            "ERROR": "#e74c3c"
        }
        
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Clear log"""
        self.log_text.delete(1.0, tk.END)
        
    def save_log(self):
        """Save log to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                f.write(self.log_text.get(1.0, tk.END))
            self.log_message("Log saved successfully", "SUCCESS")
            
    def update_progress(self, value, text):
        """Update progress bar"""
        self.progress_var.set(value)
        self.progress_label.config(text=text)
        self.root.update_idletasks()
        
    def update_status(self, status):
        """Update status bar"""
        self.status_var.set(status)
        self.root.update_idletasks()
        
    def update_email_count(self):
        """Update email count display"""
        try:
            result = subprocess.run(['osascript', '-e', 'tell application "Mail" to return count of messages of inbox'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.current_count = int(result.stdout.strip())
                self.count_label.config(text=f"📊 {self.current_count:,} emails")
                self.log_message(f"Email count updated: {self.current_count:,}", "INFO")
            else:
                self.count_label.config(text="📊 Unable to access Mail")
                self.log_message("Unable to access Mail", "ERROR")
        except Exception as e:
            self.count_label.config(text="📊 Error accessing Mail")
            self.log_message(f"Error accessing Mail: {str(e)}", "ERROR")
            
    def run_script(self, script_name, description):
        """Run a script and update progress"""
        if self.is_running:
            messagebox.showwarning("Warning", "Another operation is already running!")
            return
            
        if self.settings.get('show_confirmation', True):
            if not messagebox.askyesno("Confirm", f"Run {description}?"):
                return
                
        self.is_running = True
        self.update_status(f"Running {description}...")
        self.log_message(f"Starting {description}", "INFO")
        
        def run_in_thread():
            try:
                # Update progress
                self.update_progress(10, f"Starting {description}...")
                
                # Run the script
                script_path = os.path.join(os.path.dirname(__file__), script_name)
                if os.path.exists(script_path):
                    result = subprocess.run(['bash', script_path], 
                                          capture_output=True, text=True, timeout=300)
                    
                    self.update_progress(50, f"Running {description}...")
                    
                    if result.returncode == 0:
                        self.update_progress(100, f"{description} completed!")
                        self.log_message(f"{description} completed successfully", "SUCCESS")
                        if result.stdout:
                            self.log_message(f"Output: {result.stdout}")
                    else:
                        self.update_progress(100, f"{description} completed with warnings")
                        self.log_message(f"{description} completed with warnings", "WARNING")
                        if result.stderr:
                            self.log_message(f"Error: {result.stderr}", "ERROR")
                else:
                    self.update_progress(100, f"Script not found: {script_name}")
                    self.log_message(f"Script not found: {script_name}", "ERROR")
                    
                # Update email count
                time.sleep(1)
                self.update_email_count()
                self.update_status("Ready")
                
            except subprocess.TimeoutExpired:
                self.update_progress(100, f"{description} timed out")
                self.log_message(f"{description} timed out", "WARNING")
                self.update_status("Ready")
            except Exception as e:
                self.update_progress(100, f"Error in {description}")
                self.log_message(f"Error in {description}: {str(e)}", "ERROR")
                self.update_status("Ready")
            finally:
                self.is_running = False
                
        # Start thread
        thread = threading.Thread(target=run_in_thread)
        thread.daemon = True
        thread.start()
        
    def quick_cleanup(self):
        """Run quick cleanup"""
        self.run_script("mega_cleanup.sh", "Quick Cleanup")
        
    def smart_cleanup(self):
        """Run smart cleanup"""
        self.run_script("nuclear_cleanup.sh", "Smart Cleanup")
        
    def nuclear_cleanup(self):
        """Run nuclear cleanup"""
        self.run_script("nuclear_cleanup.sh", "Nuclear Cleanup")
        
    def analyze_inbox(self):
        """Analyze inbox"""
        self.run_script("inbox_analyzer.sh", "Inbox Analysis")
        
    def check_unsubscribe(self):
        """Check unsubscribe links"""
        self.run_script("working_unsubscribe.py", "Unsubscribe Check")
        
    def create_rules(self):
        """Create mail rules"""
        self.run_script("create_mail_rules.scpt", "Create Mail Rules")
        
    def mass_delete(self):
        """Mass delete emails"""
        self.run_script("mass_delete.sh", "Mass Delete")
        
    def custom_cleanup(self):
        """Custom cleanup based on keywords"""
        keywords = self.keyword_entry.get().strip()
        if not keywords:
            messagebox.showerror("Error", "Please enter keywords to search for!")
            return
            
        # Create custom script
        custom_script = f"""#!/bin/bash
echo "🎯 Custom Cleanup with keywords: {keywords}"
echo "=================================="
echo ""

CURRENT_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
echo "📊 Starting with: $CURRENT_COUNT emails"
echo ""

# Split keywords and clean each one
IFS=',' read -ra KEYWORDS <<< "{keywords}"
for keyword in "${{KEYWORDS[@]}}"; do
    keyword=$(echo "$keyword" | xargs)  # trim whitespace
    echo "🧹 Cleaning emails with keyword: $keyword"
    
    DELETED=$(osascript -e "tell application \"Mail\"" -e "set inboxMessages to messages of inbox" -e "set deletedCount to 0" -e "repeat with msg in inboxMessages" -e "try" -e "if subject of msg contains \"$keyword\" then" -e "delete msg" -e "set deletedCount to deletedCount + 1" -e "end if" -e "on error" -e "continue" -e "end try" -e "end repeat" -e "return deletedCount" -e "end tell" 2>/dev/null || echo "0")
    
    echo "   ✅ Deleted $DELETED emails with keyword: $keyword"
    
    NEW_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
    echo "   📊 Remaining: $NEW_COUNT emails"
    echo ""
done

FINAL_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
TOTAL_DELETED=$((CURRENT_COUNT - FINAL_COUNT))

echo "🎯 Custom cleanup complete!"
echo "==========================="
echo "📊 Starting emails: $CURRENT_COUNT"
echo "📊 Final emails: $FINAL_COUNT"
echo "🗑️  Total deleted: $TOTAL_DELETED"
"""
        
        # Save custom script
        custom_script_path = os.path.join(os.path.dirname(__file__), 'custom_cleanup.sh')
        with open(custom_script_path, 'w') as f:
            f.write(custom_script)
        os.chmod(custom_script_path, 0o755)
        
        # Run custom script
        self.run_script("custom_cleanup.sh", f"Custom Cleanup ({keywords})")
        
    def mark_all_read(self):
        """Mark all emails as read"""
        if messagebox.askyesno("Confirm", "Mark all inbox emails as read?"):
            self.run_mark_read()
            
    def run_mark_read(self):
        """Run mark all as read"""
        if self.is_running:
            messagebox.showwarning("Warning", "Another operation is already running!")
            return
            
        self.is_running = True
        self.update_status("Marking all emails as read...")
        self.log_message("Starting mark all as read", "INFO")
        
        def run_in_thread():
            try:
                self.update_progress(10, "Marking emails as read...")
                
                # Run the mark as read command
                result = subprocess.run(['osascript', '-e', 'tell application "Mail" to set read status of every message of inbox to true'], 
                                      capture_output=True, text=True, timeout=60)
                
                self.update_progress(50, "Marking emails as read...")
                
                if result.returncode == 0:
                    self.update_progress(100, "Mark as read completed!")
                    self.log_message("All emails marked as read successfully", "SUCCESS")
                else:
                    self.update_progress(100, "Mark as read completed with warnings")
                    self.log_message(f"Mark as read completed with warnings: {result.stderr}", "WARNING")
                    
                # Update email count
                time.sleep(1)
                self.update_email_count()
                self.update_status("Ready")
                
            except subprocess.TimeoutExpired:
                self.update_progress(100, "Mark as read timed out")
                self.log_message("Mark as read timed out", "WARNING")
                self.update_status("Ready")
            except Exception as e:
                self.update_progress(100, "Error in mark as read")
                self.log_message(f"Error in mark as read: {str(e)}", "ERROR")
                self.update_status("Ready")
            finally:
                self.is_running = False
                
        # Start thread
        thread = threading.Thread(target=run_in_thread)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = AdvancedEmailOrganizerGUI(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
