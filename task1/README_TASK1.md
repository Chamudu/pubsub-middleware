# Task 1: Basic Client-Server Communication

## 📋 Objective
Implement a simple client-server socket application where:
- Server listens on a specified PORT
- Client connects using server IP and PORT
- Text typed on client appears on server terminal
- Client disconnects when "terminate" is typed

---

## 🎯 Learning Goals

By completing this task, you will understand:
1. **Socket creation** - How to create TCP sockets in Python
2. **Server binding** - How servers claim a port and listen for connections
3. **Client connection** - How clients connect to a server
4. **Data transmission** - How to send/receive data over sockets
5. **Connection management** - How to properly close connections

---

## 🏗️ Architecture

```
┌─────────────────┐                    ┌─────────────────┐
│  Client         │                    │  Server         │
│  127.0.0.1      │                    │  0.0.0.0:5000   │
├─────────────────┤                    ├─────────────────┤
│ 1. Create socket│                    │ 1. Create socket│
│ 2. Connect()    │──── TCP SYN ────>  │ 2. Bind()       │
│ 3. Send data    │<─── SYN-ACK ─────  │ 3. Listen()     │
│ 4. Close        │──── ACK ────────>  │ 4. Accept()     │
└─────────────────┘                    │ 5. Recv/Print   │
                                        └─────────────────┘
```

---

## 🚀 How to Run

### Step 1: Start the Server

Open **Command Prompt** or **PowerShell**:

```bash
cd "c:\Users\Chamudu Hansana\Desktop\Projects\pubsub-middleware\task1"
python server.py 5000
```

**Expected Output:**
```
╔════════════════════════════════════════╗
║   Pub/Sub Middleware - Server (T1)    ║
╚════════════════════════════════════════╝
Server listening on 0.0.0.0:5000
Waiting for client connection...
```

---

### Step 2: Start the Client

Open **another terminal**:

```bash
cd "c:\Users\Chamudu Hansana\Desktop\Projects\pubsub-middleware\task1"
python client.py 127.0.0.1 5000
```

**Expected Output:**
```
╔════════════════════════════════════════╗
║   Pub/Sub Middleware - Client (T1)    ║
╚════════════════════════════════════════╝
Connected to server at 127.0.0.1:5000
Type your message (type 'terminate' to quit):
>
```

---

### Step 3: Send Messages

In the **client terminal**, type messages:

```
> Hello Server!
> This is a test message
> Testing socket communication
> terminate
```

**Server terminal will show:**
```
Client connected from ('127.0.0.1', 54321)
[127.0.0.1:54321]: Hello Server!
[127.0.0.1:54321]: This is a test message
[127.0.0.1:54321]: Testing socket communication
[127.0.0.1:54321]: terminate
Client disconnected.
Server shutting down...
```

---

## 📝 Code Explanation

### Server Code Breakdown

```python
import socket
import sys

# Get port from command line
PORT = int(sys.argv[1])  # python server.py 5000 → PORT = 5000
```

**Why command line argument?**
- Flexibility: Can run on different ports
- Real servers often need configurable ports
- Assignment requirement

---

```python
# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

**Breaking down the parameters:**
- `socket.AF_INET` = Address Family: IPv4 (vs IPv6 = AF_INET6)
- `socket.SOCK_STREAM` = Socket Type: TCP (vs UDP = SOCK_DGRAM)

**Why TCP?**
- ✅ Reliable: Guarantees delivery
- ✅ Ordered: Messages arrive in sequence
- ✅ Error-checked: Detects corruption
- ✅ Connection-based: Know when client disconnects

---

```python
# Allow port reuse
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

**What this does:**
Allows immediate port reuse after server stops.

**Without this:**
```
Server stops → Port in TIME_WAIT state (60s) → Can't restart immediately
Error: "Address already in use"
```

**With this:**
```
Server stops → Can restart immediately → No wait time
```

---

```python
# Bind to address and port
server_socket.bind(('0.0.0.0', PORT))
```

**What is bind()?**
Claims a specific address and port for the server.

**Address options:**
- `'0.0.0.0'` = Listen on ALL network interfaces (recommended)
- `'127.0.0.1'` = Only local connections (localhost)
- `'192.168.1.5'` = Only this specific IP

**Real-world example:**
```
Your computer has:
- 127.0.0.1: Loopback (local only)
- 192.168.1.5: WiFi interface
- 0.0.0.0: All of the above
```

---

```python
# Listen for connections
server_socket.listen(1)
```

**What is listen()?**
Tells the OS: "I'm ready to accept connections"

**Parameter (1):**
Backlog queue size = maximum pending connections

**Example:**
```
listen(5) means:
- 1 client actively connected
- 5 more can queue up
- 6th client gets "Connection refused"
```

For Task 1, we only need 1 client, so `listen(1)` is fine.

---

```python
# Accept connection
client_socket, client_address = server_socket.accept()
```

**What is accept()?**
- **Blocking call**: Waits until a client connects
- Returns: (new socket, client address)
- `client_socket`: Used to communicate with THIS specific client
- `client_address`: Tuple of (IP, port)

**Why two sockets?**
```
server_socket: Listening for new connections (mailbox)
client_socket: Talking to specific client (phone line)
```

---

```python
# Receive and print messages
while True:
    data = client_socket.recv(1024)
    if not data:
        break  # Client disconnected
    
    message = data.decode('utf-8').strip()
    print(f"[{client_address[0]}:{client_address[1]}]: {message}")
    
    if message == 'terminate':
        break
```

**Breaking down recv():**
- `recv(1024)`: Read up to 1024 bytes
- Returns **bytes**, not string
- Returns **empty bytes `b''`** when client disconnects

**Why decode()?**
```python
data = b'Hello'  # Bytes
message = data.decode('utf-8')  # 'Hello' (string)
```

Sockets transmit raw bytes, we need text.

**Why strip()?**
Removes whitespace and newline characters:
```python
'Hello\n'.strip() → 'Hello'
'  World  '.strip() → 'World'
```

---

### Client Code Breakdown

```python
# Connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
```

**Key difference from server:**
- Client: `connect()` - actively initiates connection
- Server: `bind()` + `listen()` + `accept()` - passively waits

**What connect() does:**
1. Sends SYN packet to server
2. Waits for SYN-ACK
3. Sends ACK (three-way handshake)
4. Connection established!

---

```python
# Send messages
while True:
    message = input("> ")
    client_socket.send(message.encode('utf-8'))
    
    if message == 'terminate':
        break
```

**Why encode()?**
```python
message = 'Hello'  # String
data = message.encode('utf-8')  # b'Hello' (bytes)
client_socket.send(data)
```

**Why UTF-8?**
- Universal encoding
- Supports all languages
- 1 byte for ASCII, up to 4 for others
- Standard for text transmission

---

## 🎥 Video Recording Guide

### What to Show

1. **Server Startup** (5 seconds)
   - Run `python server.py 5000`
   - Show "Server listening" message
   - Show "Waiting for connection" message

2. **Client Connection** (5 seconds)
   - Run `python client.py 127.0.0.1 5000`
   - Show connection success message
   - Show prompt for input

3. **Message Exchange** (20 seconds)
   - Type 3-4 messages in client
   - Show each message appearing on server terminal
   - Ensure both terminals are visible (split screen)

4. **Termination** (5 seconds)
   - Type "terminate" in client
   - Show client disconnect message on both sides
   - Show clean shutdown

### Screen Layout

```
┌──────────────────┬──────────────────┐
│  Server Terminal │ Client Terminal  │
│                  │                  │
│  Server          │  Client          │
│  listening...    │  Connected!      │
│                  │                  │
│  Received:       │  > Hello         │
│  Hello           │                  │
│                  │  > terminate     │
│  Received:       │                  │
│  terminate       │  Disconnected    │
│                  │                  │
│  Client          │                  │
│  disconnected    │                  │
└──────────────────┴──────────────────┘
```

Use **Windows Terminal** split panes or **screen recording software** to show both.

---

## 🐛 Common Issues & Solutions

### Issue 1: "No module named 'socket'"

**Cause:** Socket is built-in, but Python not found

**Solution:**
```bash
# Check Python installation
python --version

# Should show: Python 3.8+
```

---

### Issue 2: "Address already in use"

**Cause:** Server still running or port not released

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

### Issue 3: "Connection refused"

**Possible causes:**
1. Server not running → Start server first
2. Wrong IP/port → Check arguments
3. Firewall blocking → Allow Python in firewall

**Debug steps:**
```bash
# 1. Test locally first
python server.py 5000
python client.py 127.0.0.1 5000  # Use localhost

# 2. If that works, try LAN IP
python client.py 192.168.1.5 5000
```

---

### Issue 4: "Invalid literal for int()"

**Error:**
```
ValueError: invalid literal for int() with base 10: ''
```

**Cause:** Missing port argument

**Solution:**
```bash
# Wrong
python server.py

# Correct
python server.py 5000
```

---

### Issue 5: Nothing appears on server

**Possible causes:**
1. Client not encoding: `send(message.encode())`
2. Server not decoding: `data.decode()`
3. No newline: Add `\n` or use `strip()`

**Debug:**
```python
# Add print statements
print(f"Raw data: {data}")
print(f"Decoded: {data.decode('utf-8')}")
```

---

## ✅ Testing Checklist

Before recording the video, verify:

- [ ] Server starts without errors
- [ ] Server displays listening message
- [ ] Client connects successfully
- [ ] Connection message shows on server
- [ ] Messages typed in client appear on server
- [ ] Multiple messages work consecutively
- [ ] "terminate" keyword stops client
- [ ] Server shows disconnect message
- [ ] Both programs exit cleanly
- [ ] Can restart server immediately (no port conflict)

---

## 🎓 Key Takeaways

After completing Task 1, you should understand:

1. ✅ **Socket Creation**: How to create TCP/IP sockets
2. ✅ **Server Setup**: bind() → listen() → accept() flow
3. ✅ **Client Connection**: connect() to establish link
4. ✅ **Data Encoding**: Bytes ↔ String conversion
5. ✅ **Connection Lifecycle**: Connect → Communicate → Disconnect
6. ✅ **Error Handling**: Common socket errors and fixes

---

## 📚 Further Reading

**Python Documentation:**
- [socket — Low-level networking](https://docs.python.org/3/library/socket.html)
- [Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)

**Concepts:**
- TCP/IP Protocol Stack
- OSI Model (Layer 4: Transport)
- IPv4 vs IPv6
- Port numbers and ranges

---

## 🚀 Next Steps

Once Task 1 is working:
1. ✅ Record the screencast
2. ✅ Understand every line of code
3. ✅ Experiment: Try different ports, messages
4. ➡️ Move to **Task 2**: Multiple concurrent clients

---

**Congratulations on completing Task 1!** 🎉

*You've built your first networked application!*
