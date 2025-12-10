import discord
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Voici la commande SLASH (elle utilise app_commands au lieu de commands)
    @app_commands.command(name="aide", description="Affiche le guide des commandes du bot")
    async def aide(self, interaction: discord.Interaction):
        
        # [Barème: UI] On crée un joli panneau (Embed)
        embed = discord.Embed(
            title="📘 Guide du Joueur",
            description="Bienvenue ! Voici comment utiliser le système d'économie et de collection.",
            color=discord.Color.blue()
        )
        
        # On ajoute les champs pour expliquer les commandes "!"
        embed.add_field(name="💰 Économie", value="`!work` : Travailler pour gagner de l'argent\n`!solde` : Voir combien tu as en banque", inline=False)
        embed.add_field(name="🛒 Commerce", value="`!shop` : Voir les objets à vendre\n`!buy <objet>` : Acheter un objet (ex: `!buy Potion`)", inline=False)
        embed.add_field(name="🎒 Collection", value="`!inventaire` : Voir tes objets possédés", inline=False)
        
        embed.set_footer(text="Projet B2 - Économie des objets")

        # Pour les slash commands, on utilise interaction.response.send_message
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))