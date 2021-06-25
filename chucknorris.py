import requests

response = requests.get("http://api.icndb.com/jokes/random?exclude=explicit")
if response.status_code == 200:
    data = response.json()
    print(data["value"]["joke"])
else:
    print("ERROR:", response.status_code)
