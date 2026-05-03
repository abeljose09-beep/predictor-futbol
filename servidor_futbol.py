from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import subprocess, json, sys, os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        # Servir interfaz HTML
        if parsed.path == '/' or parsed.path == '/index.html':
            try:
                with open('interfaz_futbol.html', 'rb') as f:
                    contenido = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(contenido)
            except:
                self.send_response(404)
                self.end_headers()

        # Endpoint predicción
        elif parsed.path == '/predecir':
            params = parse_qs(parsed.query)
            local  = params.get('local',  ['Arsenal'])[0]
            visita = params.get('visita', ['Chelsea'])[0]
            try:
                result = subprocess.run(
                    [sys.executable, 'modelo_futbol.py', local, visita],
                    capture_output=True, text=True, timeout=180
                )
                # Extraer solo el JSON del output
                lineas = result.stdout.strip().split('\n')
                json_line = next((l for l in reversed(lineas) if l.startswith('{')), None)
                if json_line:
                    data = json.loads(json_line)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode())
                else:
                    raise Exception(result.stderr)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

        # Endpoint equipos (para autocompletado)
        elif parsed.path == '/equipos':
            try:
                from equipos import EQUIPOS_LIGA
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(list(EQUIPOS_LIGA.keys())).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass

puerto = int(os.environ.get('PORT', 5000))
print(f"🚀 Servidor fútbol corriendo en http://localhost:{puerto}")
HTTPServer(('0.0.0.0', puerto), Handler).serve_forever()