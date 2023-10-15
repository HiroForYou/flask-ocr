from PIL import Image
from passlib.hash import pbkdf2_sha256
import pytesseract

def allowed_file(filename):
    # Función para comprobar si la extensión del archivo es válida
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

def perform_ocr(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        # Manejo de errores al realizar OCR
        return f"Error en OCR: {str(e)}"

def check_secure_password(input_password, hashed_password):
    try:
        # Verifica si la contraseña ingresada coincide con la contraseña almacenada de manera segura
        return pbkdf2_sha256.verify(input_password, hashed_password)
    except Exception as e:
        # Manejo de errores al verificar la contraseña
        return False

