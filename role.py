import discord
from discord.ext import commands
import config
from discord.utils import get


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='get_role')
    async def add_role(self, ctx, role: discord.Role):
        message = ctx.message
        author = message.author
        guild = ctx.guild
        print(role, guild.roles[:][-1])
        await message.delete()
        if role not in author.roles:
            await author.add_roles(role)
        else:
            await author.send(f'You already have {role} role')

    @commands.command(name='all_roles')
    async def get_roles(self, ctx):
        message = ctx.message
        author = message.author
        guild = ctx.guild
        await message.delete
        await author.send(f'Here all roles on this server {guild}:'
                          f'{guild.roles}')
