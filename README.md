# Bit_Bot 🎵🤖

Bit_Bot is a feature-rich Discord bot designed to bring high-quality music playback and general utility commands to your server. Built with Python and `discord.py`, it supports YouTube, Spotify links, and custom welcome images.

## Features ✨

*   **Music Playback**:
    *   Play audio from YouTube videos and search queries.
    *   **Spotify Support**: seamlessly handles Spotify track, album, and playlist links by finding their YouTube equivalents.
    *   Queue management (add, view, skip).
    *   High-quality audio streaming using `yt-dlp` and `ffmpeg`.
*   **General Utilities**:
    *   `!ping`: Check bot latency.
    *   **Welcome System**: Automatically generates and sends a custom welcome image card when a new member joins.

## Prerequisites 🛠️

Before you begin, ensure you have the following installed:

1.  **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
2.  **FFmpeg**: Required for audio processing.
    *   **Windows**: [Download FFmpeg](https://ffmpeg.org/download.html), extract it, and add the `bin` folder to your System PATH.
    *   **Linux**: `sudo apt install ffmpeg`
    *   **Mac**: `brew install ffmpeg`

## Installation 📥

1.  **Clone the repository** (or download the source code):
    ```bash
    git clone https://github.com/yourusername/Bit_Bot.git
    cd Bit_Bot
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration ⚙️

1.  Create a file named `.env` in the root directory.
2.  Add your API keys and tokens in the following format:

    ```env
    DISCORD_TOKEN=your_discord_bot_token_here
    SPOTIFY_CLIENT_ID=your_spotify_client_id_here
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
    ```

    > **Note**: To get Spotify credentials, go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and create an app.

## Usage 🚀

Run the bot using:

```bash
python main.py
```

### Commands

| Command | Description |
| :--- | :--- |
| `!play <url/query>` | Plays a song from YouTube or Spotify. |
| `!skip` | Skips the current song. |
| `!queue` | Shows the current music queue. |
| `!stop` | Stops playback and clears the queue. |
| `!join` | Joins your voice channel. |
| `!ping` | Checks if the bot is responsive. |

## Contributing 🤝

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License 📄

This project is open-source and available under the content of the repository.
