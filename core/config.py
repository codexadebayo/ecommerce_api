from pydantic import HttpUrl, root_validator
from pydantic_settings import BaseSettings
from typing import List, Union, Optional


class Settings(BaseSettings):
    """
    Application settings class.

    This class defines all the configuration settings for the FastAPI application.
    It uses Pydantic's BaseSettings to automatically load settings from
    environment variables, with support for default values and type validation.
    """

    PROJECT_NAME: str = "E-commerce API"  # Default project name
    API_V1_STR: str = "/api/v1"  # Default API version string
    #  Make SECRET_KEY a more generic name, and require it.
    SECRET_KEY: str  # No default, Pydantic will enforce this
    ALGORITHM: str = "HS256"  # Default JWT algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Default access token expiration time (in minutes)

    # Database settings
    DB_HOST: str = "localhost"  # Default database host
    DB_PORT: Union[str, int] = 5432  # Default database port, can be a string or int
    DB_USER: str = "postgres"  # Default database user
    DB_PASS: Optional[str] = None  # Default database password (optional, can be None)
    DB_NAME: str = "ecommerce"  # Default database name

    #  The database URL is constructed from the other DB settings.
    SQLALCHEMY_DATABASE_URL: str
    #  The @root_validator decorator is used to validate the entire model
    #  and set the SQLALCHEMY_DATABASE_URL.  It's called after Pydantic
    #  has loaded all the other fields.
    @root_validator(pre=True)
    def calculate_db_url(cls, values):
        """
        Calculates the database URL from the individual database settings.

        This class method is a Pydantic root validator.  It's called after
        all the other fields have been parsed and validated.  It constructs
        the `SQLALCHEMY_DATABASE_URL` from the other database-related
        settings.

        Args:
            values (dict): The dictionary of field values.

        Returns:
            dict: The updated dictionary of field values, including the
                  `SQLALCHEMY_DATABASE_URL`.

        Raises:
            ValueError: If any of the required database settings
                (DB_HOST, DB_PORT, DB_USER, DB_NAME) are missing.
        """
        db_host = values.get("DB_HOST")
        db_port = values.get("DB_PORT")
        db_user = values.get("DB_USER")
        db_pass = values.get("DB_PASS")
        db_name = values.get("DB_NAME")

        if not all([db_host, db_port, db_user, db_name]):
            raise ValueError("Missing required database settings")

        # Construct the database URL.  Include the password if provided.
        if db_pass:
            values["SQLALCHEMY_DATABASE_URL"] = (
                f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
            )
        else:
            values["SQLALCHEMY_DATABASE_URL"] = (
                f"postgresql://{db_user}@{db_host}:{db_port}/{db_name}"
            )
        return values

    # CORS settings (Cross-Origin Resource Sharing)
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8080"]  # Default CORS origins

    #  Email Settings (Optional, for sending emails)
    MAIL_SERVER: Optional[str] = None
    MAIL_PORT: Optional[int] = None
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_USE_TLS: Optional[bool] = True
    MAIL_USE_SSL: Optional[bool] = False
    #  Email from address.
    EMAIL_FROM: Optional[str] = "example@example.com"

    #  Base URL of the application.  Useful for generating absolute URLs
    #  in email templates, etc.
    BASE_URL: HttpUrl = "http://localhost:8000"

    class Config:
        """
        Configuration class for Pydantic settings.

        This class provides configuration options for Pydantic's BaseSettings.
        Specifically, it tells BaseSettings to load variables from the
        environment and use case-sensitive matching.
        """
        env_file = ".env"  # Load variables from a .env file
        case_sensitive = True  # Make environment variable names case-sensitive


# Create a global settings instance.  This is what you import and use.
settings = Settings()

if __name__ == "__main__":
    #  This code will only run if you execute this file directly
    #  (e.g., `python core/config.py`).  It's useful for testing
    #  your configuration.
    print("Project Name:", settings.PROJECT_NAME)
    print("API Version:", settings.API_V1_STR)
    print("Database URL:", settings.SQLALCHEMY_DATABASE_URL)
    print("CORS Origins:", settings.BACKEND_CORS_ORIGINS)
    print("Base URL:", settings.BASE_URL)
    #  Check if email settings are loaded
    if settings.MAIL_SERVER:
        print("Email Server Configured")
    else:
        print("Email Server Not Configured")
