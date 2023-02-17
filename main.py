import math
import random
import time
import skills

# All characters have these stats.
class Character:
    def __init__(self, name="", hp=0):
        self.name = name
        self.hp = hp
        self.hpMax = hp

class Reimu(Character):
    def __init__(self):
        super().__init__("Reimu Hakurei", 20)
        self.sp = 0
        self.update()
        self.skills = [skills.HomingAmulet]

    def update(self):
        self.info = f'Graze {self.sp}'
    
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
        self.sp = 30
        self.update()

    def update(self):
        self.info = f'Magic {self.sp}'

    def MagicMissile(self, target):
        target.hp -= 2
        print(f"{self.name} casts Magic Missile! {target.name} takes 2 damage.")

    def MasterSpark(self, target):
        damage = 15
        target.hp -= damage
        self.sp = 0
        self.update()
        print(f"{self.name} casts Master Spark! {target.name} takes {damage} damage. {self.name}'s Magic is now 0.")

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
            result = int(input(""))
        except:
            continue
        if lowRange <= result <= highRange:
            return result
        
def askList (numberList):
    while True:
        try:
            result = int(input(""))
        except:
            continue
        if result in numberList:
            return result

def getPartyList(unit):
    if issubclass(unit,Character):
        party = []
        
        return party
    elif issubclass(unit,Foe):
        pass

def getEnemyList(unit):
    if issubclass(unit,Character):
        pass
    elif issubclass(unit,Foe):
        pass

def chooseTarget(char,skillType):
    pass

def useSkill(char,skill):
    if skill.type == 1:
        target = chooseTarget(char,skill.type)

        print(f"{char.name} used {skill.name} on {target.name}")
        target

def chooseSkill(char):
    pass


def displayBattleScreen(foes,chars):
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

def displayTurn(char):
    pass


def battleLoop(foes, chars):
    displayBattleScreen(foes, chars)




battleLoop([Marisa_Foe()],[Reimu()])