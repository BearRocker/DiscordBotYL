import random

import discord
from discord.ext import commands
import config


class InvitesToGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_embed(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return discord.Embed(author='BearRocker & Sm0keHokage', colour=discord.Colour.from_rgb(r, g, b))

    def get_channel(self):
        return self.bot.get_channel(config.INVITE_CHANNEL_ID)

    @commands.command(name='event')
    async def new_event(self, ctx, time, game, event_name, *rules):
        await ctx.message.delete()
        rules = ' '.join(rules)
        embed = self.create_embed()
        embed.add_field(name='Time:', value=time)
        embed.add_field(name='Game:', value=game)
        embed.add_field(name='Event name:', value=event_name)
        embed.add_field(name='Rules:', value=rules, inline=False)
        channel = self.get_channel()
        await channel.send(embed=embed)
        await channel.last_message.add_reaction('✅')
        await channel.last_message.add_reaction('❎')

    @commands.command(name='invite_game')
    async def new_game_inv(self, ctx, time, mode, game):
        await ctx.message.delete()
        embed = self.create_embed()
        embed.add_field(name='Time:', value=time)
        embed.add_field(name='Mode:', value=mode)
        embed.add_field(name='Game:', value=game)
        channel = self.get_channel()
        await channel.send(embed=embed)
        await channel.last_message.add_reaction('✅')
        await channel.last_message.add_reaction('❎')

    @commands.command(name='vote')
    async def create_vote(self, ctx, *both_var):
        var1 = both_var[:both_var.index('V2:')]
        var2 = both_var[both_var.index('V2:') + 1:]
        var1 = ' '.join(var1)
        var2 = ' '.join(var2)
        await ctx.message.delete()
        embed = self.create_embed()
        embed.add_field(name='Variant 1:', value=var1)
        embed.add_field(name='Variant 2:', value=var2)
        channel = self.get_channel()
        await channel.send(embed=embed)
        await channel.last_message.add_reaction('✅')
        await channel.last_message.add_reaction('❎')