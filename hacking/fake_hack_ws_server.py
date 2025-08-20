import asyncio
import websockets
import random

# Tajné soubory
secret_files = {
    "tajne_heslo.txt": "supertajneheslo123",
    "plan_budoucnosti.txt": "vlaky budou jezdit samy",
    "poklad.txt": "1000 zlatých mincí",
}

# Caesarova šifra (pouze anglická písmena – ostatní necháváme beze změny)
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if 'a' <= char <= 'z':
            result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += char
    return result

secret_name = random.choice(list(secret_files.keys()))
shift = 3
encrypted_hint = caesar_encrypt(secret_name, shift)

async def handler(websocket):
    # po připojení pošli nápovědu
    await websocket.send(f"NAPOVEDA: {encrypted_hint}")
    try:
        async for message in websocket:
            if message == secret_name:
                await websocket.send(f"OBSAH: {secret_files[secret_name]}")
            else:
                await websocket.send("Soubor nenalezen! Zkus znovu.")
    except websockets.ConnectionClosed:
        pass

async def main():
    # host="localhost" -> jen z tohoto PC; pro LAN použij host="0.0.0.0"
    async with websockets.serve(handler, host="localhost", port=8080):
        print("[SERVER] WebSocket běží na ws://localhost:8080")
        # drž server „navždy“
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
