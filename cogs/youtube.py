import discord
from discord.ext import commands, tasks
import feedparser

import os

CHANNELS = {
    "UCWOMTp0BLi41FTn6ouh_mdg": int(os.getenv("YT_CHANNEL_1", 0)),
    "UCCYq8CHiJR3Y8IEME0SgNUQ": int(os.getenv("YT_CHANNEL_2", 0)),
    "UCKK4jwSOaKBSTqQjNRbndng": int(os.getenv("YT_CHANNEL_3", 0))
}

class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check.start()

    def cog_unload(self):
        self.check.cancel()

    @tasks.loop(minutes=5)
    async def check(self):
        for yt_id, discord_channel_id in CHANNELS.items():
            channel = self.bot.get_channel(discord_channel_id)
            if not channel:
                continue

            feed = feedparser.parse(
                f"https://www.youtube.com/feeds/videos.xml?channel_id={yt_id}"
            )

            if not feed.entries:
                continue

            latest_entry = feed.entries[0]
            video_id = latest_entry.get("yt_videoid")

            async with self.bot.db.execute(
                "SELECT last_video FROM youtube WHERE channel_id = ?",
                (yt_id,)
            ) as cursor:
                row = await cursor.fetchone()

            if row is None:
                await self.bot.db.execute(
                    "INSERT INTO youtube VALUES (?, ?)",
                    (yt_id, video_id)
                )
                await self.bot.db.commit()
                continue

            if row[0] != video_id:
                await self.bot.db.execute(
                    "UPDATE youtube SET last_video = ? WHERE channel_id = ?",
                    (video_id, yt_id)
                )
                await self.bot.db.commit()

                embed = discord.Embed(
                    title=f"🎥 {latest_entry.author} just posted a video! Go check it out!",
                    description=f"**[{latest_entry.title}](https://www.youtube.com/watch?v={video_id})**",
                    color=discord.Color.red()
                )
                embed.set_image(url=f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg")

                await channel.send(content="Hey! @everyone", embed=embed)

    @check.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(YouTube(bot))