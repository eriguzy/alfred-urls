"""Default configuration settings."""
from functools import lru_cache

class Settings():
    """Default BaseSettings."""

    env_name: str = "alfredurl"
    base_url: str = "http://localhost:8000/"
    db_url: str = "sqlite:///./urlshortener.sqlite"

    # default to SQLite
    app_server: str = "development" #change to 'development' for postgres database
    
    #openai tags
    tags = [
        {'name': 'auth',
        'description': 'Routes related to Authentication and Authorization'
        },
        {'name': 'user',
        'description': 'Routes related to User Account creation'
        },
        {'name': 'url',
        'description': 'Routes related to URL adding and listing'
        },
        {'name': 'pages',
        'description': 'Routes related to browsing web pages'
        }
    ]
    
    SECRET_KEY = "alfredscissorbdbc97f82bfe593d1e45cec19ad2591af315096665512564df9af"
    ALGORITHM = "HS256"
    
    class Config:
        """Load env variables from .env file."""
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Return the current settings."""
    settings = Settings()
    if settings.app_server == "development":
        settings.db_url = "postgresql://yfprnzpj:Sy-SAwv5TVBKh7hV8JpaHzyN6nhcrb6r@raja.db.elephantsql.com/yfprnzpj"
        settings.base_url = "https://af-urls.onrender.com/"
    return settings