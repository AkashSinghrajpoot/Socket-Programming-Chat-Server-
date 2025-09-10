import socket
import threading

# Client configuration
HOST = '127.0.0.1'
PORT = 55555

def receive_messages(client_socket):
    """
    Receives and prints messages from the server.
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            # If an error occurs, the connection is lost
            print("Disconnected from server.")
            client_socket.close()
            break

def send_messages(client_socket):
    """
    Sends user input as a message to the server.
    """
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

def start_client():
    """
    Starts the client, connects to the server, and sets up threads for
    sending and receiving messages.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("Connected to the chat server!")

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    # Start a thread to send messages to the server
    send_thread = threading.Thread(target=send_messages, args=(client,))
    send_thread.start()

if __name__ == "__main__":
    start_client()