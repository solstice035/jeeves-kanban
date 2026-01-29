#!/usr/bin/env python3
"""
Jeeves Kanban Board - Local Network Server

Serves the Kanban board on your local network so you can access it
from any device (phone, tablet, other computers) on the same network.
"""

import http.server
import socketserver
import socket
import os
import sys
from pathlib import Path

# Configuration
PORT = 8888
DIRECTORY = Path(__file__).parent.absolute()

# Get local IP
def get_local_ip():
    """Get the local network IP address"""
    try:
        # Create a socket to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve from the correct directory"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for local network access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    # Change to the kanban directory
    os.chdir(DIRECTORY)
    
    # Get local IP
    local_ip = get_local_ip()
    
    # Create server
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        print("\n" + "="*60)
        print("🎯 Jeeves Kanban Board Server")
        print("="*60)
        print(f"\n✅ Server started successfully!\n")
        print(f"📱 Access from this computer:")
        print(f"   http://localhost:{PORT}/")
        print(f"   http://127.0.0.1:{PORT}/\n")
        print(f"🌐 Access from other devices on your network:")
        print(f"   http://{local_ip}:{PORT}/\n")
        print(f"📱 On your phone/tablet, open:")
        print(f"   http://{local_ip}:{PORT}/\n")
        print(f"🛑 Press Ctrl+C to stop the server\n")
        print("="*60 + "\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped by user")
            sys.exit(0)

if __name__ == "__main__":
    main()
