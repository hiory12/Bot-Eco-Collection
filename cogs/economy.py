import discord
from discord import app_commands
from discord.ext import commands
import random
from modules.data_handler import DataManager

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_embed(self, title, description, color):
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(text="B2 Economic System")
        return embed

    # On utilise @app_commands.command au lieu de @commands.command
    @app_commands.command(name="work", description="Work to earn some coins")
    async def work(self, interaction: discord.Interaction):
        player = DataManager.get_player(interaction.user.id)
        
        earnings = random.randint(10, 100)
        player.money += earnings
        DataManager.save_player(player)
        
        embed = self.create_embed("🔨 Work Complete", f"You worked hard today!", discord.Color.green())
        embed.add_field(name="💰 Earnings", value=f"**+{earnings}** coins", inline=True)
        embed.add_field(name="🏦 Current Balance", value=f"**{player.money}** coins", inline=True)
        
        # On répond à l'interaction (plus de ctx.send)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="balance", description="Check your wallet balance")
    async def balance(self, interaction: discord.Interaction):
        player = DataManager.get_player(interaction.user.id)
        
        embed = self.create_embed(f"💳 Wallet of {interaction.user.name}", "", discord.Color.gold())
        embed.add_field(name="Available Balance", value=f"# **{player.money}** 🪙", inline=False)
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))