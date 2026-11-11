
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from src.algorithms.round_robin import RoundRobin
from src.balancer.load_balancer import LoadBalancer

PORT = 8000

SERVERS = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003",
]


class LoadBalancerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, body = self.server.load_balancer.forward_request(self.path)

        self.send_response(status)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    load_balancer = LoadBalancer(SERVERS, RoundRobin())

    http_server = ThreadingHTTPServer(
        ("0.0.0.0", PORT),
        LoadBalancerHandler
    )

    http_server.load_balancer = load_balancer

    print(f"Balanceador rodando na porta {PORT}")
    http_server.serve_forever()
