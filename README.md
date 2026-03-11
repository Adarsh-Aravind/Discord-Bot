# Bit_Bot

**Bit_Bot** is a lightweight, fully-featured, and customizable Discord bot designed for server management, continuous user engagement, and real-time utilities. Built with `discord.py`, it features a modular cog-based architecture optimizing resource efficiency, making it perfect for personal deployment or small-to-medium server administration.

**Topics:** `discord-bot` `python` `f1-api` `discord-py` `anti-spam` `leveling-system` `youtube-notifications`

---

## Features

- **Automated Anti-Spam (Auto-Moderation)**: Actively monitors chat to restrict invite links, mass mentions, and excessive emojis, enforcing automatic timeouts and message deletion to preserve server integrity.
- **YouTube Notifications**: Integrates with YouTube to automatically announce new video uploads from monitored channels via customized, rich embeds.
- **Formula 1 Integration**: Fetches real-time driver and constructor standings, provides upcoming race schedules with official track layouts, and offers historical race information.
- **Automated Leveling System**: Features an SQLite-backed XP and leveling architecture to passively track user engagement, allowing users to rank up through active chat participation.
- **Direct Message (DM) Relay**: Automatically intercepts and forwards DMs sent to the bot directly to the configured bot owner.
- **Remote Channel Messaging**: Allows the bot owner to proxy messages to any server channel remotely or reply to specific users via direct DMs.
- **Modular Design**: Developed using `discord.py` Cogs for dynamic reloading, simple maintenance, and easy feature addition.

## Prerequisites

- Python 3.8+
- A valid Discord Bot Token from the [Discord Developer Portal](https://discord.com/developers/applications)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Adarsh-Aravind/Discord-Bot.git
   cd Bit_Bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   The bot utilizes `aiosqlite` for persistent storage (Leveling & YouTube history) and will automatically generate a localized `database.db` file upon its first successful boot.

## Configuration

1. Create a `.env` file in the root directory:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   ALLOWED_YT_CHANNEL=optional_discord_channel_id_for_yt_links
   ```
2. **Owner Verification**: The Owner ID is verified within `cogs/messaging.py` and `cogs/general.py`. Before deployment, ensure you replace `OWNER_ID = <your_id_here>` with your personal Discord User ID to utilize restricted commands.

## Usage

Start the bot locally or on your hosting environment:
```bash
python main.py
```

### Commands (Owner / Administrator)
*The default command prefix is `#`.*

| Command | Usage | Description |
| :--- | :--- | :--- |
| `#reply` | `#reply <user_id> <message>` | Prompts the bot to send a direct message to a targeted user. |
| `#say` | `#say <channel_id> <message>` | Prompts the bot to relay a message into a specified server channel. |
| `#setpresence` | `#setpresence <type> <text>` | Updates the bot's custom Discord activity status natively (e.g., Playing, Watching). |
| `#levelreset` | `#levelreset [user]` | Flushes a specific user's XP/level data, or completely truncates the leveling database if no target is specified. |

### Commands (Public)

| Command | Description |
| :--- | :--- |
| `#help` | Renders a custom, embedded help menu displaying public commands. |
| `#f1` | Outputs the current Formula 1 season snapshot (Top Drivers, Constructors, Next Race details). |
| `#f1next` | Yields detailed scheduling, location information, and an official layout map for the immediate upcoming F1 race. |
| `#f1last` | Provides comprehensive results and metrics for the most recently completed F1 race. |
| `#f1c {circuit}` | Queries a specific F1 circuit (e.g., "Miami") to fetch layout details, recent results, and historical data. |
| `#f1con` | Isolates and displays the current top 10 F1 constructor standings. |
| `#f1dri` | Isolates and displays the current top 10 F1 driver standings. |
| `#status` | Fetches and calculates basic diagnostic metrics regarding the host Discord server. |
| `#ping` | Evaluates and returns the bot's current API latency. |
| `#rank` | Displays an interactive embed of the user's localized XP and level progress. |

## Open Source & Contribution

This project is fully open-source. Feel free to fork, experiment, and implement your own custom Python Cogs for further utility.
