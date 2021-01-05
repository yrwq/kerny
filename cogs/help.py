import discord
import os
import asyncio
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, helpin):

        fetch_usage = {
            "sudo fetch": "show your fetch if you set one, run: sudo help setfetch to get information about how to set your fetch",
            "sudo fetch user": "show fetch of <user> if user set one"
        }

        setfetch_usage = {
            "sudo setfetch": "set your fetch, run:\n`curl -Ss https://raw.githubusercontent.com/yrwq/kerny/main/fetch.sh | sh`\n in your terminal to get your url"
        }

        if helpin == "fetch":

            embed = discord.Embed(title="Fetch", color=0xea6f91)
            embed.add_field(name="`sudo fetch`", value=fetch_usage.get("sudo fetch"), inline=False)
            embed.add_field(name="`sudo fetch <user>`", value=fetch_usage.get("sudo fetch user"), inline=False)
            await ctx.send(embed=embed)

        elif helpin == "setfetch":

            embed = discord.Embed(title="Setfetch", color=0xea6f91)
            embed.add_field(name="sudo setfetch <url>", value=setfetch_usage.get("sudo setfetch"), inline=False)
            await ctx.send(embed=embed)

        else:

            embed = discord.Embed(title="Help", color=0xea6f91)
            embed.add_field(name=f"{helpin} not found!", value="Run: `sudo help` to get available commands!", inline=False)
            await ctx.send(embed=embed)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            all_commands = {
                "sudo fetch": "show your fetch if you set one",
                "sudo fetch user": "show fetch of <user> if user set one",
                "sudo setfetch": "set your fetch using"
            }

            embed = discord.Embed(title="Help", color=0xea6f91)

            embed.add_field(name="sudo fetch", value=all_commands.get("sudo fetch"), inline=False)
            embed.add_field(name="sudo fetch <user>", value=all_commands.get("sudo fetch user"), inline=False)
            embed.add_field(name="sudo setfetch <url>", value=all_commands.get("sudo setfetch"), inline=False)
            embed.set_footer(text="run: sudo help <command> to get more information.")

            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
