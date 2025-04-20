from passlib.context import CryptContext
import re


# Create a password hashing context
pwd_context = CryptContext(
    schemes=["argon2"],
    argon2__rounds=4,
    argon2__memory_cost=102400, 
    argon2__parallelism=4,
    argon2__salt_len=32,
    argon2__hash_len=32,
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    """
    Hashes a password using the configured hashing algorithm.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain text password matches the hashed password,
              False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)



def check_password_strength(password: str) -> bool:
    """
    Checks if a password meets the minimum strength requirements.

    Args:
        password (str): The password to check.

    Returns:
        bool: True if the password is strong enough, False otherwise.
    """
    min_length = 8
    max_length = 128
    has_uppercase = bool(re.search(r"[A-Z]", password))
    has_lowercase = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]", password))

    # Enforce the password policy
    is_valid = (
        min_length <= len(password) <= max_length
        and has_uppercase
        and has_lowercase
        and has_digit
        and has_special
    )
    return is_valid
