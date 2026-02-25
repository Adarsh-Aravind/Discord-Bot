import discord
from discord.ext import commands

OWNER_ID = 615174036733034538

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def help(self, ctx):
        if ctx.author.id != OWNER_ID:
            return

        embed = discord.Embed(
            title="🤖 Bit Beast Bot Commands",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📊 Leveling",
            value="`!rank`\n`!levelreset @user`\n`!levelreset`",
            inline=False
        )

        embed.add_field(
            name="📩 Owner Commands",
            value="`!reply <user_id> <message>`\n"
                  "`!say <channel_id> <message>`\n"
                  "`!status <playing|watching|listening|competing> <text>`",
            inline=False
        )

        embed.add_field(
            name="⚡ Utility",
            value="`!ping`",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def status(self, ctx, activity_type: str, *, text: str):
        if ctx.author.id != OWNER_ID:
            return

        activity_type = activity_type.lower()

        if activity_type == "playing":
            activity = discord.Game(name=text)
        elif activity_type == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=text)
        elif activity_type == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=text)
        elif activity_type == "competing":
            activity = discord.Activity(type=discord.ActivityType.competing, name=text)
        else:
            await ctx.send("Invalid type.")
            return

        await self.bot.change_presence(activity=activity)
        await ctx.send("Status updated.")

async def setup(bot):
    await bot.add_cog(General(bot))