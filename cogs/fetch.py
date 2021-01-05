import discord
import time
import requests
import json
import os
import asyncio
from discord.ext import commands
from datetime import datetime
from time import strftime

class Fetch(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("fetchers.json", "r") as f:
            self.fetchers = json.load(f)

    @commands.command()
    async def setfetch(self, ctx, user_input):

        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)

        if not "http" in user_input:
            embed = discord.Embed(title="Fetch", color=0xea6f91)
            embed.set_footer(text="Please enter a valid url!")
            await ctx.send(embed=embed)

        if "http" in user_input:
            if ctx.author == self.client.user:
                return

            if not guild_id in self.fetchers:
                self.fetchers[guild_id] = {}

            if not user_id in self.fetchers[guild_id]:
                self.fetchers[guild_id][user_id] = {}
                self.fetchers[guild_id][user_id]['fetchUrl'] = user_input

            if user_id in self.fetchers[guild_id]:
                self.fetchers[guild_id][user_id]['fetchUrl'] = user_input

            with open("fetchers.json", "w") as f:
                json.dump(self.fetchers, f, indent=4)

            embed = discord.Embed(title="Fetch", color=0xea6f91)
            embed.set_footer(text=f"{ctx.author} successfully set fetch!")
            await ctx.send(embed=embed)

    @commands.command()
    async def fetch(self, ctx, fetcher: discord.Member):

        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        fetcher_id = str(fetcher.id)

        if not fetcher_id in self.fetchers[guild_id]:
            embed = discord.Embed(title="Fetch", color=0xea6f91)
            embed.set_footer(text=f"{fetcher} didn't set a fetch yet!")
            await ctx.send(embed=embed)

        if fetcher_id in self.fetchers[guild_id]:
            fetch_url = self.fetchers[guild_id][fetcher_id]['fetchUrl']

            try:
                fetch = requests.get(fetch_url)
                embed = discord.Embed(title="Fetch", color=0xea6f91)
                embed.set_footer(text=f"{fetch.text}")
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title="Fetch", color=0xea6f91)
                embed.set_footer(text=f"Couldn't get {fetcher}'s fetch!")
                await ctx.send(embed=embed)

    @fetch.error
    async def fetch_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            guild_id = str(ctx.guild.id)
            user_id = str(ctx.author.id)
            fetch_url = self.fetchers[guild_id][user_id]['fetchUrl']

            try:
                fetch = requests.get(fetch_url)
                embed = discord.Embed(title="Fetch", color=0xea6f91)
                embed.set_footer(text=f"{fetch.text}")
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title="Fetch", color=0xea6f91)
                embed.set_footer(text=f"Couldn't get your fetch!")
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Fetch(client))
