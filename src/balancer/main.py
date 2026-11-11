
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from src.algorithms.least_connections import LeastConnections
from src.algorithms.random import RandomAlgorithm
from src.algorithms.round_robin import RoundRobin
from src.balancer.health_check import start_health_check
from src.balancer.load_balancer import LoadBalancer

PORT = 8000

DEFAULT_SERVERS = "http://localhost:5001,http://localhost:5002,http://localhost:5003"

ALGORITHMS = {
    "round_robin": RoundRobin,
    "least_connections": LeastConnections,
    "random": RandomAlgorithm,
}


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
    algorithm_name = sys.argv[1] if len(sys.argv) > 1 else "round_robin"

    if algorithm_name not in ALGORITHMS:
        print(f"Invalid algorithm. Use: {', '.join(ALGORITHMS)}")
        sys.exit(1)

    servers = [
        server.strip()
        for server in os.environ.get("SERVERS", DEFAULT_SERVERS).split(",")
    ]

    load_balancer = LoadBalancer(servers, ALGORITHMS[algorithm_name]())

    start_health_check(load_balancer)

    http_server = ThreadingHTTPServer(("0.0.0.0", PORT), LoadBalancerHandler)
    http_server.load_balancer = load_balancer

    print(f"Load Balancer running on port {PORT} with algorithm: {algorithm_name}")
    http_server.serve_forever()
