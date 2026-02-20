import discord
from discord.ext import commands
import logging
from utils.image_gen import create_welcome_card

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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel:
            try:
                buffer = create_welcome_card(member)
                file = discord.File(buffer, filename="welcome.png")
                await channel.send(f"Welcome {member.mention} to the server!", file=file)
                self.logger.info(f"Sent welcome message for {member.name}")
            except Exception as e:
                self.logger.error(f"Failed to send welcome message: {e}")
        else:
             self.logger.warning(f"System channel not found for guild {member.guild.name}")

async def setup(bot):
    await bot.add_cog(General(bot))
