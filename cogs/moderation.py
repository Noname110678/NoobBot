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

    @cog_ext.cog_slash(description="Mutes people!", options=[
        create_option(name="user", description="User to mute", option_type=6, required=True),
        create_option(name="reason", description="Reason", option_type=3, required=False)
    ])
    async def mute(self, ctx, user: str, reason: str = None):
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")
        if not muted_role:
            muted_role = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True,
                                              read_messages=True)
        await user.add_roles(muted_role, reason=reason)
        mbed = Embed(
            title="Muted",
            description=f"Now {user.mention} is muted!",
            color=Colour.random()
        )
        await ctx.send(embed=mbed)
        await user.send(f"Looks like you've got muted in {guild.name}! Please ask owner to unmute you!")

    @cog_ext.cog_slash(description="Unmutes people!", options=[
        create_option(name="user", description="User to mute", option_type=6, required=True)
    ])
    async def unmute(self, ctx, user: str):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            await ctx.send("You havent muted anyone before!")
        else:
            user.remove_roles(muted_role, reason=None)
            mbed = Embed(
                title="Muted",
                description=f"Now {user.mention} is muted!",
                color=Colour.random()
            )
            ctx.send()

    @cog_ext.cog_slash(description="Clears some amount of messages", options=[
        create_option(name="amount", description="amount of messages you wanna delete", option_type=4, required=True)
    ])
    async def purge(self, ctx, amount=11):
        if amount > 500:
            await ctx.send("I cant remove more than 500 messages!")
        else:
            await ctx.channel.purge(limit=amount)
            await ctx.send(embed=Embed(
                title="Cleared!", description=f"Touched {amount} messages!", colour=Colour.random()
            ))

    @cog_ext.cog_slash(description="Kick a member", options=[
        create_option(name="member", description="Member to kick", option_type=6, required=True),
        create_option(name="reason", description="Reason of kicking", option_type=3, required=False)
    ])
    async def kick(self, ctx, member: str, reason: str):
        mbed = Embed(
            title="Kicked!",
            description=f"Kicked {member.mention}, reason is {reason}",
            colour=Colour.random()
        )
        await member.send(f"Looks like you've got kicked from {ctx.guild.name}")
        await member.kick(reason=reason)
        await ctx.send(embed=mbed)

    @cog_ext.cog_slash(description="Ban a member", options=[
        create_option(name="member", description="Member to ban", option_type=6, required=True),
        create_option(name="reason", description="Reason of banning", option_type=3, required=False)
    ])
    async def ban(self, ctx, member: str, reason: str):
        mbed = Embed(
            title="Banned!",
            description=f"Banned {member.mention}, reason is {reason}",
            colour=Colour.random()
        )
        await member.ban(reason=reason)
        await ctx.send(embed=mbed)
        await member.send(f"Looks like you've got banned from {ctx.guild.name} OOF!")

    @cog_ext.cog_slash(description="Unban a member", options=[
        create_option(name="member", description="Member to unban", option_type=3, required=True),
    ])
    async def unban(self, ctx, member: str):
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

    @cog_ext.cog_slash(description="Host some events in the server!", options=[
        create_option(name="title", description="How event will be called", option_type=3, required=True),
        create_option(name="description", description="Description", option_type=3, required=True),
        create_option(name="reaction", description="Reaction to see who is in!", option_type=3, required=False)
    ])
    async def event(self, ctx, title: str, description: str, reaction: str = "✅"):
        if ctx.author.has_guild_permissions(manage_messages=True):
            embed = Embed(
                title=title,
                description=description,
                color=Colour.random()
            )
            embed.set_footer(text=f"Hosted by {ctx.author}", icon_url=ctx.author.avatar_url)
            to_react = await ctx.send(embed=embed)
            await to_react.add_reaction(reaction)
        else:
            await ctx.send("You don't have permission in order of completing the command")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def event(self, ctx):
        title = ctx.message.content.split("<title>")[1]
        description = ctx.message.content.split("<description>")[1]
        embed = Embed(
            title=title,
            description=description,
            color=Colour.random()
        )
        embed.set_footer(text=f"Hosted by {ctx.author}", icon_url=ctx.author.avatar_url)
        to_react = await ctx.send(embed=embed)
        await to_react.add_reaction("✅")


def setup(bot):
    bot.add_cog(Moderation(bot))
