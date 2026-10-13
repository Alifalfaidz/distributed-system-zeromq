# Distributed System with ZeroMQ

Implementation of **Push-Pull** and **Publish-Subscribe** communication patterns using Python, ZeroMQ (PyZMQ), and Docker Compose.

This project was developed as part of the **Cloud and Distributed Computing** coursework to demonstrate how distributed components communicate, distribute computational tasks, and publish results through message-based communication.

## 1. Project Overview

This project implements a distributed computing system combining two communication patterns:

- **Push-Pull:** Distributes computational tasks from a Task Distributor to multiple Workers.
- **Publish-Subscribe:** Publishes computation results to Subscribers based on specific topics.

The system supports three mathematical operations:

- `SUM` — Addition
- `MUT` — Multiplication
- `DIV` — Division

Each component runs independently and communicates through ZeroMQ sockets.

## 2. System Architecture

The system consists of a Task Distributor, two Workers, a Task Collector that also acts as a Publisher, and three Subscribers.

**Communication Flow:**

1. **Task Distributor** generates random mathematical tasks and distributes them to available Workers.
2. **Worker 1 & Worker 2** receive tasks, perform calculations, and send the results to the Collector.
3. **Task Collector + Publisher** receives results from both Workers and publishes them based on their operation topics.
4. **Subscribers** receive only the results corresponding to their subscribed topics (`SUM`, `MUT`, or `DIV`).

### Communication Ports

| Component | Socket Type | Port |
|---|---|---|
| Task Distributor | PUSH | 5555 |
| Worker 1 & Worker 2 | PULL | 5555 |
| Worker 1 | PUSH | 5556 |
| Worker 2 | PUSH | 5557 |
| Task Collector | PULL | 5556, 5557 |
| Task Publisher | PUB | 5558 |
| Subscribers | SUB | 5558 |

## 3. Technologies Used

- **Python 3.9** — Main programming language
- **ZeroMQ (PyZMQ)** — Message-based communication
- **Docker** — Containerization
- **Docker Compose** — Multi-container orchestration

## 4. Project Structure

| File | Description |
|---|---|
| `tasks_distributor.py` | Generates and distributes computational tasks |
| `worker_1.py` | Processes tasks assigned to Worker 1 |
| `worker_2.py` | Processes tasks assigned to Worker 2 |
| `tasks_collector_publisher.py` | Collects and publishes computation results |
| `sum_subscriber.py` | Receives addition results |
| `mut_subscriber.py` | Receives multiplication results |
| `div_subscriber.py` | Receives division results |
| `docker-compose.yml` | Configures the multi-container system |
| `Dockerfile` | Defines the container image configuration |
| `env.yml` | Defines the Conda environment dependencies |

Additional Python files provide supporting functionality and configuration.

## 5. How to Run

### Prerequisites

Ensure that Docker and Docker Compose are installed and available on your system.

### Clone the Repository

```bash
git clone https://github.com/Alifalfaidz/distributed-system-zeromq.git
cd distributed-system-zeromq
```

### Build and Start the Containers

```bash
docker compose up -d --build
```

### View Container Logs

```bash
docker compose logs -f
```

### Stop the Containers

```bash
docker compose down
```

## 6. Implementation Results

The implementation demonstrates the integration of Push-Pull and Publish-Subscribe communication patterns.

Based on the conducted tests:

- The Distributor successfully sends computational tasks.
- Both Workers receive and process mathematical operations.
- The Collector receives computation results from both Workers.
- The Publisher distributes results based on operation topics.
- Each Subscriber receives messages corresponding to its subscribed topic.
- The components successfully communicate across Docker containers.

## 7. Conclusion

This project demonstrates how **Push-Pull** and **Publish-Subscribe** patterns can be combined to implement task distribution and topic-based message delivery in a distributed system.

Using Python, ZeroMQ, and Docker Compose, the system provides a practical example of asynchronous message-based communication between independent components.

---

**Course:** Cloud and Distributed Computing

**Project:** Task C — Combination of Push-Pull and Publish-Subscribe Patterns

**Author:** Alif Mahtum Alfaidz
