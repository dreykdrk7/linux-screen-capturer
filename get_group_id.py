import requests

TOKEN = 'TuTokenDeBot'
URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

response = requests.get(URL)
updates = response.json()

# Imprime todas las actualizaciones
print(updates)

# Encuentra el primer mensaje de grupo y su ID
for update in updates['result']:
    if 'message' in update and 'chat' in update['message'] and update['message']['chat']['type'] == 'group':
        print("ID del Grupo:", update['message']['chat']['id'])
        break
