# chat_ws_server.py
import asyncio
import json
import websockets
from datetime import datetime

# připojení a přezdívky
clients = set()
nick_of = {}  # websocket -> nickname

async def broadcast(payload: dict):
    """Pošli payload všem připojeným klientům jako JSON."""
    if not clients:
        return
    data = json.dumps(payload, ensure_ascii=False)
    await asyncio.gather(*(ws.send(data) for ws in list(clients)), return_exceptions=True)

async def handler(ws):
    clients.add(ws)
    nick = "Anon"
    nick_of[ws] = nick

    try:
        # očekáváme uvítací zprávu s přezdívkou
        # {"type":"hello","nick":"Jana"}
        await ws.send(json.dumps({"type": "system", "text": "Vítej! Pošli {type:'hello', nick:'TvojeJmeno'}"}))
        async for msg in ws:
            try:
                data = json.loads(msg)
            except json.JSONDecodeError:
                await ws.send(json.dumps({"type": "error", "text": "Špatný formát JSON"}))
                continue

            if data.get("type") == "hello":
                nick = data.get("nick", "Anon").strip() or "Anon"
                nick_of[ws] = nick
                await broadcast({"type": "system", "text": f"{nick} se připojil(a)."})
            elif data.get("type") == "chat":
                text = (data.get("text") or "").strip()
                if not text:
                    continue
                now = datetime.now().strftime("%H:%M:%S")
                await broadcast({"type": "chat", "nick": nick_of[ws], "text": text, "time": now})
            else:
                await ws.send(json.dumps({"type": "error", "text": "Neznámý typ zprávy"}))
    except websockets.ConnectionClosed:
        pass
    finally:
        # odpojení
        clients.discard(ws)
        left_nick = nick_of.pop(ws, "Anon")
        await broadcast({"type": "system", "text": f"{left_nick} se odpojil(a)."})

async def main():
    # pro místní PC: host="localhost"; pro LAN: host="0.0.0.0"
    async with websockets.serve(handler, host="localhost", port=8080):
        print("[SERVER] WebSocket chat běží na ws://localhost:8080")
        await asyncio.Future()  # běž navždy

if __name__ == "__main__":
    asyncio.run(main())
