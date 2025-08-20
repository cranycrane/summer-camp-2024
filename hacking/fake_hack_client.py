import socket

HOST = "localhost"
PORT = 54322

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print(client.recv(1024).decode("utf-8"))

while True:
    guess = input("Zadej název souboru: ")
    client.sendall(guess.encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    print(response)
