# Discord Music Bot

A personal-use Discord music bot built with Python, `discord.py`, and `yt-dlp`. This bot allows you to play audio from YouTube directly in your voice channels.

## Features
- Play music via YouTube URLs or search terms.
- Manage a music queue.
- Control playback (pause, resume, skip).
- Join and leave voice channels.

## Getting Started

### 1. Prerequisites
- **Python 3.8+**
- **FFmpeg**: Required for audio processing. See the [FFmpeg Setup](#ffmpeg-setup) section below.
- **Discord Bot Token**: Create one at the [Discord Developer Portal](https://discord.com/developers/applications).

### 2. Installation
To ensure all libraries are installed correctly in a private environment:
1. Double-click the `install_deps.bat` file in the root directory.
2. This will automatically create a virtual environment (`.venv`) and install all required modules like `discord.py` and `yt-dlp`.
3. Safe to run even if you don't have a C++ compiler.

### 3. Configuration
Open the `.env` file in the root directory and replace the placeholder with your actual Discord Bot Token:
```env
DISCORD_TOKEN=your_token_here
```

### 4. Running the Bot
You can run the bot in two ways:
- **With Console Visibility**: Double-click `run_bot.bat` in the root directory. This will keep a window open and show you what the bot is doing.
- **Hidden Mode**: Double-click `Start_MusicBot_Hidden.vbs`. This runs the bot in the background without a window.

## Available Commands

| Command | Alias | Description |
| :--- | :--- | :--- |
| `!play <query>` | `!p` | Plays a song from YouTube or adds it to the queue. |
| `!pause` | | Pauses/Resumes the current song. |
| `!resume` | `!r` | Resumes the current song. |
| `!skip` | `!s` | Skips the current song. |
| `!loop` | `!lp` | Toggles looping the current song. |
| `!loopqueue` | `!lq` | Toggles looping the entire queue. |
| `!queue` | `!q` | Shows the next 5 songs in the queue. |
| `!clear` | `!c` | Clears the queue and stops playback. |
| `!leave` | `!l` | Disconnects the bot from the voice channel. |

## Troubleshooting

### 1. Audio Issues (FFmpeg Setup) <a name="ffmpeg-setup"></a>
If the bot joins the channel but refuses to play audio, it's almost always because **FFmpeg** is missing.

**Easy Setup (Recommended):**
1. Go to [gyan.dev](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip) and download the FFmpeg essentials zip.
2. Open the zip file, go into the `bin` folder, and find `ffmpeg.exe`.
3. Drag and drop `ffmpeg.exe` directly into the **root folder** of this project (next to `run_bot.bat`).
4. Restart the bot. 
(I have also attached the dll for you to add to path if you would like to do this instead)
*Note: This works without adding FFmpeg to your system PATH. The included `libopus.dll` handles the rest!*

### 2. Stopping the Hidden Bot
If you are running the bot via the VBS script and need to stop it:
1. Open **Task Manager**.
2. Go to the **Details** tab.
3. Look for `pythonw.exe`. 
4. End the task. 
   - *Tip*: Enable the "Command line" column to verify it's running `src/main.py`.

---

> [!TIP]
> **Important Privacy/Legal Note**: This bot is intended for personal use in private servers. Audio is streamed directly and not stored or redistributed for profit.

> [!IMPORTANT]
> Ensure the **Message Content Intent** is enabled in your bot's configuration on the Discord Developer Portal.
