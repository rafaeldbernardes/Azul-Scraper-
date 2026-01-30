#!/usr/bin/env python3
"""
Simple HTTP server to view the flight scraper dashboard.
Open your browser to http://localhost:8000/dashboard.html
"""

import http.server
import socketserver
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def start_server():
    """Start the HTTP server."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"\n{'='*60}")
        print("🚀 Flight Scraper Dashboard")
        print(f"{'='*60}")
        print(f"\n✅ Dashboard running at: http://localhost:{PORT}/dashboard.html")
        print(f"📁 Serving from: {os.getcwd()}")
        print(f"\n💡 The dashboard auto-refreshes every 5 seconds")
        print(f"📊 Shows real-time data from best_points.json")
        print(f"\nPress Ctrl+C to stop the server\n")
        print(f"{'='*60}\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Dashboard server stopped.")
            httpd.shutdown()

if __name__ == "__main__":
    start_server()
