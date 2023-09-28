from .bot_levels import LightBot, MediumBot, HighBot


class BotMessageInterface:
    """"""


class BotDifficultyLevelsInterface(LightBot, MediumBot, HighBot):
    """Interface of bot difficulty levels for the game itself"""