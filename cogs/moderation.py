import json
from asyncio.streams import StreamReader
import discord, asyncio
from discord import Embed, Colour, Member
from discord import colour
from discord.ext.commands import cog, MissingPermissions, has_permissions
from discord_slash import cog_ext, SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(manage_messages=True)
    async def mute(self, ctx, user: Member, time, *, reason: str = None):
        if not user:
            embed = Embed(title="Syntax error!", description="Who are you going to mute? ERROR: MISSING MEMBER MENTION",
                          color=Colour.random())
            embed.add_field(name="Correct syntax", value=">mute **@mention** time reason")
            embed.add_field(name="Example of command", value=f">mute {self.bot.user.mention} 15m Staff Disrespect")
            await ctx.message.reply(embed=embed)
            return
        if not time:
            embed = Embed(title="Syntax error!", description="Whats time of mute? ERROR: MISSING MUTE TIME",
                          color=Colour.random())
            embed.add_field(name="Time syntaxes", value="1s = 1 Second\n 1m = 1 Minute\n 1h = 1 Hour\n 1d = 1 Day")
            embed.add_field(name="Correct syntax", value=">mute @mention **time** reason")
            embed.add_field(name="Example of command", value=f">mute {self.bot.user.mention} **15m** Staff Disrespect")
            await ctx.message.reply(embed=embed)
            return

        if not time.endswith("s") or time.endswith("m") or time.endswith("h") or time.endswith("d"):
            embed = Embed(title="Syntax error!", description="I didnt understood what time. ERROR: INCORRECT MUTE TIME",
                          color=Colour.random())
            embed.add_field(name="Time syntaxes", value="1s = 1 Second\n 1m = 1 Minute\n 1h = 1 Hour\n 1d = 1 Day")
            embed.add_field(name="Correct syntax", value=">mute @mention time reason")
            embed.add_field(name="Example of command",
                            value=f">mute {self.bot.user.mention} **15m** Staff Disrespect")
            await ctx.message.reply(embed=embed)
            return

        guild = ctx.guild
        mute_role = discord.utils.get(guild.roles, name="Punishment-Mute")
        time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        timemute = int(time[0]) * time_convert[time[-1]]
        if not mute_role:
            mute_role = await guild.create_role(name="Punishment-Mute")
            for channel in guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, read_messages=True,
                                              read_message_history=True)
        mbed = Embed(
            title="Muted!",
            description=f"{user.mention} got muted by reason {reason}",
            color=Colour.random()
        )
        await ctx.message.reply(embed=mbed, delete_after=8.0)
        await user.add_roles(mute_role, reason=reason)
        await user.send(f"You got muted in **{guild.name}**! Reason is: {reason}")
        await asyncio.sleep(timemute)
        await user.remove_roles(mute_role, reason="Time's up!")
        await user.send(f"You've got unmuted from **{guild.name}**, congratulations!")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "You cannot do that! Sorry, {}".format(ctx.message.author)
            await self.bot.send_message(ctx.message.channel, text, delete_after=8.0)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: Member):
        if not user:
            await ctx.message.reply(embed=Embed(title="No user! Error: MISSING USER MENTION", description=f">unmute {self.bot.user.mention}"))
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            await ctx.message.reply("You havent muted anyone before!")
        else:
            user.remove_roles(muted_role, reason=None)
            mbed = Embed(
                title="Unmuted",
                description=f"Now {user.mention} is unmuted!",
                color=Colour.random()
            )
            ctx.message.reply(embed=mbed, delete_after=8.0)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "You cannot do that! Sorry, {}".format(ctx.message.author)
            await self.bot.send_message(ctx.message.channel, text, delete_after=8.0)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=11):
        # syntax errors
        if not amount:
            await ctx.message.reply(embed=Embed(title="No amount! Error: MISSING AMOUNT", description=">purge **10**"))
            return

        if amount > 100:
            await ctx.message.reply("I cant remove more than 100 messages!")
            return
        else:
            await ctx.channel.purge(limit=amount)
            await ctx.message.reply(embed=Embed(
                title="Cleared!", description=f"Touched {amount} messages!", colour=Colour.random()
            ), delete_after=8.0)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "You cannot do that! Sorry, {}".format(ctx.message.author)
            await self.bot.send_message(ctx.message.channel, text, delete_after=8.0)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason: str = None):
        # syntax errors
        if not member:
            embed = Embed(title="Syntax error!", description="Who are you going to kick? ERROR: MISSING MEMBER MENTION",
                          color=Colour.random())
            embed.add_field(name="Correct syntax", value=">ban **@mention** reason")
            embed.add_field(name="Example of command", value=f">kick {self.bot.user.mention} Being dumbass")
            await ctx.message.reply(embed=embed)
            return

        mbed = Embed(
            title="Kicked!",
            description=f"Kicked {member.mention}, reason is {reason}",
            colour=Colour.random()
        )
        await member.send(f"Looks like you've got kicked from {ctx.guild.name}")
        await member.kick(reason=reason)
        await ctx.message.reply(embed=mbed, delete_after=8.0)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "You cannot do that! Sorry, {}".format(ctx.message.author)
            await self.bot.send_message(ctx.message.channel, text, delete_after=8.0)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, time, *, reason: str = None):
        # syntax errors

        if not member:
            embed = Embed(title="Syntax error!", description="Who are you going to ban? ERROR: MISSING MEMBER MENTION",
                          color=Colour.random())
            embed.add_field(name="Correct syntax", value=">ban **@mention** time reason")
            embed.add_field(name="Example of command", value=f">ban {self.bot.user.mention} 1d Innapropriate content")
            await ctx.message.reply(embed=embed)
            return
        if not time:
            embed = Embed(title="Syntax error!", description="I didnt understood what time. ERROR: MISSING BAN TIME",
                          color=Colour.random())
            embed.add_field(name="Time syntaxes", value="1s = 1 Second\n 1m = 1 Minute\n 1h = 1 Hour\n 1d = 1 Day")
            embed.add_field(name="Correct syntax", value=">ban @mention **time** reason")
            embed.add_field(name="Example of command", value=f">ban {self.bot.user.mention} 1d Innapropriate content")
            await ctx.message.reply(embed=embed)
            return


        if not time.endswith("s") or time.endswith("m") or time.endswith("h") or time.endswith("d"):

            embed = Embed(title="Syntax error!", description="Whats time of ban? ERROR: INCORRECT BAN TIME",
                          color=Colour.random())
            embed.add_field(name="Time syntaxes", value="1s = 1 Second\n 1m = 1 Minute\n 1h = 1 Hour\n 1d = 1 Day")
            embed.add_field(name="Correct syntax", value=">ban @mention time reason")
            embed.add_field(name="Example of command", value=f">ban {self.bot.user.mention} **1d** Innapropriate content")
            await ctx.message.reply(embed=embed)
            return


        # time desiring and banning (success)

        mbed = Embed(
            title="Banned!",
            description=f"Banned {member.mention}, reason is {reason}",
            colour=Colour.random()
        )
        time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        if time == "INFINITE":
            await member.send(
                f"Looks like you've got banned from {ctx.guild.name} reason: {reason}, time of ban **{time}**!")
            await member.ban(reason=reason)
            await ctx.message.reply(embed=mbed)
        else:
            await member.send(
                f"Looks like you've got banned from {ctx.guild.name} reason: {reason}, time of ban **{time}**!")
            await member.ban(reason=reason)
            await ctx.message.reply(embed=mbed)
            timeban = int(time[0]) * time_convert[time[-1]]
            await asyncio.sleep(timeban)
            await ctx.guild.unban(member)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "You cannot do that! Sorry, {}".format(ctx.message.author)
            await self.bot.send_message(ctx.message.channel, text, delete_after=8.0)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: Member):
        mbed = Embed(
            title="Unbanned!",
            description=f"Unbanned {member}!",
            colour=Colour.random()
        )
        banned = await ctx.guild.bans()
        name, discrim = member.split("#")
        for ban_entry in banned:
            user = ban_entry.user
            if (user.name, user.discriminator) == (name, discrim):
                await ctx.guild.unban(user)
                await ctx.message.reply(embed=mbed)

                return

    @unban.error
    async def unban(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "You cannot do that! Sorry, {}".format(ctx.message.author)
            await self.bot.send_message(ctx.message.channel, text, delete_after=8.0)


def setup(bot):
    bot.add_cog(Moderation(bot))
