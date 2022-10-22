from turtle import heading
import discord
from discord.ext import commands
import time
import json, requests
from datetime import datetime as dt
import datetime
from datetime import timezone
from functions import *

base_link = "https://data.nba.net/10s/prod/v1/{}/players.json"
pic_link = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{}.png"


class playerCog(commands.Cog, name="player command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="profile",
        usage=" [name/surname] or [id]",
        description="Display the static players profile.",
    )
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def profile(self, ctx, i1, i2=None):

        succes, pdata = getplayerbydata(i1, i2)

        if not succes:
            await ctx.send(f"The search query for `{i1} {i2}` is not found.")
            return

        draft = pdata["draft"]
        num = int(draft["pickNum"])

        dateofbirth = pdata["dateOfBirthUTC"].split("-")

        q = discord.Embed(
            title=f'{pdata["jersey"]} | {pdata["firstName"]} {pdata["lastName"]} | {getteamfromid(pdata["teamId"])}',
            description=f"User's id: {pdata['personId']}, Team's id: {pdata['teamId']}",
            color=discord.Color.blue(),
        )

        q.set_image(url=pic_link.replace("{}", pdata["personId"]))

        q.add_field(
            name="Height",
            value=f'{pdata["heightMeters"]}m / {pdata["heightFeet"]}′{pdata["heightInches"]}″',
            inline=True,
        )

        q.add_field(
            name="Weight",
            value=f'{pdata["weightKilograms"]}kg / {pdata["weightPounds"]}lb',
            inline=True,
        )

        q.add_field(
            name="Date Of Birth",
            value=f"{dateofbirth[2]}. {dateofbirth[1]}. {dateofbirth[0]}",
            inline=True,
        )

        q.add_field(name="Country", value=f"{pdata['country']}", inline=True)

        index = ""
        for i in range(len(pdata["teams"])):
            index = (
                index
                + f"{getteamfromid(pdata['teams'][i]['teamId'])} {pdata['teams'][i]['seasonStart']} - {pdata['teams'][i]['seasonEnd']}"
                + "\n"
            )

        q.add_field(name="ALL Teams", value=index, inline=False)

        if num == 1:
            endpoint = "st"
        elif num == 2:
            endpoint = "nd"
        elif num == 3:
            endpoint = "rd"
        else:
            endpoint = "th"

        q.add_field(
            name="Draft Info",
            value=f'Picked **{num}{endpoint}** in round **{draft["roundNum"]}**, by **{getteamfromid(draft["teamId"])}** year **{draft["seasonYear"]}**.',
            inline=False,
        )

        q.add_field(
            name="Other Data",
            value=f"Playing in NBA for **{pdata['yearsPro']}** years, Citizenship: **{pdata['country']}**",
            inline=False,
        )
        await ctx.send(embed=q)


def setup(bot: commands.Bot):
    bot.add_cog(playerCog(bot))
