import discord
import json
import asyncio
from discord.ext import commands


class Fetch(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("fetchers.json", "r") as f:
            self.fetchers = json.load(f)

    @commands.command()
    async def setfetch(self, ctx, *, user_input):

        user_id = str(ctx.author.id)

        if not self.fetchers:
            self.fetchers = {}

        # Parse fetch data
        fetch = user_input.split("\n")
        distro = fetch[0]
        kernel = fetch[1]
        terminal = fetch[2]
        editor = fetch[3]
        wm = fetch[4]
        resolution = fetch[5]
        display_prot = fetch[6]
        gtk_theme = fetch[7]

        if user_id not in self.fetchers:
            self.fetchers[user_id] = {}
            self.fetchers[user_id]["repos"] = []
        else:
            self.fetchers[user_id]["fetch"] = [distro, kernel, terminal, editor, wm, resolution, display_prot, gtk_theme]

        with open("fetchers.json", "w") as f:
            json.dump(self.fetchers, f, indent=4)

        embed = discord.Embed(title="Setfetch", color=0xea6f91)
        embed.set_footer(text=f"{ctx.author} successfully set fetch!")
        await ctx.send(embed=embed)

    @commands.command()
    async def setimg(self, ctx, user_input):

        user_id = str(ctx.author.id)

        if ctx.author == self.client.user:
            return

        try:
            self.fetchers[user_id]["fetchImg"] = {}
            self.fetchers[user_id]["fetchImg"] = user_input
            embed = discord.Embed(title="Fetch", color=0xea6f91)
            embed.set_footer(text=f"{ctx.author} successfully set a fetch image!")
            await ctx.send(embed=embed)

        except:
            embed = discord.Embed(title="Fetch", color=0xea6f91)
            embed.add_field(name=f"Please set a fetch first!", value=f"run:{ctx.prefix}help setfetch")
            await ctx.send(embed=embed)

        with open("fetchers.json", "w") as f:
            json.dump(self.fetchers, f, indent=4)

    @commands.command()
    async def addrepo(self, ctx, user_input):

        user_id = str(ctx.author.id)

        valid_link = "https://github.com"

        if valid_link in user_input:

            if ctx.author == self.client.user:
                return

            try:
                repo = self.fetchers[user_id]["repos"]
                if user_input in repo:
                    embed = discord.Embed(title="Fetch", color=0xea6f91)
                    embed.set_footer(text="You already added this repository!")
                    await ctx.send(embed=embed)
                else:
                    repo.append(user_input)
                    embed = discord.Embed(title="Fetch", color=0xea6f91)
                    embed.set_footer(text=f"{ctx.author} successfully set fetch repository!")
                    await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title="Fetch", color=0xea6f91)
                embed.add_field(name=f"Please set a fetch first!", value=f"run:{ctx.prefix}help setfetch")
                await ctx.send(embed=embed)

            with open("fetchers.json", "w") as f:
                json.dump(self.fetchers, f, indent=4)

        else:
            embed = discord.Embed(title="Fetch", color=0xea6f91)
            embed.set_footer(text="Please enter a valid github repository!")
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

        fetcher_id = str(fetcher.id)

        embed = discord.Embed(title="Fetch", color=0xea6f91)

        try:
            fetch = self.fetchers[fetcher_id]["fetch"]
            distro = fetch[0]
            kernel = fetch[1]
            terminal = fetch[2]
            editor = fetch[3]
            wm = fetch[4]
            resolution = fetch[5]
            display_prot = fetch[6]
            gtk_theme = fetch[7]

            embed.add_field(name="Information", value=f"""
`Distro:` {distro}
`Kernel:` {kernel}
`Terminal:` {terminal}
`Editor:` {editor}
`WM:` {wm}
`Resolution:` {resolution}
`Display protocol:` {display_prot}
`GTK-Theme:` {gtk_theme}
""", inline=True)

        except:
            embed.add_field(name="Information", value="Wow, such empty.", inline=True)

        try:
            img_url = self.fetchers[fetcher_id]["fetchImg"]
            embed.set_image(url=img_url)
        except:
            print(f"{ctx.author} didn't set an image yet")

        try:
            repo_url = self.fetchers[fetcher_id]["repos"]
            if repo_url[0] == None:
                print(f"{fetcher_id} don't have any repositories")
            else:
                embed.add_field(name="Highlighted repositories", value=repo_url, inline=True)
        except:
            print(f"{fetcher_id} don't have any repositories")

        await ctx.send(embed=embed)

    @fetch.error
    async def fetch_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):

            user_id = str(ctx.author.id)

            embed = discord.Embed(title="Fetch", color=0xea6f91)

            try:
                fetch = self.fetchers[user_id]["fetch"]
                distro = fetch[0]
                kernel = fetch[1]
                terminal = fetch[2]
                editor = fetch[3]
                wm = fetch[4]
                resolution = fetch[5]
                display_prot = fetch[6]
                gtk_theme = fetch[7]

                embed.add_field(name="Information", value=f"""
`Distro:` {distro}
`Kernel:` {kernel}
`Terminal:` {terminal}
`Editor:` {editor}
`WM:` {wm}
`Resolution:` {resolution}
`Display protocol:` {display_prot}
`GTK-Theme:` {gtk_theme}
""", inline=True)

            except:
                embed.add_field(name="Information", value="Wow, such empty.", inline=True)

            try:
                img_url = self.fetchers[user_id]["fetchImg"]
                embed.set_image(url=img_url)
            except:
                print(f"{ctx.author} didn't set an image yet")

            try:
                repo_url = self.fetchers[user_id]["repos"]
                if repo_url[0] == None:
                    print(f"{user_id} don't have any repositories")
                else:
                    repos = " ".join([str(elem) for elem in repo_url])
                    embed.add_field(name="Highlighted repositories", value=repos, inline=True)
            except:
                print(f"{user_id} don't have any repositories")

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fetch(client))
