import random
import ctypes
import asyncpraw
import discord
import pyttsx3
import aiohttp
from discord import Embed, Colour
from discord_slash import cog_ext
import requests
from discord.ext import commands
from simpledemotivators import Demotivator
import json
from discord_slash.utils.manage_commands import create_choice, create_option


class Pictures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @cog_ext.cog_slash(description="Random Cat Photo")
    @commands.command()
    async def cat(self, ctx):
        response = requests.get('https://some-random-api.ml/img/cat')  # Get-запрос
        json_data = json.loads(response.text)  # Извлекаем JSON
        link = json_data['link']  # Какаета хуетень я сам хз
        embed = Embed(
            title="Cats :3", color=Colour.random()
        )
        embed.set_image(url=link)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Random Dog Photo")
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')  # Make a request
            data = await request.json()  # Convert it to a JSON dictionary

            mbed = Embed(
                title="Woof!", color=Colour.random()
            )
            mbed.set_image(url=data['link'])
            await ctx.send(embed=mbed)

    @cog_ext.cog_slash(description="Random Fox Photo")
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://randomfox.ca/floof") as r:
                data = await r.json()

                mbed = Embed(
                    title="Foxes :D", color=Colour.random()
                )
                mbed.set_image(url=data['image'])
                await ctx.send(embed=mbed)


def setup(bot):
    bot.add_cog(Pictures(bot))
