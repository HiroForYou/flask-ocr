import requests

# Definir la URL de la aplicación Flask en ejecución
url = 'http://localhost:5000/upload'  # Ajusta la URL según tu configuración

# Cargar una imagen en formato JPEG como archivo
image_file = 'examples/test.png'  # Ajusta el nombre y la ruta de la imagen

# Datos adicionales para la solicitud
data = {'user_id': '1'}  # Reemplaza '123' con el ID de usuario adecuado

# Token de autenticación JWT (si es necesario)
jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzQxMDY1NCwianRpIjoiOGFiYWRkOGQtY2FmNC00ZDA1LWIzNzctMDZjODA5Y2RkYjI4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imhpcm8iLCJuYmYiOjE2OTc0MTA2NTQsImV4cCI6MTY5NzQxNzg1NH0.hI069ncc1I7z26_18hSUv6596iM5ZKGqroFPwRf5o_w'

# Encabezados para la solicitud (si se requiere autenticación)
headers = {'Authorization': 'Bearer ' + jwt_token}

# Crear un diccionario de archivos con el archivo de imagen
files = {'file': (image_file, open(image_file, 'rb'), 'image/png')}

# Enviar la solicitud POST
response = requests.post(url, data=data, headers=headers, files=files)

# Imprimir la respuesta
print(f'Respuesta: {response.status_code}')
print(response.json())
