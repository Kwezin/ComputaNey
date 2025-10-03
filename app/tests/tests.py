# test_api.py
import unittest
import json
from lambda_function import app
from dao.db import init_db
import os
import tempfile
# teste
class TestLambdaAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Cria um banco temporário para os testes
        cls.temp_db_fd, cls.temp_db_path = tempfile.mkstemp()
        # Sobrescreve a variável do DB no módulo db
        import db
        db.DB_PATH = cls.temp_db_path
        init_db()

    @classmethod
    def tearDownClass(cls):
        os.close(cls.temp_db_fd)
        os.remove(cls.temp_db_path)

    def test_cadastro_usuario(self):
        event = {
            "httpMethod": "POST",
            "path": "/cadastro",
            "body": json.dumps({
                "nome": "Kaue",
                "cpf": "12345678900",
                "email": "kaue@example.com",
                "tipo": "admin",
                "tags": ["dev", "cloud"]
            }),
            "headers": {"Content-Type": "application/json"}
        }
        response = app.resolve(event, None)
        body = json.loads(response["body"])
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(body["usuario"]["email"], "kaue@example.com")
        self.assertIn("Cadastro realizado com sucesso!", body["message"])

    def test_login_sucesso(self):
        # Primeiro cadastra o usuário
        self.test_cadastro_usuario()

        event = {
            "httpMethod": "POST",
            "path": "/login",
            "body": json.dumps({
                "email": "kaue@example.com",
                "senha": "1234"
            }),
            "headers": {"Content-Type": "application/json"}
        }
        response = app.resolve(event, None)
        body = json.loads(response["body"])
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Login realizado com sucesso!", body["message"])
        self.assertEqual(body["user"][3], "kaue@example.com")  # índice do email na tupla do usuário

    def test_login_falha(self):
        event = {
            "httpMethod": "POST",
            "path": "/login",
            "body": json.dumps({
                "email": "naoexiste@example.com",
                "senha": "1234"
            }),
            "headers": {"Content-Type": "application/json"}
        }
        response = app.resolve(event, None)
        self.assertEqual(response["statusCode"], 401)
        body = json.loads(response["body"])
        self.assertIn("Credenciais inválidas", body["error"] or "")

if __name__ == "__main__":
    unittest.main()
