import discord
from discord.ext import commands
import requests, json
from functions import * 
import math

output = [
	"",
	"",
	""
]



class statsCog(commands.Cog, name="stats command"):
	def __init__(self, bot:commands.bot):
		self.bot = bot
        
	@commands.command(name = "stats",
					usage="",
					description = "wip")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def stats(self, ctx, i1, i2=None, mode=""):
		
		succes,pdata = getplayerbydata(i1,i2)
		if not succes:
			await ctx.send(f"The search query for `{i1} {i2}` is not found.")
			return	


		profileData = getprofilepersondata(pdata["personId"])
		succes, wantdata, mode = frommodetodata(profileData,mode)


		if not succes:
			q = discord.Embed(
				title="Error",
				value=f"{wantdata}\nPlease do: [prefix]help stats",
				color=discord.Color.red()
			)
			await ctx.send(embed=q)
			return 

		await ctx.send(wantdata)

		#await ctx.send(profileData)

		q = discord.Embed(title=f'{pdata["jersey"]} | {pdata["firstName"]} {pdata["lastName"]} | {getteamfromid(pdata["teamId"])}', #? add team
			description=f"User's id: {pdata['personId']}, Team's id: {pdata['teamId']}",
			color=discord.Color.blue()
		)


	

def setup(bot:commands.Bot):
	bot.add_cog(statsCog(bot))