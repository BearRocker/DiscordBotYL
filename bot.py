import random
import sqlite3

import discord
from discord.utils import get
from discord.ext import commands
import config
from Cogs import mods, role, music, misc, invites, gamebot, tictactoe


intents = discord.Intents.default()
intents.members = True
connection = sqlite3.connect('server.db')
cursor = connection.cursor()


class DiscordBot(commands.Bot):  # Класс бота, в котором заключенны все команды
    def __init__(self):
        super().__init__(command_prefix=config.PREFIX, help_command=None, intents=intents)
        self.add_cog(mods.Mods(self))
        self.add_cog(role.Roles(self))
        self.add_cog(misc.Misc(self))
        self.add_cog(invites.InvitesToGame(self,))
        self.add_cog(music.Music(self))
        self.add_cog(gamebot.GameBot(self, cursor, connection))
        self.add_cog(tictactoe.TicTacToe(self, connection, cursor))
        self.activity = discord.Activity(type=discord.ActivityType.watching,
                                         name=f'Prefix - {self.command_prefix}')
        self.emoji_to_role = {
            discord.PartialEmoji(name='1️⃣'): 833734030884732960,
            discord.PartialEmoji(name='2️⃣'): 833734064565518348,
            discord.PartialEmoji(name='3️⃣'): 833734092780470342
        }

    def create_embed(self, title, desc, r=random.randint(0, 255), g=random.randint(0, 255), b=random.randint(0, 255)):
        # Создаёт embed сообщение с рандомным цветом, если не указан
        return discord.Embed(author='BearRocker & Игн0р', title=title, colour=discord.Colour.from_rgb(r, g, b), description=desc)

    async def on_ready(self):  # При инициализации бота
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    name TEXT,
                    id INT,
                    cash BIGINT,
                    rep INT,
                    lvl INT,
                    server_id INT
                )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
                    role_id INT,
                    id INT,
                    cost BIGINT
                )""")
        for guild in self.guilds:
            for member in guild.members:
                if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                    cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 1, {guild.id})")
                else:
                    pass
        connection.commit()

    async def on_message(self, message):  # При сообщении проверяется, в каком чате оно было отправлено,
        # если в указанном invite channel из файла config.py есть сообщение, то подним будут ставиться две эмоджи
        if message.author == self.user:
            return
        elif message.channel.id == config.INVITE_CHANNEL_ID:
            await message.add_reaction(config.AGREE_REACTION)
            await message.add_reaction(config.DISAGREE_REACTION)
        await bot.process_commands(message)

    async def on_raw_reaction_add(self, payload):  # При добавлении некоторых реакций на сообщение указанное в config
        # добавляется роль указанная в self.emoji_to_role
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

    async def on_raw_reaction_remove(self, payload):  # При удалении реакции на сообщении, удаляется роль
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

    async def on_member_remove(self, member):
        guild = member.guild
        channel = self.get_channel(config.LOGS_CHANNEL_ID)
        async for entry in guild.audit_logs(action=discord.AuditLogAction.kick or discord.AuditLogAction.ban, limit=1):
            embed = self.create_embed('', f'{entry.target} has been removed from server')
            ava = entry.target.avatar_url
            embed.set_image(url=ava)
            await channel.send(embed=embed)

    async def on_member_unban(self, guild, member):
        channel = self.get_channel(config.LOGS_CHANNEL_ID)
        async for things in guild.audit_logs(action=discord.AuditLogAction.unban, limit=1):
            embed = self.create_embed('', f'{things.target} has been unbanned on server')
            ava = things.target.avatar_url
            embed.set_image(url=ava)
            await channel.send(embed=embed)

    async def on_member_update(self, before, after):
        guild = after.guild
        channel = self.get_channel(config.LOGS_CHANNEL_ID)
        if before.roles != after.roles:
            async for man in guild.audit_logs(action=discord.AuditLogAction.member_role_update, limit=1):
                embed = self.create_embed('',
                                          f'{man.user} added/remove role for {man.target} ')
                ava = man.target.avatar_url
                embed.set_image(url=ava)
                if man.target == man.user:
                    embed.description = embed.description + f'take attention!'
                    await channel.send(get(guild.roles, name=config.ADMIN).mention)
                    await channel.send(embed=embed)
                else:
                    await channel.send(embed=embed)




bot = DiscordBot()
bot.run(config.DISCORD_TOKEN)
