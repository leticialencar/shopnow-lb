class RoundRobin:
    def __init__(self):
        self.counter = 0

    def choose(self, available_servers, active_connections=None):
        if not available_servers:
            raise ValueError("Nenhum servidor disponível.")

        chosen = available_servers[self.counter % len(available_servers)]
        self.counter += 1

        return chosen