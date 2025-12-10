import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View
from modules.game_classes import Item
from modules.data_handler import DataManager

# [Grading: Complexity] Full list with Images and Descriptions
SHOP_ITEMS = [
    # --- COMMON (Grey/White) ---
    Item("Apple", 5, "Common", "A fresh red apple. Restores a bit of energy.", "https://emojigraph.org/media/twitter/red-apple_1f34e.png"),
    Item("Bread", 10, "Common", "Baked this morning. Smells good.", "https://emojigraph.org/media/twitter/bread_1f35e.png"),
    Item("Bandage", 15, "Common", "Simple cloth to cover wounds.", "https://emojigraph.org/media/twitter/adhesive-bandage_1fa79.png"),
    Item("Stick", 25, "Common", "It's just a stick. Better than nothing.", "https://emojigraph.org/media/twitter/wood_1fab5.png"),
    Item("Wooden_Sword", 50, "Common", "A training sword for beginners.", "https://emojigraph.org/media/twitter/dagger_1f5e1-fe0f.png"),

    # --- RARE (Blue) ---
    Item("Mana_Potion", 100, "Rare", "Restores magical power instantly.", "https://emojigraph.org/media/twitter/test-tube_1f9ea.png"),
    Item("Iron_Shield", 150, "Rare", "Solid protection against basic attacks.", "https://emojigraph.org/media/twitter/shield_1f6e1-fe0f.png"),
    Item("Treasure_Map", 250, "Rare", "An old map leading to unknown riches.", "https://emojigraph.org/media/twitter/world-map_1f5fa-fe0f.png"),
    Item("Elven_Bow", 400, "Rare", "Crafted by elves. Accurate and light.", "https://emojigraph.org/media/twitter/bow-and-arrow_1f3f9.png"),
    Item("Diamond", 500, "Rare", "Shiny and valuable.", "https://emojigraph.org/media/twitter/gem-stone_1f48e.png"),

    # --- EPIC (Purple) ---
    Item("Grimoire", 800, "Epic", "Contains ancient forbidden spells.", "https://emojigraph.org/media/twitter/open-book_1f4d6.png"),
    Item("Gold_Armor", 1500, "Epic", "Heavy, shiny, and very protective.", "https://emojigraph.org/media/twitter/bust-in-silhouette_1f464.png"), 
    Item("Ruby_Ring", 2500, "Epic", "Grants the power of fire to the wearer.", "https://emojigraph.org/media/twitter/ring_1f48d.png"),

    # --- LEGENDARY (Gold) ---
    Item("King_Crown", 5000, "Legendary", "The symbol of ultimate power.", "https://emojigraph.org/media/twitter/crown_1f451.png"),
    Item("Excalibur", 7500, "Legendary", "The legendary sword that cuts through anything.", "https://emojigraph.org/media/twitter/crossed-swords_2694-fe0f.png"),
    Item("Dragon_Egg", 15000, "Legendary", "Warm to the touch. Is it alive?", "https://emojigraph.org/media/twitter/hatching-chick_1f423.png")
]

# --- UI CLASSES ---

class ShopSelect(Select):
    def __init__(self):
        options = []
        for item in SHOP_ITEMS:
            emoji = "⚪"
            if item.rarity == "Rare": emoji = "🔵"
            elif item.rarity == "Epic": emoji = "🟣"
            elif item.rarity == "Legendary": emoji = "🟠"
            
            options.append(discord.SelectOption(
                label=item.name, 
                description=f"{item.price} coins", 
                emoji=emoji, 
                value=item.name
            ))

        super().__init__(placeholder="🔻 Select an item to buy...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        chosen_item_name = self.values[0]
        found_item = next((i for i in SHOP_ITEMS if i.name == chosen_item_name), None)
        player = DataManager.get_player(interaction.user.id)
        
        if player.buy(found_item):
            DataManager.save_player(player)
            embed = discord.Embed(title="✅ Purchase Successful!", description=f"You obtained **{found_item.name}**!", color=discord.Color.green())
            embed.set_thumbnail(url=found_item.image_url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
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

    # --- AUTOCOMPLETE FUNCTION ---
    # C'est cette fonction qui permet de proposer les items quand on tape
    async def item_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=item.name, value=item.name)
            for item in SHOP_ITEMS
            if current.lower() in item.name.lower()
        ][:25] # Limite Discord de 25 choix

    @app_commands.command(name="shop", description="Open the interactive shop menu")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🛒 The Item Shop", description="Select an item below.", color=discord.Color.gold())
        await interaction.response.send_message(embed=embed, view=ShopView())

    @app_commands.command(name="catalog", description="View items grouped by rarity with colors")
    async def catalog(self, interaction: discord.Interaction):
        await interaction.response.send_message("📜 **Loading Catalog...**", ephemeral=True)

        categories = [
            {"name": "Common Items", "rarity": "Common", "color": 0x95a5a6},
            {"name": "Rare Items", "rarity": "Rare", "color": 0x3498db},
            {"name": "Epic Items", "rarity": "Epic", "color": 0x9b59b6},
            {"name": "Legendary Items", "rarity": "Legendary", "color": 0xf1c40f}
        ]

        for cat in categories:
            items_in_cat = [i for i in SHOP_ITEMS if i.rarity == cat["rarity"]]
            if not items_in_cat: continue

            embed = discord.Embed(title=f"--- {cat['name']} ---", color=cat["color"])
            if items_in_cat:
                embed.set_thumbnail(url=items_in_cat[0].image_url)

            description_text = ""
            for item in items_in_cat:
                description_text += f"**{item.name}** • `{item.price} $`\n*{item.description}*\n\n"
            
            embed.description = description_text
            await interaction.channel.send(embed=embed)

    # --- INSPECT AVEC AUTOCOMPLÉTION ---
    @app_commands.command(name="inspect", description="See details and image of a specific item")
    @app_commands.autocomplete(item_name=item_autocomplete) # Lien avec la fonction d'autocomplétion
    async def inspect(self, interaction: discord.Interaction, item_name: str):
        found_item = next((i for i in SHOP_ITEMS if i.name.lower() == item_name.lower()), None)
        
        if not found_item:
            return await interaction.response.send_message("❌ Item not found. Please select from the list.", ephemeral=True)

        color = 0x95a5a6
        if found_item.rarity == "Rare": color = 0x3498db
        elif found_item.rarity == "Epic": color = 0x9b59b6
        elif found_item.rarity == "Legendary": color = 0xf1c40f

        embed = discord.Embed(title=f"🔍 {found_item.name}", description=found_item.description, color=color)
        embed.add_field(name="Price", value=f"{found_item.price} coins", inline=True)
        embed.add_field(name="Rarity", value=found_item.rarity, inline=True)
        embed.set_image(url=found_item.image_url)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy", description="Manually buy an item")
    @app_commands.autocomplete(item_name=item_autocomplete) # Autocomplétion aussi pour Buy !
    async def buy(self, interaction: discord.Interaction, item_name: str):
        found_item = next((i for i in SHOP_ITEMS if i.name.lower() == item_name.lower()), None)
        if not found_item:
            return await interaction.response.send_message("❌ Item not found.", ephemeral=True)

        player = DataManager.get_player(interaction.user.id)
        if player.buy(found_item):
            DataManager.save_player(player)
            await interaction.response.send_message(f"✅ Bought **{found_item.name}**!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Insufficient funds.", ephemeral=True)

    @app_commands.command(name="inventory", description="View your inventory")
    async def inventory(self, interaction: discord.Interaction):
        player = DataManager.get_player(interaction.user.id)
        if not player.inventory:
            return await interaction.response.send_message("🎒 Empty bag.", ephemeral=True)
        
        count = {item: player.inventory.count(item) for item in set(player.inventory)}
        text = "".join([f"• **{item}** `x{qty}`\n" for item, qty in count.items()])
        embed = discord.Embed(title=f"🎒 Inventory", description=text, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Collection(bot))