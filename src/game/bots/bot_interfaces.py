from . import bot_levels, bot_logic, bot_message


class BotMessageInterface(bot_message.BotMainMessage):
    """Interface of bot creades and sends message"""


class BotDifficultyLevelsInterface(bot_levels.LightBot, bot_levels.MediumBot, bot_levels.HighBot):
    """Interface of bot difficulty levels for the game itself"""


class GenericBotInterface(bot_message.BotMainMessage, bot_logic.BotTakeShot, bot_logic.BotCreatesNewGame):
    """Interface class for all other bot mixins"""
