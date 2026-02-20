import os
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bitbot')

# Load Environment Variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    logger.error("DISCORD_TOKEN not found in .env file")
    exit(1)

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True # Required for welcome messages

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    logger.info('------')
    
    # Load Cogs
    initial_extensions = ['cogs.general', 'cogs.music']
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            logger.info(f'Loaded extension: {extension}')
        except Exception as e:
            logger.error(f'Failed to load extension {extension}: {e}')

if __name__ == '__main__':
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Bot execution failed: {e}")
