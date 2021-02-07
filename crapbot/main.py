import logging
import os

import discord
from discord.ext import commands

from .commands import MiscCog, SoundsCog
from .config import Config

TOKEN = open(os.path.join(Config.BOT_DIRECTORY, "token")).read()


def main():
    logging.basicConfig(level=logging.INFO)
    lenin_bot = commands.Bot(Config.prefix, intents=discord.Intents.all())
    lenin_bot.add_cog(SoundsCog(lenin_bot))
    lenin_bot.add_cog(MiscCog(lenin_bot))
    lenin_bot.run(TOKEN)


if __name__ == "__main__":
    main()
