import giphy_client as giphy
import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.api_instance = giphy.DefaultApi()
        self.api_key = None
        self.bot = bot

    @commands.command(name='slap')
    async def anime_slap(self, ctx, user: discord.User):
        search = 'anime slap'
        api_response = self.api_instance.gifs_search_get(self.api_key, search)
        channel = ctx.message.channel
        message = ctx.message
        await message.delete()
        await channel.send(api_response)

