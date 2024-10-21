import requests

def api(metodo, query):
    url = 'ADRESS'
    auth = ('USER', 'PASSWORD')
    headers = {'Content-Type': 'application/json'}
    payload = {'query': query}

    try:
        if metodo == 'GET':
            url = f"{url}/consulta"
            response = requests.get(url, headers=headers, auth=auth, json=payload)
        elif metodo == 'POST':
            url = f"{url}/executar"
            response = requests.post(url, headers=headers, auth=auth, json=payload)
        else:
            raise ValueError(f"Método HTTP '{metodo}' não suportado.")

        # Verifica o status da resposta
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        raise

    except Exception as e:
        print(f"Erro inesperado: {e}")
        raise
