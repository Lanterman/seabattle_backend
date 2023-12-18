from . import bot_logic, bot_message


class BotMessageInterface(bot_message.BotMainMessage, bot_message.GenericChatBotMessage):
    """Interface of bot creades and sends message"""


class BotTakeToShotInterface(bot_logic.BotTakeShot):
    """A bot shot logic interface"""


class GenericBotInterface(bot_message.BotMainMessage,
                          bot_message.GenericChatBotMessage,
                          bot_logic.BotTakeShot, 
                          bot_logic.BotCreatesNewGame):
    """Interface class for all other bot mixins"""
