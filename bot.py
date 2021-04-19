import discord
from discord.utils import get
from discord.ext import commands
import config
from mods import Mods
from role import Roles
from misc import Misc
from invites import InvitesToGame


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config.PREFIX, help_command=None)
        self.add_cog(Mods(self))
        self.add_cog(Roles(self))
        self.add_cog(Misc(self))
        self.add_cog(InvitesToGame(self))

    async def on_ready(self):
        print("I'm ready")

    async def on_message(self, message):
        if message.author == self.user:
            return
        elif message.channel.id == config.INVITE_CHANNEL_ID:
            await message.add_reaction(config.AGREE_REACTION)
            await message.add_reaction(config.DISAGREE_REACTION)
        await bot.process_commands(message)

    async def on_member_unban(self, guild, user):
        try:
            channel = guild.get_channel(config.LOGS_CHANNEL_ID)
            await channel.send(f'{user} has been unbanned')
        except Exception:
            print(f'Error 404: channel has type None')


bot = DiscordBot()
bot.run(config.DISCORD_TOKEN)
