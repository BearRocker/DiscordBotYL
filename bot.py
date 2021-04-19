import random

import discord
from discord.utils import get
from discord.ext import commands
import config
from mods import Mods
from role import Roles
from misc import Misc
from invites import InvitesToGame

intents = discord.Intents.default()
intents.members = True


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config.PREFIX, help_command=None, intents=intents)
        self.add_cog(Mods(self))
        self.add_cog(Roles(self))
        self.add_cog(Misc(self))
        self.add_cog(InvitesToGame(self))
        self.emoji_to_role = {
            discord.PartialEmoji(name='1️⃣'): 833734030884732960,
            discord.PartialEmoji(name='2️⃣'): 833734064565518348,
            discord.PartialEmoji(name='3️⃣'): 833734092780470342
        }

    def create_embed(self, title, r=random.randint(0, 255), g=random.randint(0, 255), b=random.randint(0, 255)):
        return discord.Embed(author='BearRocker & Игн0р', title=title, colour=discord.Colour.from_rgb(r, g, b))

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

    async def on_member_join(self, member):
        channel = self.get_channel(config.GREETING_CHANNEL_ID)
        embed = self.create_embed('', 0, 255, 0)
        embed.add_field(name='New member! :tada:', value=member.name)
        await channel.send(embed=embed)

    async def on_member_remove(self, member):
        channel = self.get_channel(config.GREETING_CHANNEL_ID)
        embed = self.create_embed('', 255, 0, 0)
        embed.add_field(name='Oh no someone left us( :middle_finger: ', value=member.name)
        await channel.send(embed=embed)

    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == config.REACTION_MESSAGE:
            guild_id = payload.guild_id
            guild = self.get_guild(guild_id)
            try:
                role_id = self.emoji_to_role[payload.emoji]
            except KeyError:
                return
            role = guild.get_role(role_id)
            member = guild.get_member(payload.user_id)
            if role:
                await member.add_roles(role)
            else:
                user = self.get_user(payload.user_id)
                await user.send('Incorrect emoji.')

    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id == config.REACTION_MESSAGE:
            guild_id = payload.guild_id
            guild = self.get_guild(guild_id)
            try:
                role_id = self.emoji_to_role[payload.emoji]
            except KeyError:
                return
            role = guild.get_role(role_id)
            member = guild.get_member(payload.user_id)
            if role:
                await member.remove_roles(role)
            else:
                user = self.get_user(payload.user_id)
                await user.send('Incorrect emoji.')


bot = DiscordBot()
bot.run(config.DISCORD_TOKEN)
