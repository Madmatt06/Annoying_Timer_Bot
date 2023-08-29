import discord

class timer_creation(discord.ui.View):
    @discord.ui.button(label='-', style=discord.ButtonStyle.gray)
    async def subtract(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(label='+', style=discord.ButtonStyle.gray)
    async def add(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(label='Next', style=discord.ButtonStyle.green)
    async def next(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.message.edit(content='Timer Created', view=None)
        await interaction.response.defer()