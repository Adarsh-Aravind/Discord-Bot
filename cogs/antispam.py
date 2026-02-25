import discord
from discord.ext import commands
import re
import datetime

INVITE_PATTERN = re.compile(r"(discord\.gg/|discord\.com/invite/)")
YOUTUBE_PATTERN = re.compile(r"(youtube\.com|youtu\.be)")
CUSTOM_EMOJI_PATTERN = re.compile(r"<a?:\w+:\d+>")
UNICODE_EMOJI_PATTERN = re.compile(
    r"[\U0001F600-\U0001F64F"  # emoticons
    r"\U0001F300-\U0001F5FF"  # symbols & pictographs
    r"\U0001F680-\U0001F6FF"  # transport & map
    r"\U0001F1E0-\U0001F1FF]+",  # flags
    flags=re.UNICODE
)

ALLOWED_YT_CHANNEL = 764832907260198965
MAX_USER_MENTIONS = 4
MAX_EMOJIS = 8
TIMEOUT_DURATION = 5  # minutes
WARNING_DELETE_AFTER = 30  # seconds


class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # -------------------------
        # Block @everyone / @here
        # -------------------------
        if message.mention_everyone:
            await self.punish(message, "Mass mention (@*everyone / @*here) is not allowed")
            return

        # -------------------------
        # Block mass user mentions
        # -------------------------
        if len(message.mentions) > MAX_USER_MENTIONS:
            await self.punish(message, "Mass user mentions are not allowed")
            return

        # -------------------------
        # Block invite links
        # -------------------------
        if INVITE_PATTERN.search(message.content):
            await self.punish(message, "Discord invite links are not allowed")
            return

        # -------------------------
        # Restrict YouTube links
        # -------------------------
        if YOUTUBE_PATTERN.search(message.content):
            if message.channel.id != ALLOWED_YT_CHANNEL:
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention} YouTube links are only allowed in the designated channel.",
                    delete_after=WARNING_DELETE_AFTER
                )
                return

        # -------------------------
        # Block mass emoji spam
        # -------------------------
        emoji_count = 0
        emoji_count += len(CUSTOM_EMOJI_PATTERN.findall(message.content))
        emoji_count += len(UNICODE_EMOJI_PATTERN.findall(message.content))

        if emoji_count > MAX_EMOJIS:
            await self.punish(message, "Mass emoji spam is not allowed")
            return

    async def punish(self, message, reason):
        # Delete violation message
        try:
            await message.delete()
        except Exception:
            pass

        # Timeout user
        try:
            await message.author.timeout(
                datetime.timedelta(minutes=TIMEOUT_DURATION),
                reason=reason
            )
        except Exception:
            pass

        # Send warning message (auto delete)
        try:
            await message.channel.send(
                f"{message.author.mention} ⚠ {reason}. "
                f"You have been timed out for {TIMEOUT_DURATION} minutes.",
                delete_after=WARNING_DELETE_AFTER
            )
        except Exception:
            pass


async def setup(bot):
    await bot.add_cog(AntiSpam(bot))