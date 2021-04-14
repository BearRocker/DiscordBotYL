import giphy_client as giphy
import discord
from discord.ext import commands
import config
import random


class Misc(commands.Cog):
    def __init__(self, bot):
        self.api_instance = giphy.DefaultApi()
        self.api_key = config.GIPHY_API_KEY
        self.bot = bot

    @commands.command(name='slap')
    async def anime_slap(self, ctx, user: discord.User):
        search = 'anime slap'
        api_response = self.api_instance.gifs_search_get(self.api_key, search, offset=random.randint(0, 7))
        channel = ctx.message.channel
        message = ctx.message
        author = message.author
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        embed = discord.Embed(author='BearRocker & SmokeHokage', colour=discord.Colour.from_rgb(r, g, b))
        embed.add_field(name='Slap', value=str(author)[:-5] + ' slaps ' + str(user)[:-5])
        gif = api_response.data[0].images.downsized.url
        embed.set_image(url=gif)
        await message.delete()
        await channel.send(embed=embed)

