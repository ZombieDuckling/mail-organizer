#!/usr/bin/env python3
"""
Modern Tkinter GUI for Mail Organizer
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime
import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.mail_manager import MailManager
from core.cleanup_engine import CleanupEngine
from core.unsubscribe_detector import UnsubscribeDetector
from core.mail_rules import MailRulesManager
from utils.logger import setup_logger
from config.settings import settings

class MailOrganizerGUI:
    """Modern GUI for Mail Organizer"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🍎 Mail Organizer Pro")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Initialize components
        self.mail_manager = MailManager()
        self.cleanup_engine = CleanupEngine()
        self.unsubscribe_detector = UnsubscribeDetector()
        self.mail_rules_manager = MailRulesManager()
        
        # Variables
        self.current_count = 0
        self.is_running = False
        self.logger = setup_logger('gui')
        
        self.setup_ui()
        self.update_email_count()
        
        # Auto-refresh if enabled
        if settings.get('auto_refresh', True):
            self.auto_refresh()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, text="🍎 Mail Organizer Pro", 
                              font=('Arial', 28, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Clean your inbox with ease", 
                                 font=('Arial', 14), bg='#2c3e50', fg='#bdc3c7')
        subtitle_label.pack()
        
        # Email count display
        count_frame = tk.Frame(self.root, bg='#2c3e50')
        count_frame.pack(pady=20)
        
        self.count_label = tk.Label(count_frame, text="📊 Loading email count...", 
                                   font=('Arial', 16, 'bold'), bg='#2c3e50', fg='#27ae60')
        self.count_label.pack()
        
        # Progress bar
        self.progress_frame = tk.Frame(self.root, bg='#2c3e50')
        self.progress_frame.pack(pady=10, padx=20, fill='x')
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, 
                                           maximum=100, length=500, style='TProgressbar')
        self.progress_bar.pack()
        
        self.progress_label = tk.Label(self.progress_frame, text="Ready to organize", 
                                      font=('Arial', 10), bg='#2c3e50', fg='#bdc3c7')
        self.progress_label.pack()
        
        # Main buttons frame
        buttons_frame = tk.Frame(self.root, bg='#2c3e50')
        buttons_frame.pack(pady=20)
        
        # Quick actions
        quick_frame = tk.LabelFrame(buttons_frame, text="🚀 Quick Actions", 
                                   font=('Arial', 12, 'bold'), bg='#34495e', fg='#ecf0f1')
        quick_frame.pack(pady=10, padx=10, fill='x')
        
        quick_buttons = tk.Frame(quick_frame, bg='#34495e')
        quick_buttons.pack(pady=10)
        
        self.quick_btn = tk.Button(quick_buttons, text="🚀 Quick Cleanup", 
                                  command=self.quick_cleanup, font=('Arial', 11, 'bold'),
                                  bg='#3498db', fg='white', padx=15, pady=8,
                                  relief='flat', cursor='hand2')
        self.quick_btn.pack(side='left', padx=5)
        
        self.smart_btn = tk.Button(quick_buttons, text="🧠 Smart Cleanup", 
                                  command=self.smart_cleanup, font=('Arial', 11, 'bold'),
                                  bg='#9b59b6', fg='white', padx=15, pady=8,
                                  relief='flat', cursor='hand2')
        self.smart_btn.pack(side='left', padx=5)
        
        self.nuclear_btn = tk.Button(quick_buttons, text="💥 Nuclear Cleanup", 
                                    command=self.nuclear_cleanup, font=('Arial', 11, 'bold'),
                                    bg='#e74c3c', fg='white', padx=15, pady=8,
                                    relief='flat', cursor='hand2')
        self.nuclear_btn.pack(side='left', padx=5)
        
        self.mark_read_btn = tk.Button(quick_buttons, text="📧 Mark All Read", 
                                      command=self.mark_all_read, font=('Arial', 11, 'bold'),
                                      bg='#27ae60', fg='white', padx=15, pady=8,
                                      relief='flat', cursor='hand2')
        self.mark_read_btn.pack(side='left', padx=5)
        
        # Advanced tools
        advanced_frame = tk.LabelFrame(buttons_frame, text="🔧 Advanced Tools", 
                                      font=('Arial', 12, 'bold'), bg='#34495e', fg='#ecf0f1')
        advanced_frame.pack(pady=10, padx=10, fill='x')
        
        adv_buttons = tk.Frame(advanced_frame, bg='#34495e')
        adv_buttons.pack(pady=10)
        
        self.analyze_btn = tk.Button(adv_buttons, text="🔍 Analyze Inbox", 
                                    command=self.analyze_inbox, font=('Arial', 10),
                                    bg='#f39c12', fg='white', padx=12, pady=6,
                                    relief='flat', cursor='hand2')
        self.analyze_btn.pack(side='left', padx=3)
        
        self.unsubscribe_btn = tk.Button(adv_buttons, text="🔗 Unsubscribe Check", 
                                        command=self.check_unsubscribe, font=('Arial', 10),
                                        bg='#1abc9c', fg='white', padx=12, pady=6,
                                        relief='flat', cursor='hand2')
        self.unsubscribe_btn.pack(side='left', padx=3)
        
        self.rules_btn = tk.Button(adv_buttons, text="⚙️ Create Rules", 
                                  command=self.create_rules, font=('Arial', 10),
                                  bg='#34495e', fg='white', padx=12, pady=6,
                                  relief='flat', cursor='hand2')
        self.rules_btn.pack(side='left', padx=3)
        
        # Log output
        log_frame = tk.LabelFrame(self.root, text="📋 Activity Log", 
                                 font=('Arial', 12, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        log_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, font=('Courier', 9),
                                                 bg='#34495e', fg='#ecf0f1', insertbackground='white')
        self.log_text.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             font=('Arial', 10), bg='#34495e', fg='#ecf0f1', anchor='w')
        status_bar.pack(side='bottom', fill='x')
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
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
            count = self.mail_manager.get_inbox_count()
            self.current_count = count
            self.count_label.config(text=f"📊 Current inbox: {count:,} emails")
        except Exception as e:
            self.count_label.config(text="📊 Unable to access Mail")
            self.log_message(f"Error accessing Mail: {e}")
    
    def auto_refresh(self):
        """Auto-refresh email count"""
        if settings.get('auto_refresh', True):
            self.update_email_count()
            interval = settings.get('refresh_interval', 30) * 1000  # Convert to milliseconds
            self.root.after(interval, self.auto_refresh)
    
    def run_operation(self, operation_func, description):
        """Run an operation in a separate thread"""
        if self.is_running:
            messagebox.showwarning("Warning", "Another operation is already running!")
            return
        
        self.is_running = True
        self.update_status(f"Running {description}...")
        self.log_message(f"Starting {description}")
        
        def run_in_thread():
            try:
                self.update_progress(10, f"Starting {description}...")
                result = operation_func()
                
                if result.get('success', True):
                    self.update_progress(100, f"{description} completed!")
                    self.log_message(f"✅ {description} completed successfully")
                    
                    # Log specific results
                    if 'deleted_count' in result:
                        self.log_message(f"   Deleted {result['deleted_count']:,} emails")
                    if 'emails_found' in result:
                        self.log_message(f"   Found {result['emails_found']} emails")
                else:
                    self.update_progress(100, f"{description} completed with warnings")
                    self.log_message(f"⚠️ {description} completed with warnings")
                    if 'error' in result:
                        self.log_message(f"   Error: {result['error']}")
                
                # Update email count
                time.sleep(1)
                self.update_email_count()
                self.update_status("Ready")
                
            except Exception as e:
                self.update_progress(100, f"Error in {description}")
                self.log_message(f"❌ Error in {description}: {str(e)}")
                self.update_status("Ready")
            finally:
                self.is_running = False
        
        # Start thread
        thread = threading.Thread(target=run_in_thread)
        thread.daemon = True
        thread.start()
    
    def quick_cleanup(self):
        """Run quick cleanup"""
        if messagebox.askyesno("Confirm", "This will delete promotional emails. Continue?"):
            self.run_operation(
                lambda: self.cleanup_engine.cleanup_by_level('gentle', preserve_unsubscribe=True),
                "Quick Cleanup"
            )
    
    def smart_cleanup(self):
        """Run smart cleanup"""
        if messagebox.askyesno("Confirm", "This will preserve emails with unsubscribe links. Continue?"):
            self.run_operation(
                lambda: self.cleanup_engine.cleanup_by_level('moderate', preserve_unsubscribe=True),
                "Smart Cleanup"
            )
    
    def nuclear_cleanup(self):
        """Run nuclear cleanup"""
        if messagebox.askyesno("Confirm", "This is an aggressive cleanup that will delete many emails. Continue?"):
            self.run_operation(
                lambda: self.cleanup_engine.cleanup_by_level('nuclear', preserve_unsubscribe=False),
                "Nuclear Cleanup"
            )
    
    def mark_all_read(self):
        """Mark all emails as read"""
        if messagebox.askyesno("Confirm", "Mark all inbox emails as read?"):
            self.run_operation(
                lambda: {'success': self.mail_manager.mark_all_read()},
                "Mark All Read"
            )
    
    def analyze_inbox(self):
        """Analyze inbox"""
        self.run_operation(
            lambda: self.mail_manager.analyze_inbox(),
            "Inbox Analysis"
        )
    
    def check_unsubscribe(self):
        """Check unsubscribe links"""
        self.run_operation(
            lambda: self.unsubscribe_detector.process_unsubscribe_emails('analyze'),
            "Unsubscribe Check"
        )
    
    def create_rules(self):
        """Create mail rules"""
        if messagebox.askyesno("Confirm", "This will create automatic mail rules. Continue?"):
            self.run_operation(
                lambda: self.mail_rules_manager.create_comprehensive_rules(),
                "Create Mail Rules"
            )

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = MailOrganizerGUI(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
