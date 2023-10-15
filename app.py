import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.utils import secure_filename

from services.postgres import DatabaseManager
from utils import allowed_file, check_secure_password, perform_ocr

load_dotenv()  # Carga las variables de entorno desde el archivo .env

app = Flask(__name__)

# Configuraciones. Deberían ser entornos configurables
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "./uploads")

jwt = JWTManager(app)

# Creación de una instancia de la clase DatabaseManager para manejar la base de datos
db_manager = None


def create_db_manager(unit_test=False):
    global db_manager
    if db_manager is None:
        db_host = "localhost" if unit_test else os.getenv("POSTGRES_HOST")
        db_name = os.getenv("POSTGRES_DB")
        db_user = os.getenv("POSTGRES_USER")
        db_password = os.getenv("POSTGRES_PASSWORD")
        db_manager = DatabaseManager(db_host, db_name, db_user, db_password)
        db_manager.create_connection()


# Inyección de dependencias para evitar importaciones directas
def create_app(unit_test=False):
    create_db_manager(unit_test=unit_test)
    return app


@app.route("/")
def index():
    return redirect(url_for("login"))  # Redirige a la página de inicio de sesión


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return handle_registration(request.form.to_dict())
    return render_template("register.html")


def handle_registration(data):
    username = data.get("username")
    password = data.get("password")

    try:
        if not username or not password:
            return jsonify({"message": "Faltan datos obligatorios"}), 400

        existing_user = db_manager.find_user(username)
        if existing_user:
            return jsonify({"message": "El nombre de usuario ya existe"}), 400

        create_msg = db_manager.create_user(username, password)
        return jsonify({"message": create_msg}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return handle_login(request.json)
    return render_template("login.html")


def handle_login(data):
    username = data.get("username")
    password = data.get("password")

    try:
        user = db_manager.find_user(username)
        user_id, _, hashed_password = list(user) if user else (None,) * 3
        if user and check_secure_password(password, hashed_password):
            # Crear un token con tiempo de expiración personalizado
            expires_in = timedelta(hours=2)  # Token válido por 2 horas
            access_token = create_access_token(
                identity=username, expires_delta=expires_in
            )
            response = {
                "message": "Inicio de sesión exitoso",
                "access_token": access_token,
                "user_id": user_id,
            }
            return jsonify(response), 200

        elif user:
            return jsonify({"message": "Credenciales inválidas"}), 401
        else:
            return jsonify({"message": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    file = request.files.get("file")
    user_id = request.form.get("user_id")

    try:
        return handle_upload(file, user_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def handle_upload(file, user_id):
    if not (file and allowed_file(file.filename) and user_id):
        return jsonify({"error": "Solicitud inválida"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    image_id = db_manager.insert_image(user_id, file_path)

    if isinstance(image_id, int):
        return (
            jsonify({"message": "Imagen subida exitosamente", "image_id": image_id}),
            200,
        )
    else:
        return jsonify({"error": image_id}), 400


@app.route("/send", methods=["GET"])
def send():
    return render_template("send.html")


@app.route("/extract-text", methods=["POST"])
@jwt_required()
def extract_text():
    image_id = request.json.get("image_id")

    try:
        return handle_text_extraction(image_id)
    except Exception as e:
        return jsonify({"error": "Error en la extracción de texto"}), 500


def handle_text_extraction(image_id):
    image_path = db_manager.get_image_path(image_id)

    if image_path is None:
        return jsonify({"error": "Imagen no encontrada"}), 404

    text = perform_ocr(image_path)
    return jsonify({"texto_extraído": text}), 200


if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True, host="0.0.0.0")
