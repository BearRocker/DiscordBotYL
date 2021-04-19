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
        embed = self.create_embed()
        embed.add_field(name='Slap', value=str(author)[:-5] + ' slaps ' + str(user)[:-5])
        gif = api_response.data[0].images.downsized.url
        embed.set_image(url=gif)
        await message.delete()
        await channel.send(embed=embed)

    @commands.command(name='get_gif')
    async def random_gif(self, ctx, *gif_name):
        search = ' '.join(gif_name)
        api_response = self.api_instance.gifs_search_get(self.api_key, search, offset=random.randint(0, 7))
        channel = ctx.message.channel
        message = ctx.message
        author = message.author
        await message.delete()
        embed = self.create_embed()
        embed.add_field(name='Gif by', value=str(author)[:-5])
        gif = api_response.data[0].images.downsized.url
        embed.set_image(url=gif)
        await channel.send(embed=embed)

    @commands.command(name='rnd')
    async def rnd_roll(self, ctx, max):
        result = random.randint(1, int(max))
        channel = ctx.message.channel
        embed = self.create_embed()
        embed.add_field(name='Result:', value=result)
        await channel.send(embed=embed)

    @commands.command(name='help')
    async def help(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send('```'
                                       'Roles:\n'
                                       'get_role | @role | Adding you mentioned role\n'
                                       "all_roles | None | DM's you with all roles on server\n"
                                       'Misc:\n'
                                       'slap | @user | Sending anime gif\n'
                                       'get_gif | gif name | Sending gif that gets random from first 8\n'
                                       'rnd | number | Sending random number from 1 to number\n'
                                       'Invites:\n'
                                       'event | time game event_name rules| Creating event\n'
                                       'invite_game | time mode game | Creating invite to game at specified time\n'
                                       'vote | ... V2: ... | When you write this command to division all to 2 variants'
                                       ' you need to type V2:\n'
                                       '```')
        if ctx.message.author.guild_permissions.manage_messages:
            await ctx.message.channel.send('```'
                                           'Mods:\n'
                                           'ban | @user reason | bans user | needs ban_members\n'
                                           'kick | @user reason | kicks user | needs kick_members\n'
                                           'clean | amount | clears channel by amount messages |'
                                           ' needs manage_messagesn\n'
                                           'set_muted_role | role_id | sets muted role | needs administrator\n'
                                           'mute | @user reason | gives user MUTE role and removes other roles'
                                           ' | needs administrator```')

    def create_embed(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return discord.Embed(author='BearRocker & Sm0keHokage', colour=discord.Colour.from_rgb(r, g, b))
