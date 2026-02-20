import discord
from discord.ext import commands
import logging


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bitbot')

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'General Cog loaded.')

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send(f'Pong! Latency: {round(self.bot.latency * 1000)}ms')



async def setup(bot):
    await bot.add_cog(General(bot))
