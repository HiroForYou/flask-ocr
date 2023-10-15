import unittest
import json
import logging
from faker import Faker
from werkzeug.datastructures import FileStorage

from app import create_app

# Configura el registro
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(unit_test=True).test_client()
        # Crea una instancia de Faker para generar datos aleatorios
        self.fake = Faker()
        self.test_image = "examples/test.png"

    def test_index_redirects_to_login(self):
        logger.info("\n\nTest: test_index_redirects_to_login")
        response = self.app.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith("/login"))
        logger.info("Test Passed: Redirected to /login")

    def test_register_user(self):
        logger.info("\n\nTest: test_register_user")
        # Genera un nombre de usuario y contraseña aleatorios
        username = self.fake.user_name()
        password = self.fake.password()

        response = self.app.post(
            "/register", data={"username": username, "password": password}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(data["message"], "Registro exitoso")
        logger.info("Test Passed: User registered successfully")

    def test_login_user(self):
        logger.info("\n\nTest: test_login_user")
        # Genera un nombre de usuario y contraseña aleatorios
        username = self.fake.user_name()
        password = self.fake.password()

        self.app.post("/register", data={"username": username, "password": password})
        response = self.app.post(
            "/login", json={"username": username, "password": password}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(data["message"], "Inicio de sesión exitoso")
        logger.info("Test Passed: User logged in successfully")

    def test_upload_image(self):
        logger.info("\n\nTest: test_upload_image")
        # Genera un nombre de usuario y contraseña aleatorios
        username = self.fake.user_name()
        password = self.fake.password()

        self.app.post("/register", data={"username": username, "password": password})
        login_response = self.app.post(
            "/login", json={"username": username, "password": password}
        )
        login_data = json.loads(login_response.data.decode("utf-8"))
        access_token = login_data["access_token"]

        with open(self.test_image, "rb") as image_file:
            image = FileStorage(
                stream=image_file, filename="unit_test.png", content_type="image/png"
            )
            data = {"user_id": login_data["user_id"], "file": (image, "unit_test.png")}
            response = self.app.post(
                "/upload",
                data=data,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode("utf-8"))
            self.assertEqual(data["message"], "Imagen subida exitosamente")
            logger.info("Test Passed: Image uploaded successfully")

    def test_extract_text_from_image(self):
        logger.info("\n\nTest: test_extract_text_from_image")
        # Genera un nombre de usuario y contraseña aleatorios
        username = self.fake.user_name()
        password = self.fake.password()

        self.app.post("/register", data={"username": username, "password": password})
        login_response = self.app.post(
            "/login", json={"username": username, "password": password}
        )
        login_data = json.loads(login_response.data.decode("utf-8"))
        access_token = login_data["access_token"]

        with open(self.test_image, "rb") as image_file:
            image = FileStorage(
                stream=image_file, filename="unit_test.png", content_type="image/png"
            )
            data = {"user_id": login_data["user_id"], "file": (image, "unit_test.png")}
            upload_response = self.app.post(
                "/upload",
                data=data,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            upload_data = json.loads(upload_response.data.decode("utf-8"))
            image_id = upload_data["image_id"]

        extract_response = self.app.post(
            "/extract-text",
            json={"image_id": image_id},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(extract_response.status_code, 200)
        data = json.loads(extract_response.data.decode("utf-8"))
        self.assertIn("texto_extraído", data)
        logger.info("Test Passed: Text extracted successfully")


if __name__ == "__main__":
    unittest.main()
