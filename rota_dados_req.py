import requests

# url = "http://localhost:8000/consultar-dados"
url = "http://reservasalas/consultar-dados"

response = requests.get(url)

if response.status_code == 200:
    dados = response.json()
    print("Dados recebidos:")
    for registro in dados:
        print(registro)
else:
    print(f"Erro: {response.status_code}")
    print(response.json())