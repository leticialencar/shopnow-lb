import time
from threading import Thread
from urllib.request import urlopen

def check_down_servers(load_balancer):
    for server in load_balancer.servers:
        if not load_balancer.is_alive[server]:
            try:
                urlopen(server, timeout=1)
                load_balancer.mark_as_alive(server)
            except OSError:
                pass

def health_check_loop(load_balancer, interval=3):
    while True:
        time.sleep(interval)
        check_down_servers(load_balancer)


def start_health_check(load_balancer):
    Thread(target=health_check_loop, args=(load_balancer,), daemon=True).start()
