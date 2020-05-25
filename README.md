# SM_Simulation
Simulation for the Battle Mode of the Steem Dapp Steem Monsters/Splinterlands


```
from Team import Team
from Simulation import SteemMonstersSimulation
import Simulation




#规则
noinactive=""

ai="Heavy Hitters"
player="maiyude"
player2="robot"




#team1队伍
#召唤士信息
summoner = {'id': 235, 'level': 2}
monsters = [{'id': 82, 'level': 4},{'id': 48, 'level': 5},{'id': 143, 'level': 6}]




#team2队伍
#召唤士信息
summoner2 = {'id': 74, 'level': 2}
monsters2 = [{'id': 50, 'level': 5},{'id': 131, 'level': 1}]



sm_dict=Simulation.load_SM_dict()



team1x = Team(summoner, monsters, ai, sm_dict, player)
team2x = Team(summoner2, monsters2, ai, sm_dict, "diren")




battle = SteemMonstersSimulation(team1x, team2x, sm_dict, player)
results = battle.simulate_battle（）

re=copy.deepcopy(results[0])
re1=copy.deepcopy(results[1])

if re==1:
    print("team1胜利")
else:
    print("team2胜利")
```



