import requests

# Definir la URL de la aplicación Flask en ejecución
url = 'http://localhost:5000/extract-text'  # Ajusta la URL según tu configuración

# Token de autenticación JWT si es necesario
jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzQxMDY1NCwianRpIjoiOGFiYWRkOGQtY2FmNC00ZDA1LWIzNzctMDZjODA5Y2RkYjI4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imhpcm8iLCJuYmYiOjE2OTc0MTA2NTQsImV4cCI6MTY5NzQxNzg1NH0.hI069ncc1I7z26_18hSUv6596iM5ZKGqroFPwRf5o_w'

# Datos para la extracción de texto
data = {
    'image_id': 1  # Ajusta el ID de la imagen según tus necesidades
}

# Encabezados con el token JWT si es necesario
headers = {
    'Authorization': f'Bearer {jwt_token}'  # Ajusta el encabezado JWT si es necesario
}

# Enviar la solicitud POST
response = requests.post(url, json=data, headers=headers)

# Imprimir la respuesta
print(f'Respuesta: {response.status_code}')
print(response.json())
