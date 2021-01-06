import discord
import asyncio
import os
import random
from discord.ext import commands
from pyunsplash import PyUnsplash

api_key = os.environ.get("UNS_TOKEN")

uns = PyUnsplash(api_key=api_key)

class Wall(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wall(self, ctx, query):
        # get a random wallpaper
        rand = random.randint(1,30)
        search = uns.search(type_='photos', per_page=rand, page=rand, query="wallpaper," + query)
        for entry in search.entries:
            url = entry.link_html + "/download?force=true"

        await ctx.send(url)

    @commands.command()
    async def img(self, ctx, query):
        # get a random image
        rand = random.randint(1,30)
        search = uns.search(type_='photos', per_page=rand, page=rand, query=query)
        for entry in search.entries:
            url = entry.link_html + "/download?force=true"

        await ctx.send(url)

def setup(client):
    client.add_cog(Wall(client))
