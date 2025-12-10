import discord
from discord.ext import commands
import random
from modules.data_handler import DataManager

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_embed(self, title, description, color):
        """Utility function to create uniform embeds"""
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(text="B2 Economic System")
        return embed

    @commands.command()
    async def work(self, ctx):
        player = DataManager.get_player(ctx.author.id)
        
        # Calculate earnings
        earnings = random.randint(10, 100)
        player.money += earnings
        DataManager.save_player(player)
        
        # [Pro UI] Green Embed (Success)
        embed = self.create_embed("🔨 Work Complete", f"You worked hard today!", discord.Color.green())
        embed.add_field(name="💰 Earnings", value=f"**+{earnings}** coins", inline=True)
        embed.add_field(name="🏦 Current Balance", value=f"**{player.money}** coins", inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name="balance", aliases=["solde"]) # 'aliases' allows !solde to still work
    async def balance(self, ctx):
        player = DataManager.get_player(ctx.author.id)
        
        # [Pro UI] "Credit Card" style Embed
        embed = self.create_embed(f"💳 Wallet of {ctx.author.name}", "", discord.Color.gold())
        embed.add_field(name="Available Balance", value=f"# **{player.money}** 🪙", inline=False)
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))