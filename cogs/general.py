import discord
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # SLASH COMMAND (app_commands)
    @app_commands.command(name="help", description="Displays the player guide and commands")
    async def help(self, interaction: discord.Interaction):
        
        # [Grading: UI] Clean Embed Panel
        embed = discord.Embed(
            title="📘 Player Guide",
            description="Welcome! Here is how to use the Economy and Collection system.",
            color=discord.Color.blue()
        )
        
        # Updated commands in English
        embed.add_field(
            name="💰 Economy", 
            value="`!work` : Work to earn coins\n`!balance` : Check your wallet balance", 
            inline=False
        )
        
        embed.add_field(
            name="🛒 Market", 
            value="`!shop` : Open the interactive shop menu\n`!buy <item>` : Manually buy an item (e.g., `!buy Apple`)", 
            inline=False
        )
        
        embed.add_field(
            name="🎒 Collection", 
            value="`!inventory` : View your collected items", 
            inline=False
        )
        
        embed.set_footer(text="B2 Project - Object Economy")

        # Reply to the interaction
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))