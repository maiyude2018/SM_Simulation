from Summoner import Summoner
from Monster import Monster
import json
import random
import math


class Team:
    def __init__(self,summoner,monsters,ruleset,sm_dict,player):
        self.player = player
        self.summoner = Summoner(summoner["level"],sm_dict[summoner["id"]],ruleset)
        ruleset=self.summoner.summoner_ability()

        self.monsters = []
        self.blinded = False
        self.ruleset = ruleset
        if "Silenced Summoners" not in ruleset:
            self.team_mod = self.summoner.team_mod
            self.enemy_mod = self.summoner.enemy_mod
        else:
            self.team_mod = [0]*6
            self.enemy_mod = [0]*6

        pos = 0
        for monster in monsters:
            self.monsters.append(Monster(monster["level"],sm_dict[monster["id"]],pos,ruleset))
            pos += 1

    def recompute_pos(self):

        for i in range(0,len(self.monsters)):
            self.monsters[i].pos = i

    def set_blinded(self, blinded):
        self.blinded = blinded



