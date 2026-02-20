import discord
from discord.ext import commands
import logging

# Hardcoded Owner ID as requested
OWNER_ID = 615174036733034538

class Messaging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bitbot')

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Messaging Cog loaded.')

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore own messages
        if message.author == self.bot.user:
            return

        # Check for DMs
        if isinstance(message.channel, discord.DMChannel):
            # Forward to Owner
            owner = self.bot.get_user(OWNER_ID)
            if owner:
                embed = discord.Embed(
                    title=f"📩 DM from {message.author}",
                    description=message.content,
                    color=discord.Color.gold()
                )
                embed.set_footer(text=f"User ID: {message.author.id}")
                
                # Handle attachments
                if message.attachments:
                    embed.add_field(name="Attachments", value="\n".join([a.url for a in message.attachments]))
                
                await owner.send(embed=embed)
            else:
                self.logger.error(f"Could not find owner with ID {OWNER_ID} to forward DM.")

    @commands.command(name='reply')
    async def reply(self, ctx, user_id: int, *, content):
        """Replies to a user via DM. Usage: !reply <user_id> <message>"""
        if ctx.author.id != OWNER_ID:
            return # Silent fail for unauthorized users

        user = self.bot.get_user(user_id)
        if not user:
            try:
                user = await self.bot.fetch_user(user_id)
            except Exception as e:
                await ctx.send(f"❌ Could not find user: {e}")
                return

        try:
            await user.send(content)
            await ctx.send(f"✅ Sent to **{user.name}** ({user.id}): {content}")
        except discord.Forbidden:
            await ctx.send("❌ Failed to send DM. User might have DMs blocked.")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name='say')
    async def say(self, ctx, channel_id: int, *, content):
        """Sends a message to a channel. Usage: !say <channel_id> <message>"""
        if ctx.author.id != OWNER_ID:
            return

        channel = self.bot.get_channel(channel_id)
        if not channel:
            try:
                channel = await self.bot.fetch_channel(channel_id)
            except Exception as e:
                await ctx.send(f"❌ Could not find channel: {e}")
                return

        try:
            if isinstance(channel, (discord.TextChannel, discord.VoiceChannel, discord.StageChannel)):
                await channel.send(content)
                await ctx.send(f"✅ Sent to **#{channel.name}**")
            else:
                await ctx.send("❌ Target is not a textable channel.")
        except discord.Forbidden:
            await ctx.send("❌ Missing permissions to speak in that channel.")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

async def setup(bot):
    await bot.add_cog(Messaging(bot))
