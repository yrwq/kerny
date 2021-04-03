#!/usr/bin/env python3
import discord
from discord.ext import commands

import os
from os import path

from colors import Colors
c = Colors()

devs = ["yrwq#5792", "Dempy#0053"]

token = os.environ.get("DISCORD_TOKEN")

intents=discord.Intents.all()
client = commands.Bot(command_prefix='sudo ', intents=intents)

# client = commands.Bot(command_prefix="sudo ")

@client.event
async def on_ready():

    print(f"{client.user.name} logged in ...")
    await client.change_presence(activity=discord.Game(name="https://github.com/yrwq/cool"))

    for filename in os.listdir("./modules"):
        if filename.endswith(".py"):
            client.load_extension(f"modules.{filename[:-3]}")
            print("Loaded: {}".format(filename))

@client.command()
async def load(ctx, extension):
    if str(ctx.message.author) in devs:

        if path.exists(f"modules/{extension}.py"):

            client.load_extension(f"modules.{extension}")
            await ctx.message.add_reaction("🤍")

            embed = discord.Embed(title=f"{extension} loaded!", color=c.green)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=f"{extension} doesn't exists!", color=c.red)
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="You are not a developer!", color=c.red)
        await ctx.send(embed=embed)


@client.command()
async def unload(ctx, extension):
    if str(ctx.message.author) in devs:

        client.unload_extension(f"modules.{extension}")
        await ctx.message.add_reaction("💔")

        embed = discord.Embed(title=f"{extension} unloaded!", color=c.green)
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="You are not a developer!", color=c.red)
        await ctx.send(embed=embed)

@client.command()
async def reload(ctx, extension):
    if str(ctx.message.author) in devs:

        if path.exists(f"modules/{extension}.py"):

            client.unload_extension(f"modules.{extension}")
            client.load_extension(f"modules.{extension}")

            await ctx.message.add_reaction("💖")

            embed = discord.Embed(title=f"{extension} reloaded!", color=c.green)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=f"{extension} doesn't exists!", color=c.red)
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="You are not a developer!", color=c.red)
        await ctx.send(embed=embed)

client.run(token)
