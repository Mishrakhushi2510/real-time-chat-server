import socket
import os

# Function to send a file to the server
def send_file(client_socket):
    try:
        filename = input("Enter the filename to send: ")
        if not os.path.exists(filename):
            print("[ERROR] File does not exist.")
            return

        client_socket.send("SEND_FILE".encode('utf-8'))
        client_socket.send(os.path.basename(filename).encode('utf-8'))
        
        file_size = os.path.getsize(filename)
        client_socket.send(str(file_size).encode('utf-8'))
        
        print(f"[INFO] Sending file '{filename}' of size {file_size} bytes...")

        with open(filename, "rb") as f:
            while True:
                file_data = f.read(1024)
                if not file_data:
                    break
                client_socket.send(file_data)

        server_response = client_socket.recv(1024).decode('utf-8')
        print(f"[SUCCESS] {server_response}")
    except Exception as e:
        print(f"[ERROR] Error while sending file: {e}")

# Function to receive a file from the server
def receive_file(client_socket):
    try:
        filename = input("Enter the filename to receive: ")
        client_socket.send("RECEIVE_FILE".encode('utf-8'))
        client_socket.send(filename.encode('utf-8'))
        
        response = client_socket.recv(1024).decode('utf-8')
        if response.startswith("ERROR"):
            print(f"[ERROR] {response}")
            return

        file_size = int(response)
        print(f"[INFO] Receiving file '{filename}' of size {file_size} bytes...")

        with open(f"received_{filename}", "wb") as f:
            bytes_received = 0
            while bytes_received < file_size:
                file_data = client_socket.recv(1024)
                if not file_data:
                    break
                f.write(file_data)
                bytes_received += len(file_data)

        print(f"[SUCCESS] File '{filename}' received successfully.")
    except Exception as e:
        print(f"[ERROR] Error while receiving file: {e}")

# Main function
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('192.168.140.25', 5555))  # Replace with server's IP if needed
        print("[INFO] Connected to the server.")

        while True:
            action = input("Enter 'message', 'send', 'receive', or 'exit': ").lower()
            if action == 'message':
                message = input("Enter your message: ")
                client_socket.send(message.encode('utf-8'))
                response = client_socket.recv(1024).decode('utf-8')
                print(f"Server: {response}")
            elif action == 'send':
                send_file(client_socket)
            elif action == 'receive':
                receive_file(client_socket)
            elif action == 'exit':
                print("[INFO] Exiting...")
                break
            else:
                print("[ERROR] Invalid option.")
    except Exception as e:
        print(f"[ERROR] Could not connect to the server: {e}")
    finally:
        client_socket.close()
        print("[INFO] Disconnected.")

if __name__ == "__main__":
    main()


