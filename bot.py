import discord
from discord.utils import get
from discord.ext import commands
import config
from change_prefix import Change_prefix


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config.PREFIX)
        self.add_cog(Change_prefix(self))


bot = DiscordBot()
bot.run('Nzc2Mzk2MjA2MzM0ODA0MDA4.X60RUA.SN15wVl2DWcHJDKU1QKutHMlQwA')
