import socket
import random
from time import sleep

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            # posun písmena, zachování velikosti
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


HOST = "0.0.0.0"
PORT = 54324

secret_files = {
    "tajne_heslo.txt": "SuperVelkySkibidi123",
    "plan_budoucnosti.txt": "vlaky budou jezdit samy a Lucka bude prezidentkou",
    "programovani.txt": "Vyhrál si! Zařvi 'Skibidi' a získej 1000 zlatých mincí",
}

# Vyber tajný soubor
secret_name = random.choice(list(secret_files.keys()))
shift = 5  # Caesarův posun

encrypted_hint = caesar_encrypt(secret_name, shift)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("[SERVER] Hackovací server běží...")
while True:
    conn, addr = server.accept()
    print(f"[PŘIPOJEN] {addr}")
    sleep(1)  # malá prodleva pro stabilitu
    conn.sendall(f"NAPOVEDA: {encrypted_hint}\n".encode("utf-8"))
    while True:
        try:
            file_request = conn.recv(1024).decode("utf-8").strip()
            if not file_request:
                break
            if file_request == secret_name:
                conn.sendall(f"SERVER PROLOMEN!!!".encode("utf-8"))
                conn.sendall(f"OBSAH: {secret_files[file_request]}".encode("utf-8"))
            else:
                conn.sendall(b"Soubor nenalezen! Zkus znovu.\n")
        except:
            break
    conn.close()
    print(f"[ODPOJEN] {addr}")
