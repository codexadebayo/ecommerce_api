from typing import Optional
from fastapi import HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Define email settings as a Pydantic model
class EmailSettings(BaseModel):
    mail_from: EmailStr = Field(..., env="MAIL_FROM")
    mail_password: str = Field(..., env="MAIL_PASSWORD")
    mail_server: str = Field(..., env="MAIL_SERVER")
    mail_port: int = Field(..., env="MAIL_PORT")
    mail_username: EmailStr = Field(..., env="MAIL_USERNAME")
    use_tls: bool = Field(False, env="MAIL_USE_TLS")
    use_ssl: bool = Field(True, env="MAIL_USE_SSL")
    template_folder: str = Field("./templates", env="MAIL_TEMPLATE_FOLDER")  # Default template folder


# Create an instance of EmailSettings
email_settings = EmailSettings()

# Configure email connection
conf = ConnectionConfig(
    MAIL_USERNAME=email_settings.mail_username,
    MAIL_PASSWORD=email_settings.mail_password,
    MAIL_FROM=email_settings.mail_from,
    MAIL_SERVER=email_settings.mail_server,
    MAIL_PORT=email_settings.mail_port,
    MAIL_USE_TLS=email_settings.use_tls,
    MAIL_USE_SSL=email_settings.use_ssl,
    MAIL_TEMPLATE_FOLDER=email_settings.template_folder,
)


async def send_email(
    subject: str,
    to: List[EmailStr],
    template_name: str,
    template_context: dict,
) -> bool:
    """
    Sends an email using FastAPI Mail.

    Args:
        subject: The subject of the email.
        to: A list of recipient email addresses.
        template_name: The name of the HTML template to use (without extension).
        template_context: A dictionary of variables to pass to the template.

    Returns:
        True if the email was sent successfully, False otherwise.

    Raises:
        HTTPException: If there was an error sending the email.
    """
    message = MessageSchema(
        subject=subject,
        recipients=to,
        template_body=template_context,
        subtype="html",  # Specify HTML email
    )

    fm = FastMail(conf)  # Create FastMail instance

    try:
        await fm.send_message(message, template_name=template_name)
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending email: {str(e)}",
        )
    finally:
        await fm.disconnect()
