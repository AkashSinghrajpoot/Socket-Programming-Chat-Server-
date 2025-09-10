import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 55555

# List to keep track of connected clients
clients = []

def handle_client(client_socket):
    """
    Handles a single client connection.
    """
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            # Broadcast the message to all other clients
            broadcast(message, client_socket)
        except:
            # If an error occurs, the client has disconnected
            print(f"Client {client_socket.getpeername()} disconnected.")
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, sender_socket):
    """
    Sends a message to all connected clients except the sender.
    """
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # If a client cannot receive a message, it's likely disconnected
                client.close()
                clients.remove(client)

def start_server():
    """
    Starts the server and listens for incoming connections.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        clients.append(client_socket)

        # Start a new thread for each client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()