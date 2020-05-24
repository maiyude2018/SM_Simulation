import json
import random
import math
from Team import Team
import copy


class SteemMonstersSimulation:

    def __init__(self,team1,team2,sm_dict,player):

        self.player = player
        self.team1 = team1
        self.team2 = team2
        self.sm_dict = sm_dict
        self.build_turn_order(team2)
        self.apply_buff(self.team1,self.team1.team_mod,True,False)
        self.apply_buff(self.team2,self.team2.team_mod,True,False)
        self.apply_buff(self.team2,self.team1.enemy_mod,True,False)
        self.apply_buff(self.team1,self.team2.enemy_mod,True,False)
        self.last_team = 1
        for mon in team1.monsters:
            self.apply_buff(team1,mon.team_mod,False,False)
            self.apply_buff(team2,mon.enemy_mod,False,False)



            if "Blind" in mon.abilities:
                team2.set_blinded(True)

            # 加护甲技能
            if "Protect" in mon.abilities:
                for i in team1.monsters:
                    i.base_stats[3] += 2
                    i.stats[3] += 2

            #减护甲技能
            if "Rust" in mon.abilities:
                for i in team2.monsters:
                    i.base_stats[3] -= 2
                    i.stats[3] -= 2


        for mon in team2.monsters:
            self.apply_buff(team2,mon.team_mod,False,False)
            self.apply_buff(team1,mon.enemy_mod,False,False)

            if "Blind" in mon.abilities:
                team1.set_blinded(True)

            # 加护甲技能
            if "Protect" in mon.abilities:
                for i in team2.monsters:
                    i.base_stats[3] += 2
                    i.stats[3] += 2
            # 减护甲技能
            if "Rust" in mon.abilities:
                for i in team1.monsters:
                    i.base_stats[3] -= 2
                    i.stats[3] -= 2


        if "Equalizer" in self.team1.ruleset:
            #计算两队最大HP
            hp=[]
            for i in team1.monsters:
                hp.append(i.base_stats[4])
            for i in team2.monsters:
                hp.append(i.base_stats[4])
            max_hp=hp[hp.index(max(hp))]
            #HP赋值
            for i in team1.monsters:
                i.base_stats[4]=max_hp
                i.stats[4] = max_hp
            for i in team2.monsters:
                i.base_stats[4]=max_hp
                i.stats[4] = max_hp


        #护甲负数调整
        for i in team1.monsters:
            if i.base_stats[3] < 0:
                i.stats[3] = 0

        for i in team2.monsters:
            if i.base_stats[3] < 0:
                i.stats[3] = 0







        self.inital_len_team1 = len(self.team1.monsters)
        self.inital_len_team2 = len(self.team2.monsters)

    def apply_buff(self,team,mod,summoner,reverse):
        for monster in team.monsters:
            monster.apply_buff(mod,summoner,reverse)


    def simulate_battle(self):
        turns = 0
        battle_log = ""
        battle_log += "team1队伍\n"
        battle_log += (str([m.name+str(m.stats)+str(m.abilities)+m.type for m in self.team1.monsters]) + "\n")
        battle_log += "team2队伍\n"
        battle_log += (str([m.name+str(m.stats)+str(m.abilities)+m.type for m in self.team2.monsters]) + "\n")

        #检测双方队伍人数
        while len(self.team1.monsters) > 0 and len(self.team2.monsters) > 0:
            turns += 1
            #team1or=copy.deepcopy(self.team1)
            #team2or = copy.deepcopy(self.team2)
            team1_order = self.build_turn_order(self.team1)
            team2_order = self.build_turn_order(self.team2)

            #battle_log += "回合"+str(turns)+"开始\n\n"
            #battle_log += str([m.name for m in team1_order]) +"\n"
            #battle_log += str([m.name for m in team2_order]) + "\n"
            success = False


            while len(team1_order) != 0 or len(team2_order) != 0:
                if len(self.team1.monsters) == 0:
                    break
                if len(self.team2.monsters) == 0:
                    break

                current_mon = self.get_next_mon(team1_order,team2_order)
                current_team = self.team2 if self.last_team == 2 else self.team1
                enemy_team = self.team1 if self.last_team == 2 else self.team2
                stun = current_mon.start_turn(current_team,enemy_team)

                if not current_mon.alive and current_mon.pos < len(current_team.monsters):
                    #self.is_dead(current_mon,current_team,enemy_team,current_mon.pos)
                    if not current_team.monsters:
                        break
                    if not enemy_team.monsters:
                        break
                    continue
                if stun:
                    current_mon.stun = False
                    continue

                target = current_mon.find_target(enemy_team.monsters)
                #battle_log += str([n.name +" 攻:"+str(n.stats[0])
                 #                  +" 远:" + str(n.stats[1])
                  #                 + " 魔:" + str(n.stats[2])
                   #                + " 防:" + str(n.stats[3])
                    #               + " 命:" + str(n.stats[4])
                     #              + " 速:" + str(n.stats[5])+"等:"
                      #             + str(n.level) for n in self.team1.monsters])+"\n"
                #battle_log +=str([n.name +" 攻:"+str(n.stats[0])
                 #                  +" 远:" + str(n.stats[1])
                  #                 + " 魔:" + str(n.stats[2])
                   #                + " 防:" + str(n.stats[3])
                    #               + " 命:" + str(n.stats[4])
                     #              + " 速:" + str(n.stats[5])+"等:"
                      #            + str(n.level) for n in self.team2.monsters]) +"\n"
                #battle_log += current_mon.name + "攻击类型："+current_mon.type +",攻击,攻击位置："+str(current_mon.pos)+"\n"

                if target == -1:
                    battle_log += current_mon.name + "不能攻击\n"
                    current_mon.can_attack = False
                    continue
                else:
                    current_mon.can_attack = True

                target_mon = enemy_team.monsters[target]

                if target_mon.alive:
                    battle_log += target_mon.name +" 状态：生存\n"
                    previous_mon = None
                    next_mon = None

                    if target > 0:
                        previous_mon = enemy_team.monsters[target-1]
                    if target +1 < len(enemy_team.monsters):
                        next_mon = enemy_team.monsters[target+1]
                    success = current_mon.attack(target_mon,previous_mon,next_mon,current_mon)


                    if not current_mon.alive and current_mon.pos < len(current_team.monsters):
                        battle_log += current_mon.name + " 死掉了."
                        self.is_dead(current_mon,current_team,enemy_team,current_mon.pos)
                        self.team_pos(team2_order, team1_order)
                        if not enemy_team.monsters:
                            break
                        if not current_team.monsters:
                            break
                        continue



                #battle_log += "攻击开始："+current_mon.name +" 攻击 " + target_mon.name +"\n"
                if not success:
                    battle_log += current_mon.name + " 的攻击没打中\n"


               #battle_log += "攻击力："+str(current_mon.stats[0])+","+str(current_mon.stats[1]) +","+str(current_mon.stats[2])+"生命:"+str(current_mon.stats[4])+"攻击 " + \
                #              "攻击力："+str(target_mon.stats[0])+","+str(target_mon.stats[1]) +","+str(target_mon.stats[2])+"生命:"+str(target_mon.stats[4]) +"\n"+"\n"+"\n"





                if not target_mon.alive:
                    battle_log += target_mon.name + " 状态:死亡\n"
                    self.is_dead(target_mon,enemy_team,current_team,target)
                    #self.team_pos(team1_order, team2_order)
                    #更新team_order，攻击顺序队列
                    battle_log += str([m.name for m in team1_order]) +"\n"
                    battle_log += str([m.name for m in team2_order]) + "\n"

                    if not enemy_team.monsters:
                        break
                    if not current_team.monsters:
                        break


            if turns > 20:

                i = 0
                damage = turns - 20
                battle_log += "Fatigue sets in: -" + str(damage)
                for mon in self.team1.monsters:

                    self.apply_damage(mon,damage)
                    if not mon.alive:
                        self.is_dead(mon,self.team1,self.team2,i)
                    i += 1
                i = 0
                for mon in self.team2.monsters:
                    self.apply_damage(mon,damage)
                    if not mon.alive:
                        self.is_dead(mon,self.team2,self.team1,i)
                    i += 1

            if "Earthquake" in self.team1.ruleset:
                i = 0
                for mon in self.team1.monsters:
                    if "Flying" not in mon.abilities:
                        self.apply_damage(mon,2)
                    if not mon.alive:
                        self.is_dead(mon,self.team1,self.team2,i)
                    i += 1
                i = 0
                for mon in self.team2.monsters:
                    if "Flying" not in mon.abilities:
                        self.apply_damage(mon,2)
                    if not mon.alive:
                        self.is_dead(mon,self.team2,self.team1,i)
                    i += 1
            #battle_log += "team1\n"
            #battle_log += str([m.name+str(m.stats)+str(m.abilities)+m.type for m in self.team1.monsters]) + "\n"
            #battle_log += "team2\n"
            #battle_log += str([m.name+str(m.stats)+str(m.abilities)+m.type for m in self.team2.monsters]) + "\n"
            #battle_log += "\n\回合"+str(turns)+"结束\n"
        #print(battle_log)
        self.battle_log = ""
        rcc=len(self.team1.monsters)-len(self.team2.monsters)

        if rcc > 0:
            result = 1
        else:
            result = -1
        lenteam1=len(self.team1.monsters)
        lenteam2 = len(self.team2.monsters)
        result=[result,lenteam1,lenteam2]
        return result

    def is_dead(self,mon,current_team,enemy_team,pos):
        current_team.monsters.pop(pos)
        current_team.recompute_pos()
        for m in enemy_team.monsters:
            if m.can_resurrect:
                m.can_resurrect = False
                mon.alive = True
                mon.stats[4] = 1
                return
        enemy_mod = [ i*-1 for i in mon.enemy_mod]
        team_mod = [ i*-1 for i in mon.team_mod]
        #致盲失效
        if "Blind" in mon.abilities:
            enemy_team.set_blinded(False)

        # 加护甲技能失效
        if "Protect" in mon.abilities:
            for i in current_team.monsters:
                i.base_stats[3] -= 2
                i.stats[3] -= 2

        #减护甲失效
        if "Rust" in mon.abilities:
            for i in enemy_team.monsters:
                if i.base_stats[3] >= 0 :
                    i.stats[3] += 2
                if i.base_stats[3] == -1:
                    i.stats[3] += 1
                i.base_stats[3] += 2

        if "Redemption" in mon.abilities:
            for m in enemy_team.monsters:
                m.stats[4] -= 1
                if m.stats[4] <=0:
                    m.alive = False

        for i in current_team.monsters:
            if "Scavenger" in i.abilities:
                i.stats[4] += 1
                i.base_stats[4] += 1

        for i in enemy_team.monsters:
            if "Scavenger" in i.abilities:
                i.stats[4] += 1
                i.base_stats[4] += 1

        self.apply_buff(current_team,team_mod,True,True)
        self.apply_buff(enemy_team,enemy_mod,True,True)
        try:
            for k in enemy_team.monsters:
                if not k.alive:
                    self.is_dead(mon, current_team, enemy_team, k)
        except Exception as e:
            pass


    def apply_damage(self,monster,damage):
        mod = 0
        if "Shield" in monster.abilities:
            mod = -1

        if monster.stats[3] > 0:
            rem_armor = monster.stats[3] - (damage + mod)
            if rem_armor < 0:
                rem_armor = 0

            monster.stats[3] = rem_armor
        else:
            rem_health = monster.stats[4] - (damage + mod)
            if rem_health < 0:
                rem_health = 0
            monster.stats[4] = rem_health

            if monster.stats[4] <= 0:
                monster.alive = False


    def get_next_mon(self,team1_order,team2_order):
        if len(team1_order)==0:
            self.last_team = 2
            return team2_order.pop()
        elif len(team2_order)==0:
            self.last_team = 1
            return team1_order.pop()
        mon1 = team1_order[len(team1_order)-1].stats
        mon2 = team2_order[len(team2_order)-1].stats
        if mon1[5] > mon2[5]:
            self.last_team = 1
            return team1_order.pop()
        elif mon2[5] > mon1[5]:
            self.last_team = 2
            return team2_order.pop()
        else:


            sel = random.randint(1,2)

            if sel == 1:
                self.last_team = 1
                return team1_order.pop()
            else:
                self.last_team = 2
                return team2_order.pop()

            #self.last_team = 1
            #return team1_order.pop()
    def build_turn_order(self,team):
        sorted_team = []
        if "Reverse Speed" not in self.team1.ruleset:
            sorted_team = sorted(team.monsters,key = lambda m: (m.stats[5]))
        else:
            sorted_team = sorted(team.monsters,key = lambda m: (m.stats[5]),reverse=True)
        return sorted_team

    def team_pos(self,team1_order,team2_order):
        if self.last_team == 1:
            try:
                team2_order.pop(0)
            except:
                oo=0
            try:
                oo = 0
                for i in team2_order:
                    i.__dict__.update({'pos': oo})
                    oo += 1
            except:
                oo=0
        else:
            try:
                team1_order.pop(0)
            except:
                oo=0
            try:
                oo = 0
                for i in team1_order:
                    i.__dict__.update({'pos': oo})
                    oo += 1
            except:
                oo=0



def load_SM_dict():
    f = open("get_details.json","r").read()
    sm_dict = dict()
    for entry in json.loads(f):
        sm_dict[entry["id"]] = entry
    return sm_dict

