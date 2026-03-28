import http.server, os, sys

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=os.path.dirname(os.path.abspath(__file__)), **kw)
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.path = "/dashboard.html"
        super().do_GET()
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    def log_message(self, *a): pass

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
print(f"Dashboard at http://localhost:{port}")
http.server.HTTPServer(("0.0.0.0", port), Handler).serve_forever()
