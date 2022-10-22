import discord
from discord.ext import commands
import requests, json
from functions import *
import math


class statsCog(commands.Cog, name="stats command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="stats", usage="", description="wip")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def stats(self, ctx, i1, i2=None, mode=""):

        succes, pdata = getplayerbydata(i1, i2)
        if not succes:
            await ctx.send(f"The search query for `{i1} {i2}` is not found.")
            return

        profileData = getprofilepersondata(pdata["personId"])
        succes, wantdata, mode = frommodetodata(profileData, mode)

        if not succes:
            q = discord.Embed(
                title="Error",
                description=f"{wantdata}\nPlease do: [prefix]help stats",
                color=discord.Color.red(),
            )
            await ctx.send(embed=q)
            return

        wantedlist = getwantedlist(wantdata)

        q = discord.Embed(
            title=f'{pdata["jersey"]} | {pdata["firstName"]} {pdata["lastName"]} | {getteamfromid(pdata["teamId"])}',  # ? add team
            description=f"User's id: {pdata['personId']}, Team's id: {pdata['teamId']}",
            color=discord.Color.blue(),
        )

        output = [
            f"Points: {wantdata['points']}",
            f"Points per game {wantdata['ppg']}",
            f"Rebounds: {wantdata['totReb']}",
            f"Rebounds per game: {wantdata['rpg']}",
            f"Offensive rebounds: {wantdata['offReb']}",
            f"Defensive rebounds: {wantdata['defReb']}",
            f"Assists: {wantdata['assists']}",
            f"Assists per game: {wantdata['apg']}",
            f"Turnovers per game: {wantdata['topg']}",
            f"Time played: {wantdata['mpg']} m",
            f"Steals: {wantdata['steals']}" f"Steals per game: {wantdata['spg']}",
            f"Blocks: {wantdata['blocks']}" f"Blocks per game: {wantdata['bpg']}",
            f"Free trowns: {wantdata['ftp']}%",
            f"Field goal percentage: {wantdata['fgp']}%",
            f"Three point percentage {wantdata['tpp']}%",
            f"Lost balls: {wantdata['turnovers']}",
            f"Field goals made: {wantdata['fgm']}",
            f"Field goal attempts: {wantdata['fga']}",
            f"3-Points made {wantdata['tpm']}"
            f"3-Points attempts: {wantdata['tpa']}"
            f"Free throws made: {wantdata['ftm']}",
            f"Free Throw Attempt: {wantdata['fta']}",
            f"Player fouls {wantdata['pFouls']}",
            f"Games played: {wantdata['gamesPlayed']}, started: {wantdata['gamesStarted']}",
            f"Double double: {wantdata['dd2']}",
            f"Tripple double: {wantdata['td3']}",
        ]

        out = ""
        for item in output:
            out = out + item + "\n"

        q.add_field(name="Data", value=out)
        await ctx.send(embed=q)


def setup(bot: commands.Bot):
    bot.add_cog(statsCog(bot))
