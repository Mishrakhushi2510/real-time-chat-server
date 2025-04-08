import socket
import threading
import os

# Function to handle a client connection
def handle_client(client_socket, client_address):
    print(f"[INFO] Connection established with {client_address}")
    
    try:
        while True:
            # Receive command from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f"[INFO] Connection closed by {client_address}")
                break
            
            if data == "SEND_FILE":
                receive_file(client_socket)
            elif data == "RECEIVE_FILE":
                send_file(client_socket)
            else:
                # Handle chat messages
                print(f"[CHAT] {client_address}: {data}")
                response = f"Server Echo: {data}"
                client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] An error occurred with {client_address}: {e}")
    finally:
        client_socket.close()

# Function to receive a file from the client
def receive_file(client_socket):
    try:
        filename = client_socket.recv(1024).decode('utf-8')
        if not filename:
            return

        file_size = int(client_socket.recv(1024).decode('utf-8'))
        print(f"[INFO] Receiving file '{filename}' of size {file_size} bytes...")

        # Save the received file
        with open(f"received_{filename}", "wb") as f:
            bytes_received = 0
            while bytes_received < file_size:
                file_data = client_socket.recv(1024)
                if not file_data:
                    break
                f.write(file_data)
                bytes_received += len(file_data)

        print(f"[SUCCESS] File '{filename}' received successfully.")
        client_socket.send(b"File received successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to receive file: {e}")
        client_socket.send(b"ERROR: Failed to receive file.")

# Function to send a file to the client
def send_file(client_socket):
    try:
        filename = client_socket.recv(1024).decode('utf-8')
        if not os.path.exists(filename):
            client_socket.send(b"ERROR: File not found")
            return

        file_size = os.path.getsize(filename)
        client_socket.send(str(file_size).encode('utf-8'))
        client_socket.recv(1024)  # Wait for acknowledgment (optional)

        print(f"[INFO] Sending file '{filename}' of size {file_size} bytes...")

        # Read and send the file in chunks
        with open(filename, "rb") as f:
            while True:
                file_data = f.read(1024)
                if not file_data:
                    break
                client_socket.send(file_data)

        print(f"[SUCCESS] File '{filename}' sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send file: {e}")
        client_socket.send(b"ERROR: Failed to send file.")

# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.140.25', 5555))  # Bind to all interfaces
    server_socket.listen(5)
    print("[INFO] Server is listening on port 5555...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down the server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
