import requests

# Definir la URL de la aplicación Flask en ejecución
url = 'http://localhost:5000/login'  # Ajusta la URL según tu configuración

# Datos para el inicio de sesión
data = {
    'username': 'hiro',
    'password': '123'
}

# Enviar la solicitud POST
response = requests.post(url, json=data)

# Imprimir la respuesta
print(f'Respuesta: {response.status_code}')
print(response.json())
