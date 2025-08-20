# Jak prolomit server?
1. Vědět co je klient a co je server
2. Vědět co je IP adresa a co port
3. Chápat, jak funguje Caesarova šifra
---------------------------------------------
4. Vytvořit TCP klienta, který se připojí na IP a port serveru
5. Klient musí být schopen zprávy přijímat i odesílat

IP: 192.168.111.180
Port: 54323
Wifi: FreeDK


## Papírový protokol
Klient -> Server: TCP connect
Server -> Klient: "NAPOVEDA: <zasifrovano>\n"
Klient -> Server: "poklad.txt"
Server -> Klient: "SERVER PROLOMEN!!!"
Server -> Klient: "OBSAH: 1000 zlatých mincí"

### Chyba
Klient -> Server: "neexistuje.txt"
Server -> Klient: "Soubor nenalezen! Zkus znovu."
