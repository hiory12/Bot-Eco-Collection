import discord
from discord.ext import commands
from discord.ui import Select, View
from modules.game_classes import Objet
from modules.data_handler import DataManager

# [Barème: Complexité] Liste complète des objets
BOUTIQUE = [
    # --- Niveau 1 : Objets Communs ---
    Objet("Pomme", 5, "Commune"),
    Objet("Pain", 10, "Commune"),
    Objet("Bandage", 15, "Commune"),
    Objet("Baton", 25, "Commune"),
    Objet("Epee_Bois", 50, "Commune"),

    # --- Niveau 2 : Objets Rares ---
    Objet("Potion_Mana", 100, "Rare"),
    Objet("Bouclier_Fer", 150, "Rare"),
    Objet("Carte_Tresor", 250, "Rare"),
    Objet("Arc_Elfique", 400, "Rare"),
    Objet("Diamant", 500, "Rare"),

    # --- Niveau 3 : Objets Épiques ---
    Objet("Grimoire", 800, "Épique"),
    Objet("Armure_Or", 1500, "Épique"),
    Objet("Anneau_Rubis", 2500, "Épique"),

    # --- Niveau 4 : Objets Légendaires ---
    Objet("Couronne_Roi", 5000, "Légendaire"),
    Objet("Epee_Excalibur", 7500, "Légendaire"),
    Objet("Oeuf_Dragon", 15000, "Légendaire")
]

# --- CLASSES D'INTERFACE (UI) ---

class ShopSelect(Select):
    """Le menu déroulant qui contient TOUS les objets"""
    def __init__(self):
        options = []
        for objet in BOUTIQUE:
            # Gestion des Emojis selon la rareté
            emoji = "⚪"
            description_text = f"{objet.prix} $ - Commun"
            
            if objet.rarete == "Rare": 
                emoji = "🔵"
                description_text = f"{objet.prix} $ - Rare"
            elif objet.rarete == "Épique": 
                emoji = "🟣"
                description_text = f"{objet.prix} $ - Épique"
            elif objet.rarete == "Légendaire": 
                emoji = "🟠"
                description_text = f"{objet.prix} $ - Légendaire"
            
            # Création de l'option dans le menu
            options.append(discord.SelectOption(
                label=objet.nom, 
                description=description_text, 
                emoji=emoji,
                value=objet.nom
            ))

        # Placeholder = Le texte affiché avant de cliquer
        super().__init__(placeholder="🔻 Clique ici pour voir les objets...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        """Action au clic"""
        nom_objet_choisi = self.values[0]
        objet_trouve = next((o for o in BOUTIQUE if o.nom == nom_objet_choisi), None)
        
        joueur = DataManager.get_joueur(interaction.user.id)
        
        # Logique d'achat
        succes = joueur.acheter(objet_trouve)
        
        if succes:
            DataManager.save_joueur(joueur)
            # Message invisible (ephemeral)
            await interaction.response.send_message(
                f"✅ **Achat réussi !** Tu as reçu : {objet_trouve.nom}", 
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ **Fonds insuffisants.** Prix : {objet_trouve.prix} pièces.", 
                ephemeral=True
            )

class ShopView(View):
    def __init__(self):
        super().__init__()
        self.add_item(ShopSelect())

# --- MODULE COLLECTION ---

class Collection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):
        """Affiche la boutique (Menu uniquement, pas de liste texte)"""
        
        # On crée un Embed très simple et propre
        embed = discord.Embed(
            title="🛒 La Boutique", 
            description="Bienvenue au marché ! Utilise le menu ci-dessous pour parcourir le catalogue et faire tes achats.", 
            color=discord.Color.gold()
        )
        
        # On envoie l'embed ET la vue (le menu déroulant)
        await ctx.send(embed=embed, view=ShopView())

    @commands.command()
    async def inventaire(self, ctx):
        joueur = DataManager.get_joueur(ctx.author.id)
        
        if not joueur.inventaire:
            return await ctx.send(embed=discord.Embed(description="🎒 Ton sac est vide.", color=discord.Color.red()))
        
        # Affichage propre de l'inventaire
        comptage = {obj: joueur.inventaire.count(obj) for obj in set(joueur.inventaire)}
        texte = ""
        for obj, qte in comptage.items():
            texte += f"• **{obj}** `x{qte}`\n"
            
        embed = discord.Embed(title=f"🎒 Sac de {ctx.author.name}", description=texte, color=discord.Color.blue())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Collection(bot))