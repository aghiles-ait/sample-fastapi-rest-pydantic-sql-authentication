from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import get_db

from repositories import user as user_repository
from schemas.user import CurrentUser, LoginRequest, RegisterRequest, TokenResponse, UserResponse
from security import (DUMMY_PASSWORD_HASH, create_access_token, decode_access_token,
                      hash_password, verify_password)

router = APIRouter(tags=["auth"])

# Lit le header "Authorization: Bearer <token>".
# auto_error=False : sinon FastAPI repond 403 quand le header manque, alors que
# l'absence d'authentification est un 401. On gere donc le cas nous-memes.
bearer_scheme = HTTPBearer(auto_error=False)

def unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=401,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},  # exige par la norme sur un 401
    )

def get_current_user(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)]
) -> CurrentUser:
    """Dependance FastAPI : extrait l'utilisateur courant du JWT.
    A brancher sur toute route a proteger via Depends(get_current_user)."""
    if credentials is None:
        raise unauthorized("Not authenticated")

    try:
        payload = decode_access_token(credentials.credentials)
    except ExpiredSignatureError:                 # sous-classe d'InvalidTokenError :
        raise unauthorized("Token has expired")   # ce except doit rester en premier
    except InvalidTokenError:
        raise unauthorized("Could not validate credentials")

    try:
        # Un token signe par nous mais forge a une epoque ou le payload avait une
        # autre forme passerait la signature : on valide quand meme le contenu.
        return CurrentUser(id=payload['id'], username=payload['sub'], role=payload['role'])
    except KeyError:
        raise unauthorized("Could not validate credentials")

@router.get("/me", response_model=CurrentUser)
def read_current_user(current_user: Annotated[CurrentUser, Depends(get_current_user)]):
    """Expose get_current_user comme endpoint testable.
    Sert aussi de modele : toute route a proteger se branche de la meme facon."""
    return current_user

@router.post("/login", response_model=TokenResponse)
def login(login_request: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    user = user_repository.get_user_by_username(db, login_request.username)

    if user is None:
        # On hashe quand meme, pour que la reponse prenne le meme temps qu'avec
        # un compte existant (voir DUMMY_PASSWORD_HASH).
        verify_password(login_request.password, DUMMY_PASSWORD_HASH)
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(login_request.password, user.hashed_password):
        # Meme message que ci-dessus : ne jamais dire lequel des deux est faux,
        # sinon l'API devient un annuaire des comptes existants.
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not user.is_active:
        # Apres la verification du mot de passe seulement, sinon on revelerait
        # l'existence du compte a qui ne connait pas le mot de passe.
        raise HTTPException(status_code=403, detail="Inactive user")

    return TokenResponse(access_token=create_access_token(user.username, user.id, user.role))

@router.post("/register", status_code=201, response_model=UserResponse)
def register(register_request: RegisterRequest, db: Annotated[Session, Depends(get_db)]):
    if user_repository.get_user_by_username(db, register_request.username) is not None:
        raise HTTPException(status_code=409, detail="Username already taken")

    try:
        return user_repository.create_user(
            db,
            username=register_request.username,
            hashed_password=hash_password(register_request.password), # jamais le mot de passe en clair
        )
    except IntegrityError:
        # deux inscriptions simultanées sur le même username : c'est la contrainte
        # unique de la base qui tranche, le contrôle ci-dessus ne suffit pas.
        raise HTTPException(status_code=409, detail="Username already taken")

#@router.post("/logout")
#async def logout(request: LogoutRequest):
#    return {"message": "Hello, World!"}
