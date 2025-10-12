#!/usr/bin/env python3
"""
Email Organizer GUI
A modern graphical interface for the email organizer toolkit
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import os
import time

class EmailOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🍎 Email Organizer Pro")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.current_count = 0
        self.is_running = False
        
        self.setup_ui()
        self.update_email_count()
        
    def setup_ui(self):
        # Main title
        title_frame = tk.Frame(self.root, bg='#f0f0f0')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, text="🍎 Email Organizer Pro", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Clean your inbox with ease", 
                                 font=('Arial', 12), bg='#f0f0f0', fg='#7f8c8d')
        subtitle_label.pack()
        
        # Email count display
        count_frame = tk.Frame(self.root, bg='#f0f0f0')
        count_frame.pack(pady=20)
        
        self.count_label = tk.Label(count_frame, text="📊 Loading email count...", 
                                   font=('Arial', 14, 'bold'), bg='#f0f0f0', fg='#27ae60')
        self.count_label.pack()
        
        # Progress bar
        self.progress_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.progress_frame.pack(pady=10, padx=20, fill='x')
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.pack()
        
        self.progress_label = tk.Label(self.progress_frame, text="Ready to organize", 
                                      font=('Arial', 10), bg='#f0f0f0', fg='#7f8c8d')
        self.progress_label.pack()
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg='#f0f0f0')
        buttons_frame.pack(pady=20)
        
        # Quick cleanup button
        self.quick_btn = tk.Button(buttons_frame, text="🚀 Quick Cleanup", 
                                  command=self.quick_cleanup, font=('Arial', 12, 'bold'),
                                  bg='#3498db', fg='white', padx=20, pady=10,
                                  relief='flat', cursor='hand2')
        self.quick_btn.pack(side='left', padx=10)
        
        # Smart cleanup button
        self.smart_btn = tk.Button(buttons_frame, text="🧠 Smart Cleanup", 
                                  command=self.smart_cleanup, font=('Arial', 12, 'bold'),
                                  bg='#9b59b6', fg='white', padx=20, pady=10,
                                  relief='flat', cursor='hand2')
        self.smart_btn.pack(side='left', padx=10)
        
        # Nuclear cleanup button
        self.nuclear_btn = tk.Button(buttons_frame, text="💥 Nuclear Cleanup", 
                                    command=self.nuclear_cleanup, font=('Arial', 12, 'bold'),
                                    bg='#e74c3c', fg='white', padx=20, pady=10,
                                    relief='flat', cursor='hand2')
        self.nuclear_btn.pack(side='left', padx=10)
        
        # Mark as read button
        self.mark_read_btn = tk.Button(buttons_frame, text="📧 Mark All Read", 
                                      command=self.mark_all_read, font=('Arial', 12, 'bold'),
                                      bg='#27ae60', fg='white', padx=20, pady=10,
                                      relief='flat', cursor='hand2')
        self.mark_read_btn.pack(side='left', padx=10)
        
        # Advanced options frame
        advanced_frame = tk.LabelFrame(self.root, text="🔧 Advanced Options", 
                                      font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        advanced_frame.pack(pady=20, padx=20, fill='x')
        
        # Advanced buttons
        adv_buttons_frame = tk.Frame(advanced_frame, bg='#f0f0f0')
        adv_buttons_frame.pack(pady=10)
        
        self.analyze_btn = tk.Button(adv_buttons_frame, text="🔍 Analyze Inbox", 
                                    command=self.analyze_inbox, font=('Arial', 10),
                                    bg='#f39c12', fg='white', padx=15, pady=5,
                                    relief='flat', cursor='hand2')
        self.analyze_btn.pack(side='left', padx=5)
        
        self.unsubscribe_btn = tk.Button(adv_buttons_frame, text="📧 Unsubscribe Check", 
                                        command=self.check_unsubscribe, font=('Arial', 10),
                                        bg='#1abc9c', fg='white', padx=15, pady=5,
                                        relief='flat', cursor='hand2')
        self.unsubscribe_btn.pack(side='left', padx=5)
        
        self.rules_btn = tk.Button(adv_buttons_frame, text="⚙️ Create Rules", 
                                  command=self.create_rules, font=('Arial', 10),
                                  bg='#34495e', fg='white', padx=15, pady=5,
                                  relief='flat', cursor='hand2')
        self.rules_btn.pack(side='left', padx=5)
        
        self.mass_delete_btn = tk.Button(adv_buttons_frame, text="💀 Mass Delete", 
                                        command=self.mass_delete, font=('Arial', 10),
                                        bg='#c0392b', fg='white', padx=15, pady=5,
                                        relief='flat', cursor='hand2')
        self.mass_delete_btn.pack(side='left', padx=5)
        
        # Log output
        log_frame = tk.LabelFrame(self.root, text="📋 Activity Log", 
                                 font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        log_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, font=('Courier', 9),
                                                 bg='#2c3e50', fg='#ecf0f1', insertbackground='white')
        self.log_text.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             font=('Arial', 10), bg='#34495e', fg='white', anchor='w')
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
            result = subprocess.run(['osascript', '-e', 'tell application "Mail" to return count of messages of inbox'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.current_count = int(result.stdout.strip())
                self.count_label.config(text=f"📊 Current inbox: {self.current_count:,} emails")
            else:
                self.count_label.config(text="📊 Unable to access Mail")
        except Exception as e:
            self.count_label.config(text="📊 Error accessing Mail")
            
    def run_script(self, script_name, description):
        """Run a script and update progress"""
        if self.is_running:
            messagebox.showwarning("Warning", "Another operation is already running!")
            return
            
        self.is_running = True
        self.update_status(f"Running {description}...")
        self.log_message(f"Starting {description}")
        
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
                        self.log_message(f"✅ {description} completed successfully")
                        self.log_message(f"Output: {result.stdout}")
                    else:
                        self.update_progress(100, f"{description} completed with warnings")
                        self.log_message(f"⚠️ {description} completed with warnings")
                        self.log_message(f"Error: {result.stderr}")
                else:
                    self.update_progress(100, f"Script not found: {script_name}")
                    self.log_message(f"❌ Script not found: {script_name}")
                    
                # Update email count
                time.sleep(1)
                self.update_email_count()
                self.update_status("Ready")
                
            except subprocess.TimeoutExpired:
                self.update_progress(100, f"{description} timed out")
                self.log_message(f"⏰ {description} timed out")
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
            self.run_script("mega_cleanup.sh", "Quick Cleanup")
            
    def smart_cleanup(self):
        """Run smart cleanup"""
        if messagebox.askyesno("Confirm", "This will preserve emails with unsubscribe links. Continue?"):
            self.run_script("nuclear_cleanup.sh", "Smart Cleanup")
            
    def nuclear_cleanup(self):
        """Run nuclear cleanup"""
        if messagebox.askyesno("Confirm", "This is an aggressive cleanup. Continue?"):
            self.run_script("nuclear_cleanup.sh", "Nuclear Cleanup")
            
    def analyze_inbox(self):
        """Analyze inbox"""
        self.run_script("inbox_analyzer.sh", "Inbox Analysis")
        
    def check_unsubscribe(self):
        """Check unsubscribe links"""
        self.run_script("working_unsubscribe.py", "Unsubscribe Check")
        
    def create_rules(self):
        """Create mail rules"""
        if messagebox.askyesno("Confirm", "This will create automatic mail rules. Continue?"):
            self.run_script("create_mail_rules.scpt", "Create Mail Rules")
            
    def mass_delete(self):
        """Mass delete emails"""
        if messagebox.askyesno("Confirm", "This will delete emails in large batches. This is DANGEROUS! Continue?"):
            self.run_script("mass_delete.sh", "Mass Delete")
            
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
        self.log_message("Starting mark all as read")
        
        def run_in_thread():
            try:
                self.update_progress(10, "Marking emails as read...")
                
                # Run the mark as read command
                result = subprocess.run(['osascript', '-e', 'tell application "Mail" to set read status of every message of inbox to true'], 
                                      capture_output=True, text=True, timeout=60)
                
                self.update_progress(50, "Marking emails as read...")
                
                if result.returncode == 0:
                    self.update_progress(100, "Mark as read completed!")
                    self.log_message("✅ All emails marked as read successfully")
                else:
                    self.update_progress(100, "Mark as read completed with warnings")
                    self.log_message(f"⚠️ Mark as read completed with warnings: {result.stderr}")
                    
                # Update email count
                time.sleep(1)
                self.update_email_count()
                self.update_status("Ready")
                
            except subprocess.TimeoutExpired:
                self.update_progress(100, "Mark as read timed out")
                self.log_message("⏰ Mark as read timed out")
                self.update_status("Ready")
            except Exception as e:
                self.update_progress(100, "Error in mark as read")
                self.log_message(f"❌ Error in mark as read: {str(e)}")
                self.update_status("Ready")
            finally:
                self.is_running = False
                
        # Start thread
        thread = threading.Thread(target=run_in_thread)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = EmailOrganizerGUI(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
