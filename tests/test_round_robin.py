
import unittest

from src.algorithms.round_robin import RoundRobin


class TestRoundRobin(unittest.TestCase):
    def test_distributes_requests_sequentially(self):
        algorithm = RoundRobin()
        servers = ["Server 1", "Server 2", "Server 3"]

        results = [
            algorithm.choose(servers)
            for _ in range(6)
        ]

        self.assertEqual(
            results,
            [
                "Server 1",
                "Server 2",
                "Server 3",
                "Server 1",
                "Server 2",
                "Server 3",
            ],
        )

    def test_raises_error_without_available_servers(self):
        algorithm = RoundRobin()

        with self.assertRaises(ValueError):
            algorithm.choose([])


if __name__ == "__main__":
    unittest.main()