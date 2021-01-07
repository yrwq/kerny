import discord
import os
import asyncio
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, helpin):

        usage = {
            f"{ctx.prefix}fetch": f"show your fetch if you set one, run: `{ctx.prefix}help setfetch` to get information about how to set your fetch",
            f"{ctx.prefix}fetch user": "show fetch of <user> if user set one",
            f"{ctx.prefix}setfetch": "set your fetch, run:\n`curl -Ss https://raw.githubusercontent.com/yrwq/kerny/main/fetch.sh | sh`\n in your terminal to get your url",
            f"{ctx.prefix}setimg": "Add an image to your fetch.",
            f"{ctx.prefix}addrepo": "Add a repository to your highlighted repositories.",
            f"{ctx.prefix}wall tags": f"get a random wallpaper from `https://unsplash.com`\n\n example: `{ctx.prefix}wall mountain,snow`",
            f"{ctx.prefix}img tags": f"get a random image from `https://unsplash.com`\n\n example: `{ctx.prefix}img mountain,snow`",
            f"{ctx.prefix}play query": f"play a song from `https://youtube.com`\n\n example: `{ctx.prefix}play song_title`",
            f"{ctx.prefix}stop": "stop currently playing song",
            f"{ctx.prefix}vol percentage": f"set current song's volume \n\n example: `{ctx.prefix}vol 50`"
        }

        if helpin == "fetch":

            embed = discord.Embed(title="Fetch", color=0xea6f91)
            embed.add_field(name=f"`{ctx.prefix}fetch`", value=usage.get(f"{ctx.prefix}fetch"), inline=False)
            embed.add_field(name=f"`{ctx.prefix}fetch <user>`", value=usage.get(f"{ctx.prefix}fetch user"), inline=False)
            await ctx.send(embed=embed)

        elif helpin == "setfetch":

            embed = discord.Embed(title="Setfetch", color=0xea6f91)
            embed.add_field(name=f"{ctx.prefix}setfetch <url>", value=usage.get(f"{ctx.prefix}setfetch"), inline=False)
            await ctx.send(embed=embed)

        elif helpin == "wall":

            embed = discord.Embed(title="Wall", color=0xea6f91)
            embed.add_field(name=f"{ctx.prefix}wall tags", value=usage.get(f"{ctx.prefix}wall tags"), inline=False)
            await ctx.send(embed=embed)

        elif helpin == "img":

            embed = discord.Embed(title="Img", color=0xea6f91)
            embed.add_field(name=f"{ctx.prefix}img tags", value=usage.get(f"{ctx.prefix}img tags"), inline=False)
            await ctx.send(embed=embed)

        elif helpin == "play":

            embed = discord.Embed(title="Play", color=0xea6f91)
            embed.add_field(name=f"{ctx.prefix}play query", value=usage.get(f"{ctx.prefix}play query"), inline=False)
            await ctx.send(embed=embed)

        elif helpin == "stop":

            embed = discord.Embed(title="Stop", color=0xea6f91)
            embed.add_field(name=f"{ctx.prefix}stop", value=usage.get(f"{ctx.prefix}stop"), inline=False)
            await ctx.send(embed=embed)

        elif helpin == "vol":

            embed = discord.Embed(title="Volume", color=0xea6f91)
            embed.add_field(name=f"{ctx.prefix}vol percentage", value=usage.get(f"{ctx.prefix}vol percentage"), inline=False)
            await ctx.send(embed=embed)

        elif helpin == "setimg":

            embed = discord.Embed(title="Setimg", color=0xea6f91)
            embed.add_field(name=f"{ctx.prefix}setimg <url>", value=usage.get(f"{ctx.prefix}setimg"), inline=False)
            await ctx.send(embed=embed)

        elif helpin == "addrepo":

            embed = discord.Embed(title="Volume", color=0xea6f91)
            embed.add_field(name=f"{ctx.prefix}addrepo <url>", value=usage.get(f"{ctx.prefix}addrepo"), inline=False)
            await ctx.send(embed=embed)

        else:

            embed = discord.Embed(title="Help", color=0xea6f91)
            embed.add_field(name=f"{helpin} not found!", value=f"Run: `{ctx.prefix}help` to get available commands!", inline=False)
            await ctx.send(embed=embed)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            all_commands = {
                f"{ctx.prefix}fetch": "show your fetch if you set one",
                f"{ctx.prefix}fetch user": "show fetch of <user> if user set one",
                f"{ctx.prefix}setfetch": "set your fetch using",
                f"{ctx.prefix}setimg": "set your fetch image",
                f"{ctx.prefix}addrepo": "add a repository to your highlighted repositories",
                f"{ctx.prefix}wall": "get a random wallpaper from unsplash",
                f"{ctx.prefix}img": "get a random image from unsplash",
                f"{ctx.prefix}play": "play a song",
                f"{ctx.prefix}stop": "stop current song",
                f"{ctx.prefix}vol": "set song's volume"
            }

            embed = discord.Embed(title="Help", color=0xea6f91)

            embed.add_field(name=f"`{ctx.prefix}fetch`", value=all_commands.get(f"{ctx.prefix}fetch"), inline=False)
            embed.add_field(name=f"`{ctx.prefix}fetch <user>`", value=all_commands.get(f"{ctx.prefix}fetch user"), inline=False)
            embed.add_field(name=f"`{ctx.prefix}setfetch <url>`", value=all_commands.get(f"{ctx.prefix}setfetch"), inline=False)
            embed.add_field(name=f"`{ctx.prefix}setimg <url>`", value=all_commands.get(f"{ctx.prefix}setimg"), inline=False)
            embed.add_field(name=f"`{ctx.prefix}addrepo <url>`", value=all_commands.get(f"{ctx.prefix}addrepo"), inline=False)
            embed.add_field(name=f"`{ctx.prefix}wall`", value=all_commands.get(f"{ctx.prefix}wall"), inline=False)
            embed.add_field(name=f"`{ctx.prefix}img`", value=all_commands.get(f"{ctx.prefix}img"), inline=False)
            embed.add_field(name=f"`{ctx.prefix}play`", value=all_commands.get(f"{ctx.prefix}play"), inline=False)
            embed.add_field(name=f"`{ctx.prefix}stop`", value=all_commands.get(f"{ctx.prefix}stop"), inline=False)
            embed.add_field(name=f"`{ctx.prefix}vol`", value=all_commands.get(f"{ctx.prefix}vol"), inline=False)
            embed.add_field(name=">", value=f"run: `{ctx.prefix}help <command>` to get more information.")

            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
