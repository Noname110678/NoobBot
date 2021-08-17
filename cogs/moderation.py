import json
from asyncio.streams import StreamReader
import discord, asyncio
from discord import Embed, Colour, Member
from discord import colour
from discord.ext.commands import cog
from discord_slash import cog_ext, SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord.ext import commands



class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: Member, time, *, reason: str = None):
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="NoobBotPunishment")
        if not muted_role:
            muted_role = await guild.create_role(name="NoobBotPunishment")
            for channel in guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True,
                                              read_messages=True)
        await user.add_roles(muted_role, reason=reason)
        if time.endswith("s"):
            await asyncio.sleep(time.split("s")[0])
            await user.remove_roles(muted_role, reason=None)
            mebed = Embed(
                title="Unmuted",
                description=f"Now {user.mention} is unmuted!",
                color=Colour.random()
            )
            await ctx.send(embed=mebed)
        elif time.endswith("m"):
            await asyncio.sleep(time.split("m")[0] * 60)
            await user.remove_roles(muted_role, reason=None)
            mebed = Embed(
                title="Unmuted",
                description=f"Now {user.mention} is unmuted!",
                color=Colour.random()
            )
            await ctx.send(embed=mebed)
        elif time.endswith("h"):
            await asyncio.sleep(time.split("h")[0] * 3600)
            await user.remove_roles(muted_role, reason=None)
            mebed = Embed(
                title="Unmuted",
                description=f"Now {user.mention} is unmuted!",
                color=Colour.random()
            )
            await ctx.send(embed=mebed)
        mbed = Embed(
            title="Muted",
            description=f"{user.mention} is now muted!",
            color=Colour.random()
        )
        await ctx.send(embed=mbed)
        await user.send(f"Looks like you've got muted in {guild.name}!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            await ctx.send("You havent muted anyone before!")
        else:
            user.remove_roles(muted_role, reason=None)
            mbed = Embed(
                title="Unmuted",
                description=f"Now {user.mention} is unmuted!",
                color=Colour.random()
            )
            ctx.send(embed=mbed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=11):
        if amount > 100:
            await ctx.send("I cant remove more than 100 messages!")
        else:
            await ctx.channel.purge(limit=amount)
            await ctx.send(embed=Embed(
                title="Cleared!", description=f"Touched {amount} messages!", colour=Colour.random()
            ))

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason: str):
        mbed = Embed(
            title="Kicked!",
            description=f"Kicked {member.mention}, reason is {reason}",
            colour=Colour.random()
        )
        await member.send(f"Looks like you've got kicked from {ctx.guild.name}")
        await member.kick(reason=reason)
        await ctx.send(embed=mbed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, *, reason: str):
        mbed = Embed(
            title="Banned!",
            description=f"Banned {member.mention}, reason is {reason}",
            colour=Colour.random()
        )
        await member.ban(reason=reason)
        await ctx.send(embed=mbed)
        await member.send(f"Looks like you've got banned from {ctx.guild.name} OOF!")

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
                await ctx.send(embed=mbed)

                return




def setup(bot):
    bot.add_cog(Moderation(bot))
