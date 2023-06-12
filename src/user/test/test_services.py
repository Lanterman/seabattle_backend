import pytest

from src.user import services


class TestValidate_password:
    """Testing validate_password function"""

    @pytest.mark.parametrize(
        "test_input, output", 
        [
            (("password", "passwodr"), False), 
            (("string", "StRinG"), False), 
            (("password", ""), False),
            (("password", "password"), True), 
            (("StRinG", "StRinG"), True), 
            (("", ""), True)
        ]
    )
    def test_invalid_password(self, test_input: str, output: bool):
        """Testing the _clear_board method"""

        response = services.validate_password(*test_input)

        assert response == output, response
