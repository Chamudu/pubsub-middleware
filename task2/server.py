import sys
import socket
import threading

publishers = []
subscribers = []
client_lock = threading.Lock()


def print_header():
     print("   Pub/Sub Middleware - Server (T2)   ")

def validate_arguments():
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    try :
        port = int(sys.argv[1])
        if port < 1024 or port > 65535:
            print("Port must be between 1024 - 65535")
            sys.exit(1)
        return port

    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid port number")
        sys.exit(1)

def handle_clients(client_socket, client_address):

    try:
        client_socket.send("Enter your role (PUBLISHER/SUBSCRIBER) : ".encode('utf-8'))

        role = client_socket.recv(1024).decode('utf-8').strip().upper()
        print(f"[{client_address[0]}:{client_address[1]}] Role: {role}")

        if role == 'PUBLISHER':
            with client_lock:
                publishers.append(client_socket)
            print(f"{client_address} added as a publisher ")

            while True:
                data = client_socket.recv(1024)
                if not data:
                    print(f"Publisher {client_address} disconnected")
                    break

                message = data.decode('utf-8').strip()
                print(f"[PUBLISHER {client_address[0]}:{client_address[1]}]: {message}")

                broadcast_to_subs(message, client_address)
                if message == 'terminate':
                    break

        
        elif role == "SUBSCRIBER":
            with client_lock:
                subscribers.append(client_socket)
            print(f"{client_address} added as a subscriber ")

            client_socket.send("Waiting for messages...\n".encode('utf-8'))

            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        print(f"Subscriber {client_address} disconnected")
                        break
                except:
                    break

        else:
            client_socket.send("Invalid role! Disconnecting.\n".encode('utf-8'))
            client_socket.close()
            return

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
        
    # Remove client from lists
    finally:
        with client_lock:
            if client_socket in publishers:
                publishers.remove(client_socket)
                print(f"Publisher removed. Total: {len(publishers)}")
            if client_socket in subscribers:
                subscribers.remove(client_socket)
                print(f"Subscriber removed. Total: {len(subscribers)}")
        # close socket
        client_socket.close() 
        print(f"Connection closed for {client_address}")

def broadcast_to_subs(message, sender_address):
    pub_message = f"[FROM {sender_address[0]}:{sender_address[1]}] : {message} \n"    

    with client_lock:
        dead_subs = []

        for sub in subscribers:
            try:
                sub.send(pub_message.encode('utf-8'))
            except:
                dead_subs.append(sub)

        # Remove dead subscribers
        for dead_sub in dead_subs:
            subscribers.remove(dead_sub)
            print("Removed disconnected subscriber")




def start_server(port):
    HOST = '0.0.0.0'
    BUFFER_SIZE = 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, port))
        print(f'Server bound - {HOST} : {port}')

        server_socket.listen(10)
        print(f'server listening on port {port}, waiting for client conection..')
        print()

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected from IP: {client_address[0]} PORT:{client_address[1]}")

            # create a new thread for the client
            client_thread = threading.Thread(
                target=handle_clients,
                args=(client_socket, client_address)
            )
            client_thread.daemon = True  # Thread dies when main program exits
            client_thread.start()  # Start thread (runs in background)

            print(f"Client thread started. Active clients: {threading.active_count() - 1}")

    except KeyboardInterrupt:
        print("\n\nServer interrupted by user (Ctrl+C)")

    except Exception as e:
        print(f"\nERROR: {e}")

    finally:
        server_socket.close()
        print("Server socket closed. Server shutting down...")

       

def main():
    print_header()
    port = validate_arguments()
    start_server(port)

if __name__ == "__main__":
    main()










