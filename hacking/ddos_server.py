import socket
import threading
import time
import matplotlib.pyplot as plt
from collections import deque

HOST = "localhost"
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

request_count = 0
history = deque(maxlen=60)  # posledních 30 sekund

# funkce pro obsluhu klienta
def handle_client(conn, addr):
    global request_count
    while True:
        try:
            msg = conn.recv(1024)
            if not msg:
                break
            request_count += 1
        except:
            break
    conn.close()

# funkce pro monitorování a graf
def monitor():
    global request_count
    plt.ion()  # interaktivní režim
    fig, ax = plt.subplots()
    while True:
        time.sleep(1)
        history.append(request_count)
        ax.clear()
        ax.plot(list(history), marker='o')
        ax.set_ylim(0, max(10, max(history)))  # automatické škálování
        ax.set_xlabel("Sekundy")
        ax.set_ylabel("Počet požadavků")
        ax.set_title("Simulovaný DDoS - počet požadavků za sekundu")
        plt.pause(0.01)
        request_count = 0

# spustit monitor
threading.Thread(target=monitor, daemon=True).start()

print("[SERVER] Běží...")
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
