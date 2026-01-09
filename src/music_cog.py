import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os
import logging

logger = logging.getLogger('discord_bot.music')

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.is_playing = False
        self.is_paused = False
        self.is_looping = False
        self.is_loopqueue = False
        self.current_song = None
        self.vc = None

        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'noplaylist': 'True',
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            # 'source_address': '0.0.0.0' # Commented out as it can cause issues on some Windows network stacks
        }

        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Monitor voice state changes for the bot."""
        if member.id == self.bot.user.id:
            if before.channel is not None and after.channel is None:
                logger.info(f"Bot was disconnected from {before.channel.name}")
                self.vc = None
                self.is_playing = False

    async def update_presence(self, song):
        if song:
            activity = discord.Activity(
                type=discord.ActivityType.listening,
                name=song[0]['title'],
                details="Enjoying some music",
                state=f"Queue: {len(self.queue)} songs"
            )
            await self.bot.change_presence(activity=activity)
        else:
            await self.bot.change_presence(activity=None)

    def search_yt(self, item):
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(item, download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                return {'source': info['url'], 'title': info['title']}
            except Exception:
                return False

    def play_next(self, error=None):
        if self.vc is None or not self.vc.is_connected():
            logger.warning("play_next called but VC is disconnected or None.")
            self.is_playing = False
            return

        if self.is_looping and self.current_song:
            self.is_playing = True
            m_url = self.current_song[0]['source']
            try:
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(e))
            except Exception:
                self.is_playing = False
        elif len(self.queue) > 0:
            self.is_playing = True
            self.current_song = self.queue.pop(0)
            m_url = self.current_song[0]['source']
            
            if self.is_loopqueue:
                self.queue.append(self.current_song)
            
            try:
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(e))
                self.bot.loop.create_task(self.update_presence(self.current_song))
            except Exception:
                self.is_playing = False
        else:
            self.is_playing = False
            self.current_song = None
            self.bot.loop.create_task(self.update_presence(None))

    async def play_music(self, ctx):
        if len(self.queue) > 0:
            self.is_playing = True
            self.current_song = self.queue.pop(0)
            m_url = self.current_song[0]['source']
            target_vc = self.current_song[1]
            
            if self.is_loopqueue:
                self.queue.append(self.current_song)

            # --- Connection Logic ---
            # Explicitly cleanup any old connection state before starting a new one
            if self.vc:
                logger.info("Cleaning up existing voice connection state.")
                try:
                    await self.vc.disconnect(force=True)
                    await asyncio.sleep(1) 
                except Exception as e:
                    logger.debug(f"Cleanup error (ignoring): {e}")
                self.vc = None
            logger.info(f"Connecting to voice channel: {target_vc.name}")
            try:
                # Use a smaller timeout for the initial call, as discord.py will handle retries internally if reconnect=True
                self.vc = await target_vc.connect(timeout=20, reconnect=True, self_deaf=True)
                logger.info(f"Connected to {target_vc.name}")
            except Exception as e:
                logger.error(f"Connection failed: {e}")
                await ctx.send(f"Failed to connect to voice: {e}")
                self.is_playing = False
                return

            if not self.vc or not self.vc.is_connected():
                await ctx.send("Could not establish a stable voice connection.")
                self.is_playing = False
                return

            # --- FFmpeg Verification ---
            import shutil
            ffmpeg_path = shutil.which("ffmpeg")
            if not ffmpeg_path:
                # Try finding it in the project root if not in PATH
                root_ffmpeg = os.path.join(os.getcwd(), "ffmpeg.exe")
                if os.path.exists(root_ffmpeg):
                    ffmpeg_path = root_ffmpeg
                else:
                    await ctx.send("CRITICAL ERROR: `ffmpeg` not found. Please install FFmpeg and add it to your PATH.")
                    self.is_playing = False
                    return

            # --- Playback ---
            logger.info(f"Playing: {self.current_song[0]['title']}")
            try:
                self.vc.play(discord.FFmpegPCMAudio(m_url, executable=ffmpeg_path, **self.FFMPEG_OPTIONS), 
                             after=lambda e: self.play_next(e))
                await self.update_presence(self.current_song)
            except Exception as e:
                logger.error(f"Playback error: {e}")
                await ctx.send(f"Error during playback setup: {e}")
                self.is_playing = False
        else:
            self.is_playing = False
            self.current_song = None
            await self.update_presence(None)

    @commands.command(name="play", aliases=["p", "playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            if self.vc and self.vc.is_connected():
                self.vc.resume()
                self.is_paused = False
                self.is_playing = True
            else:
                await ctx.send("Lost voice connection. Re-adding song.")
                self.is_paused = False
                self.is_playing = False
        else:
            song = self.search_yt(query)
            if type(song) == bool:
                await ctx.send("Could not find the song.")
            else:
                await ctx.send(f"Song added to the queue: **{song['title']}**")
                self.queue.append([song, voice_channel])
                
                if not self.is_playing:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.vc and self.vc.is_playing():
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await ctx.send("Paused.")
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            await ctx.send("Resumed.")

    @commands.command(name="resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        if self.vc and self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            await ctx.send("Resumed.")

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc is not None and self.vc.is_connected():
            self.is_looping = False
            self.vc.stop()
            
    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.queue)):
            if i > 4: break
            retval += f"{i+1}. {self.queue[i][0]['title']}\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        if self.vc is not None and self.vc.is_connected():
            self.vc.stop()
        self.queue = []
        self.current_song = None
        self.is_playing = False
        self.is_paused = False
        self.is_looping = False
        self.is_loopqueue = False
        await self.update_presence(None)
        await ctx.send("Music queue cleared")

    @commands.command(name="stop", aliases=["st"], help="Stops the music and disconnects")
    async def stop(self, ctx):
        self.is_playing = False
        self.is_paused = False
        self.is_looping = False
        self.is_loopqueue = False
        if self.vc:
            await self.vc.disconnect()
            self.vc = None
        self.queue = []
        self.current_song = None
        await self.update_presence(None)
        await ctx.send("Stopped and disconnected.")

    @commands.command(name="leave", aliases=["l", "disconnect"], help="Kick the bot from VC")
    async def leave(self, ctx):
        await self.stop(ctx)

    @commands.command(name="loop", aliases=["lp"], help="Toggles looping the current song")
    async def loop(self, ctx):
        if self.vc is not None and self.vc.is_connected():
            self.is_looping = not self.is_looping
            status = "enabled" if self.is_looping else "disabled"
            await ctx.send(f"Looping {status}")
        else:
            await ctx.send("No music is currently playing")

    @commands.command(name="loopqueue", aliases=["lq"], help="Toggles looping the entire queue")
    async def loopqueue(self, ctx):
        if self.vc is not None and self.vc.is_connected():
            self.is_loopqueue = not self.is_loopqueue
            status = "enabled" if self.is_loopqueue else "disabled"
            await ctx.send(f"Looping queue {status}")
        else:
            await ctx.send("No music is currently playing")

async def setup(bot):
    await bot.add_cog(MusicCog(bot))
