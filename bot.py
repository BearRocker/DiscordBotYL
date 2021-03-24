import discord
from discord.utils import get
from discord.ext import commands
import config
from change_prefix import Commands_list


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config.PREFIX)
        self.add_cog(Commands_list(self))


bot = DiscordBot()
bot.run(TOKEN)
