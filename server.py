#!/usr/bin/env python3
"""
Simple HTTP server for CV site (vaiosphere.com/cv_mode/)
Serves static files on port 9002
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 9002
DIRECTORY = Path(__file__).parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Add security headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        super().end_headers()

def main():
    print(f"Starting CV site server on port {PORT}")
    print(f"Serving directory: {DIRECTORY}")
    print(f"URL: http://localhost:{PORT}")

    with socketserver.TCPServer(("127.0.0.1", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Server running at http://127.0.0.1:{PORT}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()

if __name__ == "__main__":
    main()
