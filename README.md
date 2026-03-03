# Bit_Bot 📩🤖

Bit_Bot is a lightweight, personal messaging relay bot for Discord. It forwards all Direct Messages (DMs) to the bot owner and allows them to reply or speak in channels through the bot.

## Features ✨

*   **DM Forwarding**: Automatically forwards any DM sent to the bot to the owner.
*   **Reply System**: Reply to users directly via DM using the `!reply` command.
*   **Channel Speaking**: Send messages to any server channel using the `!say` command.
*   **Formula 1 Integration**: Real-time driver and constructor standings, upcoming race schedules with track layouts, and historical race information for specific circuits.
*   **Automated Leveling**: An integrated XP/level system for active chat members.
*   **YouTube Notifications**: Automatically annouces new videos uploaded by predefined channels with custom embeds.
*   **Lightweight**: Minimal dependencies, optimized for low-resource hosting.

## Prerequisites 🛠️

*   **Python 3.8+**

## Installation 📥

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Adarsh-Aravind/Discord-Bot.git
    cd Bit_Bot
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration ⚙️

1.  Create a `.env` file in the root directory:
    ```env
    DISCORD_TOKEN=your_discord_bot_token_here
    ```
2.  **Note**: The Owner ID is currently hardcoded in `cogs/messaging.py`. If you fork this, change `OWNER_ID` to your own Discord User ID.

## Usage 🚀

Run the bot:
```bash
python main.py
```

### Commands (Owner Only)

| Command | Usage | Description |
| :--- | :--- | :--- |
| `!reply` | `!reply <user_id> <message>` | Sends a DM to the specified user. |
| `!say` | `!say <channel_id> <message>` | Sends a message to the specified channel. |
| `!setpresence` | `!setpresence <type> <text>` | Changes the bot's custom activity status (e.g. playing, watching). |
| `!levelreset` | `!levelreset [user]` | Resets a specific user's level, or entirely resets the tracker if no user. |

### Commands (Public)

| Command | Description |
| :--- | :--- |
| `!help` | Displays the custom help menu with all available public commands. |
| `!f1` | Displays the complete F1 current season info (Drivers, Constructors, Next Race). |
| `!f1next` | Displays information and an official track layout picture for the upcoming race. |
| `!f1c {circuit}` | Searches for a specific circuit (e.g., "Miami") and displays info along with the previous winner. |
| `!f1con` | Displays only the top 10 constructor standings. |
| `!f1dri` | Displays only the top 10 driver standings. |
| `!status` | Displays basic metrics about the Discord server (members, roles, creation date). |
| `!ping` | Checks bot latency. |
| `!rank` | Shows the user's current level and XP. |

## License 📄

This project is open-source.
