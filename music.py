import asyncio
import os
import random
import time
from asyncio import sleep
from os import listdir
import discord
import youtube_dl
import config
from discord.ext import commands

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_embed(self, title):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return discord.Embed(author='BearRocker & Игн0р', title=title, colour=discord.Colour.from_rgb(r, g, b))

    @commands.command(name='join')
    async def join(self, ctx, channel: discord.VoiceChannel):
        if ctx.voice_channel is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command(name='play')
    async def play(self, ctx, url):
        embed = self.create_embed('')
        async with ctx.typing():
            player = await YTDLSource.from_url(url)
            embed.add_field(name='Playing audio:', value=player.title)
            ctx.voice_client.play(player)
            ctx.voice_client.source.volume = config.VIDEO_VOLUME
            message = await ctx.send(embed=embed)
        while ctx.voice_client.is_playing():
            await sleep(1)
        await ctx.voice_client.disconnect()
        embed_2 = self.stop_()
        await message.edit(embed=embed_2)

    @commands.command(name='volume')
    async def volume(self, ctx, volume: int):
        embed = self.create_embed('')
        embed.add_field(name='Volume:', value=str(volume))
        config.VIDEO_VOLUME = volume
        await ctx.send(embed=embed)

    @commands.command(name='stop')
    async def stop(self, ctx):
        embed = self.create_embed('')
        embed.add_field(name='Stopped audio', value='🛑')
        await ctx.voice_client.disconnect()
        all_files = listdir('.')
        for item in all_files:
            if item.endswith('.m4a') or item.endswith('.webm'):
                os.remove(os.path.join('.', item))
        await ctx.send(embed=embed)

    def stop_(self,):
        embed = self.create_embed('')
        embed.add_field(name='Stopped audio', value='🛑')
        all_files = listdir('.')
        for item in all_files:
            if item.endswith('.m4a') or item.endswith('.webm'):
                os.remove(os.path.join('.', item))
        return embed

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
