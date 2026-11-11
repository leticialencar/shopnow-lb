class LeastConnections:
    def choose(self, available_servers, active_connections):
        return min(available_servers, key=lambda server: active_connections[server])
