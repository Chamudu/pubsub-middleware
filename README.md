# Publish-Subscribe Middleware System 🚀

## 📖 Table of Contents
- [Overview](#overview)
- [Learning Objectives](#learning-objectives)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Implementation Tasks](#implementation-tasks)
- [How to Run](#how-to-run)
- [Concepts Explained](#concepts-explained)
- [Video Recording Guide](#video-recording-guide)

---

## 🎯 Overview

This project implements a **Publish-Subscribe (Pub/Sub) Middleware** using socket programming in Python. It demonstrates asynchronous communication patterns where:
- **Publishers** send messages on specific topics
- **Subscribers** receive messages from topics they're interested in
- **Middleware (Server)** routes messages between publishers and subscribers

### Real-World Applications
- **Chat Applications**: WhatsApp, Slack, Discord
- **IoT Systems**: Sensor data distribution
- **Stock Market**: Real-time price updates
- **Notification Systems**: Push notifications
- **Distributed Systems**: Microservices communication

---

## 🎓 Learning Objectives

By completing this assignment, you will learn:

1. **Socket Programming Fundamentals**
   - TCP/IP communication
   - Client-server architecture
   - Connection management

2. **Concurrent Programming**
   - Multi-threading concepts
   - Thread synchronization
   - Race condition handling

3. **Design Patterns**
   - Publish-Subscribe pattern
   - Observer pattern
   - Message routing

4. **Distributed Systems Concepts**
   - Message queuing
   - Topic-based filtering
   - System reliability & availability

---

## 🏗️ System Architecture

### Task 1: Basic Client-Server
```
┌────────────┐         ┌────────────┐
│   Client   │ ───────>│   Server   │
│            │<─────── │            │
└────────────┘         └────────────┘
```

### Task 2: Pub/Sub with Multiple Clients
```
┌─────────────┐         ┌────────────┐         ┌─────────────┐
│ Publisher 1 │ ─────>  │            │  ─────> │ Subscriber 1│
└─────────────┘         │   Server   │         └─────────────┘
┌─────────────┐         │(Middleware)│         ┌─────────────┐
│ Publisher 2 │ ─────>  │            │  ─────> │ Subscriber 2│
└─────────────┘         └────────────┘         └─────────────┘
```

### Task 3: Topic-Based Routing
```
Publisher (SPORTS) ──────┐
                         ├──> Server ──> Subscriber (SPORTS)
Publisher (NEWS) ────────┤         └──> Subscriber (NEWS)
                         └──────────────> Subscriber (SPORTS)
```

---

## 🔧 Prerequisites

### Required Software
- **Python 3.8+** (Already installed on Windows)
- **Command Prompt / PowerShell**
- **Text Editor** (VS Code, PyCharm, or any editor)

### Python Knowledge Required
- Basic syntax (variables, functions, loops)
- Classes and objects
- Exception handling
- File I/O

---

## 📁 Project Structure

```
pubsub-middleware/
│
├── README.md                   # This file - comprehensive documentation
├── LEARNING_NOTES.md          # Detailed concept explanations
├── ARCHITECTURE_DESIGN.md     # Task 4 - Distributed architecture proposal
│
├── task1/
│   ├── server.py              # Basic server implementation
│   ├── client.py              # Basic client implementation
│   └── README_TASK1.md        # Task 1 specific documentation
│
├── task2/
│   ├── server.py              # Multi-client server with Pub/Sub
│   ├── client.py              # Publisher/Subscriber client
│   └── README_TASK2.md        # Task 2 specific documentation
│
├── task3/
│   ├── server.py              # Topic-based filtering server
│   ├── client.py              # Topic-aware client
│   └── README_TASK3.md        # Task 3 specific documentation
│
├── utils/
│   ├── constants.py           # Shared constants
│   └── logger.py              # Logging utilities
│
└── screencasts/
    ├── task1_demo.mp4         # Video demonstration for Task 1
    ├── task2_demo.mp4         # Video demonstration for Task 2
    └── task3_demo.mp4         # Video demonstration for Task 3
```

---

## 🚀 Implementation Tasks

### Task 1: Basic Client-Server Communication
**Goal**: Establish basic socket connection and message exchange

**Key Concepts**:
- Socket creation (`socket.socket()`)
- Binding server to address (`bind()`)
- Listening for connections (`listen()`)
- Accepting connections (`accept()`)
- Sending/receiving data (`send()`, `recv()`)

**Expected Output**:
1. Server starts and listens on port 5000
2. Client connects to server
3. Text typed in client appears on server terminal
4. Typing "terminate" closes client connection

---

### Task 2: Publishers and Subscribers
**Goal**: Handle multiple concurrent clients with different roles

**Key Concepts**:
- Threading for concurrent connections (`threading.Thread`)
- Client role identification (PUBLISHER vs SUBSCRIBER)
- Message broadcasting to specific client types
- Thread-safe data structures (`Lock`, `Queue`)

**Expected Output**:
1. Multiple clients connect simultaneously
2. Publisher clients send messages
3. Only Subscriber clients receive published messages
4. Server displays all client activities

---

### Task 3: Topic-Based Filtering
**Goal**: Route messages based on topics/subjects

**Key Concepts**:
- Topic registration and management
- Selective message routing
- Data structure for topic-subscriber mapping
- Message filtering logic

**Expected Output**:
1. Clients specify topics (e.g., SPORTS, NEWS, WEATHER)
2. Publishers send messages on specific topics
3. Only subscribers to that topic receive messages
4. Multiple topics can coexist

---

### Task 4: Distributed Architecture Design
**Goal**: Propose improved architecture for reliability

**Key Concepts**:
- Single Point of Failure (SPOF)
- Load balancing
- Server replication
- Message queuing
- Fault tolerance

**Deliverable**: Architecture diagram + written explanation

---

## 🎬 How to Run

### Task 1 Example

**Terminal 1 (Server):**
```bash
cd "c:\Users\Chamudu Hansana\Desktop\Projects\pubsub-middleware\task1"
python server.py 5000
```

**Terminal 2 (Client):**
```bash
cd "c:\Users\Chamudu Hansana\Desktop\Projects\pubsub-middleware\task1"
python client.py 192.168.10.2 5000
```

*(Detailed instructions for each task in respective README files)*

---

## 💡 Concepts Explained

### 1. **What is a Socket?**
A socket is an **endpoint for sending or receiving data** across a network. Think of it as a "phone line" between two programs.

**Analogy**: 
- Server = Phone company's switchboard
- Client = Your phone
- Port = Phone line number
- Message = Conversation

### 2. **TCP vs UDP**
- **TCP** (Transmission Control Protocol): Reliable, ordered, connection-based ✅ (We use this)
- **UDP** (User Datagram Protocol): Fast, connectionless, no guarantee ❌

### 3. **Why Threading?**
A single-threaded server can only handle **one client at a time**. Threading allows:
- **Concurrent connections**: Multiple clients simultaneously
- **Non-blocking**: Server doesn't freeze waiting for one client
- **Scalability**: Can handle many publishers/subscribers

### 4. **Publish-Subscribe Pattern**
**Traditional Request-Response**:
```
Client → "Give me data" → Server
Client ← "Here's data" ← Server
```

**Pub/Sub**:
```
Publisher → "Here's new data!" → Server → Interested Subscribers
(Publishers don't know who receives)
(Subscribers don't know who published)
```

**Benefits**:
- **Decoupling**: Publishers and subscribers are independent
- **Scalability**: Easy to add more publishers/subscribers
- **Flexibility**: Dynamic subscription management

---

## 🎥 Video Recording Guide

### Task 1 Recording Checklist
- [ ] Show server starting on port 5000
- [ ] Show client connecting with IP and port
- [ ] Type messages in client CLI
- [ ] Show messages appearing on server CLI
- [ ] Type "terminate" to close client
- [ ] Show clean disconnection

### Task 2 Recording Checklist
- [ ] Start server
- [ ] Start 2-3 Publishers
- [ ] Start 2-3 Subscribers
- [ ] Show Publishers typing messages
- [ ] Show messages appearing ONLY on Subscribers
- [ ] Demonstrate server displaying all activities

### Task 3 Recording Checklist
- [ ] Start server
- [ ] Start Publishers with different topics (SPORTS, NEWS)
- [ ] Start Subscribers with specific topic interests
- [ ] Show topic-based message routing
- [ ] Demonstrate message filtering (SPORTS → SPORTS only)

---

## 📚 Additional Resources

### Python Socket Programming
- [Official Python Socket Documentation](https://docs.python.org/3/library/socket.html)
- [Real Python Socket Programming Guide](https://realpython.com/python-sockets/)

### Threading in Python
- [Python Threading Tutorial](https://docs.python.org/3/library/threading.html)
- [Threading vs Multiprocessing](https://realpython.com/intro-to-python-threading/)

### Pub/Sub Pattern
- [Pub/Sub Pattern Explained](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)
- [Message Queue Systems](https://www.cloudamqp.com/blog/what-is-message-queuing.html)

---

## 🏆 Grading Criteria

| Task | Marks | Focus Area |
|------|-------|------------|
| Task 1 | 20/100 | Basic socket communication |
| Task 2 | 30/100 | Concurrent connections + Pub/Sub roles |
| Task 3 | 40/100 | Topic-based filtering |
| Task 4 | 10/100 | Architecture design |

---

## 📝 Notes for Learning

- **Start simple**: Get Task 1 working perfectly before moving to Task 2
- **Test incrementally**: Test each feature as you add it
- **Use print statements**: Debug by printing connection states, messages, etc.
- **Read error messages**: Python error messages are very helpful
- **Commit often**: Save your progress with Git

---

## 🤝 Team Collaboration Tips

- **Divide tasks**: Different team members can work on client/server/documentation
- **Code review**: Review each other's code before submission
- **Test together**: Run integration tests with full team
- **Practice demo**: Rehearse video recording before final submission

---

**Good luck with your assignment! 🎓**

*Last Updated: January 2026*
