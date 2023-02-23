import math
import random
import time
import sys

pause = 0.2
endTurnPause = 1

#skills
class Skill():
    def __init__(self,name="",info="",info2=""):
        self.name = name
        self.info = info
        self.info2 = info2

class OneTargetAttack(Skill):
    def __init__(self,name="",damage=1,cost=0,info="",info2=""):
        super().__init__(self,name=name,info=info,info2=info2)
        self.type = "onetarget"
        self.damage = damage
        self.cost = cost

class HomingAmulet(OneTargetAttack):
    def __init__(self):
        super().__init__("Homing Amulet",4,0,"Cost: 0 Points","Deals 4 Damage")

class FantasySeal(OneTargetAttack):
    def __init__(self):
        super().__init__("Fantasy Seal",10,5,"Cost: 5 Points","Deals 10 Damage")

class MagicMissile(OneTargetAttack):
    pass
    

# All characters have these stats.
class Character:
    def __init__(self, name="", hp=0):
        self.name = name
        self.hp = hp
        self.hpMax = hp

class Reimu(Character):
    def __init__(self):
        super().__init__("Reimu Hakurei", 32)
        self.sp = 0
        self.term = "Points"
        self.skills = [HomingAmulet(),FantasySeal()]
        self.costType = "spend"
        self.update()
        
    def update(self):
        self.info = f'{self.term} {self.sp}'
    
class Marisa(Character):
    def __init__(self):
        super().__init__("Marisa Kirisame", 24)
        self.sp = 30
        self.update()

    def update(self):
        self.info = f'Magic {self.sp}'

class Foe:
    def __init__(self, name="", hp=0):
        self.name = name
        self.hp = hp
        self.hpMax = hp

class Marisa_Foe(Foe):
    def __init__(self):
        super().__init__("Marisa Kirisame", 50)
        self.sp = 20
        self.update()

    def update(self):
        self.info = f'Magic {self.sp}'

def box(text):
    boxSize = 100
    print(f'{"":-^{boxSize+2}}')
    rows = len(text)
    for x in range(0,rows):
        columns = len(text[x])
        margin = boxSize//columns
        print ("|",end="")
        for y in text[x]:
            print(f'{y: ^{margin}}',end="")
        print ("|")
    print(f'{"":-^{boxSize+2}}')

def percentage(part, whole, size):
    return size * float(part) / float(whole)

def healthbar(HP,maxHP,size):
    if maxHP <= size:
        bar = ('|'*HP)
        result = (f'[{bar: <{maxHP}}]')
    elif maxHP > size:
        percent = math.ceil(percentage(HP,maxHP,size))
        bar = ('|'*percent)
        result = (f'[{bar: <{size}}]')
    return result

def ask (lowRange,highRange):
    while True:
        try:
            result = int(input("Choose a number: "))
        except:
            continue
        if lowRange <= result <= highRange:
            return result
        
def askList (numberList):
    while True:
        try:
            result = int(input("Choose a number: "))
        except:
            continue
        if result in numberList:
            return result

def getPartyList(unit,koed,enemy):
    if isinstance(unit,Character):
        party = []
        if enemy:
            for foe in foes:
                if koed:
                    party.append(foe) 
                elif foe.hp > 0:
                    party.append(foe)
        else:
            for char in chars:
                if koed:
                    party.append(char)
                elif char.hp > 0:
                    party.append(char)
        return party
    elif isinstance(unit,Foe):
        party = []
        for foe in foes:
            if koed:
                party.append(foe) 
            elif foe.hp > 0:
                party.append(foe)
        return party

def chooseTarget(char,skill):
    if skill.type == "onetarget":
        party = getPartyList(char,True,True)
        if len(party) != 1:
            display = [[f'-- Choose an target for {skill.name} --'],
                       [str(party.index(foe)+1)+ ". " + foe.name for foe in party]]
            box(display)
            result = ask(1,len(party))
            result = party[result-1]
        else:
            result = party[0]
        return result
    
def useSkill(char,skill):
    if skill.type == "onetarget":
        if isinstance(char,Character):
            target = chooseTarget(char,skill)
        damage = skill.damage
        target.hp -= damage
        time.sleep(pause)
        print(f"{char.name} used {skill.name}!")
        time.sleep(pause)
        print (f'{target.name} took {damage} damage!')
        if target.hp <= 0:
            target.hp = 0
            time.sleep(pause)
            print (f'{target.name} is defeated!')
        
def chooseSkill(char):
    display = [[f'-- Choose an action for {char.name} --'],
            [str(char.skills.index(s)+1)+ ". " + s.name for s in char.skills],
            [s.info for s in char.skills],
            [s.info2 for s in char.skills]]
    box(display)
    while True:
        result = ask(1,len(char.skills))
        result = char.skills[result-1]
        if char.costType == "spend":
            if result.cost <= char.sp:
                char.sp -= result.cost
                time.sleep(pause)
                print (f"Spent {result.cost} {char.term}")
                return result
            else:
                time.sleep(pause)
                print(f"Not enough {char.term}")

    return result

def displayBattleScreen():
    characters = [char for char in chars]
    enemies = [foe for foe in foes]
    boxList1 = [[foe.name for foe in enemies],
                [f"Health {foe.hp}/{foe.hpMax}" for foe in enemies],
                [healthbar(foe.hp,foe.hpMax,50) for foe in enemies],
                [foe.info for foe in enemies]]
    boxList2 = [[char.name for char in characters],
                [f"HP {char.hp}/{char.hpMax}" for char in characters],
                [healthbar(char.hp,char.hpMax,10) for char in characters],
                [char.info for char in characters]]
    box(boxList1)
    box(boxList2)

def unitTurn(unit):
    if isinstance(unit,Character):
        displayBattleScreen()
        useSkill(unit,chooseSkill(unit))
    if isinstance(unit,Foe):
        pass
    
def battleLoop():
    while len([char for char in chars if char.hp > 0]) > 0 and len([foe for foe in foes if foe.hp > 0]) > 0:
        for char in chars:
            if char.hp > 0:
                unitTurn(char)
                time.sleep(endTurnPause)
        for foe in foes:
            if foe.hp > 0:
                unitTurn(foe)
                time.sleep(endTurnPause)







chars = [Reimu()]
foes = [Marisa_Foe()]

battleLoop()