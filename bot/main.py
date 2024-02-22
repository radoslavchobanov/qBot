import discord
from discord.ext import commands
from dotenv import load_dotenv
import config

load_dotenv()

# Define intents
intents = discord.Intents.default()
intents.messages = True  # If you plan to listen to messages
intents.guilds = True  # If you need information about guilds (servers)
intents.message_content = True  # Enable privileged message content intent
intents.all()

bot = commands.Bot(command_prefix=config.BOT_PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    await bot.load_extension("music_cog")


bot.run(config.DISCORD_TOKEN)

# COMMENT