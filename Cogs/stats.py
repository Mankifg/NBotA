import discord
from discord.ext import commands
import requests, json

class statsCog(commands.Cog, name="stats command"):
	def __init__(self, bot:commands.bot):
		self.bot = bot
        
	@commands.command(name = "stats",
					usage="",
					description = "Display the bot's stats.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def stats(self, ctx):
		await ctx.send("test")

def setup(bot:commands.Bot):
	bot.add_cog(statsCog(bot))