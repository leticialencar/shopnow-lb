
import unittest

from src.algorithms.least_connections import LeastConnections

class TestLeastConnections(unittest.TestCase):
    def test_selects_server_with_fewest_connections(self):
        algorithm = LeastConnections()

        servers = ["server1", "server2", "server3"]
        connections = {
            "server1": 5,
            "server2": 2,
            "server3": 8,
        }

        chosen = algorithm.choose(servers, connections)

        self.assertEqual(chosen, "server2")


if __name__ == "__main__":
    unittest.main()