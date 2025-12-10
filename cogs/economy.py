import discord
from discord.ext import commands
import random
from modules.data_handler import DataManager

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_embed(self, title, description, color):
        """Fonction utilitaire pour créer des embeds uniformes"""
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(text="Système Économique B2")
        return embed

    @commands.command()
    async def work(self, ctx):
        joueur = DataManager.get_joueur(ctx.author.id)
        
        # Calcul du gain
        gain = random.randint(10, 100)
        joueur.argent += gain
        DataManager.save_joueur(joueur)
        
        # [UI Pro] Utilisation d'un Embed vert (Succès) avec mise en forme
        embed = self.create_embed("🔨 Travail Terminé", f"Tu as travaillé dur aujourd'hui !", discord.Color.green())
        embed.add_field(name="💰 Gain", value=f"**+{gain}** pièces", inline=True)
        embed.add_field(name="🏦 Solde Actuel", value=f"**{joueur.argent}** pièces", inline=True)
        
        await ctx.send(embed=embed)

    @commands.command()
    async def solde(self, ctx):
        joueur = DataManager.get_joueur(ctx.author.id)
        
        # [UI Pro] Embed style "Carte Bancaire"
        embed = self.create_embed(f"💳 Portefeuille de {ctx.author.name}", "", discord.Color.gold())
        embed.add_field(name="Solde disponible", value=f"# **{joueur.argent}** 🪙", inline=False)
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))