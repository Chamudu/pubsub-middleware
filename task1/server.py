import sys
import socket

def print_header():
     print("   Pub/Sub Middleware - Server (T1)   ")

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

def start_server(port):
    HOST = '0.0.0.0'
    BUFFER_SIZE = 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, port))
        print(f'Server bound - {HOST} : {port}')

        server_socket.listen(1)
        print(f'server listening on port {port}, waiting for client conection..')
        print()

        client_socket, client_address = server_socket.accept()
        print(f"Client connected from IP: {client_address[0]} PORT:{client_address[1]}")
        print("─" * 50)
        print()

        # Message recieving loop
        while True:
            data = client_socket.recv(BUFFER_SIZE)

            if not data:
                print("Client conection closed")
                break

            message = data.decode('utf-8').strip()

            print(f"[{client_address[0]} : {client_address[1]}] : {message}")

            if message == 'terminate':
                print("\n Termination signal received")
                break
        print()
        print("─" * 50)
        print("Client disconnected.")

    except KeyboardInterrupt:
        print("\n\ Server interrupted by user (Ctrl+C)")

    except Exception as e:
        print(f"\n ERROR: {e}")
        

    finally:
        try:
            client_socket.close()
            print("client socket closed")
        
        except:
            pass

        server_socket.close()
        print("server socket closed. Server shutting down..")

def main():
    print_header()
    port = validate_arguments()
    start_server(port)

if __name__ == "__main__":
    main()










