import discord
from discord.ext import commands
import config


class Commands_list(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Ban')
    async def Ban(self, ctx, user: discord.User, *reason):
        reason = ' '.join(reason[1:])
        guild = ctx.guild
        await guild.ban(user, reason=reason)

    @commands.command(name='kick')
    async def kick(self, ctx, user: discord.User, *reason):
        reason = ' '.join(reason[1:])
        guild = ctx.guild
        await guild.kick(user, reason)

    @commands.command(name='clean')
    async def clean(self, ctx, amount):
        channel = ctx.message.channel
        message = ctx.message
        await message.delete()
        await channel.purge(limit=int(amount))
