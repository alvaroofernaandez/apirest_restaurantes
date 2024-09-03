import jwt
from django.conf import settings
from datetime import datetime, timedelta

def create_jwt(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1),  # Expira en 1 día
        'iat': datetime.utcnow()  # Tiempo en el que se emitió el token
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload  # Retorna el payload si es válido
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido
