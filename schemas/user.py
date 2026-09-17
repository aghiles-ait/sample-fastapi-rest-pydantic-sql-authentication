from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72) # bcrypt ne lit que les 72 premiers octets

    model_config = {
        "json_schema_extra" : {
            "example": {
                "username": "aghiles",
                "password": "a-strong-password"
            }
        }
    }
    # NB: 'role' n'est volontairement pas exposé ici, sinon n'importe qui
    # pourrait s'inscrire en tant qu'admin. Il garde sa valeur par défaut.


class LoginRequest(BaseModel):
    # Pas de min_length ici : les regles de longueur s'appliquent a l'inscription.
    # A la connexion elles ne protegent rien, et un 422 revelerait la politique de
    # mots de passe a qui teste au hasard.
    username: str
    password: str

    model_config = {
        "json_schema_extra" : {
            "example": {
                "username": "aghiles",
                "password": "a-strong-password"
            }
        }
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUser(BaseModel):
    """L'utilisateur tel que le token le decrit. Ce n'est pas une entite ORM :
    ces valeurs viennent du JWT, pas d'une lecture en base."""
    id: int
    username: str
    role: str


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool
    role: str

    model_config = {"from_attributes": True}   # authorize Pydantic to read an ORM object
    # NB: hashed_password est absent du DTO, il ne sort jamais de l'API.
