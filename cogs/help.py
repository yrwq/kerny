import discord
import os
import asyncio
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, helpin):

        # TODO Add longer descriptions, properly describe what items do.

        if "fetch" in helpin:

            fetch_usage = {
                "y!fetch": "show your fetch",
                "y!fetch user": "show a user's fetch"
            }

            embed = discord.Embed(title="Fetch", color=0xea6f91)
            embed.add_field(name="y!fetch", value=fetch_usage.get("y!fetch"), inline=False)
            embed.add_field(name="y!fetch user", value=fetch_usage.get("y!fetch user"), inline=False)
            await ctx.send(embed=embed)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            all_commands = {
                "y!fetch": "show your fetch",
                "y!fetch user": "show a user's fetch",
                "y!setfetch": "set your fetch url"
            }

            embed = discord.Embed(title="Help", color=0xea6f91)

            embed.add_field(name="y!fetch", value=all_commands.get("y!fetch"), inline=False)
            embed.add_field(name="y!fetch user", value=all_commands.get("y!fetch user"), inline=False)
            embed.add_field(name="y!setfetch", value=all_commands.get("y!setfetch"), inline=False)

            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
