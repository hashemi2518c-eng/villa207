#!/usr/bin/env python3
# Serves the attendance page and relays its API calls to the Google Apps Script
# web app, so phones in Iran never talk to Google directly. Python stdlib only.
import os, sys, urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

GAS = 'https://script.google.com/macros/s/AKfycbym7MpYvKkwFJaLuTStK0Khs7pWmp6TOLL65VHstiXWGhsV_0GUtCEEu0hRE8RaqzfGCw/exec'
ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get('PORT', '8207'))

def gas(data=None, query=''):
    req = urllib.request.Request(GAS + query, data=data,
        headers={'Content-Type': 'text/plain;charset=utf-8'} if data else {})
    with urllib.request.urlopen(req, timeout=40) as r:  # follows Google's 302 as GET
        return r.read()

class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)

    def reply(self, code, body):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers(); self.wfile.write(body)

    def relay(self, data=None, query=''):
        try: self.reply(200, gas(data, query))
        except Exception as e:
            self.reply(502, ('{"ok":false,"error":"relay: %s"}' % str(e).replace('"', "'")).encode())

    def do_GET(self):
        if self.path.startswith('/relay'):
            return self.relay(query='?action=attPing')
        if self.path.split('?')[0].endswith(('.py', '.sh', '.service')):
            return self.send_error(404)
        super().do_GET()

    def do_POST(self):
        if not self.path.startswith('/relay'): return self.send_error(404)
        n = int(self.headers.get('Content-Length') or 0)
        self.relay(self.rfile.read(n))

    def log_message(self, *a): pass

if __name__ == '__main__':
    print('villa207 attendance on port', PORT); sys.stdout.flush()
    ThreadingHTTPServer(('0.0.0.0', PORT), H).serve_forever()
