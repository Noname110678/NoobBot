import random
import ctypes
import asyncpraw
import discord
import pyttsx3
import aiohttp
from discord import Embed, Colour
from discord_slash import cog_ext
from discord.ext import commands
from simpledemotivators import Demotivator
from discord_slash.utils.manage_commands import create_choice, create_option


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if not msg.guild:
            if msg.author != self.bot.user:
                await msg.add_reaction("🆗")

    @cog_ext.cog_slash(name="ball",description="Ask a question to the ball", options=[
        create_option(name="question",description="The question", option_type=3,required=True)
    ])
    async def ball(self, ctx, question: str):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful.",
                     "Maybe."]
        mbed = Embed(
            title="8Ball",
            description=f"Question was [{question}]\nAnswer is [{random.choice(responses)}]",
            color=Colour.random()
        )
        await ctx.send(embed=mbed)

   
    @cog_ext.cog_slash(description="Checks the ping of bot!")
    async def ping(self, ctx):
        mbed = Embed(
            title="Pong!",
            description=f"Bot ping is {round(self.bot.latency * 1000)}ms",
            colour=Colour.random()
        )
        await ctx.send(embed=mbed)

    @cog_ext.cog_slash(description="Get a meme!")
    async def meme(self, ctx):
        msg = await ctx.send("Loading meme ... <a:Loading:845258574434795570>")
        reddit = asyncpraw.Reddit(client_id="16udYmOO1rdFRF0BgZk1bQ",
                                  client_secret="pqynqNrbCl1xU60c3EdNo7138_gAzw",
                                  username="Noname1105678",
                                  password="justjustjusttest",
                                  user_agent="noname1105678")

        subreddit = await reddit.subreddit("meme")
        all_subs = []
        top = subreddit.top(limit=450)
        async for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        mbed = Embed(title=f"{name}", colour=Colour.random(), url=url)

        mbed.set_image(url=url)
        mbed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        mbed.set_author(name="Here is your meme!")
        await msg.edit(content="", embed=mbed)


    @cog_ext.cog_slash(description="Information of the bot!")
    async def info(self, ctx):
        mbed = Embed(
            title="Information of the bot",
            colour=Colour.random()
        )
        mbed.add_field(name="Creator", value="NonameTheSus#0437", inline=False)
        mbed.add_field(name="Using", value="Discord.py", inline=False)
        mbed.add_field(name="Bot was created", value="7/2/2021, 2:18:55 PM (Creator's time)", inline=False)
        mbed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/860449450807263233/ffe1ae61afa8f343c0b5e9049f9a105c.png?size=1024")
        pog_msg = await ctx.send(embed=mbed)
        await pog_msg.add_reaction("👍")

    @cog_ext.cog_slash(description="Sends demotivator pic!", options=[
        create_option(name="url", description="Url for demotivator", option_type=3, required=True),
        create_option(name="toptext", description="Top Text for demotivator pic", option_type=3, required=True),
        create_option(name="bottomtext", description="Bottom Text for demotivator pic", option_type=3, required=False)
    ])
    async def demotivator(self, ctx, url: str, toptext: str, bottomtext: str = ""):
        dem = Demotivator(f'{toptext}', f'{bottomtext}')
        dem.create(f"{url}", url=True)
        await ctx.send(file=discord.File("./demresult.jpg"))


def setup(bot):
    bot.add_cog(User(bot))
