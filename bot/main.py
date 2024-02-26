import discord
from discord.ext import commands
from dotenv import load_dotenv
import config

load_dotenv()

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.all()

bot = commands.Bot(command_prefix=config.BOT_PREFIX, intents=intents, help_command=None)


@bot.event
async def on_ready():
    await bot.load_extension("music_cog")
    await bot.load_extension("crypto_cog")


bot.run(config.DISCORD_TOKEN)
