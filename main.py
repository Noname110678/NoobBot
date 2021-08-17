import discord
import os
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
import json
import asyncio


# JSON THING LOAD FROM JSON FILE TO PYTHON

configFile = open("config.json", "r") # lmao # what why
configJSON = configFile.read()
obj = json.loads(configJSON)
token = obj["token"]
prefix = obj["default_prefix"]

# MAKING BOT

bot = commands.Bot(command_prefix=f"{prefix}", help_command=None, self_bot=False)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print("Bot is ready!")
    await bot.change_presence(status=discord.Status.do_not_disturb,
                            activity=discord.Streaming(name="Working", url="https://www.twitch.tv/noname110567e"))

@bot.event
async def on_member_join(member, ctx):
    if member.id == 838402467858612224:
        ctx.send("Thanks for adding NoobBot! The prefix is **>** >help for commands")
    
# COGS COMMANDS


@bot.command()
async def load(ctx, extension: str):
    if ctx.author.id == 838402467858612224:
        if extension == "all":
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    bot.load_extension(f"cogs.{filename}")
                    await ctx.send("Loaded Every Cog!")
        else:
            bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"Cog {extension} is loaded!")
    else:
        await ctx.send("youre not dev of this bot dont try this thing")


@bot.command()
async def unload(ctx, extension: str):
    if ctx.author.id == 838402467858612224:
        if extension == "all":
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    bot.unload_extension(f"cogs.{filename}")
                    await ctx.send("Unloaded Every Cog!")
        else:
            bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"Cog {extension} is unloaded!")
    else:
        await ctx.send("youre not dev of this bot dont try this thing")


@bot.command()
async def reload(ctx, extension: str):
    if ctx.author.id == 838402467858612224:
        if extension == "all":
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    bot.unload_extension(f"cogs.{filename}")
                    bot.load_extension(f"cogs.{filename[:-3]}")
                    await ctx.send("Reloaded Every Cog!")
        else:
            bot.unload_extension(f"cogs.{extension}")
            bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"Cog {extension} is reloaded!")
    else:
        await ctx.send("youre not dev of this bot dont try this thing")

@bot.command()
async def oof(ctx):
    if ctx.author.id == 838402467858612224:
        await ctx.send("OOFING BOT...")
        quit()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")
    # RUNNING BOT

bot.run(token, bot=True)
