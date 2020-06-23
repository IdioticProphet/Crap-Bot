import logging
from .commands import SoundsCog, MiscCog
from .config import Config
from discord.ext import commands
import os
TOKEN = open(os.path.join(Config.BOT_DIRECTORY, "token"))

def main():
    logging.basicConfig(level=logging.INFO)
    lenin_bot = commands.Bot(Config.prefix)
    lenin_bot.add_cog(SoundsCog(lenin_bot))
    lenin_bot.add_cog(MiscCog(lenin_bot))
    lenin_bot.run(TOKEN)

if __name__ == "__main__":
    main()
