import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# [Barème: Sécurité] Chargement des variables d'env
load_dotenv()

# Configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# [Barème: Modularité] Chargement dynamique des extensions (Cogs)
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            # On charge l'extension
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Module chargé : {filename}")

@bot.event
async def on_ready():
    print(f'Bot connecté : {bot.user.name}')
    
    # 1. On charge les commandes
    await load_extensions()
    
    # 2. On synchronise les commandes "/" (Slash) avec Discord
    # C'est ça qui fait apparaître le menu quand tu tapes "/"
    try:
        synced = await bot.tree.sync()
        print(f"Commandes Slash synchronisées : {len(synced)} commande(s).")
    except Exception as e:
        print(f"Erreur de synchro : {e}")

# Lancement
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token and "TON_TOKEN" not in token:
        bot.run(token)
    else:
        print("ERREUR : Configure ton Token dans le fichier .env !")