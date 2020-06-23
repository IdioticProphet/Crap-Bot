import os
class Config:
    prefix = ["!", ""]
    BOTNAME = "AP Communism Management Bot"
    BOT_DIRECTORY = os.getcwd()
    BOT_LOG_CATEGORY = "logs"
    BOT_LOG_CHANNEL = "bot-logs"
    BOT_SOUND_DIR = os.path.join(BOT_DIRECTORY,"sounds")
