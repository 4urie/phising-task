"""Local classroom simulation. Run: python lab_demo.py"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

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
        self.send_header('Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src https://images.unsplash.com; form-action 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    print('Classroom simulation: http://127.0.0.1:8000\nOther devices: http://<this-laptop-LAN-IP>:8000\nPress Ctrl+C to stop.')
    try:
        HTTPServer(('0.0.0.0', 8000), Handler).serve_forever()
    except KeyboardInterrupt:
        print('\nDemo stopped.')
