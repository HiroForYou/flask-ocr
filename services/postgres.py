import psycopg2
from passlib.hash import pbkdf2_sha256
import time


class DatabaseManager:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
        self.port = "5432"

    def create_connection(self):
        max_retries = 4
        retry_interval = 2
        for _ in range(max_retries):
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                )
                print("Conexión exitosa a la BD")
                self.create_tables()
                break  # Si la conexión es exitosa, salir del bucle
            except psycopg2.Error as e:
                print(f"Error al conectar a la base de datos: {e}, reintentando")
                self.conn = None
                time.sleep(retry_interval)  # Esperar antes de intentar nuevamente

    def create_tables(self):
        if self.conn is None:
            print("No se pudo conectar a la base de datos.")
            return

        try:
            cursor = self.conn.cursor()

            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(255) NOT NULL
            );
            """

            create_images_table = """
            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),
                upload_timestamp TIMESTAMP NOT NULL,
                image_path VARCHAR(255) NOT NULL
            );
            """

            cursor.execute(create_users_table)
            cursor.execute(create_images_table)

            cursor.close()
            self.conn.commit()
            print("Tablas creadas con éxito (si no existían).")
        except psycopg2.Error as e:
            print(f"Error al crear las tablas: {e}")

    def create_user(self, username, password):
        if self.conn is None:
            return "No se pudo conectar a la base de datos"

        try:
            # Generar el hash de la contraseña usando passlib
            hashed_password = pbkdf2_sha256.hash(password)

            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s);",
                (username, hashed_password),
            )
            self.conn.commit()
            cursor.close()
            return "Registro exitoso"
        except psycopg2.Error as e:
            return f"Error al crear el usuario: {e}"

    def find_user(self, username):
        if self.conn is None:
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s;", (username,))
            user_data = cursor.fetchone()
            cursor.close()

            if user_data:
                return user_data
            return None
        except psycopg2.Error as e:
            return None

    def insert_image(self, user_id, image_path):
        if self.conn is None:
            return "No se pudo conectar a la base de datos"

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
            user_data = cursor.fetchone()

            if user_data is None:
                return "El usuario no existe en la base de datos"

            cursor.execute(
                "INSERT INTO images (user_id, upload_timestamp, image_path) VALUES (%s, now(), %s) RETURNING id;",
                (user_id, image_path),
            )
            image_id = cursor.fetchone()[0]
            self.conn.commit()
            cursor.close()
            return image_id
        except psycopg2.Error as e:
            return f"Error al insertar la imagen: {e}"

    def get_image_path(self, image_id):
        if self.conn is None:
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT image_path FROM images WHERE id = %s;", (image_id,))
            result = cursor.fetchone()
            cursor.close()

            if result is None:
                return None
            return result[0]
        except psycopg2.Error as e:
            return None
