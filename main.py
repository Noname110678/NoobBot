import discord
import os
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
import json
import asyncio
import config


# JSON THING LOAD FROM JSON FILE TO PYTHON

token = config.token
prefix = config.prefix

# MAKING BOT

bot = commands.Bot(command_prefix=f"{prefix}", help_command=None, self_bot=False)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}")
    await bot.change_presence(status=discord.Status.idle,
                            activity=discord.Game(name="Noname cares about bot?"))

@bot.event
async def on_member_join(member, ctx):
    if member.id == 838402467858612224:
        await ctx.send("Thanks for adding NoobBot! The prefix is **>** >help for commands")
    
# COGS COMMANDS


@bot.command()
async def load(ctx, extension: str):
    if ctx.author.id == 838402467858612224:
            bot.load_extension(f"cogs.{extension}")
            await ctx.message.reply(f"Cog {extension} is loaded!")
    else:
        await ctx.message.reply("youre not dev of this bot dont try this thing")


@bot.command()
async def unload(ctx, extension: str):
    if ctx.author.id == 838402467858612224:
            bot.unload_extension(f"cogs.{extension}")
            await ctx.message.reply(f"Cog {extension} is unloaded!")
    else:
        await ctx.message.reply("youre not dev of this bot dont try this thing")


@bot.command()
async def reload(ctx, extension: str):
    if ctx.author.id == 838402467858612224:
            bot.unload_extension(f"cogs.{extension}")
            bot.load_extension(f"cogs.{extension}")
            await ctx.message.reply(f"Cog {extension} is reloaded!")
    else:
        await ctx.message.reply("youre not dev of this bot dont try this thing")

@bot.command()
async def oof(ctx):
    if ctx.author.id == 838402467858612224:
        await ctx.message.reply("OOFING BOT...")
        quit()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")
    # RUNNING BOT

bot.run(token, bot=True)
