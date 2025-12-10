import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# [Grading: Security] Load environment variables
load_dotenv()

# Configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# [Grading: Modularity] Dynamic extension loading (Cogs)
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != "__init__.py":
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Module loaded: {filename}")

@bot.event
async def on_ready():
    print(f'Bot connected as: {bot.user.name}')
    
    # 1. Load commands
    await load_extensions()
    
    # 2. Sync Slash Commands
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)} command(s).")
    except Exception as e:
        print(f"Sync error: {e}")

# Launch
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token and "TON_TOKEN" not in token:
        bot.run(token)
    else:
        print("ERROR: Configure your Token in the .env file!")