from rest_framework.test import APITestCase

from src.game.bots import bot_message


class TestGenericChatBotMessage(APITestCase):
    """Testing GenericChatBotMessage class methods"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.instance = bot_message.GenericChatBotMessage()

    def test_get_bot_message_with_user_action(self):
        """Testing get_bot_message_with_user_action method"""
    
        # if len(field_dict) > 1
        response = self.instance.get_bot_message_with_user_action("EASY", {1: 1, 2:2})
        self.assertIs(type(response), str)

        response = self.instance.get_bot_message_with_user_action("MEDIUM", {1: 1, 2:2})
        self.assertIs(type(response), str)

        response = self.instance.get_bot_message_with_user_action("HIGH", {1: 1, 2:2})
        self.assertIs(type(response), str)

        # if list(field_dict.values())[0] == "miss"
        response = self.instance.get_bot_message_with_user_action("EASY", {1: "miss"})
        self.assertIs(type(response), str)

        response = self.instance.get_bot_message_with_user_action("MEDIUM", {1: "miss"})
        self.assertIs(type(response), str)

        response = self.instance.get_bot_message_with_user_action("HIGH", {1: "miss"})
        self.assertIs(type(response), str)

        # other options
        response = self.instance.get_bot_message_with_user_action("EASY", {1: "hit"})
        self.assertIsNone(response)

        response = self.instance.get_bot_message_with_user_action("MEDIUM", {1: 1})
        self.assertIsNone(response)

        response = self.instance.get_bot_message_with_user_action("HIGH", {1: "Miss"})
        self.assertIsNone(response)
    
    def test_get_bot_message_user_dont_hit(self):
        """Testing get_bot_message_user_dont_hit method"""

        # if bot_level == "EASY"
        response = self.instance.get_bot_message_user_dont_hit("EASY")
        self.assertIs(type(response), str)

        # if bot_level == "MEDIUM"
        response = self.instance.get_bot_message_user_dont_hit("MEDIUM")
        self.assertIs(type(response), str)

        # if bot_level == "HIGH"
        response = self.instance.get_bot_message_user_dont_hit("HIGH")
        self.assertIs(type(response), str)

        # doesn't match any bot level
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_user_dont_hit("")
        
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_user_dont_hit("high")
        
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_user_dont_hit("High")
    
    def test_get_bot_message_user_destroyed_ship(self):
        """Testing get_bot_message_user_destroyed_ship method"""

        # if bot_level == "EASY"
        response = self.instance.get_bot_message_user_destroyed_ship("EASY")
        self.assertIs(type(response), str)

        # if bot_level == "MEDIUM"
        response = self.instance.get_bot_message_user_destroyed_ship("MEDIUM")
        self.assertIs(type(response), str)

        # if bot_level == "HIGH"
        response = self.instance.get_bot_message_user_destroyed_ship("HIGH")
        self.assertIs(type(response), str)

        # doesn't match any bot level
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_user_destroyed_ship("")
        
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_user_destroyed_ship("high")
        
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_user_destroyed_ship("High")
    
    def test_get_bot_message_bot_dont_hit(self):
        """Testing get_bot_message_bot_dont_hit method"""

        # if bot_level == "EASY"
        response = self.instance.get_bot_message_bot_dont_hit("EASY")
        self.assertIs(type(response), str)

        # if bot_level == "MEDIUM"
        response = self.instance.get_bot_message_bot_dont_hit("MEDIUM")
        self.assertIs(type(response), str)

        # if bot_level == "HIGH"
        response = self.instance.get_bot_message_bot_dont_hit("HIGH")
        self.assertIs(type(response), str)

        # doesn't match any bot level
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_bot_dont_hit("")
        
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_bot_dont_hit("high")
        
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_bot_dont_hit("High")
    
    def test_get_bot_message_bot_destroyed_ship(self):
        """Testing get_bot_message_bot_destroyed_ship method"""

        # if bot_level == "EASY"
        response = self.instance.get_bot_message_bot_destroyed_ship("EASY")
        self.assertIs(type(response), str)

        # if bot_level == "MEDIUM"
        response = self.instance.get_bot_message_bot_destroyed_ship("MEDIUM")
        self.assertIs(type(response), str)

        # if bot_level == "HIGH"
        response = self.instance.get_bot_message_bot_destroyed_ship("HIGH")
        self.assertIs(type(response), str)

        # doesn't match any bot level
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_bot_destroyed_ship("")
        
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_bot_destroyed_ship("high")
        
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_bot_destroyed_ship("High")
    
    def test_get_bot_message_bot_won(self):
        """Testing get_bot_message_bot_won method"""

        # if bot_level == "EASY"
        response = self.instance.get_bot_message_bot_won("EASY")
        self.assertIs(type(response), str)

        # if bot_level == "MEDIUM"
        response = self.instance.get_bot_message_bot_won("MEDIUM")
        self.assertIs(type(response), str)

        # if bot_level == "HIGH"
        response = self.instance.get_bot_message_bot_won("HIGH")
        self.assertIs(type(response), str)

        # doesn't match any bot level
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_bot_won("")
        
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_bot_won("high")
        
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_bot_won("High")
    
    def test_get_bot_message_user_won(self):
        """Testing get_bot_message_user_won method"""

        # if bot_level == "EASY"
        response = self.instance.get_bot_message_user_won("EASY")
        self.assertIs(type(response), str)

        # if bot_level == "MEDIUM"
        response = self.instance.get_bot_message_user_won("MEDIUM")
        self.assertIs(type(response), str)

        # if bot_level == "HIGH"
        response = self.instance.get_bot_message_user_won("HIGH")
        self.assertIs(type(response), str)

        # doesn't match any bot level
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_user_won("")
        
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_user_won("high")
        
        with self.assertRaises(ValueError):
            self.instance.get_bot_message_user_won("High")
        

