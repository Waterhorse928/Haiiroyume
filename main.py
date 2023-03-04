import math
import random
import time
import os

pause = 0.2
endTurnPause = 0.8
turnNumber = 0
chars = []
foes = []
dir_path = os.path.dirname(os.path.abspath(__file__))
save = 0

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

class OneTargetSupport(Skill):
    def __init__(self):
        super().__init__()
        self.type = "onesupport"

class PartyAttack(Skill):
    def __init__(self):
        super().__init__()
        self.type = "partyattack"
        self.damage = 1

class HomingAmulet(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 4
        self.name = 'Homing Amulet'
        self.info = f"No cost"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "free"

class FantasySeal(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 10
        self.cost = 5
        self.name = 'Fastasy Seal'
        self.info = f"Cost: {self.cost} Points"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class FantasyHeaven(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 40
        self.cost = 25
        self.name = 'Fantasy Heaven'
        self.info = f"Cost: {self.cost} Points"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class Graze(SelfSupport):
    def __init__(self):
        super().__init__()
        self.name = "Graze"
        self.cooldownTurns = 2
        self.cooldown = 0
        self.info = f"Cooldown: 1 Turn"
        self.info2 = f"Graze incoming attacks"
        self.info3 = f"to gain points"
        self.costType = "cooldown"

class MagicMissile(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 6
        self.cost = 2
        self.name = 'Magic Missile'
        self.info = f"Cost: {self.cost} Magic"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class MasterSpark(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 30
        self.cost = 12
        self.name = 'Master Spark'
        self.info = f"Cost: {self.cost} Magic"
        self.info2 = f"Deals {self.damage} damage"
        self.info3= f"Dodge incoming attacks"
        self.costType = "spend"
    
class Concentrate(SelfSupport):
    def __init__(self):
        super().__init__()
        self.name = "Concentrate"
        self.info = f"No cost"
        self.info2 = f"Recover 5 Magic"
        self.costType = "free"

class BronzeSword(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 3
        self.uses = 40
        self.name = 'Bronze Sword'
        self.info = f"/40 uses"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "uses"

class LevinSword(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 6
        self.uses = 8
        self.name = 'Levin Sword'
        self.info = f"/{self.uses} uses"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "uses"

class Nosferatu(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 8
        self.uses = 4
        self.name = 'Nosferatu'
        self.info = f"/{self.uses} uses"
        self.info2 = f"Deals {self.damage} damage"
        self.info3 = f"Recover half damage dealt"
        self.costType = "uses"

class Thoron(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 14
        self.uses = 2
        self.name = 'Thoron'
        self.info = f"/{self.uses} uses"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "uses"

class Elixir(OneTargetSupport):
    def __init__(self):
        super().__init__()
        self.uses = 1
        self.name = 'Elixir'
        self.info = f"/{self.uses} uses"
        self.info2 = f"Recovers all health."
        self.costType = "uses"

class StrikeFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 16
        self.name = 'Exalted Falchion - Strike'
        self.info = f"No cost"
        self.info2 = f"Deals {self.damage} damage"      
        self.costType = "free"  

class ExaltedFalchionFoe(SelfSupport):
    def __init__(self):
        super().__init__()
        self.heal = 20
        self.name = 'Exalted Falchion - Heal'
        self.info = f"No cost"
        self.info2 = f"Recover {self.heal} health"      
        self.costType = "free"  

class Strike(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 8
        self.name = 'Exalted Falchion - Strike'
        self.info = f"No cost"
        self.info2 = f"Deals {self.damage} damage"      
        self.costType = "free"  

class ExaltedFalchion(SelfSupport):
    def __init__(self):
        super().__init__()
        self.heal = 10
        self.name = 'Exalted Falchion - Heal'
        self.info = f"No cost"
        self.info2 = f"Recover {self.heal} health"      
        self.costType = "free"  

class FlyingHeadFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 10
        self.name = f"Flying Head"
        self.rank = 1
        self.info = f"Required: {self.rank} Head"
        self.info2 = f"Deals {self.damage} damage"      
        self.costType = "rank" 

class RokurokubiFlightFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 18
        self.name = f"Rokurokubi Flight"
        self.rank = 3
        self.info = f"Required: {self.rank} Heads"
        self.info2 = f"Deals {self.damage} damage"      
        self.costType = "rank" 

class MultiplicativeHeadFoe(PartyAttack):
    def __init__(self):
        super().__init__()
        self.damage = 8
        self.name = f"Multiplicative Head"
        self.rank = 5
        self.info = f"Required: {self.rank} Heads"
        self.info2 = f"Deals {self.damage} damage"  
        self.info3 = f"to all enemies"    
        self.costType = "rank" 

class SeventhHeadFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 32
        self.name = f"Seventh Head"
        self.rank = 7
        self.info = f"Required: {self.rank} Heads"
        self.info2 = f"Deals {self.damage} damage"      
        self.costType = "rank" 

class DullahanNightFoe(PartyAttack):
    def __init__(self):
        super().__init__()
        self.damage = 40
        self.name = f"Dullahan Night"
        self.cost = 10
        self.info = f"Cost: {self.cost} Heads"
        self.info2 = f"Deals {self.damage} damage"  
        self.info3 = f"to all enemies"    
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
        self.skills = [HomingAmulet(),Graze(),FantasySeal(),FantasyHeaven()]
        self.graze = False

class Marisa(Character):
    def __init__(self):
        super().__init__("Marisa Kirisame", 52)
        self.sp = 0
        self.term = "Magic"
        self.skills = [Concentrate(),MagicMissile(),MasterSpark()]
        self.dodge = False

class Robin(Character):
    def __init__(self):
        super().__init__("Robin", 56)
        self.sp = ""
        self.term = ""
        self.skills = [BronzeSword(),LevinSword(),Nosferatu(),Thoron(),Elixir()]

class Chrom(Character):
    def __init__(self):
        super().__init__("Chrom", 60)
        self.sp = ""
        self.term = ""
        self.skills = [Strike(),ExaltedFalchion()]

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
        self.insight = 0

class MarisaFoe(Foe):
    def __init__(self):
        super().__init__("Marisa Kirisame", 52)
        self.sp = 20
        self.term = "Magic"
        self.dodge = False

class RobinFoe(Foe):
    def __init__(self):
        super().__init__("Robin", 112)
        self.sp = ""
        self.term = ""
        self.thoron = False
        self.skills = [BronzeSword(),LevinSword(),Nosferatu(),Thoron(),Elixir()]

class ChromFoe(Foe):
    def __init__(self):
        super().__init__("Chrom", 120)
        self.sp = ""
        self.term = ""
        self.extraTurns = False
        self.nextList = []
        self.targetList = []

class SekibankiFoe(Foe):
    def __init__(self):
        super().__init__("Sekibanki", 96)
        self.sp = 0
        self.term = "Heads"

class KogasaFoe(Foe):
    def __init__(self):
        super().__init__("Kogasa Tatara", 70)
        self.sp = ""
        self.term = ""

class KurohebiFoe(Foe):
    def __init__(self):
        super().__init__("Kurohebi", 70)
        self.sp = ""
        self.term = ""

class MediasFoe(Foe):
    def __init__(self):
        super().__init__("Medias Moritake", 70)
        self.sp = ""
        self.term = ""

class WilliamFoe(Foe):
    def __init__(self):
        super().__init__("William", 70)
        self.sp = ""
        self.term = ""

class NeomaFoe(Foe):
    def __init__(self):
        super().__init__("Neoma", 70)
        self.sp = ""
        self.term = ""

class AlfonseFoe(Foe):
    def __init__(self):
        super().__init__("Alfonse Steadsteel", 70)
        self.sp = ""
        self.term = ""

class MarkFoe(Foe):
    def __init__(self):
        super().__init__("Mark Mapleridge", 70)
        self.sp = ""
        self.term = ""

def box(text):
    boxSize = 120
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
    party = []
    if isinstance(unit,Character):

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
    elif isinstance(unit,Foe):

        if enemy:
            for char in chars:
                if koed:
                    party.append(char)
                elif char.hp > 0:
                    party.append(char)
        else:
            for foe in foes:
                if koed:
                    party.append(foe) 
                elif foe.hp > 0:
                    party.append(foe)
    return party

def chooseTarget(char,skill):
    if skill.type == "onetarget" or skill.type == "onesupport":
        if skill.type == "onetarget":
            party = getPartyList(char,False,True)
        elif skill.type == "onesupport":
            party = getPartyList(char,False,False)
        if len(party) != 1:
            display = [[f'-- Choose an target for {skill.name} --'],
                       [str(party.index(unit)+1)+ ". " + unit.name for unit in party]]
            box(display)
            result = ask(1,len(party))
            result = party[result-1]
        else:
            result = party[0]
        return result

def useSkill(unit,skill):
    if isinstance(skill,MasterSpark):
        unit.dodge = True
    if skill.costType == "spend":
        unit.sp -= skill.cost
        time.sleep(pause)
        print(f"{unit.name} spends {skill.cost} {unit.term},")
    elif skill.costType == "uses":
        skill.uses -= 1
    if skill.type == "onetarget" or skill.type == "partyattack":
        targetList = []
        time.sleep(pause)
        print(f"{unit.name} used {skill.name}!")
        if skill.type == "onetarget":
            if isinstance(unit,Character):
                targetList.append(chooseTarget(unit,skill))
            if isinstance(unit,Foe):
                targetList.append(unit.nextTarget)
        if skill.type == "partyattack":
            targetList = getPartyList(unit,False,True)
        for target in targetList:
            damage = skill.damage
            if target.term == "Heads" and target.sp != 0:
                time.sleep(pause)
                print (f"{target.name} blocks the attack with one of her heads!")
                target.sp -= 1
                damage = round(damage/2)
            if getattr(target, 'graze', False):
                target.sp += damage
                print(f"Reimu gains {damage} points as she grazes it!")
            elif getattr(target, 'dodge', False):
                print(f"{target.name} dodges the attack!")
            else:
                hpBefore = target.hp
                target.hp -= damage
                if target.hp <= 0:
                    target.hp = 0
                time.sleep(pause)
                print (f'{target.name} took {hpBefore-target.hp} damage!')
                if isinstance(skill,Nosferatu):
                    hpHealed = unit.hp
                    unit.hp = min(unit.hpMax,(unit.hp + round((hpBefore-target.hp)/2)))
                    hpHealed = unit.hp - hpHealed
                    print(f"{unit.name} recovered {hpHealed} health!")
                if target.hp <= 0:
                    time.sleep(pause)
                    print (f'{target.name} is defeated!')
    elif skill.type == "selfsupport":
        time.sleep(pause)
        print(f"{unit.name} used {skill.name}!")
        if isinstance(skill,Graze):
            unit.graze = True
        if isinstance(skill,Concentrate):
            unit.sp += 5
            time.sleep(pause)
            print(f"{unit.name} recovered 5 Magic!")
        if isinstance(skill,ExaltedFalchionFoe or ExaltedFalchion):
            hpBefore = unit.hp
            unit.hp = min(unit.hpMax,unit.hp+skill.heal)
            time.sleep(pause)
            print(f"{unit.name} recovered {unit.hp-hpBefore} health!")
    elif skill.type == "onesupport":
        if isinstance(unit,Character):
            target = chooseTarget(unit,skill)
        if isinstance(unit,Foe):
            target = unit.nextTarget
        time.sleep(pause)
        print(f"{unit.name} used {skill.name}!")
        if isinstance(skill,Elixir):
            time.sleep(pause)
            print(f"{target.name} recovered {target.hpMax - target.hp} health!")
            target.hp = target.hpMax
        
def chooseSkill(char):
    display = [[f'-- Choose an action for {char.name} --'],
            [str(char.skills.index(s))+ ". " + s.name for s in char.skills],
            [str(s.uses) + s.info if s.costType == "uses" else s.info for s in char.skills],
            [s.info2 for s in char.skills],
            [s.info3 if hasattr(s, 'info3') else '' for s in char.skills]]
    box(display)
    while True:
        result = ask(0,len(char.skills))
        result = char.skills[result]
        if result.costType == "spend":
            if result.cost <= char.sp:
                return result
            else:
                time.sleep(pause)
                print(f"Not enough {char.term}.")
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
        elif result.costType == "uses":
            if result.uses != 0:
                return result
            else:
                time.sleep(pause)
                print(f"{result.name} can't be used anymore.")
        elif result.costType == "free":
            return result
        elif result.costType == "rank":
            if result.rank <= char.sp:
                return result
            else:
                time.sleep(pause)
                print(f"Not enough {char.term}.")

def displayBattleScreen():
    characters = [char for char in chars]
    enemies = [foe for foe in foes]
    boxList1 = [["-- Boss --"],
                [foe.name for foe in enemies],
                [f"Health {foe.hp}/{foe.hpMax}" for foe in enemies],
                [healthbar(foe.hp,foe.hpMax,50) for foe in enemies],
                [str(foe.sp)+" "+foe.term for foe in enemies]]
    boxList2 = [["-- Party --"],
                [char.name for char in characters],
                [f"HP {char.hp}/{char.hpMax}" for char in characters],
                [healthbar(char.hp,char.hpMax,10) for char in characters],
                [str(char.sp)+" "+char.term for char in characters]]
    box(boxList1)
    box(boxList2)

def unitTurn(unit):
    if isinstance(unit,Character):
        useSkill(unit,chooseSkill(unit))
    elif isinstance(unit,Foe):
        if getattr(unit, 'extraTurns', False):
            for x in unit.nextList:
                unit.nextTarget = x[1]
                useSkill(unit,x[0])
            unit.extraTurns = False
        elif isinstance(unit,SekibankiFoe):
            time.sleep(pause)
            if unit.sp == 1:
                s = ""
            else:
                s = "s"
            print(f"{unit.name} has {unit.sp} Head{s}!")
            if unit.sp >= 10:
                unit.nextSkill = DullahanNightFoe()
            elif unit.sp >= 7:
                unit.nextSkill = SeventhHeadFoe()
            elif unit.sp >= 5:
                unit.nextSkill = MultiplicativeHeadFoe()
            elif unit.sp >= 3:
                unit.nextSkill = RokurokubiFlightFoe()
            else:
                unit.nextSkill = FlyingHeadFoe()
            useSkill(unit,unit.nextSkill)
        else:
            useSkill(unit,unit.nextSkill)

def marisaAI(foe):
    foe.insightSkill = random.randint(0, 2)
    foe.insightTarget = 2
    foe.nextTarget = chars[0]
    if turnNumber == 1:
        foe.nextSkill = MagicMissile()
    elif turnNumber == 2:
        foe.nextSkill = MasterSpark()
        foe.dodge = True
        foe.insightSkill = 2
    elif foe.sp < 2:
        foe.nextSkill = Concentrate()
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
        elif isinstance(foe.nextSkill,Concentrate):
            text.append(f"{foe.name} is looking at her Mini-Hakkero.")
            text.append(f"{foe.name} is closing her eyes.")
    elif foe.insightSkill == 2:
        text.append(f"{foe.name} is getting ready to use {foe.nextSkill.name}!")
    foe.insightDisplay = random.choice(text) 

def robinAI(foe):
    foe.insight = random.randint(0, 5)
    foe.nextTarget = random.choice(getPartyList(chars[0],False,False))
    if foe.hp < foe.hpMax/2 and foe.skills[4].uses == 1:
        foe.nextSkill = foe.skills[4]
        foe.nextTarget = foe
        foe.thoron = False
    elif foe.thoron == True:
        foe.nextSkill = foe.skills[0]
        foe.thoron = False
    else:
        skills = foe.skills
        skills = [skill for skill in skills if skill.name != "Elixir"]
        if foe.hp >= foe.hpMax-4:
            skills = [skill for skill in skills if skill.name != "Nosferatu"]
        skills = [c for c in skills if c.uses != 0]
        foe.nextSkill = random.choice(skills)
        if isinstance(foe.nextSkill,Thoron):
            foe.thoron = True
    text = []
    if foe.insight == 0:
        text.append(f"{foe.name} is concealing his next move.")
        text.append(f"{foe.name} seems to be lost in thought.")
        text.append(f"{foe.name} is up to something.")
    elif foe.insight == 1:
        text.append(f"{foe.name} is planning to use {foe.nextSkill.name} on {foe.nextTarget.name}!")
    else:
        if isinstance(foe.nextSkill,BronzeSword):
            text.append(f"{foe.name} is conserving resources.")
            text.append(f"{foe.name} is trying to bait a dodge.")
            text.append(f"{foe.name} is preparing to use a sword.")
        if isinstance(foe.nextSkill,LevinSword):
            text.append(f"{foe.name} checks his Levin Sword for damage.")
            text.append(f"{foe.name} is ready to unleash an electric strike.")
            text.append(f"{foe.name} is preparing to use a sword.")
        if isinstance(foe.nextSkill,Nosferatu):
            text.append(f"{foe.name} is reciting a sinister incantation.")
            text.append(f"{foe.name} is worried about his condition.")
            text.append(f"{foe.name} is preparing to use a tome.")
        if isinstance(foe.nextSkill,Thoron):
            text.append(f"{foe.name} is about to use his trump card!")
            text.append(f"{foe.name} is ready to unleash an electric strike.")
            text.append(f"{foe.name} is preparing to use a tome.")
        if isinstance(foe.nextSkill,Elixir):
            text.append(f"{foe.name} is reaching for a vial at his belt.")
            text.append(f"{foe.name} is worried about his condition.")
            text.append(f"{foe.name} is trying to bait a dodge.")
        if isinstance(foe.nextTarget,Reimu):
            text.append(f"{foe.name} is studying Reimu's movements.")
        if isinstance(foe.nextTarget,Marisa):
            text.append(f"{foe.name} is betting Marisa is unprepared.")
    foe.insightDisplay = random.choice(text) 

def chromAI(foe):
    if len(foe.targetList) == 0:
        foe.targetList = getPartyList(foe,False,True)
    target = random.choice(foe.targetList)
    foe.targetList.remove(target)
    if foe.hp <= 110:
        foe.extraTurns = True
        foe.nextList = [[StrikeFoe(),target],[ExaltedFalchionFoe(),foe]]
    else:
        foe.nextSkill = StrikeFoe()
        foe.nextTarget = target
    text = []
    text.append(f"{foe.name} is going to attack {target.name}!")
    text.append(f"{foe.name} points his sword towards {target.name} in challenge.")
    text.append(f"{foe.name} is about to engage {target.name}!")
    text.append(f"{foe.name} prepares to strike {target.name}.")
    text.append(f"{target.name} is {foe.name}'s next target.")
    text.append(f"{foe.name} takes a stance facing {target.name}.")
    text.append(f"{foe.name} charges at {target.name}!")
    text.append(f"{foe.name}'s next target isn't clear.")
    foe.insightDisplay = random.choice(text) 

def sekibankiAI(foe):
    foe.sp += 5
    foe.insightTarget = random.randint(0, 1)
    targetWeak = random.choice([True, False])
    if targetWeak:
        party = getPartyList(foe,False,True)
        foe.nextTarget = min(party, key=lambda x: x.hp / x.hpMax)
    else:
        foe.nextTarget = random.choice(getPartyList(foe,False,True))
    text = []
    if foe.insightTarget <= 0:
        text.append(f"{foe.name} is going to attack {foe.nextTarget.name}!")
        text.append(f"{foe.name}'s heads are gathering around {foe.nextTarget.name}.")
        text.append(f"{foe.name} seems focused on {foe.nextTarget.name}.")
        if random.choice([True,False]):
            text.append(f"{foe.name} strikes a dramatic pose pointing at {foe.nextTarget.name}.")
    else:
        if foe.sp >=10:
            text.append(f"{foe.name} wants to use her strongest move.")
        if targetWeak:
            text.append(f"{foe.name} is planning to go for the weak link.")
            text.append(f"{foe.name} is tracking the party's condition.")
        else:
            text.append(f"{foe.name}'s heads are hard to keep track of.")
            text.append(f"{foe.name} is hiding her next attack.")
    foe.insightDisplay = random.choice(text) 

def kogasaAI(foe):
    pass

def kurohebiAI(foe):
    pass

def mediasAI(foe):
    pass

def williamAI(foe):
    pass

def neomaAI(foe):
    pass

def alfonseAI(foe):
    pass

def markAI(foe):
    pass

def insightTurn():
    display = []
    for foe in foes:
        if foe.hp > 0:
            if isinstance(foe,MarisaFoe):
                marisaAI(foe)
            if isinstance(foe,RobinFoe):
                robinAI(foe)
            if isinstance(foe,ChromFoe):
                chromAI(foe)
            if isinstance(foe,SekibankiFoe):
                sekibankiAI(foe)
            if isinstance(foe,KogasaFoe):
                kogasaAI(foe)
            if isinstance(foe,KurohebiFoe):
                kurohebiAI(foe)
            if isinstance(foe,MediasFoe):
                mediasAI(foe)
            if isinstance(foe,WilliamFoe):
                williamAI(foe)
            if isinstance(foe,NeomaFoe):
                neomaAI(foe)
            if isinstance(foe,AlfonseFoe):
                alfonseAI(foe)
            if isinstance(foe,MarkFoe):
                markAI(foe)

    display = [["-- Insight --"],[foe.insightDisplay for foe in foes]]
    box(display)
    
def cleanup():
    for char in chars:
        if getattr(char, 'graze', False):
            char.graze = False
        if getattr(char, 'dodge', False):
            char.dodge = False
        for skill in char.skills:
            if skill.costType == "cooldown":
                if skill.cooldown != 0:
                    skill.cooldown -= 1

    for foe in foes:
        if getattr(foe, 'dodge', False):
            foe.dodge = False
        if isinstance(foe,RobinFoe):
            foe.sp = foe.nextSkill.name
            foe.term = f"{foe.nextSkill.uses}{foe.nextSkill.info}"

def battleLoop():
    global turnNumber
    turnNumber = 0
    while len([char for char in chars if char.hp > 0]) > 0 and len([foe for foe in foes if foe.hp > 0]) > 0:
        turnNumber += 1
        insightTurn()
        displayBattleScreen()
        for char in chars:
            if char.hp > 0:
                unitTurn(char)
                print()
                time.sleep(endTurnPause)
            if not len([foe for foe in foes if foe.hp > 0]) > 0:
                break
        for foe in foes:
            if foe.hp > 0:
                unitTurn(foe)
                print()
                time.sleep(endTurnPause)
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

def characterSelect():
    charList = [Reimu()]
    if readSave(0):
        charList.append(Marisa())
    if readSave(1):
        charList.append(Robin())
    if readSave(2):
        charList.append(Chrom())
    charInt = [*range(0,len(charList))]
    charListReturn = []
    for y in range(0,min(4,len(charList))):
        display = [["-- Character Select --"]]
        for x in charInt:
            display.append([f"{x}. {charList[x].name}"])
        box(display)
        n = askList(charInt)
        charInt.remove(n)
        charListReturn.append(charList[n])
        print (f"Selected {charListReturn[y].name}")
    return charListReturn
    
def area(place,actions):
    display = [[f"-- {place} --"],[]]
    n = 0
    for action in actions:
        display[1].append(f'{n}. {action}')
        n += 1
    box(display)
    index = ask(0, len(actions))
    return actions[index]

def beginBattle(foe,win,lose):
    global chars
    global foes
    if not readSave(lose):
        startStory(f"enter{foe}")
        updateSave(lose)
    chars = characterSelect()
    foes = [globals()[foe + "Foe"]()]
    if battleLoop():
        startStory(f"victory{foe}")
        updateSave(win)
    else:
        startStory(f"defeat{foe}")
        updateSave(lose)

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
                actions = ["Enter the Gate"]
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
        elif act == "Enter the Gate" or act == "Re-enter":
            beginBattle("Marisa",0,17)
        elif act == "Look Around":
            startStory("lookHakurei")
        elif act == "Back" or act == "Enter the Portal":
            break

def barracks():
    global chars
    global foes
    while True:
        place = "Shepherds' Barracks"
        actions = []
        if not readSave(18):
            startStory("enterBarracks")
            updateSave(18)
        if not readSave(1):
            actions.append("Enter Robin's Gate")
            actions.append("Examine Chrom's Gate")
        elif not readSave(2):
            actions.append("Enter Chrom's Gate")
        actions.append("Look Around")
        actions.append("Back")

        act = area(place,actions)
        if act == "Enter Robin's Gate":
            beginBattle("Robin",1,19)
        elif act == "Examine Chrom's Gate":
            startStory("examineChromGate")
        elif act == "Enter Chrom's Gate":
            beginBattle("Chrom",2,20)
        elif act == "Look Around":
            startStory("lookBarracks")
        elif act == "Back":
            break

def area8(locale,unit1,unit2):
    global chars
    global foes
    while True:
        place = locale[0]
        actions = []
        if not readSave(locale[1]):
            startStory(f"arrive{locale[2]}")
            updateSave(locale[1])
        if not readSave(unit1[1]):
            actions.append(f"Enter {unit1[0]}'s Gate")
        if not readSave(unit2[1]):
            actions.append(f"Enter {unit2[0]}'s Gate")
        actions.append("Look Around")
        actions.append("Back")

        act = area(place,actions)
        if act == f"Enter {unit1[0]}'s Gate":
            beginBattle(unit1[3],unit1[1],unit1[2])
        elif act == f"Enter {unit2[0]}'s Gate":
            beginBattle({unit2[3]},unit2[1],unit2[2])
        elif act == "Look Around":
            startStory(f"look{locale[2]}")
        elif act == "Back":
            break

def restPoint():
    while True:
        if not readSave(0):
            hakureiShrine()
        if not readSave(16):
            startStory("portalHakurei")
            updateSave(16)
        place = "Rest Point"
        actions = []
        if readSave(0):
            actions.append("Hakurei Shrine")
            actions.append("Shepherds' Barracks")
        if readSave(1) and readSave(2):
            actions.append("Human Village")
            actions.append("Devanagara")
            actions.append("Arcton Fort")
            actions.append("Dream Arena")
        actions.append("Quit")
        act = area(place,actions)
        if act == "Hakurei Shrine":
            hakureiShrine()
        if act == "Shepherds' Barracks":
            barracks()
        if act == "Human Village":
            area8(["Human Village",29,"Village"],["Sekibanki",3,21,"Sekibanki"],["Kogasa Tatara",4,22,"Kogasa"])
        if act == "Devanagara":
            area8(["Devanagara",30,"Devanagara"],["Kurohebi",5,23,"Kurohebi"],["Medias Moritake",6,24,"Medias"]) 
        if act == "Arcton Fort":
            area8(["Arcton Fort",31,"Fort"],["William",7,25,"William"],["Neoma",8,26,"Neoma"]) 
        if act == "Dream Arena":
            area8(["Dream Arena",30,"Arena"],["Alfonse Steadsteel",9,27,"Alfonse"],["Mark Mapleridge",10,28,"Mark"]) 
        if act == "My Castle":
            pass
        if act == "Quit":
            break
        
mainMenu()