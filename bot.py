#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import os
from os import path

devs = ["yrwq#5792", "Dempy#0053"]

TOKEN_AUTH = os.environ.get("DISCORD_TOKEN")
# TOKEN_AUTH = "token"

client = commands.Bot(command_prefix="sudo ")
client.remove_command("help")

@client.event
async def on_ready():

    print(f"{client.user.name} logged in ...")

    await client.change_presence(activity=discord.Game(name="https://github.com/yrwq/kerny"))

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")
            print("Loaded: {}".format(filename))

@client.command()
async def load(ctx, extension):
    if str(ctx.message.author) in devs:

        if path.exists(f"cogs/{extension}.py"):

            client.load_extension(f"cogs.{extension}")
            await ctx.message.add_reaction("🤍")

            embed = discord.Embed(title=f"{extension} loaded! 🤍", color=0x9bced7)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=f"{extension} doesn't exists! 💔", color=0xea6f91)
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="You are not a developer! 💔", color=0xea6f91)
        await ctx.send(embed=embed)


@client.command()
async def unload(ctx, extension):
    if str(ctx.message.author) in devs:

        client.unload_extension(f"cogs.{extension}")
        await ctx.message.add_reaction("💔")

        embed = discord.Embed(title=f"{extension} unloaded! 💔", color=0x34738e)
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="You are not a developer! 💔", color=0xea6f91)
        await ctx.send(embed=embed)

@client.command()
async def reload(ctx, extension):
    if str(ctx.message.author) in devs:

        if path.exists(f'cogs/{extension}.py'):

            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')

            await ctx.message.add_reaction("💖")

            embed = discord.Embed(title=f"{extension} reloaded! 💖", color=0x9bced7)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=f"{extension} doesn't exists! 💔", color=0xea6f91)
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="You are not a developer! 💖", color=0xea6f91)
        await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        embed = discord.Embed(title="Command not found! 💔", color=0xea6f91)
        embed.set_footer(text="For available commands, type: sudo help")
        await ctx.send(embed=embed)

client.run(TOKEN_AUTH)
