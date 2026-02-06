import secrets
import string
from sqlalchemy.orm import Session
from app.models.tokens import Token


def generar_token(longitud: int = 12):
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))


def generar_token_unico(db: Session, longitud: int = 12):

    while True:
        nuevo_token = generar_token(longitud)

        existe = db.query(Token)\
                   .filter(Token.Token == nuevo_token)\
                   .first()

        if not existe:
            return nuevo_token