import discord
import requests
import json
import os
import asyncio
from discord.ext import commands

class Fetch(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("fetchers.json", "r") as f:
            self.fetchers = json.load(f)

    @commands.command()
    async def setfetch(self, ctx, user_input):

        user_id = str(ctx.author.id)

        valid_link = "0x0.st/"

        if not valid_link in user_input:
            embed = discord.Embed(title="Setfetch", color=0xea6f91)
            embed.add_field(name="Error", value="Please enter a valid url!", inline=False)
            embed.add_field(name="Usage", value="For a list of valid urls and more information, type: sudo help setfetch", inline=False)
            await ctx.send(embed=embed)

        if valid_link in user_input:
            if ctx.author == self.client.user:
                return

            if not self.fetchers:
                self.fetchers = {}

            if not user_id in self.fetchers:
                self.fetchers[user_id] = {}
                self.fetchers[user_id]["fetchUrl"] = user_input

            with open("fetchers.json", "w") as f:
                json.dump(self.fetchers, f, indent=4)

            embed = discord.Embed(title="Setfetch", color=0xea6f91)
            embed.set_footer(text=f"{ctx.author} successfully set fetch!")
            await ctx.send(embed=embed)

    @commands.command()
    async def fetchimg(self, ctx, user_input):

        user_id = str(ctx.author.id)

        valid_link = "0x0.st/"

        if not valid_link in user_input:
            embed = discord.Embed(title="Fetchimg", color=0xea6f91)
            embed.add_field(name="Error", value="Please enter a valid url!", inline=False)
            embed.add_field(name="Usage", value="For a list of valid urls and more information, type: sudo help setimg", inline=False)
            await ctx.send(embed=embed)

        if valid_link in user_input:
            if ctx.author == self.client.user:
                return

            if not self.fetchers:
                self.fetchers = {}

            if not user_id in self.fetchers:
                self.fetchers[user_id] = {}

            if user_id in self.fetchers:
                self.fetchers[user_id]["fetchImg"] = user_input

            with open("fetchers.json", "w") as f:
                json.dump(self.fetchers, f, indent=4)

            embed = discord.Embed(title="Fetchimg", color=0xea6f91)
            embed.set_footer(text=f"{ctx.author} successfully set fetch image!")
            await ctx.send(embed=embed)

    @commands.command()
    async def fetchrepo(self, ctx, user_input):

        user_id = str(ctx.author.id)

        valid_link = "https://github.com"

        if not valid_link in user_input:
            embed = discord.Embed(title="Fetchrepo", color=0xea6f91)
            embed.add_field(name="Error", value="Please enter a valid url!", inline=False)
            embed.add_field(name="Usage", value="For a list of valid urls and more information, type: sudo help fetchrepo", inline=False)
            await ctx.send(embed=embed)

        if valid_link in user_input:
            if ctx.author == self.client.user:
                return

            if not self.fetchers:
                self.fetchers = {}

            if not user_id in self.fetchers:
                self.fetchers[user_id] = {}

            if user_id in self.fetchers:
                self.fetchers[user_id]["fetchRepo"] = user_input

            with open("fetchers.json", "w") as f:
                json.dump(self.fetchers, f, indent=4)

            embed = discord.Embed(title="Fetchrepo", color=0xea6f91)
            embed.set_footer(text=f"{ctx.author} successfully set fetch repository!")
            await ctx.send(embed=embed)

    @commands.command()
    async def clearfetch(self, ctx):

        user_id = str(ctx.author.id)

        if user_id in self.fetchers:
            del self.fetchers[user_id]

        with open("fetchers.json", "w") as f:
            json.dump(self.fetchers, f, indent=4)

        embed = discord.Embed(title="Setfetch", color=0xea6f91)
        embed.set_footer(text=f"{ctx.author} successfully cleared fetch!")
        await ctx.send(embed=embed)

    @commands.command()
    async def fetch(self, ctx, fetcher: discord.Member):

        user_id = str(ctx.author.id)
        fetcher_id = str(fetcher.id)

        if not self.fetchers:
            embed = discord.Embed(title="Fetch", color=0xea6f91)
            embed.set_footer(text="No one set a fetch yet!")
            await ctx.send(embed=embed)
            self.fetchers = {}

        if not self.fetchers[fetcher_id]["fetchUrl"]:
            embed = discord.Embed(title="Fetch", color=0xea6f91)
            embed.set_footer(text=f"{fetcher} didn't set a fetch yet!")
            await ctx.send(embed=embed)

        if self.fetchers[fetcher_id]:


            if self.fetchers[fetcher_id]["fetchUrl"]:
                try:
                    fetch_url = self.fetchers[user_id]["fetchUrl"]
                    fetch = requests.get(fetch_url)
                except:
                    embed = discord.Embed(title="Fetch", color=0xea6f91)
                    embed.set_footer(text=f"Couldn't get {fetcher}'s fetch!")
                    await ctx.send(embed=embed)

            if self.fetchers[fetcher_id]["fetchImg"]:

                try:
                    img_url = self.fetchers[user_id]["fetchImg"]

                except:
                    embed = discord.Embed(title="Fetch", color=0xea6f91)
                    embed.set_footer(text=f"Couldn't get {fetcher}'s fetch image!")

            if self.fetchers[fetcher_id]["fetchRepo"]:

                try:
                    repo_url = self.fetchers[user_id]["fetchRepo"]

                except:
                    embed = discord.Embed(title="Fetch", color=0xea6f91)
                    embed.set_footer(text=f"Couldn't get {fetcher}'s fetch repository!")

            embed = discord.Embed(title="Fetch", color=0xea6f91)
            embed.set_image(url=img_url)
            embed.add_field(name="Information", value=fetch.text, inline=True)
            embed.add_field(name="Repository", value=repo_url, inline=True)
            await ctx.send(embed=embed)

    @fetch.error
    async def fetch_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            user_id = str(ctx.author.id)

            try:
                fetch_url = self.fetchers[user_id]["fetchUrl"]
                fetch = requests.get(fetch_url)
                embed = discord.Embed(title="Fetch", color=0xea6f91)
                embed.set_footer(text=f"{fetch.text}")
                await ctx.send(embed=embed)

            except:
                if not self.fetchers:
                    embed = discord.Embed(title="Fetch", color=0xea6f91)
                    embed.set_footer(text="No one set a fetch yet!")
                    await ctx.send(embed=embed)
                    self.fetchers = {}

                if not user_id in self.fetchers:
                    embed = discord.Embed(title="Fetch", color=0xea6f91)
                    embed.set_footer(text="You didn't set a fetch yet!")
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(title="Fetch", color=0xea6f91)
                    embed.set_footer(text=f"Couldn't get your fetch!")
                    await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Fetch(client))
