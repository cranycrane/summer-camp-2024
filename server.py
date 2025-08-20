import socket
import threading

HOST = "localhost"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def handle_client(conn, addr):
    print(f"[PŘIPOJEN] {addr}")
    while True:
        try:
            msg = conn.recv(1024).decode("utf-8")
            if not msg:
                break
            print(f"[{addr}] {msg}")
            broadcast(msg, conn)
        except:
            break

    conn.close()
    clients.remove(conn)
    print(f"[ODPOJEN] {addr}")

def broadcast(msg, sender_conn):
    for client in clients:
        if client != sender_conn:
            client.sendall(msg.encode("utf-8"))

print("[SERVER] Běží...")
while True:
    conn, addr = server.accept()
    clients.append(conn)
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
