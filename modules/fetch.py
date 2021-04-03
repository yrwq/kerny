import discord
import asyncio
import json

from discord.ext import commands


import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from colors import Colors
c = Colors()

class Fetch(commands.Cog):
    def __init__(self, client):
        self.client = client

        try:
            self.load_fetchers()
        except:
            f = open("fetchers.json","w+")
            f.write("{}")
            f.close()
            self.load_fetchers()

    def load_fetchers(self):
        with open("fetchers.json", "r") as f:
            self.fetchers = json.load(f)

    def save_fetchers(self):
        with open("fetchers.json", "w") as f:
            json.dump(self.fetchers, f, indent=4)

    @commands.command(aliases=["sf"])
    async def setfetch(self, ctx, *, inp):
        user_id = str(ctx.author.id)
        
        # Parse fetch data
        fetch = inp.split("\n")
        distro = fetch[0]
        kernel = fetch[1]
        term = fetch[2]
        editor = fetch[3]
        wm = fetch[4]
        res = fetch[5]
        prot = fetch[6]
        theme = fetch[7]
        disk = fetch[8]

        if user_id not in self.fetchers:
            self.fetchers[user_id] = {}
            self.fetchers[user_id]["fetch"] = [
                    distro,
                    kernel,
                    term,
                    editor,
                    wm,
                    res,
                    prot,
                    theme,
                    disk
                    ]

        self.save_fetchers()
        
        embed = discord.Embed(title="Setfetch", color=c.magenta)
        embed.set_footer(text=f"{ctx.author} successfully set a fetch!")
        await ctx.send(embed=embed)


    @commands.command(aliases=["clf"])
    async def clearfetch(self, ctx):

        user_id = str(ctx.author.id)

        if user_id in self.fetchers:
            del self.fetchers[user_id]

        self.save_fetchers()

        embed = discord.Embed(title="Setfetch", color=0xea6f91)
        embed.set_footer(text=f"{ctx.author} successfully cleared fetch!")
        await ctx.send(embed=embed)


    @commands.command()
    async def fetch(self, ctx, user: discord.Member = None):

        if user == None:
            user = ctx.author
            pass

        user_id = str(user.id)

        try:
            fetch = self.fetchers[user_id]["fetch"]
            distro = fetch[0]
            kernel = fetch[1]
            term = fetch[2]
            editor = fetch[3]
            wm = fetch[4]
            res = fetch[5]
            prot = fetch[6]
            theme = fetch[7]
            disk = fetch[8]
        except:
            await ctx.send(f"{user} didn't set a fetch yet")

        embed = discord.Embed(title="Fetch", color=c.magenta)
        embed.add_field(name = "Distro", value = f"{distro}")
        embed.add_field(name = "Kernel", value = f"{kernel}")
        embed.add_field(name = "Terminal", value = f"{term}")
        embed.add_field(name = "Editor", value = f"{editor}")
        embed.add_field(name = "Wm", value = f"{wm}")
        embed.add_field(name = "Resolution", value = f"{res}")
        embed.add_field(name = "Disp prot", value = f"{prot}")
        embed.add_field(name = "Gtk theme", value = f"{theme}")
        embed.add_field(name = "Disk", value = f"{disk}")
        await ctx.send(embed=embed)
    
def setup(client):
    client.add_cog(Fetch(client))
