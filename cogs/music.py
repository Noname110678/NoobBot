import discord
from discord.ext import commands
from discord import Colour, Embed
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
import youtube_dl
import os


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Plays music!", options=[
        create_option(name="url", description="Enter the valid URL (link) of a youtube video you want to listen!",
                      option_type=3, required=True)
    ])
    async def play(self, ctx = discord.ext.commands.context.Context, url: str = ''):

        embed = Embed(title="Playing!", description=f"Playing {url}..!", color=Colour.random())
        embed.set_footer(text=f"Queued by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

@cog_ext.cog_slash(description="Leaves the voice channel!")
async def leave(self,ctx):
    bot = self.bot
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")
    embed = Embed(title="Left!", description="Left the voice channel!", color=Colour.random())
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))
