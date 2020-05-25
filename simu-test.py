
import time
from api import Api
from Team import Team
from simulation import SteemMonstersSimulation
import simulation
import copy

api = Api()


noinactive=""
#规则
ai="Heavy Hitters"
#ai="Super Sneak"
#ai="Aim True"
#ai="Equalizer"
#ai=""
player="maiyude"
player2="robot"


b1=0
kk=1
zhunque=0

#team1队伍
# 召唤士信息
summoner = {'id': 235, 'level': 2}
monsters = [{'id': 82, 'level': 4},{'id': 48, 'level': 5},{'id': 143, 'level': 6}]
monsters = [{'id': 211, 'level': 4},{'id': 131, 'level': 1},{'id':131,'level':1}]
#monsters = [{'id': 177, 'level': 4}]



#team2队伍
# 召唤士信息
summoner2 = {'id': 74, 'level': 2}

monsters2 = [{'id': 50, 'level': 5},{'id': 131, 'level': 1},{'id':131,'level':1}]
monsters2 = [{'id': 143, 'level': 6},{'id': 82, 'level': 4},{'id': 48, 'level': 5}]
monsters2 = [{'id': 136, 'level': 1},{'id': 136, 'level': 6},{'id': 144, 'level': 1}]


sm_dict=simulation.load_SM_dict()

#sumssss=sm_dict[235]
#print()

#time.sleep(3600)

team1x = Team(summoner, monsters, ai, sm_dict, player)
team2x = Team(summoner2, monsters2, ai, sm_dict, "diren")
#team2_mon=team2x.monsters
#print(team2_mon[1].__dict__)

#team1_mon=team1x.monsters
#print(team1_mon[0].__dict__)


#time.sleep(3600)
battle = SteemMonstersSimulation(team1x, team2x, sm_dict, player)
results = battle.simulate_battle()

re=copy.deepcopy(results[0])
re1=copy.deepcopy(results[1])

if re==1:
    print("team1胜利")
else:
    print("team2胜利")






