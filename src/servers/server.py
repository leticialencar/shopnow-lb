import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

port = int(sys.argv[1])

class ShopNowHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = f"Responded by the server on port {port}\n".encode()

        print(
            f"[REQUEST] {self.command} {self.path} "
            f"-> server:{port}",
            flush=True
        )

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    print(f"[START] ShopNow server running on port {port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), ShopNowHandler).serve_forever()
