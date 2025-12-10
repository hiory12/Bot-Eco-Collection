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
        
        embed.add_field(name="💰 Economy", value="`/work`\n`/balance`", inline=True)
        
        embed.add_field(
            name="🛒 Market", 
            value="`/shop` (Menu)\n`/catalog` (Visual List)\n`/inspect [item]` (Image)\n`/buy [item]`", 
            inline=False
        )
        
        embed.add_field(name="🎒 Collection", value="`/inventory`", inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))