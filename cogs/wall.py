import discord
import os
import asyncio
import requests
from discord.ext import commands

class Wall(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wall(self, ctx, query):
        url = "https://source.unsplash.com/1600x900/?" + query
        session = requests.Session()
        r = session.head(url, allow_redirects=True)
        print(r.url)
        await ctx.send(r.url)

def setup(client):
    client.add_cog(Wall(client))
