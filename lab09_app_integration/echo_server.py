import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
    except ConnectionResetError:
        print(f"Client {addr} disconnected abruptly")
    print(f"Connection with {addr} closed")

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"Echo server listening on {HOST}:{PORT}")
    try:
        while True:
            conn, addr = server_sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nShutting down server. Goodbye!")
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()
