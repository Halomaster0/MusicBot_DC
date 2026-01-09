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

### 1. Audio Issues (Opus/FFmpeg)
- **Opus**: The `libopus.dll` is included in this repository, so it should work out of the box.
- **FFmpeg**: If the bot sits in silence, ensure `ffmpeg` is installed and in your system PATH.
- **Logs**: Detailed information is written to `bot.log` in the root directory if any errors occur.

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
