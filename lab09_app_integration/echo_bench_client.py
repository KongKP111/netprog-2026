import socket
import sys
import time
import json

def run_benchmark(server_ip, port=5000, count=50, msg_size=64):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, port))
    payload = b"x" * msg_size
    rtts_ms = []
    for i in range(count):
        start = time.perf_counter()                                # TODO 1
        sock.sendall(payload)
        sock.recv(msg_size)
        rtts_ms.append((time.perf_counter() - start) * 1000)       # TODO 2
    sock.close()
    return rtts_ms

if __name__ == "__main__":
    server_ip = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else "run"
    rtts_ms = run_benchmark(server_ip)
    print(f"{label}: min={min(rtts_ms):.3f}ms avg={sum(rtts_ms)/len(rtts_ms):.3f}ms max={max(rtts_ms):.3f}ms")
    with open(f"rtt_{label}.json", "w") as f:
        json.dump(rtts_ms, f)
