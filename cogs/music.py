import asyncio
import discord
import youtube_dl
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

        self.title = data.get("title")
        self.likes = data.get("like_count")
        self.dislikes = data.get("dislike_count")
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['yt', 'p'])
    async def play(self, ctx, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        embed = discord.Embed(title="Now playing", color=0x30c223)
        embed.add_field(name="Title:", value="{}".format(player.title), inline=False)
        embed.add_field(name="Likes", value="👍🏼 {}  👎🏼 {}".format(player.likes, player.dislikes), inline=False)
        embed.set_footer(text=f"Queued by: {ctx.author.name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=':interrobang: Error!', description='No argument given!', color=0xff0011)
            await ctx.send(embed=embed)
        else:
            raise

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int):

        if volume > 100:
            embed = discord.Embed(title=':interrobang: Error!', description='Given argument can\'t be greater than 100!', color=0xff0011)
            await ctx.send(embed=embed)
        elif volume < 0:
            embed = discord.Embed(title=':interrobang: Error!', description='Given argument can\'t be less or equal to 0!', color=0xff0011)
            await ctx.send(embed=embed)
        else:
            if ctx.voice_client is None:
                embed = discord.Embed(title=':interrobang: Error!', description='Not connected to a voice channel!', color=0xff0011)
                await ctx.send(embed=embed)

            ctx.voice_client.source.volume = volume / 100
            embed = discord.Embed(title="Music", color=0x30c223)
            embed.add_field(name="Volume", value="{}%".format(volume))
            await ctx.send(embed=embed)

    @volume.error
    async def volume_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=':interrobang: Error!', description='No argument given!', color=0xff0011)
            await ctx.send(embed=embed)
        else:
            raise

    @commands.command(aliases=['l'])
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()

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


def setup(client):
    client.add_cog(Music(client))
