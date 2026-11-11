import random

class RandomAlgorithm:
    def choose(self, available_servers, active_connections):
        return random.choice(available_servers)
