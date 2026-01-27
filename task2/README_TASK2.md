# Task 2: Publishers and Subscribers (Multi-Client Pub/Sub)

## 📋 Objective

Implement a **Publish-Subscribe (Pub/Sub) middleware** that:
- Handles **multiple concurrent clients** simultaneously
- Supports two client roles: **PUBLISHER** and **SUBSCRIBER**
- Publishers send messages that are **broadcast to all subscribers**
- Uses **threading** for concurrent connection handling

---

## 🎯 Learning Goals

By completing Task 2, you will understand:

1. **Threading (Concurrency)**
   - Running multiple tasks simultaneously
   - Creating and managing threads in Python
   - Thread synchronization and safety

2. **Publish-Subscribe Pattern**
   - Decoupled communication between components
   - Message broadcasting
   - Role-based client behavior

3. **Thread Safety**
   - Race conditions and how to prevent them
   - Using locks (`threading.Lock()`)
   - Thread-safe data structures

4. **Advanced Socket Programming**
   - Managing multiple client connections
   - Bidirectional communication
   - Connection lifecycle management

---

## 🏗️ System Architecture

```
PUBLISHERS                SERVER                 SUBSCRIBERS
(Send messages)       (Routes messages)      (Receive messages)

┌─────────────┐                               ┌─────────────┐
│ Publisher 1 │───"Breaking news!"────┐       │Subscriber 1 │
└─────────────┘                       │       └─────────────┘
                                      ↓              ↑
┌─────────────┐               ┌──────────────┐      │
│ Publisher 2 │───"Sports!"───→│   SERVER     │──────┤
└─────────────┘                │ (Middleware) │      │
                               │              │      │
                               │ Features:    │      ↓
                               │ - Threading  │ ┌─────────────┐
                               │ - Broadcast  │ │Subscriber 2 │
                               │ - Roles      │ └─────────────┘
                               └──────────────┘

Flow: Publishers → Server → All Subscribers
```

---

## 🔑 Key Concepts Explained

### 1. **Threading (Concurrent Execution)**

#### **The Problem (Task 1 Approach):**
```python
# Single-threaded server (Task 1)
while True:
    client_socket, addr = server_socket.accept()  # Accept client 1
    handle_client(client_socket)                  # Handle client 1 (BLOCKS!)
    # Can't accept client 2 until client 1 finishes!
```

**Result:** Only ONE client at a time. Others must wait.

---

#### **The Solution (Task 2 Approach):**
```python
# Multi-threaded server (Task 2)
while True:
    client_socket, addr = server_socket.accept()  # Accept client
    
    # Create NEW THREAD for this client
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()  # Runs in BACKGROUND
    
    # Immediately ready to accept next client!
```

**Result:** Multiple clients handled simultaneously!

---

#### **How Threading Works:**

```
Main Thread:              Thread 1:            Thread 2:            Thread 3:
├─ Start server          ├─ Handle Client 1   ├─ Handle Client 2   ├─ Handle Client 3
├─ Accept Client 1 ──────┤                    │                    │
├─ Accept Client 2 ───────────────────────────┤                    │
├─ Accept Client 3 ────────────────────────────────────────────────┤
├─ Accept Client 4...    │                    │                    │
└─ (keeps accepting)     └─ (handles msgs)    └─ (handles msgs)    └─ (handles msgs)

ALL running at the SAME TIME!
```

**Analogy:**
- **Without threading:** Restaurant with 1 waiter (serves one table completely before next)
- **With threading:** Restaurant with many waiters (all tables served simultaneously)

---

### 2. **Publish-Subscribe Pattern**

#### **Traditional Request-Response (Task 1):**
```
Client: "Send me data"
  ↓
Server: "Here's your data"
  ↓
Client: "Thanks!"

Direct 1-to-1 communication
```

#### **Pub/Sub Pattern (Task 2):**
```
Publisher: "Here's news!" → Server → → → All Subscribers get it
                                    ↓
                                Subscriber 1
                                    ↓
                                Subscriber 2
                                    ↓
                                Subscriber 3

Publishers don't know who receives
Subscribers don't know who published
```

**Benefits:**
- **Decoupling:** Publishers and subscribers are independent
- **Scalability:** Easy to add more publishers/subscribers
- **Flexibility:** Subscribers can join/leave anytime

**Real-World Examples:**
- **YouTube:** Creators publish videos → Subscribers get notifications
- **WhatsApp Groups:** Someone sends message → All members receive
- **Stock Market:** Exchanges publish prices → Traders receive updates

---

### 3. **Thread Safety and Locks**

#### **The Problem: Race Conditions**

```python
# Two threads trying to modify the same list simultaneously:

# Thread 1 (at exact same time)     # Thread 2 (at exact same time)
subscribers.append(client1)          subscribers.append(client2)
#           ↑                        #           ↑
#    Both accessing same memory location!
#    ⚠️ Can cause data corruption or crash
```

**What can happen:**
- Data corruption (lost clients)
- Program crash
- Unpredictable behavior

---

#### **The Solution: Locks**

```python
# Create a lock
client_lock = threading.Lock()

# Thread 1
with client_lock:  # Acquire lock (like locking bathroom door)
    subscribers.append(client1)
# Release lock automatically

# Thread 2
with client_lock:  # Waits until Thread 1 releases lock
    subscribers.append(client2)
# Release lock

# ✅ Safe! Only one thread modifies at a time
```

**Analogy:**
```
Lock = Bathroom door lock
- Only ONE person can be inside at a time
- Others wait outside until door unlocks
- When done, next person can enter
```

---

### 4. **Client Roles**

#### **PUBLISHER Role:**
```python
1. Connect to server
2. Send role: "PUBLISHER"
3. Loop:
   - Type message
   - Send to server
   - Server broadcasts to all subscribers
4. Type "terminate" to quit
```

**Code Flow:**
```python
while True:
    message = input("> ")
    client_socket.send(message.encode('utf-8'))
    # Server handles broadcasting
```

---

#### **SUBSCRIBER Role:**
```python
1. Connect to server
2. Send role: "SUBSCRIBER"
3. Start background thread to receive messages
4. Main thread keeps connection alive
5. Press Ctrl+C to quit
```

**Code Flow:**
```python
# Start background thread
receive_thread = threading.Thread(target=receive_messages, args=(socket,))
receive_thread.start()

# Background thread continuously receives:
def receive_messages(client_socket):
    while True:
        data = client_socket.recv(1024)
        print(data.decode('utf-8'))
```

**Why threading for subscribers?**
- Need to **continuously listen** for messages
- Can't block on `input()` because messages might arrive
- Background thread handles receiving, main thread keeps program alive

---

## 🚀 How to Run

### **Prerequisites**
- Python 3.8+
- Multiple terminal windows (5+ recommended for full demo)
- Working Task 1 knowledge (basic sockets)

---

### **Step 1: Start the Server**

**Terminal 1:**
```bash
cd "c:\Users\Chamudu Hansana\Desktop\Projects\pubsub-middleware\task2"
python server.py 5000
```

**Expected Output:**
```
   Pub/Sub Middleware - Server (T2)   
Server bound - 0.0.0.0 : 5000
server listening on port 5000, waiting for client conection..
```

---

### **Step 2: Start Publishers**

**Terminal 2 (Publisher 1):**
```bash
cd "c:\Users\Chamudu Hansana\Desktop\Projects\pubsub-middleware\task2"
python client.py 127.0.0.1 5000
```

**Interaction:**
```
   Pub/Sub Middleware - Client (T2)   
Connecting to server at 127.0.0.1:5000...
Server Connected
Enter your role (PUBLISHER/SUBSCRIBER) : PUBLISHER    ← Type this

registerd as PUBLISHER

You are a PUBLISHER. Type messages to broadcast.
Type 'terminate' to quit.

> Breaking news!                                       ← Type messages
message sent

> Sports update!                                       ← Type messages
message sent
```

**Terminal 3 (Publisher 2):**
```bash
python client.py 127.0.0.1 5000
# Same process, type PUBLISHER
```

---

### **Step 3: Start Subscribers**

**Terminal 4 (Subscriber 1):**
```bash
cd "c:\Users\Chamudu Hansana\Desktop\Projects\pubsub-middleware\task2"
python client.py 127.0.0.1 5000
```

**Interaction:**
```
   Pub/Sub Middleware - Client (T2)   
Connecting to server at 127.0.0.1:5000...
Server Connected
Enter your role (PUBLISHER/SUBSCRIBER) : SUBSCRIBER   ← Type this

registerd as SUBSCRIBER
Waiting for messages...

You are a SUBSCRIBER. Waiting for messages...
Press Ctrl+C to quit.

[FROM 127.0.0.1:50123] : Breaking news!    ← Received from Publisher 1
[FROM 127.0.0.1:50124] : Sports update!    ← Received from Publisher 2
```

**Terminal 5 (Subscriber 2):**
```bash
python client.py 127.0.0.1 5000
# Same process, type SUBSCRIBER
# Receives SAME messages as Subscriber 1
```

---

### **What You Should See:**

```
SERVER TERMINAL:
─────────────────────────────────────────
Client connected from IP: 127.0.0.1 PORT:50123
Client thread started. Active clients: 1
[127.0.0.1:50123] Role: PUBLISHER
(127.0.0.1, 50123) added as a publisher 

Client connected from IP: 127.0.0.1 PORT:50124
Client thread started. Active clients: 2
[127.0.0.1:50124] Role: SUBSCRIBER
(127.0.0.1, 50124) added as a subscriber 

[PUBLISHER 127.0.0.1:50123]: Breaking news!
```

---

## 📝 Code Breakdown

### **Server Side**

#### **1. Global Variables (Thread-Shared Data)**
```python
publishers = []      # List of publisher sockets
subscribers = []     # List of subscriber sockets
client_lock = threading.Lock()  # For thread-safe access
```

**Why global?**
- All threads need access to these lists
- Shared between all client handlers
- Must be protected with lock

---

#### **2. Main Server Loop (Multi-Threaded Accept)**
```python
while True:
    client_socket, client_address = server_socket.accept()
    
    # Create NEW thread for each client
    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )
    client_thread.daemon = True  # Dies when main program exits
    client_thread.start()        # Runs in background
```

**`daemon = True` Explained:**
- **Normal thread:** Program waits for thread to finish before exiting
- **Daemon thread:** Dies automatically when main program exits
- **Use case:** Background workers (like our client handlers)

---

#### **3. Handle Client Function (Per-Client Logic)**
```python
def handle_client(client_socket, client_address):
    # 1. Ask for role
    client_socket.send("Enter your role...".encode('utf-8'))
    role = client_socket.recv(1024).decode('utf-8').strip().upper()
    
    # 2. Add to appropriate list (thread-safe)
    if role == "PUBLISHER":
        with client_lock:  # ← LOCK!
            publishers.append(client_socket)
    
    # 3. Handle based on role
    if role == "PUBLISHER":
        while True:
            data = client_socket.recv(1024)
            message = data.decode('utf-8')
            broadcast_to_subscribers(message, client_address)
    
    elif role == "SUBSCRIBER":
        # Just wait (messages sent via broadcast)
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
```

---

#### **4. Broadcast Function (Core Pub/Sub Logic)**
```python
def broadcast_to_subscribers(message, sender_address):
    formatted_message = f"[FROM {sender_address[0]}:{sender_address[1]}]: {message}\n"
    
    with client_lock:  # ← THREAD-SAFE
        for subscriber in subscribers:
            try:
                subscriber.send(formatted_message.encode('utf-8'))
            except:
                # Handle disconnected subscribers
                pass
```

**What this does:**
1. Format message with sender info
2. Lock the subscribers list (thread-safe)
3. Send to ALL subscribers
4. Handle errors (disconnected clients)

---

### **Client Side**

#### **1. Publisher Mode (Simple Loop)**
```python
if role == "PUBLISHER":
    while True:
        message = input("\n> ")
        client_socket.send(message.encode('utf-8'))
        
        if message == 'terminate':
            break
```

**Simple because:**
- Only sends, doesn't receive
- Sequential: type → send → wait for next input

---

#### **2. Subscriber Mode (Threading Required)**
```python
if role == "SUBSCRIBER":
    # Start background thread to receive
    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,)
    )
    receive_thread.daemon = True
    receive_thread.start()
    
    # Main thread: keep alive
    try:
        while True:
            time.sleep(1)  # Just wait
    except KeyboardInterrupt:
        print("Disconnecting...")
```

**Why threading?**
- Can't use `input()` (would block)
- Need to **continuously listen** for messages
- Background thread handles receiving
- Main thread keeps program running

---

#### **3. Receive Messages Function (Background Thread)**
```python
def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"\n{message}", end='')
        except:
            break
```

**This runs continuously in background**, printing messages as they arrive.

---

## 🎥 Video Recording Guide

### **Setup (Before Recording)**
- Open 5 terminal windows
- Arrange in grid layout (server + 2 publishers + 2 subscribers)
- Test once to ensure everything works

### **Recording Checklist**

**Part 1: Server Startup (5 seconds)**
- [ ] Show server starting
- [ ] Display server IP and port

**Part 2: Connect Clients (10 seconds)**
- [ ] Start Publisher 1, show role selection
- [ ] Start Publisher 2, show role selection
- [ ] Start Subscriber 1, show role selection
- [ ] Start Subscriber 2, show role selection

**Part 3: Demonstrate Pub/Sub (20 seconds)**
- [ ] Publisher 1 sends message
- [ ] Show message appearing on BOTH subscribers
- [ ] Publisher 2 sends different message
- [ ] Show message appearing on BOTH subscribers
- [ ] Demonstrate simultaneous publishing

**Part 4: Show Server Log (5 seconds)**
- [ ] Switch to server terminal
- [ ] Show client connections
- [ ] Show message routing logs

**Part 5: Clean Shutdown (5 seconds)**
- [ ] Type "terminate" in publisher
- [ ] Press Ctrl+C in subscriber
- [ ] Show clean disconnection

---

## 🐛 Common Issues & Solutions

### **Issue 1: "Address already in use"**

**Cause:** Server port not released from previous run

**Solution:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID 12345 /F

# Or use different port
python server.py 5001
```

---

### **Issue 2: Subscribers not receiving messages**

**Possible causes:**
1. Typo in role name (check spelling: SUBSCRIBER)
2. Function name mismatch (`broadcast_to_subs` vs `broadcast_to_sub`)
3. Lock not released (deadlock)

**Debug:**
```python
# Add print statements in broadcast function
print(f"Broadcasting to {len(subscribers)} subscribers")
```

---

### **Issue 3: "TypeError: 'list' object is not callable"**

**Cause:** Using `()` instead of `[]` for list access

**Fix:**
```python
# WRONG
sys.argv(1)

# CORRECT
sys.argv[1]
```

---

### **Issue 4: Messages not formatted correctly**

**Check:**
```python
# Publisher should use strip()
if message.strip() == 'terminate':  # Not just: if message == 'terminate'
```

---

### **Issue 5: Subscriber exits immediately**

**Cause:** Main thread not kept alive

**Fix:**
```python
# Need this loop to keep program running
while True:
    time.sleep(1)
```

---

## ✅ Testing Checklist

Before recording video:

**Server:**
- [ ] Starts without errors
- [ ] Accepts multiple connections
- [ ] Shows client roles correctly
- [ ] Displays published messages
- [ ] Handles client disconnections

**Publisher:**
- [ ] Connects successfully
- [ ] Sends role correctly
- [ ] Can send multiple messages
- [ ] Terminate command works
- [ ] Clean exit

**Subscriber:**
- [ ] Connects successfully
- [ ] Sends role correctly
- [ ] Receives messages from ALL publishers
- [ ] Can exit with Ctrl+C
- [ ] No errors when receiving

**Integration:**
- [ ] Multiple publishers can publish simultaneously
- [ ] All subscribers receive ALL messages
- [ ] Order of messages is preserved
- [ ] No messages lost
- [ ] Server doesn't crash when client disconnects

---

## 📚 Key Takeaways

After completing Task 2, you should understand:

1. ✅ **Threading Fundamentals**
   - Creating threads with `threading.Thread()`
   - Daemon threads vs normal threads
   - Running code concurrently

2. ✅ **Thread Safety**
   - Race conditions and their dangers
   - Using `threading.Lock()` for protection
   - `with lock:` pattern for safe access

3. ✅ **Pub/Sub Pattern**
   - Publisher role: produces messages
   - Subscriber role: consumes messages
   - Server role: routes messages
   - Decoupling producers from consumers

4. ✅ **Advanced Socket Concepts**
   - Managing multiple connections
   - Bidirectional communication
   - Connection lifecycle (connect → communicate → cleanup)
   - Error handling for network issues

5. ✅ **Real-World Applications**
   - Chat systems (WhatsApp, Slack)
   - Notification systems (push notifications)
   - Live updates (stock prices, sports scores)
   - IoT data distribution

---

## 🎓 Comparison: Task 1 vs Task 2

| Feature | Task 1 | Task 2 |
|---------|--------|--------|
| **Clients** | 1 at a time | Multiple concurrent |
| **Threading** | No | Yes (server + subscriber) |
| **Pattern** | Simple messaging | Pub/Sub |
| **Roles** | No roles | Publisher/Subscriber |
| **Complexity** | Simple | Moderate |
| **Real-world** | Basic demo | Production-like |

---

## 📖 Further Reading

### **Threading Concepts:**
- [Python Threading Tutorial](https://docs.python.org/3/library/threading.html)
- [Real Python: Threading](https://realpython.com/intro-to-python-threading/)
- [Thread Safety in Python](https://superfastpython.com/thread-safe-in-python/)

### **Pub/Sub Pattern:**
- [Publish-Subscribe Pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)
- [Message Queue Systems](https://www.cloudamqp.com/blog/what-is-message-queuing.html)
- [Redis Pub/Sub](https://redis.io/topics/pubsub)

### **Concurrency:**
- [Threading vs Multiprocessing](https://realpython.com/python-concurrency/)
- [GIL in Python](https://realpython.com/python-gil/)

---

## 🚀 Next Steps

Once Task 2 is working:
1. ✅ Record the screencast
2. ✅ Test with multiple clients (5+)
3. ✅ Understand every line of code
4. ➡️ Move to **Task 3**: Topic-based filtering (subscribers choose what to receive)

---

## 💡 Bonus Challenge

Try enhancing your Task 2:
- Add client names/IDs
- Show online client count
- Add message timestamps
- Handle network errors gracefully
- Add message history for new subscribers

---

**Congratulations on completing Task 2!** 🎉

*You've built a concurrent, multi-client publish-subscribe system!*

*Last Updated: January 2026*
