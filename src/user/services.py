def validate_password(input_password: str, db_password: hex) -> bool:
    """Validate user password"""

    return input_password == db_password
