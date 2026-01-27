import threading
import socket
import sys

def print_header():
    print("   Pub/Sub Middleware - Client (T2)")
    print("-"*40)
    print()

def validate_arguments():
    if len(sys.argv) != 3 :
        print("ERROR: Invalid number of arguments")
        print("Usage: python client.py <SERVER_IP> <SERVER_PORT>")
        sys.exit(1)

    server_ip = sys.argv[1]

    try:
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            print("ERROR: Port must be between 1024 and 65535")
            sys.exit(1)
        return server_ip, server_port
    except ValueError:
        print(f"ERROR: '{sys.argv[2]}' is not a valid port number")
        sys.exit(1)

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                print("Server conection lost")
                break
            
            message = data.decode('utf-8')
            print(f"\n{message}", end='')
        
        except Exception as e:
            print(f"\n✗ Error receiving message: {e}")
            break

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        print(f"Connecting to server at {server_ip}:{server_port}...")
        client_socket.connect((server_ip, server_port))

        print("Server Connected")
        print("─" * 50)

        # role request from the server
        role_req = client_socket.recv(1024).decode('utf-8')
        print(role_req, end='')

        # get role from user
        role = input().strip().upper()

        if role not in ['PUBLISHER', 'SUBSCRIBER']:
            print("Invalid role! Must be PUBLISHER or SUBSCRIBER")
            client_socket.close()
            return

        client_socket.send(role.encode('utf-8'))
        print(f"registerd as {role}")
        print()

        if role == 'PUBLISHER':
            print("─" * 50)
            print("You are a PUBLISHER. Type messages to broadcast.")
            print("Type 'terminate' to quit.")
            print("─" * 50)

            while True:
                message = input("\n> ")

                if not message.strip():
                    print('message cant be empty')
                    continue

                client_socket.send(message.encode('utf-8'))
                print('message sent')

                if message == 'terminate':
                    print('Disconnecting...')
                    break
        elif role == "SUBSCRIBER":
            confirmation = client_socket.recv(1024).decode('utf-8')
            print(confirmation)

            print("─" * 50)
            print("You are a SUBSCRIBER. Waiting for messages...")
            print("Press Ctrl+C to quit.")
            print("─" * 50)
            print()

            receive_thread = threading.Thread(
                target=receive_messages,
                args=(client_socket,)
            )

            receive_thread.daemon = True
            receive_thread.start()

            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print('\n Subscriber Disconecting..')
    
    except KeyboardInterrupt:
        print('ctrl+c interupt')
    
    finally:
        client_socket.close()
        print('client socket closed and shuting down...')



def main():
    print_header()
    server_ip, server_port = validate_arguments()
    start_client(server_ip, server_port)

if __name__ == "__main__":
    main()




