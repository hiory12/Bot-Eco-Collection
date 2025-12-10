import discord
from discord.ext import commands
from discord.ui import Select, View
from modules.game_classes import Item
from modules.data_handler import DataManager

# [Grading: Complexity] Full list of items in English
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
    """The dropdown menu containing ALL items"""
    def __init__(self):
        options = []
        for item in SHOP_ITEMS:
            # Emoji management based on rarity
            emoji = "⚪"
            description_text = f"{item.price} coins - Common"
            
            if item.rarity == "Rare": 
                emoji = "🔵"
                description_text = f"{item.price} coins - Rare"
            elif item.rarity == "Epic": 
                emoji = "🟣"
                description_text = f"{item.price} coins - Epic"
            elif item.rarity == "Legendary": 
                emoji = "🟠"
                description_text = f"{item.price} coins - Legendary"
            
            # Create the menu option
            options.append(discord.SelectOption(
                label=item.name, 
                description=description_text, 
                emoji=emoji,
                value=item.name
            ))

        super().__init__(placeholder="🔻 Click here to browse items...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        """Action on click (Menu)"""
        chosen_item_name = self.values[0]
        found_item = next((i for i in SHOP_ITEMS if i.name == chosen_item_name), None)
        
        player = DataManager.get_player(interaction.user.id)
        
        # Buying logic
        success = player.buy(found_item)
        
        if success:
            DataManager.save_player(player)
            await interaction.response.send_message(
                f"✅ **Purchase Successful!** You received: {found_item.name}", 
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ **Insufficient Funds.** Price: {found_item.price} coins.", 
                ephemeral=True
            )

class ShopView(View):
    def __init__(self):
        super().__init__()
        self.add_item(ShopSelect())

# --- COLLECTION MODULE ---

class Collection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):
        """Displays the interactive shop menu"""
        embed = discord.Embed(
            title="🛒 The Item Shop", 
            description="Welcome to the market! Use the menu below to buy instantly, or type `!buy ItemName`.", 
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed, view=ShopView())

    # --- NOUVELLE COMMANDE CATALOGUE VISUEL ---
    @commands.command()
    async def catalog(self, ctx):
        """Displays a clean visual list of all items and prices"""
        
        embed = discord.Embed(
            title="📜 Full Item Catalog",
            description="Here is the complete price list grouped by rarity.",
            color=discord.Color.gold()
        )

        # Emoji map for clean display
        emoji_map = {"Common": "⚪", "Rare": "🔵", "Epic": "🟣", "Legendary": "🟠"}

        # Group items by rarity automatically
        grouped_items = {"Common": [], "Rare": [], "Epic": [], "Legendary": []}
        for item in SHOP_ITEMS:
            grouped_items[item.rarity].append(item)

        # Create a field for each rarity group
        for rarity, items in grouped_items.items():
            if not items: continue # Skip empty categories
            
            field_text = ""
            for item in items:
                field_text += f"{emoji_map[rarity]} **{item.name}** : `{item.price} coins`\n"
            
            embed.add_field(name=f"--- {rarity} Items ---", value=field_text, inline=False)

        embed.set_footer(text="Use !buy <name> to purchase items.")
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, *, item_name: str):
        """Manually buy an item (ex: !buy Apple)"""
        found_item = next((i for i in SHOP_ITEMS if i.name.lower() == item_name.lower()), None)
        
        if not found_item:
            return await ctx.send(f"❌ Item **{item_name}** not found in the shop.")

        player = DataManager.get_player(ctx.author.id)
        success = player.buy(found_item)
        
        if success:
            DataManager.save_player(player)
            await ctx.send(f"✅ **Purchase Successful!** You bought **{found_item.name}** for {found_item.price} coins.")
        else:
            await ctx.send(f"❌ **Insufficient Funds.** You need {found_item.price} coins (You have: {player.money}).")

    @commands.command(name="inventory", aliases=["inv", "bag"])
    async def inventory(self, ctx):
        player = DataManager.get_player(ctx.author.id)
        
        if not player.inventory:
            return await ctx.send(embed=discord.Embed(description="🎒 Your bag is empty.", color=discord.Color.red()))
        
        count = {item: player.inventory.count(item) for item in set(player.inventory)}
        text = ""
        for item, qty in count.items():
            text += f"• **{item}** `x{qty}`\n"
            
        embed = discord.Embed(title=f"🎒 {ctx.author.name}'s Inventory", description=text, color=discord.Color.blue())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Collection(bot))