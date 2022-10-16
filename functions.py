import os
import json
from datetime import datetime as dt
import re
import time
import requests
 
players_link = "https://data.nba.net/10s/prod/v1/{}/players.json"
team_link = "https://data.nba.net/10s/prod/v1/{}/teams.json"
profile_url = "https://data.nba.net/10s/prod/v1/2022/players/{}_profile.json"

total = ["full","all","total","f","t"]
latest = ["latest","l"]

def getplayers():
    return requests.get(players_link.format(dt.now().year)).json()

def getteams():
    return requests.get(team_link.format(dt.now().year)).json()


def getteamfromid(id):
    data = getteams()
    data = data["league"]["standard"]
    for i,v in enumerate(data):
        if v["teamId"] == id:
            return data[i]["fullName"]

def getplayerbydata(data1,data2=None):
    data = getplayers()
    data = data["league"]["standard"]

    found_index = None

    if data2 == None or data2 == "":
        #id
        mode = "id"

        for i in range(len(data)):
            if data[i]["personId"] == data1:
                found_index = i
    else:
        # name/surname
        mode = "name"

        found_index = None
        for i in range(len(data)):
            if ((data[i]["firstName"].lower() == data1 and data[i]["lastName"].lower() == data2) or 
                (data[i]["firstName"].lower() == data2 and data[i]["lastName"].lower() == data2)):
                    found_index = i

    if found_index is not None:
        success = True
        return success, data[found_index]
    else:
        success = False
        return success, -1

def getprofilepersondata(id):
    return requests.get(profile_url.format(id)).json()

def frommodetodata(data,mode):
    data = data["league"]["standard"]["stats"]
    mode = mode.lower()

    if mode == "": 
        mode = "latest"


    if mode in latest:
        mode = "Latest"
        return True, data["latest"], mode
    elif mode in total:
        mode = "Total"
        return True, data["careerSummary"],mode


    else:
        try:
            num = int(mode)
        except ValueError:
            return False, "Wrong mode.", None
        
        if len(str(num)) == 2:
            if num > 47:     #! first nba game i think, if you think you can make it better pls do it
                num = f"19{num}"
            else:
                num = f"20{num}"

        data = data["regularSeason"]["season"]  
        found = False 
        for i in range(len(data)):
            if int(data[i]["seasonYear"]) == int(num):
                found = True
                data = data[i]

        if not found:
            return False,"Date not found", None
        else:
            return True, data,str(num)