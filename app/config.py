from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RECRUITMENT_REGISTRY_URL: str
    SKILLS_REGISTRY_URL: str
    PROJECT_ID: str

    # AUTH_PATH: str
    #
    # JWT_ALGORITHM: str
    # ACCESS_TOKEN_PUBLIC_KEY: str

    ALLOWED_HOSTS: str = "http://127.0.0.1 http://10.0.0.21"
    VERSION: str = "0.0.1"
    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()

method_to_function_map = {
    "DELETE_VACANCY": 'delete_vacancy',
    "GET_VACANCY": 'get_vacancy',
    "POST_VACANCY": 'create_vacancy',
    "PATCH_VACANCY": 'update_vacancy',
}
