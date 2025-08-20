import socket
import threading

HOST = "localhost"
PORT = 12345

# Připojení k serveru
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Nastavení jména
nickname = input("Zadej své jméno: ")

def receive_messages():
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            if msg:
                print("\n" + msg)
        except:
            print("Došlo k chybě při příjmu zprávy.")
            client.close()
            break

def send_messages():
    while True:
        msg = input()
        full_msg = f"{nickname}: {msg}"
        client.sendall(full_msg.encode("utf-8"))

# Spuštění vláken: příjem + odesílání
threading.Thread(target=receive_messages, daemon=True).start()
send_messages()
