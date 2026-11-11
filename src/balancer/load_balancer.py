from threading import Lock
from urllib.request import urlopen


class LoadBalancer:
    def __init__(self, servers, algorithm, timeout=2):
        self.servers = servers
        self.algorithm = algorithm
        self.timeout = timeout
        self.lock = Lock()
        self.is_alive = {server: True for server in servers}
        self.active_connections = {server: 0 for server in servers}

    def choose_server(self):
        with self.lock:
            available = [s for s in self.servers if self.is_alive[s]]

            if not available:
                return None

            chosen = self.algorithm.choose(available, self.active_connections)
            self.active_connections[chosen] += 1
            return chosen

    def mark_as_down(self, server):
        with self.lock:
            self.is_alive[server] = False
        print(f"[FALHA] {server} fora do ar")

    def mark_as_alive(self, server):
        with self.lock:
            self.is_alive[server] = True
        print(f"[RECUPERADO] {server} voltou")

    def forward_request(self, path):
        for _ in range(len(self.servers)):
            server = self.choose_server()

            if server is None:
                break

            try:
                with urlopen(server + path, timeout=self.timeout) as response:
                    return 200, response.read()
            except OSError:
                self.mark_as_down(server)
            finally:
                with self.lock:
                    self.active_connections[server] -= 1

        return 503, b"Nenhum servidor disponivel\n"
