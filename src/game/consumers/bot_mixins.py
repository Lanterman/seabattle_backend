class BotMessage:
    """Mixin that generates message from the bot"""

    def get_bot_message_with_offer(self, answer: bool) -> str:
        """Get a bot message with a response to the offer to play again"""
   
        if answer:
            return f"{self.user.username.capitalize()} want to play again."
        else:
            return f"{self.user.username.capitalize()} doesn't want to play again."
    
    def get_bot_message_with_connected_player(self) -> str:
        """Get a message from a bot with a connected player"""

        return f"{self.user.username.capitalize()} connected to the game."


class GenericBotMixin(BotMessage):
    """Interface class for all other bot mixins"""