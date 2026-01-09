import discord
import os
import asyncio
import logging
from discord.ext import commands
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    handlers=[
        logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('discord_bot')

# Handle environment variables
root_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
src_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

if os.path.exists(root_env):
    load_dotenv(root_env)
    logger.info(f"Loaded .env from root: {root_env}")
elif os.path.exists(src_env):
    load_dotenv(src_env)
    logger.info(f"Loaded .env from src: {src_env}")
else:
    logger.warning("No .env file found in root or src directories.")

TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN or TOKEN.strip() == "" or TOKEN == "your_token_here":
    print("\n" + "="*60)
    print(" CRITICAL ERROR: DISCORD_TOKEN NOT FOUND")
    print("="*60)
    print(f"I looked for a .env file here: {root_env}")
    print("\nPlease ensure:")
    print("1. You have a file named exactly '.env' (not '.env.txt')")
    print("2. It contains: DISCORD_TOKEN=your_actual_token_here")
    print("="*60)
    input("\nPress Enter to exit...")
    exit()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True # Explicitly ensure voice states are enabled

# Initialize Bot
bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    """Load the music cog."""
    try:
        await bot.load_extension('music_cog')
    except Exception as e:
        logger.error(f"Failed to load music cog: {e}")

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    logger.info(f'Discord.py Version: {discord.__version__}')
    
    # Ensure Opus is loaded for voice support
    if not discord.opus.is_loaded():
        logger.info("Opus not loaded. Searching for library...")
        try:
            import ctypes.util
            # Search in common locations and also the root directory of the project
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            local_paths = [
                os.path.join(root_dir, 'libopus.dll'),
                os.path.join(root_dir, 'opus.dll'),
                os.path.join(os.path.dirname(__file__), 'libopus.dll'),
                os.path.join(os.path.dirname(__file__), 'opus.dll'),
                'C:\\Windows\\System32\\opus.dll',
                'C:\\Windows\\System32\\libopus.dll',
            ]
            
            for path in local_paths:
                if os.path.exists(path):
                    try:
                        discord.opus.load_opus(path)
                        if discord.opus.is_loaded():
                            logger.info(f"Found and loaded Opus at: {path}")
                            break
                    except Exception as e:
                        logger.error(f"Attempted {path} but failed: {e}")
            
            if not discord.opus.is_loaded():
                for name in ['libopus-0', 'libopus', 'opus']:
                    system_path = ctypes.util.find_library(name)
                    if system_path:
                        try:
                            discord.opus.load_opus(system_path)
                            if discord.opus.is_loaded():
                                logger.info(f"Found and loaded system library: {name}")
                                break
                        except Exception as e:
                            logger.error(f"Attempted system {name} but failed: {e}")
        except Exception as e:
            logger.critical(f"Serious error during Opus search: {e}")

    if discord.opus.is_loaded():
        logger.info("Music Bot is ready!")
    else:
        logger.critical("Opus library NOT loaded.")

@bot.event
async def on_command_error(ctx, error):
    """Global error handler for commands."""
    print(f"COMMAND ERROR: {error}")
    if isinstance(error, commands.CommandNotFound):
        return # Ignore unknown commands
    await ctx.send(f"An error occurred: {error}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
