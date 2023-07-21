import pytest

from src.user import services


def test_create_salt():
    """Testing the create_salt function"""

    pass


def test_password_hashing():
    """Testing the password_hashing function"""

    pass


@pytest.mark.parametrize(
    "test_input, output", 
    [
        (("password", "KtQrvyHOiHFU$b18f34385035abe98c305d63d2121ff72a8bca7385a7d217d1891a1c43d397ae"), False), 
        (("password", "zebNbHEPCvpn$e9cb2c4a1d0757f3fb38eeb67148370cfa70f5433101843c9eaa23d04b735b0f"), False), 
        (("karmavdele2", "iEmhsIVjCkVh$19b074e240f28205f2bb2304d1e72f3257334dd9e4879392f527d40a8e4db9cb"), True), 
        (("karmavdele", "KtQrvyHOiHFU$b18f34385035abe98c305d63d2121ff72a8bca7385a7d217d1891a1c43d397ae"), True), 
    ]
)
def test_validate_password(test_input: str, output: bool):
    """Testing the validate_password function"""

    response = services.validate_password(*test_input)
    assert response == output, response


def test_create_hashed_password():
    """Testing the create_hashed_password function"""

    pass

def test_create_user_secret_key():
    """Testing the create_user_secret_key function"""

    pass

def test_create_jwttoken():
    """Testing the create_jwttoken function"""

    pass