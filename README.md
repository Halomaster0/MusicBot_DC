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
- **FFmpeg**: Must be installed and added to your system's PATH.
- **Discord Bot Token**: Create one at the [Discord Developer Portal](https://discord.com/developers/applications).

### 2. Installation
Run the following command to install the required libraries:
```powershell
pip install -r requirements.txt
```

### 3. Configuration
Open the `.env` file in the root directory and replace the placeholder with your actual Discord Bot Token:
```env
DISCORD_TOKEN=your_token_here
```

### 4. Running the Bot
Navigate to the `src` directory and run the main script:
```powershell
cd src
python main.py
```

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

## Troubleshooting & Advanced Setup

### 1. Fix: Opus Not Loaded (No Audio)
If the bot joins but doesn't play audio, it's because Windows can't find the **Opus** library.
1.  Download `libopus.dll` (64-bit) from a trusted source like [this direct link](https://github.com/GyanD/codexffmpeg/raw/master/builds/ffmpeg-git-full.7z) (extract it from the `bin` folder) or search for "libopus.dll download".
2.  Place `libopus.dll` directly into the `src` folder of this project.
3.  Restart the bot. It should now say `Opus: Loaded`.

### 2. Running in the Background (No Window)
If you want the bot to stay active without a terminal window open:
1.  Ensure your `.env` token is set and the bot works normally.
2.  Double-click the `run_hidden.vbs` file in the root directory.
3.  The bot will start silently. To stop it, use the **Task Manager** to end the "Python" or "pythonw.exe" task.

---

> [!TIP]
> **Important Privacy/Legal Note**: This bot is intended for personal use in private servers. Audio is streamed directly and not stored or redistributed for profit.

> [!IMPORTANT]
> Ensure the **Message Content Intent** is enabled in your bot's configuration on the Discord Developer Portal.
