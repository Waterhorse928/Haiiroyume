import math
import random
import time
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
        self.skills = [self.homingAmulet]

    def update(self):
        self.info = f'Graze {self.sp}'

# Attacks and Skills
    def homingAmulet(self, target):
        result = {"name":"Homing Amulet","damage":4,"info":"Deals 4 damage."}
        return result
    


class Marisa(Character):
    def __init__(self):
        super().__init__("Marisa Kirisame", 24)
        self.sp = 30
        self.update()

    def update(self):
        self.info = f'Magic {self.sp}'

class Boss:
    def __init__(self, name="", hp=0):
        self.name = name
        self.hp = hp
        self.hpMax = hp

class Marisa_Boss(Boss):
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

def displayBattleScreen(boss,chars):
    characters = [char for char in (chars) if char != 0]
    numberOfChar = len(characters)
    boxList1 = [[boss.name],
                [f"Health {boss.hp}/{boss.hpMax}"],
                [healthbar(boss.hp,boss.hpMax,50)],
                [boss.info]]
    boxList2 = [[char.name for char in characters],
                [f"HP {char.hp}/{char.hpMax}" for char in characters],
                [healthbar(char.hp,char.hpMax,10) for char in characters],
                [char.info for char in characters]]
    box(boxList1)
    if numberOfChar > 0:
        box(boxList2)

def displayTurn(char):
    displaySkills = [["Choose an action:"]]
    for x in char.skills:
        pass


    box([["Choose an action:"]])


def battleLoop(boss, chars):
    displayBattleScreen(boss, chars)




battleLoop(Marisa_Boss(),[Reimu()])