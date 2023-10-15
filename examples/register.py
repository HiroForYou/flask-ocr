import requests

# Definir la URL de la aplicación Flask en ejecución
url = 'http://localhost:5000/register'  # Ajusta la URL según tu configuración

# Datos para el registro
data = {
    'username': 'user_test',
    'password': 'pwd_test'
}

# Enviar la solicitud POST
response = requests.post(url, data=data)

# Imprimir la respuesta
print(f'Respuesta: {response.status_code}')
print(response.json())
