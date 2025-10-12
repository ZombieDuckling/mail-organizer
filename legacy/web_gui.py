#!/usr/bin/env python3
"""
Web-based Email Organizer GUI
A simple web interface for the email organizer toolkit
"""

import http.server
import socketserver
import webbrowser
import subprocess
import threading
import json
import os
from urllib.parse import urlparse, parse_qs

class EmailOrganizerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>🍎 Email Organizer Pro</title>
                <style>
                    body { 
                        font-family: Arial, sans-serif; 
                        background: linear-gradient(135deg, #2c3e50, #34495e);
                        color: white; 
                        margin: 0; 
                        padding: 20px;
                        min-height: 100vh;
                    }
                    .container { 
                        max-width: 800px; 
                        margin: 0 auto; 
                        background: rgba(52, 73, 94, 0.9);
                        padding: 30px;
                        border-radius: 15px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    }
                    h1 { 
                        text-align: center; 
                        color: #ecf0f1; 
                        margin-bottom: 10px;
                        font-size: 2.5em;
                    }
                    .subtitle {
                        text-align: center;
                        color: #bdc3c7;
                        margin-bottom: 30px;
                        font-size: 1.2em;
                    }
                    .email-count {
                        text-align: center;
                        font-size: 1.5em;
                        color: #27ae60;
                        margin: 20px 0;
                        padding: 15px;
                        background: rgba(39, 174, 96, 0.2);
                        border-radius: 10px;
                    }
                    .button-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                        gap: 15px;
                        margin: 30px 0;
                    }
                    .btn {
                        padding: 15px 20px;
                        border: none;
                        border-radius: 10px;
                        font-size: 16px;
                        font-weight: bold;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        text-decoration: none;
                        display: block;
                        text-align: center;
                    }
                    .btn:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                    }
                    .btn-quick { background: #3498db; color: white; }
                    .btn-smart { background: #9b59b6; color: white; }
                    .btn-nuclear { background: #e74c3c; color: white; }
                    .btn-mark-read { background: #27ae60; color: white; }
                    .btn-analyze { background: #f39c12; color: white; }
                    .btn-unsubscribe { background: #1abc9c; color: white; }
                    .btn-rules { background: #34495e; color: white; }
                    .btn-mass { background: #c0392b; color: white; }
                    .log {
                        background: #2c3e50;
                        border: 1px solid #34495e;
                        border-radius: 10px;
                        padding: 20px;
                        margin-top: 30px;
                        min-height: 200px;
                        font-family: monospace;
                        font-size: 14px;
                        overflow-y: auto;
                        max-height: 300px;
                    }
                    .status {
                        text-align: center;
                        margin: 20px 0;
                        padding: 10px;
                        background: rgba(52, 73, 94, 0.5);
                        border-radius: 5px;
                    }
                    .progress {
                        width: 100%;
                        height: 20px;
                        background: #34495e;
                        border-radius: 10px;
                        overflow: hidden;
                        margin: 10px 0;
                    }
                    .progress-bar {
                        height: 100%;
                        background: linear-gradient(90deg, #27ae60, #2ecc71);
                        width: 0%;
                        transition: width 0.3s ease;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🍎 Email Organizer Pro</h1>
                    <p class="subtitle">Clean your inbox with ease</p>
                    
                    <div class="email-count" id="emailCount">
                        📊 Loading email count...
                    </div>
                    
                    <div class="status" id="status">Ready</div>
                    
                    <div class="progress">
                        <div class="progress-bar" id="progressBar"></div>
                    </div>
                    
                    <div class="button-grid">
                        <button class="btn btn-quick" onclick="runAction('quick')">🚀 Quick Cleanup</button>
                        <button class="btn btn-smart" onclick="runAction('smart')">🧠 Smart Cleanup</button>
                        <button class="btn btn-nuclear" onclick="runAction('nuclear')">💥 Nuclear Cleanup</button>
                        <button class="btn btn-mark-read" onclick="runAction('mark-read')">📧 Mark All Read</button>
                        <button class="btn btn-analyze" onclick="runAction('analyze')">🔍 Analyze Inbox</button>
                        <button class="btn btn-unsubscribe" onclick="runAction('unsubscribe')">📧 Unsubscribe Check</button>
                        <button class="btn btn-rules" onclick="runAction('rules')">⚙️ Create Rules</button>
                        <button class="btn btn-mass" onclick="runAction('mass')">💀 Mass Delete</button>
                    </div>
                    
                    <div class="log" id="log">
                        <div>📋 Activity Log</div>
                        <div>Ready to organize your emails...</div>
                    </div>
                </div>
                
                <script>
                    function updateStatus(status) {
                        document.getElementById('status').textContent = status;
                    }
                    
                    function updateProgress(percent) {
                        document.getElementById('progressBar').style.width = percent + '%';
                    }
                    
                    function addLog(message) {
                        const log = document.getElementById('log');
                        const time = new Date().toLocaleTimeString();
                        log.innerHTML += '<div>[' + time + '] ' + message + '</div>';
                        log.scrollTop = log.scrollHeight;
                    }
                    
                    function updateEmailCount() {
                        fetch('/api/email-count')
                            .then(response => response.json())
                            .then(data => {
                                document.getElementById('emailCount').textContent = '📊 ' + data.count.toLocaleString() + ' emails';
                            })
                            .catch(error => {
                                document.getElementById('emailCount').textContent = '📊 Unable to access Mail';
                            });
                    }
                    
                    function runAction(action) {
                        if (!confirm('Are you sure you want to run ' + action + '?')) {
                            return;
                        }
                        
                        updateStatus('Running ' + action + '...');
                        updateProgress(10);
                        addLog('Starting ' + action + '...');
                        
                        fetch('/api/run/' + action, {method: 'POST'})
                            .then(response => response.json())
                            .then(data => {
                                updateProgress(100);
                                updateStatus('Ready');
                                addLog('✅ ' + action + ' completed: ' + data.message);
                                updateEmailCount();
                            })
                            .catch(error => {
                                updateProgress(100);
                                updateStatus('Ready');
                                addLog('❌ Error: ' + error.message);
                            });
                    }
                    
                    // Update email count on load
                    updateEmailCount();
                    
                    // Update email count every 30 seconds
                    setInterval(updateEmailCount, 30000);
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        elif self.path.startswith('/api/'):
            self.handle_api()
        else:
            super().do_GET()
    
    def handle_api(self):
        if self.path == '/api/email-count':
            try:
                result = subprocess.run(['osascript', '-e', 'tell application "Mail" to return count of messages of inbox'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    count = int(result.stdout.strip())
                    self.send_json_response({'count': count})
                else:
                    self.send_json_response({'count': 0, 'error': 'Unable to access Mail'})
            except Exception as e:
                self.send_json_response({'count': 0, 'error': str(e)})
                
        elif self.path.startswith('/api/run/'):
            action = self.path.split('/')[-1]
            self.handle_run_action(action)
        else:
            self.send_json_response({'error': 'Unknown API endpoint'})
    
    def handle_run_action(self, action):
        try:
            if action == 'mark-read':
                result = subprocess.run(['osascript', '-e', 'tell application "Mail" to set read status of every message of inbox to true'], 
                                      capture_output=True, text=True, timeout=60)
                self.send_json_response({'message': 'All emails marked as read'})
            elif action == 'quick':
                result = subprocess.run(['bash', 'mega_cleanup.sh'], 
                                      capture_output=True, text=True, timeout=300)
                self.send_json_response({'message': 'Quick cleanup completed'})
            elif action == 'smart':
                result = subprocess.run(['bash', 'nuclear_cleanup.sh'], 
                                      capture_output=True, text=True, timeout=300)
                self.send_json_response({'message': 'Smart cleanup completed'})
            elif action == 'nuclear':
                result = subprocess.run(['bash', 'nuclear_cleanup.sh'], 
                                      capture_output=True, text=True, timeout=300)
                self.send_json_response({'message': 'Nuclear cleanup completed'})
            elif action == 'analyze':
                result = subprocess.run(['bash', 'inbox_analyzer.sh'], 
                                      capture_output=True, text=True, timeout=60)
                self.send_json_response({'message': 'Inbox analysis completed'})
            elif action == 'unsubscribe':
                result = subprocess.run(['python3', 'working_unsubscribe.py'], 
                                      capture_output=True, text=True, timeout=60)
                self.send_json_response({'message': 'Unsubscribe check completed'})
            elif action == 'rules':
                result = subprocess.run(['osascript', 'create_mail_rules.scpt'], 
                                      capture_output=True, text=True, timeout=60)
                self.send_json_response({'message': 'Mail rules created'})
            elif action == 'mass':
                result = subprocess.run(['bash', 'mass_delete.sh'], 
                                      capture_output=True, text=True, timeout=300)
                self.send_json_response({'message': 'Mass delete completed'})
            else:
                self.send_json_response({'error': 'Unknown action'})
        except Exception as e:
            self.send_json_response({'error': str(e)})
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def main():
    PORT = 8080
    
    # Change to the mail organizer directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), EmailOrganizerHandler) as httpd:
        print(f"🍎 Email Organizer Web GUI")
        print(f"==========================")
        print(f"🌐 Server running at: http://localhost:{PORT}")
        print(f"📱 Open your web browser and go to: http://localhost:{PORT}")
        print(f"⏹️  Press Ctrl+C to stop the server")
        print()
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
            print("🚀 Browser opened automatically!")
        except:
            print("⚠️  Could not open browser automatically")
        
        print()
        httpd.serve_forever()

if __name__ == "__main__":
    main()
