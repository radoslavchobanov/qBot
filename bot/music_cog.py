from discord.ext import commands
import discord
import yt_dlp

# Suppress noise about console usage from errors
yt_dlp.utils.bug_reports_message = lambda: ""


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:  # Ensuring the queue is not empty
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)  # Now it's safe to pop
        else:
            await ctx.send("The song queue is currently empty.")

    async def play_song(self, ctx, song):
        try:
            url = song["source"]

            ctx.voice_client.play(
                discord.FFmpegPCMAudio(url, options="-vn"),
                after=lambda e: self.bot.loop.create_task(self.check_queue(ctx)),
            )
            ctx.voice_client.is_playing()

            await ctx.send(f'Now playing: {song["title"]}')
        except Exception as e:
            await ctx.send("An error occurred while processing this request.")
            print(f"Error playing song: {e}")

    @commands.command(name="join", help="Tells the bot to join the voice channel")
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return

        channel = ctx.message.author.voice.channel

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(name="play", help="Plays a selected song from YouTube")
    async def play(self, ctx, *, url):
        if not ctx.voice_client:
            await ctx.invoke(self.join)

        # Define ydl_opts with your desired options
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "default_search": "ytsearch",
            "extractaudio": True,  # Only keep the audio
            "noplaylist": True,  # Only download a single song, not a playlist
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                song = {"source": info["formats"][0]["url"], "title": info["title"]}
                self.song_queue[ctx.guild.id].append(song)
                await ctx.send(f'Added {song["title"]} to the queue.')
            except Exception as e:
                await ctx.send("An error occurred while processing this request.")
                print(f"Error extracting video info: {e}")

        if not ctx.voice_client.is_playing():
            if self.song_queue[ctx.guild.id]:  # Check if the queue is not empty
                await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
                self.song_queue[ctx.guild.id].pop(0)
            else:
                await ctx.send("The queue is currently empty.")

    @commands.command(
        name="leave", help="Clears the song queue and leaves the voice channel"
    )
    async def leave(self, ctx):
        self.song_queue[ctx.guild.id] = []
        await ctx.voice_client.disconnect()

    @commands.command(name="queue", help="Shows the current song queue")
    async def queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) == 0:
            await ctx.send("The queue is currently empty.")
        else:
            queue_str = "\n".join(
                [song["title"] for song in self.song_queue[ctx.guild.id]]
            )
            await ctx.send(f"Current queue:\n{queue_str}")

    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await self.check_queue(ctx)


async def setup(bot):
    print("Bot Setup!")
    await bot.add_cog(Music(bot))
