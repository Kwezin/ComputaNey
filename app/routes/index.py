from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.logging import Logger
from dao.db import init_db, insert_user, get_user

logger = Logger()
router = Router()

# Inicializa banco na primeira execução
init_db()

@router.post("/login")
def login():
    body = router.current_event.json_body
    email = body.get("email")
    senha = body.get("senha")

    # Exemplo de login fake: checa se o usuário existe no banco
    user = get_user(email)
    if user and senha == "1234":  # senha fixa só para teste
        return {"message": "Login realizado com sucesso!", "user": user}
    return {"error": "Credenciais inválidas"}, 401


@router.post("/cadastro")
def cadastro():
    body = router.current_event.json_body
    nome = body.get("nome")
    cpf = body.get("cpf")
    email = body.get("email")
    tipo = body.get("tipo")
    tags = body.get("tags", [])

    insert_user(nome, cpf, email, tipo, tags)

    return {
        "message": "Cadastro realizado com sucesso!",
        "usuario": {
            "nome": nome,
            "cpf": cpf,
            "email": email,
            "tipo": tipo,
            "tags": tags
        }
    }
