import discord
from discord.ext import commands
import config
import random


class Commands_list(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ban')
    async def ban(self, ctx, user: discord.User, *reason):
        reason = ' '.join(reason[1:])
        guild = ctx.guild
        channel = self.bot.get_channel(config.LOGS_CHANNEL_ID)
        avatar = user.avatar_url
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        embed = discord.Embed(author='BearRocker & Sm0keHokage', title='Ban',
                              colour=discord.Colour.from_rgb(r, g, b))
        embed.add_field(name='Забанен: ', value=user.name, inline=True)
        embed.add_field(name='Причина: ', value=reason, inline=False)
        embed.set_image(url=avatar)
        await channel.send(embed=embed)
        await guild.ban(user, reason=reason)
        for channels in guild.text_channels:
            await channels.purge(limit=None, check=lambda m: m.author == user)

    @commands.command(name='kick')
    async def kick(self, ctx, user: discord.User, *reason):
        reason = ' '.join(reason[1:])
        guild = ctx.guild
        channel = self.bot.get_channel(config.LOGS_CHANNEL_ID)
        await channel.send(f'Member: {user} has been kicked for {reason}')
        await guild.kick(user, reason)

    @commands.command(name='clean')
    async def clean(self, ctx, amount):
        channel = ctx.message.channel
        message = ctx.message
        await message.delete()
        await channel.purge(limit=int(amount))
