"""Local, non-caching preview of the same directory used for publication."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]


class PreviewHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        super().end_headers()

    def list_directory(self, path):
        self.send_error(404, 'Página não encontrada')

    def send_error(self, code, message=None, explain=None):
        page = Path(self.directory) / '404.html'
        if code != 404 or not page.is_file():
            return super().send_error(code, message, explain)
        # The published 404 uses the GitHub project URL; preview recovery stays local.
        content = page.read_bytes().replace(b'https://luizgusfilhoo.github.io/lgrepresentacoes/', b'/')
        self.send_response(404)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8767)
    args = parser.parse_args()
    if not (ROOT / 'dist/index.html').is_file():
        raise SystemExit('Distribuição ausente. Execute npm run build primeiro.')
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(PreviewHandler, directory=str(ROOT / 'dist')))
    except OSError as error:
        raise SystemExit(f'Não foi possível iniciar a prévia na porta {args.port}: {error}')
    print(f'Prévia LG: http://127.0.0.1:{args.port}/ (Ctrl+C encerra)', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
