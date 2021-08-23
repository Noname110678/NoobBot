import random
import ctypes
import asyncpraw
import discord
import pyttsx3
import asyncio
import aiohttp
from discord import Embed, Colour
from discord.ext import commands
from simpledemotivators import Demotivator


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if not msg.guild:
            if msg.author != self.bot.user:
                await msg.add_reaction("🆗")

    @commands.command()
    async def ball(self, ctx, *, question: str):
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
        await ctx.message.reply(embed=mbed)

    @commands.command()
    async def embed(self,ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        colRandom = False

        titlemsg = await ctx.message.reply("Write title of embed please!", delete_after=15.0)
        title = await self.bot.wait_for('message', check=check)  
        await titlemsg.delete()

        descmsg = await ctx.message.reply("Write description of embeed please!", delete_after=15.0)
        desc = await self.bot.wait_for('message', check=check)
        await descmsg.delete()
        colormsg = await ctx.message.reply("write rgb code in this syntax **rgb(code)** **RANDOM** for random color")
        color = await self.bot.wait_for('message', check=check)
        if color.content is not "RANDOM":
            color = color.content.split(")")[0].split("rgb(")[1]
            embed = Embed(
            title = title.content, description = desc.content, color=Colour.from_rgb(color)
        )
        else:
            embed = Embed(
            title = title.content, description = desc.content, color=Colour.random()
        )
        await colormsg.delete()

        await ctx.message.reply(embed=embed)

        # making da embed :))))
        
        


    @commands.command()
    async def ping(self, ctx):
        mbed = Embed(
            title="Pong!",
            description=f"Bot ping is {round(self.bot.latency * 1000)}ms",
            colour=Colour.random()
        )
        await ctx.message.reply(embed=mbed)

    @commands.command()
    async def meme(self, ctx):
        msg = await ctx.message.reply("Loading meme ... <a:Loading:845258574434795570>")
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


    @commands.command()
    async def info(self, ctx):
        mbed = Embed(
            title="Information of the bot",
            colour=Colour.random()
        )
        mbed.add_field(name="Creator", value="Noname1105#0437", inline=False)
        mbed.add_field(name="Using", value="Discord.py", inline=False)
        mbed.add_field(name="Bot was created", value="7/2/2021, 2:18:55 PM (Creator's time)", inline=False)
        mbed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/860449450807263233/ffe1ae61afa8f343c0b5e9049f9a105c.png?size=1024")
        pog_msg = await ctx.message.reply(embed=mbed)
        await pog_msg.add_reaction("👍")

    @commands.command()
    async def help(self, ctx, cmd=""):
        embed = Embed(
            title="Commands list of NoobBot",
            description=">help <command> to show description and use syntax of specified command!",
            color=Colour.random()
        )
        embed.add_field(name="info", value="Shows the info of the bot!", inline=False)
        embed.add_field(name="ping", value="Shows the ping of the bot!", inline=False)
        embed.add_field(name="demotivator", value="Sends a demotivator!", inline=False)

        if cmd == "info":
            mbed = Embed(
                    title="Info Command",
                    description="Tells the info of the bot!",
                    color=Colour.random()
                )
            await ctx.message.reply(embed=mbed)
        elif cmd == "ping":
                mbed = Embed(
                    title="Ping Command",
                    description="Tells the ping of bot!",
                    color=Colour.random()
                )
                await ctx.message.reply(embed=mbed)
        elif cmd == "demotivator":
            mbed = Embed(
                title="Demotivator Command",
                description="Creates demotivator!",
                color=Colour.random()
            )
            mbed.add_field(name="Syntax",value=">demotivator")
            await ctx.message.reply(embed=mbed)
        elif cmd == "":
            await ctx.message.reply(embed=embed)


    @commands.command()
    async def demotivator(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        topmsg = await ctx.message.reply("Please send what should be in demotivator as top text",delete_after=15.0)
        top = await self.bot.wait_for('message', check=check)
        await topmsg.delete()

        bottommsg = await ctx.message.reply("Please send what should be in demotivator as bottom text",delete_after=15.0)
        bottom = await self.bot.wait_for('message', check=check)
        await bottommsg.delete()
        urlmsg = await ctx.message.reply("Send the url of image which will be in demotivator!",delete_after=15.0)
        url = await self.bot.wait_for('message', check=check)
        await urlmsg.delete()
        
        dem = Demotivator(f'{top.content}', f'{bottom.content}')
        dem.create(f"{url.content}", url=True)
        await ctx.message.reply(file=discord.File("./demresult.jpg"))
        await top.delete()
        await asyncio.sleep(1)
        await bottom.delete()
        await asyncio.sleep(1)
        await url.delete()


def setup(bot):
    bot.add_cog(User(bot))
