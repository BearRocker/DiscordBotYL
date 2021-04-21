import asyncio

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
        return discord.Embed(author='BearRocker & Игн0р', title=title, colour=discord.Colour.from_rgb(r, g, b))

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
        channel = self.bot.get_channel(config.LOGS_CHANNEL_ID)
        embed = self.create_embed('')
        config.INVITE_CHANNEL_ID = int(channel_id)
        embed.add_field(name='CHANGED INVITE CHANNEL', value=self.bot.get_channel(config.INVITE_CHANNEL_ID))
        await channel.send(embed=embed)

    @commands.command(name='set_logs_channel')
    @commands.has_permissions(administrator=True)
    async def set_channel(self, ctx, channel_id):
        await ctx.message.delete()
        channel = self.bot.get_channel(config.LOGS_CHANNEL_ID)
        embed = self.create_embed('')
        config.LOGS_CHANNEL_ID = int(channel_id)
        embed.add_field(name='CHANGED LOGS CHANNEL', value=self.bot.get_channel(config.LOGS_CHANNEL_ID))
        await channel.send(embed=embed)

    @commands.command(name='set_muted_role')
    @commands.has_permissions(administrator=True)
    async def set_role(self, ctx, role_id):
        await ctx.message.delete()
        channel = self.bot.get_channel(config.LOGS_CHANNEL_ID)
        config.MUTE_ROLE = role_id
        guild = ctx.guild
        embed = self.create_embed('')
        embed.add_field(name='CHANGED MUTE ROLE', value=guild.get_role(role_id).name)
        await channel.send(embed=embed)

    @commands.command(name='mute')
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, user: discord.Member, time=0, *reason):
        if reason:
            reason = ' '.join(reason)
        else:
            reason = 'No reason specified'
        await ctx.message.delete()
        guild = ctx.guild
        avatar = user.avatar_url
        user_roles = []
        for roles in user.roles[1:]:
            user_roles.append(roles)
            await user.remove_roles(guild.get_role(roles.id))
        await user.add_roles(guild.get_role(config.MUTE_ROLE))
        channel = self.bot.get_channel(config.LOGS_CHANNEL_ID)
        embed = self.create_embed('')
        embed.add_field(name='Muted:', value=user.name)
        embed.add_field(name='Reason:', value=reason)
        if time > 0:
            embed.add_field(name='Time:', value=str(time) + ' minute(s)')
        else:
            embed.add_field(name='Time', value='NaN')
        embed.set_image(url=avatar)
        await channel.send(embed=embed)
        if time > 0:
            await asyncio.sleep(time * 60)
            await user.remove_roles(guild.get_role(config.MUTE_ROLE))
            if user_roles:
                for i in user_roles:
                    await user.add_roles(guild.get_role(i.id))
