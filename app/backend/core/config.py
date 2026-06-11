from pydantic_settings import BaseSettings


class Configuracoes(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres.kihnzaimbeyklvakezbu:Admin_supabase@aws-1-us-west-2.pooler.supabase.com:5432/postgres"

    class Config:
        env_file = ".env"


settings = Configuracoes()
