import discord
from discord.ext import commands
import random
import math

OWNER_ID = 615174036733034538


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        xp_gain = random.randint(5, 10)

        async with self.bot.db.execute(
            "SELECT xp, level FROM levels WHERE user_id = ?",
            (message.author.id,)
        ) as cursor:
            row = await cursor.fetchone()

        if row is None:
            xp = xp_gain
            level = 0
            await self.bot.db.execute(
                "INSERT INTO levels VALUES (?, ?, ?)",
                (message.author.id, xp, level)
            )
        else:
            xp, level = row
            xp += xp_gain

        new_level = int(math.sqrt(xp) // 10)

        # 🔥 Level Up Notification
        if new_level > level:
            level = new_level

            await message.channel.send(
                f"🎉 **{message.author.name}** has reached level **{level}**!"
            )

        await self.bot.db.execute(
            "UPDATE levels SET xp = ?, level = ? WHERE user_id = ?",
            (xp, level, message.author.id)
        )

        await self.bot.db.commit()

    @commands.command()
    async def rank(self, ctx):
        async with self.bot.db.execute(
            "SELECT xp, level FROM levels WHERE user_id = ?",
            (ctx.author.id,)
        ) as cursor:
            row = await cursor.fetchone()

        if not row:
            await ctx.send("No data yet.")
            return

        xp, level = row
        await ctx.send(f"Level: {level} | XP: {xp}")

    @commands.command()
    async def levelreset(self, ctx, user: discord.Member = None):
        if ctx.author.id != OWNER_ID:
            return

        if user:
            await self.bot.db.execute(
                "DELETE FROM levels WHERE user_id = ?",
                (user.id,)
            )
        else:
            await self.bot.db.execute("DELETE FROM levels")

        await self.bot.db.commit()
        await ctx.send("Levels reset.")


async def setup(bot):
    await bot.add_cog(Leveling(bot))