import os
import json
from datetime import datetime as dt
import time
import requests
 
players_link = "https://data.nba.net/10s/prod/v1/{}/players.json"
team_link = "https://data.nba.net/10s/prod/v1/{}/teams.json"


def getplayers():
    return requests.get(players_link.replace("{}",str(dt.now().year))).json()

def getteams():
    return requests.get(team_link.replace("{}",str(dt.now().year))).json()


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