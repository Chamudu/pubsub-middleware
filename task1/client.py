import socket
import sys

def print_header():
    print("   Pub/Sub Middleware - Client (T1)")
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

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"Connecting to server at {server_ip}:{server_port}...")
    client_socket.connect((server_ip, server_port))
        
    print("Server Connected")
    print("─" * 50)

    while True:
        message = input("Type a message > ")

        if not message.strip():
            print("Message cant be empty")
            continue

        client_socket.send(message.encode('utf-8'))

        print("Message Sent")

        if message.strip() == 'terminate':
            print("Disconecting from server")
            break

    print()
    print("disconected succesfully")
    client_socket.close()

def main():
    print_header()
    server_ip, server_port = validate_arguments()
    start_client(server_ip, server_port)

if __name__ == "__main__":
    main()




