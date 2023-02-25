import math
import random
import time
import os

pause = 0.2
endTurnPause = 1
turnNumber = 0
chars = []
foes = []
dir_path = os.path.dirname(os.path.abspath(__file__))
save = 0
chars = []
foes = []

#skills
class Skill():
    def __init__(self):
        self.name = ''
        self.info = ""
        self.info2 = ""

class OneTargetAttack(Skill):
    def __init__(self):
        super().__init__()
        self.type = "onetarget"
        self.damage = 1

class SelfSupport(Skill):
    def __init__(self):
        super().__init__()
        self.type = "selfsupport"

class HomingAmulet(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 4
        self.cost = 0
        self.name = 'Homing Amulet'
        self.info = f"Cost: {self.cost} Points"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "spend"

class FantasySeal(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 10
        self.cost = 5
        self.name = 'Fastasy Seal'
        self.info = f"Cost: {self.cost} Points"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "spend"

class FantasyHeaven(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 40
        self.cost = 30
        self.name = 'Fantasy Heaven'
        self.info = f"Cost: {self.cost} Points"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "spend"

class Graze(SelfSupport):
    def __init__(self):
        super().__init__()
        self.name = "Graze"
        self.cooldownTurns = 2
        self.cooldown = 0
        self.info = f"Cooldown: 1 Turn"
        self.info2 = f"Graze incoming attacks."
        self.costType = "cooldown"

class MagicMissile(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 6
        self.cost = 2
        self.name = 'Magic Missile'
        self.info = f"Cost: {self.cost} Magic"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "spend"

class MasterSpark(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 30
        self.cost = 12
        self.name = 'Master Spark'
        self.info = f"Cost: {self.cost} Magic"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "spend"
    
class Focus(SelfSupport):
    def __init__(self):
        super().__init__()
        self.name = "Focus"
        self.cost = 0
        self.info = f"Cost: {self.cost} Magic"
        self.info2 = f"Recovers 5 Magic"
        self.costType = "spend"

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
        self.skills = [Graze(),HomingAmulet(),FantasySeal(),FantasyHeaven()]
        self.graze = False

class Marisa(Character):
    def __init__(self):
        super().__init__("Marisa Kirisame", 24)
        self.sp = 30
        self.update()

    def update(self):
        self.info = f'Magic {self.sp}'

#Ze bosses themselves
class Foe:
    def __init__(self, name="", hp=0):
        self.name = name
        self.hp = hp
        self.hpMax = hp
        self.nextSkill = 0
        self.nextTarget = 0
        self.insightSkill = 0
        self.insightTarget = 0
        self.insightDisplay = ''

class Marisa_Foe(Foe):
    def __init__(self):
        super().__init__("Marisa Kirisame", 50)
        self.sp = 20
        self.term = "Magic"

def box(text):
    boxSize = 100
    print(f'{"":-^{boxSize+2}}')
    rows = len(text)
    for x in range(0,rows):
        columns = len(text[x])
        margin = boxSize//columns
        print ("|",end="")
        for y in text[x]:
            y = str(y)
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
    
def useSkill(unit,skill):
    if skill.costType == "spend":
        unit.sp -= skill.cost
        time.sleep(pause)
        print(f"{unit.name} spends {skill.cost} {unit.term},")
    if skill.type == "onetarget":
        if isinstance(unit,Character):
            target = chooseTarget(unit,skill)
        if isinstance(unit,Foe):
            target = unit.nextTarget
        damage = skill.damage
        time.sleep(pause)
        print(f"{unit.name} used {skill.name}!")
        if isinstance(target,Reimu) and target.graze:
            target.sp += damage
            print(f"Reimu gains {damage} points as she grazes it!")
        else:
            target.hp -= damage
            time.sleep(pause)
            print (f'{target.name} took {damage} damage!')
            if target.hp <= 0:
                target.hp = 0
                time.sleep(pause)
                print (f'{target.name} is defeated!')
    elif skill.type == "selfsupport":
        time.sleep(pause)
        print(f"{unit.name} used {skill.name}!")
        if isinstance(skill,Graze):
            unit.graze = True
        if isinstance(skill,Focus):
            unit.sp += 5
            time.sleep(pause)
            print(f"{unit.name} recovered 5 Magic!")
        
def chooseSkill(char):
    display = [[f'-- Choose an action for {char.name} --'],
            [str(char.skills.index(s))+ ". " + s.name for s in char.skills],
            [s.info for s in char.skills],
            [s.info2 for s in char.skills]]
    box(display)
    while True:
        result = ask(0,len(char.skills))
        result = char.skills[result]
        if result.costType == "spend":
            if result.cost <= char.sp:
                return result
            else:
                time.sleep(pause)
                print(f"Not enough {char.term}")
        elif result.costType == "cooldown":
            if result.cooldown == 0:
                result.cooldown = result.cooldownTurns
                return result
            else:
                time.sleep(pause)
                if result.cooldown == 1:
                    print(f"{result.name} is on cooldown for {result.cooldown} more turn.")
                else:
                    print(f"{result.name} is on cooldown for {result.cooldown} more turns.")

def displayBattleScreen():
    characters = [char for char in chars]
    enemies = [foe for foe in foes]
    boxList1 = [["-- Boss --"],
                [foe.name for foe in enemies],
                [f"Health {foe.hp}/{foe.hpMax}" for foe in enemies],
                [healthbar(foe.hp,foe.hpMax,50) for foe in enemies],
                [foe.term+" "+str(foe.sp) for foe in enemies]]
    boxList2 = [["-- Party --"],
                [char.name for char in characters],
                [f"HP {char.hp}/{char.hpMax}" for char in characters],
                [healthbar(char.hp,char.hpMax,10) for char in characters],
                [char.term+" "+str(char.sp) for char in characters]]
    box(boxList1)
    box(boxList2)

def unitTurn(unit):
    if isinstance(unit,Character):
        displayBattleScreen()
        useSkill(unit,chooseSkill(unit))
    elif isinstance(unit,Foe):
        useSkill(unit,unit.nextSkill)

def marisaAI(foe):
        foe.insightSkill = random.randint(0, 2)
        foe.insightTarget = 2
        foe.nextTarget = chars[0]
        if turnNumber == 1:
            foe.nextSkill = MagicMissile()
        elif turnNumber == 2:
            foe.nextSkill = MasterSpark()
            foe.insightSkill = 2
        elif foe.sp < 2:
            foe.nextSkill = Focus()
        else:
            foe.nextSkill = MagicMissile()
        text = []
        if foe.insightSkill == 0:
            text.append(f"It's hard to tell what {foe.name} is doing.")
            text.append(f"{foe.name} is grinning.")
        elif foe.insightSkill == 1:
            if isinstance(foe.nextSkill,MagicMissile):
                text.append(f"{foe.name} is tracking Reimu's movement.")
                text.append(f"{foe.name} is preparing to fire.")
            elif isinstance(foe.nextSkill,Focus):
                text.append(f"{foe.name} is looking at her Mini-Hakkero.")
                text.append(f"{foe.name} is closing her eyes.")
        elif foe.insightSkill == 2:
            text.append(f"{foe.name} is getting ready to use {foe.nextSkill.name}!")
        foe.insightDisplay = random.choice(text) 

def insightTurn():
    display = []
    for foe in foes:
        if foe.hp > 0:
            if isinstance(foe,Marisa_Foe):
                marisaAI(foe)

    display = [["-- Insight --"],[foe.insightDisplay for foe in foes]]
    box(display)
    
def cleanup():
    for char in chars:
        if isinstance(char,Reimu) and char.graze:
                char.graze = False
        for skill in char.skills:
            if skill.costType == "cooldown":
                if skill.cooldown != 0:
                    skill.cooldown -= 1

    for foe in foes:
        pass

def battleLoop():
    global turnNumber
    turnNumber = 0
    while len([char for char in chars if char.hp > 0]) > 0 and len([foe for foe in foes if foe.hp > 0]) > 0:
        turnNumber += 1
        insightTurn()
        for char in chars:
            if char.hp > 0:
                unitTurn(char)
                input("\r")
            if not len([foe for foe in foes if foe.hp > 0]) > 0:
                break
        for foe in foes:
            if foe.hp > 0:
                unitTurn(foe)
                input("\r")
            if len([char for char in chars if char.hp > 0]) > 0:
                break
        cleanup()
    if not len([char for char in chars if char.hp > 0]) > 0:
        box([["Your party was defeated!"]])
        return False
    if not len([foe for foe in foes if foe.hp > 0]) > 0:
        box([["You defeated the boss!"]])
        return True

def startStory (file):
    x = open(f"{dir_path}/txt/story/{file}.txt","r",encoding='utf-8')
    y = x.readlines()
    for z in y:
        z = z.replace("\n","")
        print(z, end='')
        a = input(" ")
        if a == "skip":
            return
        if a == "menu":
            return "menu"

def mapMenu():
    pass

def newSave():
    txt_dir = os.path.join(dir_path, "txt", "save")

    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)

    # Get a list of all the txt files in the directory
    txt_files = [f for f in os.listdir(txt_dir) if f.endswith('.txt')]

    # If there are no txt files, create a new file with name '0.txt'
    if not txt_files:
        filename = os.path.join(txt_dir, '0.txt')
    else:
        # Otherwise, get the highest numbered file and add 1 to it
        max_num = max([int(f[:-4]) for f in txt_files])
        filename = os.path.join(txt_dir, f"{max_num+1}.txt")

    # Create the new file with the calculated name
    with open(filename, 'w') as f:
        f.write('0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

    # Extract the number from the filename and return it
    file_number = int(os.path.splitext(os.path.basename(filename))[0])
    return file_number

def readSave(position):
    txt_dir = os.path.join(dir_path, "txt", "save")
    filename = os.path.join(txt_dir, f"{save}.txt")

    if not os.path.exists(filename):
        raise ValueError(f"File {filename} does not exist")

    with open(filename, 'r') as f:
        content = f.read()

    try:
        value = int(content[position])
    except (ValueError, IndexError):
        raise ValueError(f"Invalid position {position} for file {filename}")

    return value

def updateSave(position):
    txt_dir = os.path.join(dir_path, "txt", "save")
    filename = os.path.join(txt_dir, f"{save}.txt")

    if not os.path.exists(filename):
        raise ValueError(f"File {filename} does not exist")

    with open(filename, 'r') as f:
        content = list(f.read())

    # Check if the position is valid
    if position >= len(content):
        raise ValueError(f"Invalid position {position} for file {filename}")

    # Update the content at the specified position
    if content[position] == '0':
        content[position] = '1'
    else:
        content[position] = '0'

    # Write the updated content back to the file
    with open(filename, 'w') as f:
        f.write(''.join(content))

def listSaveFiles():
    txt_dir = os.path.join(dir_path, "txt", "save")
    
    if not os.path.exists(txt_dir):
        return []
    
    # Get a list of all the txt files in the directory
    txt_files = [f for f in os.listdir(txt_dir) if f.endswith('.txt')]

    # Extract the number from the filename for each txt file
    file_numbers = [int(os.path.splitext(f)[0]) for f in txt_files]

    # Sort the file numbers in ascending order
    file_numbers.sort()

    # Check for gaps in the file numbers and add them to the list
    save_files = []
    last_num = -1
    for num in file_numbers:
        if num != last_num + 1:
            for missing_num in range(last_num + 1, num):
                save_files.append(missing_num)
        save_files.append(num)
        last_num = num

    return save_files

def mainMenu():
    while True:
        box([["-- Project Labyrinth --"],
            ["0. Continue"],
            ["1. New Game"],
            ["2. Quit"]])
        global save
        select = ask(0,2)
        if select == 0:
            l = listSaveFiles()
            box([["-- Choose a save file --"],[l]])
            save = askList(l)
            restPoint()
        if select == 1:
            save = newSave()
            startStory("newgame")
            restPoint()
        if select == 2:
            break

def area(place,actions):
    display = [[f"-- {place} --"],[]]
    n = 0
    for action in actions:
        display[1].append(f'{n}. {action}')
        n += 1
    box(display)
    index = ask(0, len(actions))
    return actions[index]

def hakureiShrine():
    global chars
    global foes
    while True:
        if not readSave(0):
            if not readSave(14):
                startStory("awake")
                place = "??????? Shrine"
                actions = ["Explore"]
            elif readSave(17):
                place = "Hakurei Shrine"
                actions = ["Re-enter"]
            elif readSave(15):
                place = "Hakurei Shrine"
                actions = ["Enter"]
            elif readSave(14):
                place = "??????? Shrine"
                actions = ["Talk"]
        elif readSave(0):
            if readSave(16):
                place = "Hakurei Shrine"
                actions = ["Look Around","Back"]
            elif not readSave(16):
                place = "Hakurei Shrine"
                actions = ["Enter the Portal"]

        act = area(place,actions)
        if act == "Explore":
            startStory("exploreHakurei")
            updateSave(14)
        elif act == "Talk":
            startStory("talkHakurei")
            updateSave(15)
        elif act == "Enter" or "Re-enter":
            if act == "Enter":
                startStory("enterHakurei")
            chars = [Reimu()]
            foes = [Marisa_Foe()]
            if battleLoop():
                startStory("victoryHakurei")
                updateSave(0)
            else:
                startStory("defeatHakurei")
                updateSave(17)
        elif act == "Look Around":
            startStory("lookHakurei")
        elif act == "Back" or "Enter the Portal":
            if act == "Enter the Portal":
                startStory("portalHakurei")
            break
              
def restPoint():
    while True:
        if not readSave(0):
            hakureiShrine()
        else:
            break

mainMenu()