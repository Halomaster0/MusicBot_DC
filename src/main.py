import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading commands

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
    print('------')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
