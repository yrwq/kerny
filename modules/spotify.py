import discord
import asyncio
from discord import Spotify
from discord.ext import commands

class Xd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["listening"])
    async def current(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
            pass
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    embed = discord.Embed(description="Listening on spotify", color=0xffc926)
                    embed.set_author(name =user.name, icon_url = user.avatar_url)
                    embed.add_field(name="Track", value=f"{activity.title}", inline=False)
                    embed.add_field(name="Album", value=f"{activity.album}", inline=False)
                    embed.add_field(name="Artist", value=f"{activity.artist}", inline=False)
                    embed.set_thumbnail(url=activity.album_cover_url)
                    await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Xd(client))
