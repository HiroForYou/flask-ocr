# Usa una imagen base de Python
FROM darktohka/pytesseract-docker

# Establece el directorio de trabajo en app
WORKDIR app

# Copia todo al directorio de trabajo
COPY . .

# Instala las dependencias
RUN pip install -r requirements.txt --no-cache-dir

# Expon el puerto en el que se ejecutará Uvicorn
EXPOSE 5000

# Define el punto de entrada para la aplicación
ENTRYPOINT ["python", "app.py"]
