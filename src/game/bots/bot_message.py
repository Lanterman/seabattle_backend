from random import choice

class BotMainMessage:
    """Creating messages related to notifications and alerts for users"""

    def get_bot_message_with_offer(self, answer: bool, username: str) -> str:
        """Get a bot message with a response to the offer to play again"""
   
        if answer:
            return f"{username.capitalize()} want to play again."
        else:
            return f"{username.capitalize()} doesn't want to play again."
    
    def get_bot_message_with_connected_player(self, username: str) -> str:
        """Get a message from a bot with a connected player"""

        return f"{username.capitalize()} connected to the game."
    
    def get_bot_message_dont_have_enough_money(self, username: str) -> str:
        """Get a message about don't have enough money to play"""

        return f"{username.capitalize()} don't have enough money to play."


# Chat in a game with a bot 
class ChatEasyBotMessage:
    """Creating messages in a game with an easy bot"""

    def get_easy_bot_message_user_dont_hit(self) -> str:
        """Get a message a user don't hit a ship"""

        list_message = [
            "It's okay! The match isn't over yet.",
            "Don't worry. You're just learning to play!",
            "Everything is fine! Great minds aren't born, they are made!"
        ]

        return choice(list_message)
    
    def get_easy_bot_message_user_destroyed_ship(self) -> str:
        """Get a message a user destroyed a ship"""

        list_message = [
            "This's good! You destroyed one of my ships!",
            "Not bad! You're succeeding!",
            "Wow! Well done!"
        ]

        return choice(list_message)
    
    def get_easy_bot_message_bot_dont_hit(self) -> str:
        """Get a message a bot don't hit a ship"""

        list_message = [
            "Don't worry! This isn't the end!",
            "Wow! I miss!",
            "You turn!"
        ]

        return choice(list_message)
    
    def get_easy_bot_message_bot_destroyed_ship(self) -> str:
        """Get a message a bot destroyed a ship"""

        list_message = [
            "I'm making progress!",
            "Yeah. Minus one!",
            "I'm sorry! I'm didn't want it!"
        ]

        return choice(list_message)
    
    def get_easy_bot_message_bot_won(self) -> str:
        """Get a message bot won"""

        list_message = [
            "Don't worry. This is just the game!",
            "Oops. I'm didn't want it!",
            "Everything's okay! You'll win a next game."
        ]

        return choice(list_message)
    
    def get_easy_bot_message_user_won(self) -> str:
        """Get a message user won"""

        list_message = [
            "Congratulations! You won!",
            "Not bad! You're succeeding!",
            "Wow! Well done!"
        ]

        return choice(list_message)


class ChatMediumBotMessage:
    """Creating messages in a game with a medium bot"""

    def get_medium_bot_message_user_dont_hit(self) -> str:
        """Get a message a user don't hit a ship"""

        list_message = [
            "Is it all?",
            "Maybe you'll win me later.",
            "Miss. He he."
        ]

        return choice(list_message)
    
    def get_medium_bot_message_user_destroyed_ship(self) -> str:
        """Get a message a user destroyed a ship"""

        list_message = [
            "Nice work.",
            "Good. It's finally happend).",
            "Minus one. Good."
        ]

        return choice(list_message)
    
    def get_medium_bot_message_bot_dont_hit(self) -> str:
        """Get a message a bot don't hit a ship"""

        list_message = [
            "Your turn!",
            "I almost hit!",
            "I give you a chance!"
        ]

        return choice(list_message)
    
    def get_medium_bot_message_bot_destroyed_ship(self) -> str:
        """Get a message a bot destroyed a ship"""

        list_message = [
            "I'm the best!",
            "Yeap! I'm make a success",
            "Oops!"
        ]

        return choice(list_message)
    
    def get_medium_bot_message_bot_won(self) -> str:
        """Get a message bot won"""

        list_message = [
            "I'm a champion!",
            "I won!",
            "You lose!"
        ]

        return choice(list_message)
    
    def get_medium_bot_message_user_won(self) -> str:
        """Get a message user won"""

        list_message = [
            "Good work!",
            "I'm so glad you finally do it!",
            "Maybe are we play again?"
        ]

        return choice(list_message)


class ChatHighBotMessage:
    """Creating messages in a game with a hign bot"""

    def get_high_bot_message_user_dont_hit(self) -> str:
        """Get a message a user don't hit a ship"""
        
        list_message = [
            "Losser",
            "It is all?",
            "I'm giving you a chance to give in."
        ]

        return choice(list_message)
    
    def get_high_bot_message_user_destroyed_ship(self) -> str:
        """Get a message a user destroyed a ship"""
        
        list_message = [
            "So Yoa are lucky!",
            "This is your last chance to win me!",
            "Stop. This is my game. I have to win you!"
        ]

        return choice(list_message)
    
    def get_high_bot_message_bot_dont_hit(self) -> str:
        """Get a message a bot don't hit a ship"""
        
        list_message = [
            "Great bot gave you a chance!",
            "Your turn, loser!",
            "Don't try to laugh at me!"
        ]

        return choice(list_message)
    
    def get_high_bot_message_bot_destroyed_ship(self) -> str:
        """Get a message a bot destroyed a ship"""
        
        list_message = [
            "Loser!",
            "This is just the beginning!",
            "I'm a pussy destroyer!!!"
        ]

        return choice(list_message)
    
    def get_high_bot_message_bot_won(self) -> str:
        """Get a message bot won"""
        
        list_message = [
            "This is to be expected!",
            "Don't cry. I'm just better that you!",
            "Another victory for me. Congratulations to myself!"
        ]

        return choice(list_message)
    
    def get_high_bot_message_user_won(self) -> str:
        """Get a message user won"""
        
        list_message = [
            "You are lucky today. This won't happen anymore!",
            "Shit! I'm unlucky in this game.",
            "Wow! Finally you won!"
        ]

        return choice(list_message)


class GenericChatBotMessage(ChatEasyBotMessage, ChatMediumBotMessage, ChatHighBotMessage):
    """Creating messages related to playing with a bot"""

    def get_bot_message_with_user_action(self, bot_level: str, field_dict: dict) -> str | None:
        """Get a message with a user action"""
        
        if len(field_dict) > 1:
            return self.get_bot_message_user_destroyed_ship(bot_level)
        elif list(field_dict.values())[0] == "miss":
            return self.get_bot_message_user_dont_hit(bot_level)
        return

    def get_bot_message_user_dont_hit(self, bot_level: str) -> str: 
        """Get a message a user don't hit a ship"""

        if bot_level == "EASY":
            return self.get_easy_bot_message_user_dont_hit()
        elif bot_level == "MEDIUM":
            return self.get_medium_bot_message_user_dont_hit()
        elif bot_level == "HIGH":
            return self.get_high_bot_message_user_dont_hit()
        raise ValueError()
    
    def get_bot_message_user_destroyed_ship(self, bot_level: str) -> str: 
        """Get a message a user destroyed a ship"""

        if bot_level == "EASY":
            return self.get_easy_bot_message_user_destroyed_ship()
        elif bot_level == "MEDIUM":
            return self.get_medium_bot_message_user_destroyed_ship()
        elif bot_level == "HIGH":
            return self.get_high_bot_message_user_destroyed_ship()
        raise ValueError()
    
    def get_bot_message_bot_dont_hit(self, bot_level: str) -> str: 
        """Get a message a bot don't hit a ship"""

        if bot_level == "EASY":
            return self.get_easy_bot_message_bot_dont_hit()
        elif bot_level == "MEDIUM":
            return self.get_medium_bot_message_bot_dont_hit()
        elif bot_level == "HIGH":
            return self.get_high_bot_message_bot_dont_hit()
        raise ValueError()
    
    def get_bot_message_bot_destroyed_ship(self, bot_level: str) -> str: 
        """Get a message a bot destroyed a ship"""

        if bot_level == "EASY":
            return self.get_easy_bot_message_bot_destroyed_ship()
        elif bot_level == "MEDIUM":
            return self.get_medium_bot_message_bot_destroyed_ship()
        elif bot_level == "HIGH":
            return self.get_high_bot_message_bot_destroyed_ship()
        raise ValueError()
    
    def get_bot_message_bot_won(self, bot_level: str) -> str: 
        """Get a message bot won"""

        if bot_level == "EASY":
            return self.get_easy_bot_message_bot_won()
        elif bot_level == "MEDIUM":
            return self.get_medium_bot_message_bot_won()
        elif bot_level == "HIGH":
            return self.get_high_bot_message_bot_won()
        raise ValueError()
    
    def get_bot_message_user_won(self, bot_level: str) -> str:
        """Get a message user won"""

        if bot_level == "EASY":
            return self.get_easy_bot_message_user_won()
        elif bot_level == "MEDIUM":
            return self.get_medium_bot_message_user_won()
        elif bot_level == "HIGH":
            return self.get_high_bot_message_user_won()
        raise ValueError()
