import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View
from modules.game_classes import Item
from modules.data_handler import DataManager

SHOP_ITEMS = [
    # --- Level 1 : Common Items ---
    Item("Apple", 5, "Common"),
    Item("Bread", 10, "Common"),
    Item("Bandage", 15, "Common"),
    Item("Stick", 25, "Common"),
    Item("Wooden_Sword", 50, "Common"),

    # --- Level 2 : Rare Items ---
    Item("Mana_Potion", 100, "Rare"),
    Item("Iron_Shield", 150, "Rare"),
    Item("Treasure_Map", 250, "Rare"),
    Item("Elven_Bow", 400, "Rare"),
    Item("Diamond", 500, "Rare"),

    # --- Level 3 : Epic Items ---
    Item("Grimoire", 800, "Epic"),
    Item("Gold_Armor", 1500, "Epic"),
    Item("Ruby_Ring", 2500, "Epic"),

    # --- Level 4 : Legendary Items ---
    Item("King_Crown", 5000, "Legendary"),
    Item("Excalibur", 7500, "Legendary"),
    Item("Dragon_Egg", 15000, "Legendary")
]

# --- UI CLASSES ---

class ShopSelect(Select):
    def __init__(self):
        options = []
        for item in SHOP_ITEMS:
            emoji = "⚪"
            desc = f"{item.price} coins - Common"
            
            if item.rarity == "Rare": 
                emoji = "🔵"
                desc = f"{item.price} coins - Rare"
            elif item.rarity == "Epic": 
                emoji = "🟣"
                desc = f"{item.price} coins - Epic"
            elif item.rarity == "Legendary": 
                emoji = "🟠"
                desc = f"{item.price} coins - Legendary"
            
            options.append(discord.SelectOption(label=item.name, description=desc, emoji=emoji, value=item.name))

        super().__init__(placeholder="🔻 Click here to browse items...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        chosen_item_name = self.values[0]
        found_item = next((i for i in SHOP_ITEMS if i.name == chosen_item_name), None)
        player = DataManager.get_player(interaction.user.id)
        
        if player.buy(found_item):
            DataManager.save_player(player)
            await interaction.response.send_message(f"✅ **Purchase Successful!** You received: {found_item.name}", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ **Insufficient Funds.** Price: {found_item.price} coins.", ephemeral=True)

class ShopView(View):
    def __init__(self):
        super().__init__()
        self.add_item(ShopSelect())

# --- COLLECTION MODULE ---

class Collection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shop", description="Open the interactive shop menu")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛒 The Item Shop", 
            description="Welcome! Use the menu below or use `/buy`.", 
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed, view=ShopView())

    @app_commands.command(name="catalog", description="View the full visual price list")
    async def catalog(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📜 Full Item Catalog", color=discord.Color.gold())
        emoji_map = {"Common": "⚪", "Rare": "🔵", "Epic": "🟣", "Legendary": "🟠"}
        grouped_items = {"Common": [], "Rare": [], "Epic": [], "Legendary": []}
        
        for item in SHOP_ITEMS:
            grouped_items[item.rarity].append(item)

        for rarity, items in grouped_items.items():
            if not items: continue
            text = "".join([f"{emoji_map[rarity]} **{item.name}** : `{item.price} coins`\n" for item in items])
            embed.add_field(name=f"--- {rarity} Items ---", value=text, inline=False)

        await interaction.response.send_message(embed=embed)

    # Note l'argument 'item_name' : Discord va créer une case texte pour l'utilisateur !
    @app_commands.command(name="buy", description="Manually buy an item by name")
    async def buy(self, interaction: discord.Interaction, item_name: str):
        found_item = next((i for i in SHOP_ITEMS if i.name.lower() == item_name.lower()), None)
        
        if not found_item:
            return await interaction.response.send_message(f"❌ Item **{item_name}** not found.", ephemeral=True)

        player = DataManager.get_player(interaction.user.id)
        
        if player.buy(found_item):
            DataManager.save_player(player)
            await interaction.response.send_message(f"✅ **Purchase Successful!** Bought **{found_item.name}** for {found_item.price} coins.")
        else:
            await interaction.response.send_message(f"❌ **Insufficient Funds.** Cost: {found_item.price} coins.", ephemeral=True)

    @app_commands.command(name="inventory", description="View your inventory")
    async def inventory(self, interaction: discord.Interaction):
        player = DataManager.get_player(interaction.user.id)
        
        if not player.inventory:
            return await interaction.response.send_message(embed=discord.Embed(description="🎒 Your bag is empty.", color=discord.Color.red()))
        
        count = {item: player.inventory.count(item) for item in set(player.inventory)}
        text = "".join([f"• **{item}** `x{qty}`\n" for item, qty in count.items()])
            
        embed = discord.Embed(title=f"🎒 {interaction.user.name}'s Inventory", description=text, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Collection(bot))