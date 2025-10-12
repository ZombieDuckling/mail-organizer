#!/usr/bin/env python3
"""
Mark All Emails as Read GUI
A simple GUI to mark all emails as read
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time

class MarkReadGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📧 Mark All Emails as Read")
        self.root.geometry("500x400")
        self.root.configure(bg='#2c3e50')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50')
        header_frame.pack(pady=20)
        
        title_label = tk.Label(header_frame, text="📧 Mark All Emails as Read", 
                              font=('Arial', 24, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Mark all your emails as read with one click", 
                                 font=('Arial', 12), bg='#2c3e50', fg='#bdc3c7')
        subtitle_label.pack()
        
        # Options frame
        options_frame = tk.LabelFrame(self.root, text="📋 Options", 
                                     font=('Arial', 14, 'bold'), bg='#34495e', fg='#ecf0f1')
        options_frame.pack(pady=20, padx=20, fill='x')
        
        # Inbox only button
        self.inbox_btn = tk.Button(options_frame, text="📥 Mark Inbox as Read", 
                                  command=self.mark_inbox_read, font=('Arial', 12, 'bold'),
                                  bg='#3498db', fg='white', padx=20, pady=15,
                                  relief='flat', cursor='hand2')
        self.inbox_btn.pack(fill='x', padx=10, pady=10)
        
        # All mailboxes button
        self.all_btn = tk.Button(options_frame, text="📁 Mark All Mailboxes as Read", 
                                command=self.mark_all_read, font=('Arial', 12, 'bold'),
                                bg='#9b59b6', fg='white', padx=20, pady=15,
                                relief='flat', cursor='hand2')
        self.all_btn.pack(fill='x', padx=10, pady=10)
        
        # Quick mark button
        self.quick_btn = tk.Button(options_frame, text="⚡ Quick Mark Inbox", 
                                  command=self.quick_mark, font=('Arial', 12, 'bold'),
                                  bg='#27ae60', fg='white', padx=20, pady=15,
                                  relief='flat', cursor='hand2')
        self.quick_btn.pack(fill='x', padx=10, pady=10)
        
        # Progress bar
        progress_frame = tk.Frame(self.root, bg='#2c3e50')
        progress_frame.pack(pady=20, padx=20, fill='x')
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.pack()
        
        self.progress_label = tk.Label(progress_frame, text="Ready", 
                                      font=('Arial', 10), bg='#2c3e50', fg='#bdc3c7')
        self.progress_label.pack()
        
        # Status
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = tk.Label(self.root, textvariable=self.status_var, 
                               font=('Arial', 10), bg='#34495e', fg='#ecf0f1')
        status_label.pack(side='bottom', fill='x', pady=10)
        
    def update_progress(self, value, text):
        """Update progress bar"""
        self.progress_var.set(value)
        self.progress_label.config(text=text)
        self.root.update_idletasks()
        
    def update_status(self, status):
        """Update status"""
        self.status_var.set(status)
        self.root.update_idletasks()
        
    def mark_inbox_read(self):
        """Mark inbox emails as read"""
        if messagebox.askyesno("Confirm", "Mark all inbox emails as read?"):
            self.run_script("mark_all_read.scpt", "Mark Inbox as Read")
            
    def mark_all_read(self):
        """Mark all mailboxes as read"""
        if messagebox.askyesno("Confirm", "Mark all emails in all mailboxes as read?"):
            self.run_script("mark_all_read_advanced.scpt", "Mark All Mailboxes as Read")
            
    def quick_mark(self):
        """Quick mark inbox as read"""
        if messagebox.askyesno("Confirm", "Quick mark all inbox emails as read?"):
            self.run_quick_script()
            
    def run_script(self, script_name, description):
        """Run a script"""
        self.update_status(f"Running {description}...")
        self.update_progress(10, f"Starting {description}...")
        
        def run_in_thread():
            try:
                script_path = f"./{script_name}"
                result = subprocess.run(['osascript', script_path], 
                                      capture_output=True, text=True, timeout=60)
                
                self.update_progress(50, f"Running {description}...")
                
                if result.returncode == 0:
                    self.update_progress(100, f"{description} completed!")
                    self.update_status("Ready")
                    messagebox.showinfo("Success", f"{description} completed successfully!")
                else:
                    self.update_progress(100, f"{description} completed with warnings")
                    self.update_status("Ready")
                    messagebox.showwarning("Warning", f"{description} completed with warnings")
                    
            except Exception as e:
                self.update_progress(100, f"Error in {description}")
                self.update_status("Ready")
                messagebox.showerror("Error", f"Error in {description}: {str(e)}")
                
        thread = threading.Thread(target=run_in_thread)
        thread.daemon = True
        thread.start()
        
    def run_quick_script(self):
        """Run quick mark script"""
        self.update_status("Quick marking inbox as read...")
        self.update_progress(10, "Starting quick mark...")
        
        def run_in_thread():
            try:
                script = '''
                tell application "Mail"
                    set inboxMessages to messages of inbox
                    repeat with msg in inboxMessages
                        try
                            set read status of msg to true
                        on error
                            continue
                        end try
                    end repeat
                end tell
                '''
                
                result = subprocess.run(['osascript', '-e', script], 
                                      capture_output=True, text=True, timeout=30)
                
                self.update_progress(100, "Quick mark completed!")
                self.update_status("Ready")
                messagebox.showinfo("Success", "All inbox emails marked as read!")
                
            except Exception as e:
                self.update_progress(100, "Error in quick mark")
                self.update_status("Ready")
                messagebox.showerror("Error", f"Error in quick mark: {str(e)}")
                
        thread = threading.Thread(target=run_in_thread)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = MarkReadGUI(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
