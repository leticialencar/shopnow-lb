# ShopNow Load Balancer

A Python-based load balancing system designed to distribute HTTP requests across multiple server instances, improving availability, fault tolerance, and request distribution.

## Overview

ShopNow is a distributed application architecture consisting of three independent server instances behind load balancers.

The project implements different load balancing algorithms and provides health monitoring, failure detection, automatic server recovery, and load testing using Apache Benchmark.

Two load balancing implementations are available:

- **Custom Python Load Balancer** — Implements request forwarding, server selection algorithms, and health checks.
- **Nginx Load Balancer** — Uses Nginx upstream configurations to distribute incoming traffic.

## Architecture

The system runs three server instances, each listening on a different port. Incoming requests are received by a load balancer and forwarded to an available server.

```text
                    Client
                      |
             +--------+--------+
             |                 |
       Python LB             Nginx
       Port 8000            Port 8001
             |                 |
             +--------+--------+
                      |
              +-------+-------+
              |       |       |
           Server 1 Server 2 Server 3
           :5001    :5002    :5003
```

## Features

- Three independent HTTP server instances.
- Multiple load balancing algorithms.
- Automatic request distribution.
- Server health checks.
- Failure detection and automatic recovery.
- Automatic failover when a server becomes unavailable.
- Docker-based environment.
- Nginx reverse proxy configuration.
- Unit tests for load balancing algorithms.
- Load testing with Apache Benchmark (ab).

## Load Balancing Algorithms

The custom Python load balancer supports three algorithms:

| Algorithm | Description |
|---|---|
| Round Robin | Distributes requests sequentially across available servers. |
| Least Connections | Selects the server with the fewest active connections. |
| Random | Selects an available server randomly. |

Nginx also provides two configurations:

- **Round Robin** — Default Nginx upstream distribution.
- **Least Connections** — Uses the `least_conn` directive.

## Technologies

- Python 3.12
- Docker
- Docker Compose
- Nginx
- Apache Benchmark (ab)
- Makefile
- Unittest

## Getting Started

### Requirements

Make sure you have the following installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.12+](https://www.python.org/downloads/)
- Make (optional, for using the Makefile commands)

### Run the application

Clone the repository:

```bash
git clone https://github.com/leticialencar/shopnow-lb.git
cd shopnow-lb
```

Build and start all services:

```bash
make up
```

Alternatively, use Docker Compose:

```bash
docker compose up --build -d
```

This starts:

| Service | Port |
|---|---:|
| Server 1 | 5001 |
| Server 2 | 5002 |
| Server 3 | 5003 |
| Python Load Balancer | 8000 |
| Nginx Load Balancer | 8001 |

## Usage

### Send requests

Send a request through the Python load balancer:

```bash
make request
```

Send a request through Nginx:

```bash
make request-nginx
```

Or access the endpoints directly:

- Python: `http://localhost:8000/`
- Nginx: `http://localhost:8001/`

Each response identifies which server handled the request.

### Select a load balancing algorithm

The Python load balancer uses Round Robin by default.

To change the algorithm:

```bash
make round-robin
```

```bash
make least-connections
```

```bash
make random
```

Check the configured algorithm:

```bash
make algorithm
```

The corresponding Nginx configuration is also selected through the `ALGORITHM` environment variable.

## Failure Simulation

Server failures can be simulated by stopping individual containers.

Stop a server:

```bash
make stop-server-1
```

Start it again:

```bash
make start-server-1
```

The same commands are available for servers 2 and 3.

When a server becomes unavailable, the Python load balancer detects the failure and stops forwarding requests to it. A background health check periodically checks unavailable servers and automatically restores them to the available pool when they recover.

Nginx also uses upstream failure parameters and retry settings to handle unavailable instances.

## Load Testing

Apache Benchmark (ab) is used to simulate concurrent HTTP requests and evaluate the load balancers.

Run the benchmark against the Python load balancer:

```bash
make benchmark
```

Run the benchmark against Nginx:

```bash
make benchmark-nginx
```

The current benchmark configuration uses:

| Parameter | Value |
|---|---:|
| Total requests | 1,000 |
| Concurrent requests | 50 |
| Tool | Apache Benchmark |

Apache Benchmark provides metrics such as:

- Requests per second.
- Time per request.
- Transfer rate.
- Failed requests.
- Connection and response times.

These metrics can be used to compare the behavior of both load balancing implementations.

## Testing

Run the unit tests:

```bash
make test
```

The test suite covers the Round Robin and Least Connections algorithms.

## Logs and Monitoring

View the Python load balancer logs:

```bash
make logs
```

Check the status of all containers:

```bash
make status
```

View logs from individual servers:

```bash
docker compose logs -f server1
```

Replace `server1` with `server2` or `server3` to inspect the other instances.

---

**End of documentation. :)** 
