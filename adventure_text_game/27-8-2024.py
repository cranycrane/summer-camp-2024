import requests 

url = "https://data.kurzy.cz/json/meny/b%5B1%5D.json" 
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)