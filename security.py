from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from config import settings

# Hash d'un mot de passe bidon, utilise quand le username n'existe pas : on verifie
# quand meme pour que la reponse prenne le meme temps que pour un compte existant.
# Sans ca, un attaquant deduit l'existence d'un compte en chronometrant /login.
DUMMY_PASSWORD_HASH = '$2b$12$bH7k2xZs9wMhFPij/DUW2uYv8OHbCcOHCcRwIJITtYQsIohyEu9R6'

def hash_password(password: str) -> str:
    """Hash un mot de passe en clair. Le sel est généré à chaque appel et stocké
    dans le hash lui-même, donc deux mêmes mots de passe donnent deux hashs différents."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    """Compare un mot de passe en clair au hash stocké en base.
    On ne déchiffre rien : on rejoue le hash avec le sel extrait de hashed_password."""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def create_access_token(username: str, user_id: int, role: str) -> str:
    """Construit un JWT signé avec la clé secrète de l'application.
    Le token n'est pas chiffré : son contenu est lisible par tous, mais la signature
    empêche de le modifier. N'y mettre aucune donnée sensible."""
    payload = {
        'sub': username,    # 'subject' : le champ standard qui identifie le porteur
        'id': user_id,
        'role': role,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_access_token(token: str) -> dict:
    """Vérifie la signature et l'expiration, puis rend le payload.
    Lève ExpiredSignatureError si le token est périmé, InvalidTokenError sinon.
    C'est à l'appelant de traduire ces erreurs en réponse HTTP."""
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
