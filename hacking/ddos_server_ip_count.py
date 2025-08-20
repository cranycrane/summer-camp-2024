import socket
import threading
import time
import matplotlib.pyplot as plt
from collections import deque, defaultdict, Counter

HOST = "0.0.0.0"   # aby se mohli připojit i ostatní v síti
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(200)  # větší fronta čekajících spojení

# --- sdílený stav ---
request_count = 0
per_ip_current = defaultdict(int)
lock = threading.Lock()

history_total = deque(maxlen=60)
per_ip_history = deque(maxlen=10)
TOP_K = 8

# --- obsluha klienta ---
def handle_client(conn, addr):
    global request_count
    ip = addr[0]
    try:
        while True:
            msg = conn.recv(1024)
            if not msg:
                break
            with lock:
                request_count += 1
                per_ip_current[ip] += 1
    except Exception:
        pass
    finally:
        try:
            conn.close()
        except:
            pass

# --- monitorovací vlákno ---
def monitor():
    global request_count, per_ip_current
    
    plt.ion()
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    while True:
        time.sleep(1)

        with lock:
            total = request_count
            snapshot = dict(per_ip_current)
            request_count = 0
            per_ip_current.clear()

        history_total.append(total)
        per_ip_history.append(snapshot)

        # ---- graf 1: celkem req/s ----
        ax1.clear()
        ax1.plot(list(history_total), marker='o')
        ax1.set_ylim(0, max(10, max(history_total)))
        ax1.set_xlabel("Sekundy (posledních 60)", fontsize=32)
        ax1.set_ylabel("Požadavky / s", fontsize=32)
        ax1.set_title("Celkem požadavků za sekundu", fontsize=32)
        ax1.tick_params(axis='both', labelsize=32)
        plt.pause(0.001)

        # ---- graf 2: TOP IP ----
        agg = Counter()
        for d in per_ip_history:
            agg.update(d)
        top = agg.most_common(TOP_K)

        ax2.clear()
        if top:
            labels = [ip for ip, c in top]
            values = [c for ip, c in top]
            ax2.bar(labels, values)
            ax2.set_ylim(0, max(5, max(values)))
            ax2.set_ylabel("Požadavky (součet za 10 s)", fontsize=32)
            ax2.set_title(f"TOP {TOP_K} IP (rolling 10 s)", fontsize=32)
            ax2.set_xticklabels(labels, rotation=45, ha='right', fontsize=32)
            ax2.tick_params(axis='y', labelsize=32)
        else:
            ax2.set_title("TOP IP (zatím žádná data)", fontsize=32)
        plt.pause(0.001)

# spustit monitor
threading.Thread(target=monitor, daemon=True).start()

print(f"[SERVER] Běží na {HOST}:{PORT}…")
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
