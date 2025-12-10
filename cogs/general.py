import discord
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Displays the player guide")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📘 Player Guide",
            description="Welcome! Use the **Slash Commands** (`/`) to interact.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="💰 Economy", 
            value="`/work` : Earn coins\n`/balance` : Check wallet", 
            inline=False
        )
        
        embed.add_field(
            name="🛒 Market", 
            value=(
                "`/shop` : Open interactive menu\n"
                "`/catalog` : View price list\n"
                "`/buy [item]` : Buy specific item"
            ), 
            inline=False
        )
        
        embed.add_field(
            name="🎒 Collection", 
            value="`/inventory` : View your bag", 
            inline=False
        )
        
        embed.set_footer(text="B2 Project - Full Slash Commands")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))