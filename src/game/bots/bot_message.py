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


class Bot:
    """Creating messages related to playing with a bot"""
