import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Could not reach server — is it running?")
        return
    print("Connected to server. Type a message and press Enter ('quit' to exit).")
    with sock:
        while True:
            msg = input("> ")
            if msg == "quit":
                break
            sock.sendall(msg.encode("utf-8"))
            data = sock.recv(1024)
            print(f"Echoed back: {data.decode('utf-8')}")

if __name__ == "__main__":
    main()
