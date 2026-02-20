# Bit_Bot 📩🤖

Bit_Bot is a lightweight, personal messaging relay bot for Discord. It forwards all Direct Messages (DMs) to the bot owner and allows them to reply or speak in channels through the bot.

## Features ✨

*   **DM Forwarding**: Automatically forwards any DM sent to the bot to the owner.
*   **Reply System**: Reply to users directly via DM using the `!reply` command.
*   **Channel Speaking**: Send messages to any server channel using the `!say` command.
*   **Lightweight**: Minimal dependencies, optimized for low-resource hosting (e.g., 308MB RAM).

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
| `!ping` | `!ping` | Checks bot latency. |

## License 📄

This project is open-source.
