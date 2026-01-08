import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from the root directory
# This works whether you run from root or from /src
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN or TOKEN == "your_token_here":
    print("ERROR: DISCORD_TOKEN not found in .env file or is still set to placeholder.")
    print("Please update the .env file with your actual bot token.")
    input("Press Enter to exit...") # Keeps window open for the user
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
        # Note: 'music_cog' refers to music_cog.py in the same directory
        await bot.load_extension('music_cog')
        print("Music cog loaded successfully.")
    except Exception as e:
        print(f"Failed to load music cog: {e}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    
    # Ensure Opus is loaded for voice support
    if not discord.opus.is_loaded():
        try:
            import ctypes.util
            opus_path = ctypes.util.find_library('libopus')
            if opus_path:
                discord.opus.load_opus(opus_path)
            else:
                for name in ['libopus-0', 'libopus', 'opus']:
                    try:
                        discord.opus.load_opus(name)
                        break
                    except:
                        continue
        except:
            pass

    if discord.opus.is_loaded():
        print("Music Bot is ready!")
    else:
        print("WARNING: Opus library not loaded. Voice features may not work.")
    print('------')

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
