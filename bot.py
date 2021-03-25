import discord
from discord.utils import get
from discord.ext import commands
import config
from mods import Commands_list
from role import Roles


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config.PREFIX)
        self.add_cog(Commands_list(self))
        self.add_cog(Roles(self))

    async def on_ready(self):
        print("I'm ready")

    async def on_message(self, message):
        if message.author == self.user:
            return
        elif message.channel.id == config.INVITE_CHANNEL_ID:
            await message.add_reaction(config.AGREE_REACTION)
            await message.add_reaction(config.DISAGREE_REACTION)
        await bot.process_commands(message)


bot = DiscordBot()
bot.run(TOKEN)
