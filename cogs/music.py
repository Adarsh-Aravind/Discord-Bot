import discord
from discord.ext import commands
import yt_dlp
import asyncio
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        
        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'best',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                data = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=not stream))

            if 'entries' in data:
                # take first item from a playlist
                data = data['entries'][0]

            filename = data['url'] if stream else ydl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, options='-vn'), data=data)
        
        except Exception as e:
            logging.error(f"Error extracting audio from {url}: {e}")
            raise e

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        
        # Setup Spotify Client
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if client_id and client_secret:
            try:
                self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
                print("Spotify integration enabled.")
            except Exception as e:
                print(f"Failed to initialize Spotify: {e}")
                self.sp = None
        else:
            print("Spotify credentials missing in .env. Spotify support disabled.")
            self.sp = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Music Cog loaded.')

    def _get_spotify_tracks(self, url):
        """Resolves Spotify URL to a list of search queries (Artist - Title)"""
        if not self.sp:
            return []
            
        tracks = []
        try:
            if 'track' in url:
                track = self.sp.track(url)
                tracks.append(f"{track['artists'][0]['name']} - {track['name']}")
            elif 'playlist' in url:
                results = self.sp.playlist_items(url)
                for item in results['items']:
                    track = item['track']
                    if track:
                        tracks.append(f"{track['artists'][0]['name']} - {track['name']}")
            elif 'album' in url:
                 results = self.sp.album_tracks(url)
                 for item in results['items']:
                     tracks.append(f"{item['artists'][0]['name']} - {item['name']}")
        except Exception as e:
            print(f"Spotify lookup failed: {e}")
            
        return tracks

    @commands.command(name='join', help='Joins a voice channel')
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return False
        
        channel = ctx.message.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
            return True
        
        await channel.connect()
        return True

    @commands.command(name='play', help='Plays a song')
    async def play(self, ctx, *, url):
        async with ctx.typing():
            try:
                if not ctx.voice_client:
                    success = await self.join(ctx)
                    if not success:
                        return
                
                search_queries = []
                
                # Check for Spotify Link
                if 'spotify.com' in url:
                    if not self.sp:
                        await ctx.send("Spotify support is not enabled on this bot.")
                        return
                    
                    await ctx.send("🔎 **Spotify detected!** Fetching tracks...")
                    search_queries = await self.bot.loop.run_in_executor(None, self._get_spotify_tracks, url)
                    
                    if not search_queries:
                        await ctx.send("Could not find any tracks from that Spotify link.")
                        return
                        
                    await ctx.send(f"Found {len(search_queries)} track(s). Queuing them up!")
                else:
                    # Treat as standard YouTube link/search
                    search_queries = [url]

                # Process all queries (1 for normal, N for Spotify playlist)
                for i, query in enumerate(search_queries):
                    # For playlists, only announce the first one immediately to avoid spam
                    # or if it's the only song
                    
                    player = await YTDLSource.from_url(query, loop=self.bot.loop, stream=True)
                    
                    if ctx.voice_client.is_playing() or i > 0:
                        self.queue.append(player)
                        if i == 0: # Only confirm the first add to avoid spam for playlists
                            await ctx.send(f'Added to queue: **{player.title}**')
                    else:
                        ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))
                        await ctx.send(f'Now playing: **{player.title}**')
                        
            except Exception as e:
                import traceback
                traceback.print_exc()
                await ctx.send(f"An error occurred: {e}")

    def play_next(self, ctx):
        if len(self.queue) > 0:
            player = self.queue.pop(0)
            ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))
            asyncio.run_coroutine_threadsafe(ctx.send(f'Now playing: **{player.title}**'), self.bot.loop)
        else:
            # Optionally disconnect or just wait
            pass

    @commands.command(name='queue', help='Shows the current queue')
    async def queue(self, ctx):
        if len(self.queue) == 0:
            await ctx.send("Queue is empty.")
        else:
            # Show top 10 only to avoid huge messages
            queue_list = "\n".join([f"{i+1}. {song.title}" for i, song in enumerate(self.queue[:10])])
            remaining = len(self.queue) - 10
            msg = f"**Queue:**\n{queue_list}"
            if remaining > 0:
                msg += f"\n...and {remaining} more."
            await ctx.send(msg)

    @commands.command(name='skip', help='Skips the current song')
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped!")

    @commands.command(name='stop', help='Stops and disconnects')
    async def stop(self, ctx):
        if ctx.voice_client:
            self.queue.clear()
            await ctx.voice_client.disconnect()
            await ctx.send("Stopped and disconnected.")

async def setup(bot):
    await bot.add_cog(Music(bot))
