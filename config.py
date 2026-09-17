from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    # Pas de valeur par defaut : l'application refuse de demarrer si la cle est absente.
    # Une cle en dur dans le code finirait publiee avec le depot, et n'importe qui
    # pourrait alors forger un token valide.
    jwt_secret_key: str

    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30

settings = Settings()
