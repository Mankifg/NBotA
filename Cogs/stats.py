import discord
from discord.ext import commands
import requests, json
from functions import * 



class statsCog(commands.Cog, name="stats command"):
	def __init__(self, bot:commands.bot):
		self.bot = bot
        
	@commands.command(name = "profile",
					usage="",
					description = "	wip")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def profile(self, ctx, i1, i2=None):
		
		succes,pdata = getplayerbydata(i1,i2)
		if not succes:
			await ctx.send(f"The search query for `{i1} {i2}` is not found.")
			return	

		profileData = getprofilepersondata()

		await ctx.send(profileData)

		q = discord.Embed(title=f'{pdata["jersey"]} | {pdata["firstName"]} {pdata["lastName"]} | {getteamfromid(pdata["teamId"])}', #? add team
			description=f"User's id: {pdata['personId']}, Team's id: {pdata['teamId']}",
			color=discord.Color.blue()
		)


	

def setup(bot:commands.Bot):
	bot.add_cog(statsCog(bot))