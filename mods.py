import discord
from discord.ext import commands
import config
import random


class Mods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_embed(self, title):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return discord.Embed(author='BearRocker & Sm0keHokage', title=title, colour=discord.Colour.from_rgb(r, g, b))

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *reason):
        if reason:
            reason = ' '.join(reason)
        else:
            reason = 'No reason specified'
        guild = ctx.guild
        channel = self.bot.get_channel(config.LOGS_CHANNEL_ID)
        avatar = user.avatar_url
        embed = self.create_embed('Ban')
        embed.add_field(name='Banned: ', value=user.name)
        embed.add_field(name='Reason: ', value=reason, inline=False)
        embed.set_image(url=avatar)
        await ctx.message.delete()
        await channel.send(embed=embed)
        await guild.ban(user, reason=reason)
        for channels in guild.text_channels:
            await channels.purge(limit=None, check=lambda m: m.author == user)

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.User, *reason):
        if reason:
            reason = ' '.join(reason)
        else:
            reason = 'No reason specified'
        guild = ctx.guild
        avatar = user.avatar_url
        channel = self.bot.get_channel(config.LOGS_CHANNEL_ID)
        embed = self.create_embed('Kick')
        embed.add_field(name='Kicked: ', value=user.name)
        embed.add_field(name='Reason: ', value=reason, inline=False)
        embed.set_image(url=avatar)
        await ctx.message.delete()
        await channel.send(embed=embed)
        await guild.kick(user, reason)

    @commands.command(name='clean')
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, amount):
        channel = ctx.message.channel
        message = ctx.message
        await message.delete()
        await channel.purge(limit=int(amount))

    @commands.command(name='set_invite_channel')
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, channel_id):
        await ctx.message.delete()
        config.INVITE_CHANNEL_ID = int(channel_id)

    @commands.command(name='set_logs_channel')
    @commands.has_permissions(administrator=True)
    async def set_channel(self, ctx, channel_id):
        await ctx.message.delete()
        config.LOGS_CHANNEL_ID = int(channel_id)

    @commands.command(name='set_muted_role')
    @commands.has_permissions(administrator=True)
    async def set_role(self, ctx, role_id):
        await ctx.message.delete()
        config.MUTE_ROLE = role_id

    @commands.command(name='mute')
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, user: discord.Member, *reason):
        if reason:
            reason = ' '.join(reason)
        else:
            reason = 'No reason specified'
        await ctx.message.delete()
        guild = ctx.guild
        avatar = user.avatar_url
        for roles in user.roles[1:]:
            await user.remove_roles(guild.get_role(roles.id))
        await user.add_roles(guild.get_role(config.MUTE_ROLE))
        channel = self.bot.get_channel(config.LOGS_CHANNEL_ID)
        embed = self.create_embed('Mute')
        embed.add_field(name='Muted:', value=user.name)
        embed.add_field(name='Reason:', value=reason)
        embed.set_image(url=avatar)
        await channel.send(embed=embed)
