import asyncio
import os
import random
from asyncio import sleep
from os import listdir
from threading import Timer

import discord
import youtube_dl
import config
from discord.ext import commands
queue = []
youtube_dl.utils.bug_reports_message = lambda: ''
check = False
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


class YTDLSource(discord.PCMVolumeTransformer):  # Класс позволяющий запускать видео с yt
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


class Music(commands.Cog):  # Класс с командами относящихся к музыке
    def __init__(self, bot):
        self.bot = bot

    def create_embed(self, title):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return discord.Embed(author='BearRocker & Игн0р', title=title, colour=discord.Colour.from_rgb(r, g, b))

    @commands.command(name='join')
    async def join(self, ctx, channel: discord.VoiceChannel):  # Функция присоединения бота к войсу
        if ctx.voice_channel is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command(name='play')
    async def play(self, ctx, url):  # Функция получающая на вход url, после чего вызывает класс YTDL
        global queue
        player = await YTDLSource.from_url(url)
        embed = self.create_embed('')
        if len(queue) == 0:
            queue.append(player)
            self.start_playing(ctx.voice_client, player)
            async with ctx.typing():
                embed.add_field(name='Playing audio:', value=player.title)
                message = await ctx.send(embed=embed)
        else:
            queue.append(player)
            message = await ctx.send(embed=embed.add_field(name='Added to queue', value=url))
        while ctx.voice_client.is_playing():
            await sleep(1)
        self.start_playing(ctx.voice_client, player)


    @commands.command(name='volume')
    async def volume(self, ctx, volume: int):  # Функция изменения громкости звука
        embed = self.create_embed('')
        embed.add_field(name='Volume:', value=str(volume))
        ctx.voice_client.source.volume = volume / 100
        config.VIDEO_VOLUME = volume / 100
        await ctx.send(embed=embed)

    def start_playing(self, voice_client, player):
        global queue
        queue[0] = player
        i = 0
        while i < len(queue):
            try:
                voice_client.play(queue[i], after=lambda e: print('Player error: %s' % e) if e else None)
            except:
                pass
            i += 1

    @commands.command(name='stop')
    async def stop(self, ctx):  # Функция остановки звука
        global queue
        queue = []
        embed = self.create_embed('')
        embed.add_field(name='Stopped audio', value='🛑')
        await ctx.voice_client.disconnect()
        all_files = listdir('.')
        for item in all_files:
            if item.endswith('.m4a') or item.endswith('.webm'):
                os.remove(os.path.join('.', item))
        await ctx.send(embed=embed)

    def stop_(self):  # Аналогична async def stop
        global queue
        queue = []
        embed = self.create_embed('')
        embed.add_field(name='Stopped audio', value='🛑')
        all_files = listdir('.')
        for item in all_files:
            if item.endswith('.m4a') or item.endswith('.webm'):
                os.remove(os.path.join('.', item))
        return embed

    @play.before_invoke
    async def ensure_voice(self, ctx):  # Вызывается перед тем, как сработает команда play
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
