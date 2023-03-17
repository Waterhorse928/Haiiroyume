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

#Skill Types
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

class TwoTargetSupport(Skill):
    def __init__(self):
        super().__init__()
        self.type = "twosupport"

class PartyAttack(Skill):
    def __init__(self):
        super().__init__()
        self.type = "partyattack"
        self.damage = 1

class OneTargetDebuff(Skill):
    def __init__(self):
        super().__init__()
        self.type = "onedebuff"

#Reimu
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

#Marisa
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

#Robin
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
        self.info3 = f"Recover health"
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
        self.info3 = f"Choose one ally"
        self.costType = "uses"

#Chrom
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

#Sekibanki
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
        self.info2 = f"Deals Heads*4 damage"  
        self.info3 = f"to all enemies"    
        self.costType = "spendall" 

class FlyingHead(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 5
        self.name = f"Flying Head"
        self.rank = 1
        self.info = f"Required: {self.rank} Head"
        self.info2 = f"Deals {self.damage} damage"      
        self.costType = "rank" 

class RokurokubiFlight(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 6
        self.name = f"Rokurokubi Flight"
        self.rank = 3
        self.info = f"Required: {self.rank} Heads"
        self.info2 = f"Deals {self.damage} damage"  
        self.info3 = f"Gain 1 Head" 
        self.costType = "rank" 

class MultiplicativeHead(SelfSupport):
    def __init__(self):
        super().__init__()
        self.name = f"Multiplicative Head"
        self.rank = 5
        self.info = f"Required: {self.rank} Heads"
        self.info2 = f"Gain 3 Heads."   
        self.costType = "rank" 

class SeventhHead(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 14
        self.name = f"Seventh Head"
        self.rank = 7
        self.info = f"Required: {self.rank} Heads"
        self.info2 = f"Deals {self.damage} damage"      
        self.costType = "rank" 

class DullahanNight(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 30
        self.name = f"Dullahan Night"
        self.cost = 10
        self.info = f"Cost: {self.cost} Heads"
        self.info2 = f"Deals x3 damage"
        self.info3 = f"x = number of Heads"
        self.costType = "spendall" 

#Kogasa
class DanmakuFoe(PartyAttack):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.name = 'Danmaku'
        self.info = f"No cost"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "free"

class RainyNightFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 12
        self.cost = 15
        self.name = "A Rainy Night's Ghost Story"
        self.info = f"Cost: {self.cost} Terror"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class NightTrainFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 25
        self.cost = 30
        self.name = "A Forgotten Umbrella's Night Train"
        self.info = f"Cost: {self.cost} Terror"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class KarakasaFlashFoe(PartyAttack):
    def __init__(self):
        super().__init__()
        self.damage = 50
        self.cost = 60
        self.name = "Karakasa Surprising Flash"
        self.info = f"Cost: {self.cost} Terror"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class Danmaku(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 1
        self.name = 'Danmaku'
        self.info = f"No cost"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "free"

class RainyNight(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 12
        self.cost = 15
        self.name = "A Rainy Night's Ghost Story"
        self.info = f"Cost: {self.cost} Terror"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class NightTrain(OneTargetSupport):
    def __init__(self):
        super().__init__()
        self.damage = 25
        self.cost = 30
        self.name = "A Forgotten Umbrella's Night Train"
        self.info = f"Cost: {self.cost} Terror"
        self.info2 = f"Dodge this turn"
        self.info3 = f'Choose one ally'
        self.costType = "spend"

class KarakasaFlash(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 50
        self.cost = 100
        self.name = "Karakasa Surprising Flash"
        self.info = f"Cost: {self.cost} Terror"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

#Kurohebi
class BlindShotFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 4
        self.cost = 1
        self.name = 'Blind Shot'
        self.info = f"Cost: {self.cost} Points"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class SlitSnakeFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 32
        self.cost = 1
        self.name = 'Slit Snake'
        self.info = f"No cost"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class ImperceptibleFoe(PartyAttack):
    def __init__(self):
        super().__init__()
        self.damage = 24
        self.cost = 3
        self.name = 'Imperceptible'
        self.info = f"No cost"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class BlindShot(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.name = 'Blind Shot'
        self.info = f"No cost"
        self.info2 = f"Deals {self.damage} damage"
        self.info3 = f"10% chance to blind"
        self.costType = "free"

class SlitSnake(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 12
        self.cost = 1
        self.name = 'Slit Snake'
        self.info = f"Cost: {self.cost} Darkness"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class Imperceptible(OneTargetDebuff):
    def __init__(self):
        super().__init__()
        self.cost = 3
        self.name = 'Imperceptible'
        self.info = f"Cost: {self.cost} Darkness"
        self.info2 = f"Blinds the target"
        self.costType = "spend"

#Medias
class EmperorDanceFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 20
        self.cost = 0
        self.name = "Emperor Dance"
        self.info = f"Cost: {self.cost} Momentum"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "free"

class PenguinHighwayFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 40
        self.cost = 10
        self.name = "Penguin Highway"
        self.info = f"Cost: {self.cost} Momentum"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class EmperorsClawFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 60
        self.cost = 30
        self.name = "Emperor's Claw"
        self.info = f"Cost: {self.cost} Momentum"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class EmperorDance(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 3
        self.cost = 0
        self.name = "Emperor Dance"
        self.info = f"No cost"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "free"

class PenguinHighway(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 10
        self.cost = 5
        self.name = "Penguin Highway"
        self.info = f"Cost: {self.cost} Momentum"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class EmperorsClaw(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 30
        self.cost = 20
        self.name = "Emperor's Claw"
        self.info = f"Cost: {self.cost} Momentum"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

#William
class WarpFoe(OneTargetDebuff):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.name = "Warp"
        self.info = f"Cost: {self.cost} Fate"
        self.info2 = f"Redirects the target's attack"
        self.costType = "spend"

class EllightFoe(PartyAttack):
    def __init__(self):
        super().__init__()
        self.cost = 3
        self.damage = 20
        self.name = "Ellight"
        self.info = f"Cost: {self.cost} Fate"
        self.info2 = f"Deals {self.damage} damage"
        self.info3 = f"to all enemies"
        self.costType = "spend"

class HealFoe(SelfSupport):
    def __init__(self):
        super().__init__()
        self.cost = 9
        self.heal  = 60
        self.name = "Heal"
        self.info = f"Cost: {self.cost} Fate"
        self.info2 = f"Recovers {self.heal} health"
        self.costType = "spend"

class Warp(TwoTargetSupport):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.name = "Warp"
        self.info = f"Cost: {self.cost} Fate"
        self.info2 = f"Swaps two target's fates"
        self.costType = "spend"

class Ellight(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.cost = 3
        self.damage = 8
        self.name = "Ellight"
        self.info = f"Cost: {self.cost} Fate"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class Heal(SelfSupport):
    def __init__(self):
        super().__init__()
        self.cost = 8
        self.heal  = 30
        self.name = "Heal"
        self.info = f"Cost: {self.cost} Fate"
        self.info2 = f"Recovers {self.heal} health"
        self.costType = "spend"

#Neoma
class FluxFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 15
        self.cost = 0
        self.name = 'Flux'
        self.info = f"Cost: {self.cost} Spirits"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class LunaFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 20
        self.cost = 2
        self.name = 'Luna'
        self.info = f"Cost: {self.cost} Spirits"
        self.info2 = f"Deals {self.damage} damage"
        self.info3 = f"30% crit: 3* damage and heal"
        self.costType = "spend"

class InexorableDestinyFoe(OneTargetDebuff):
    def __init__(self):
        super().__init__()
        self.cost = 12
        self.name = 'Inexorable Destiny'
        self.info = f"Cost: {self.cost} Spirits"
        self.info2 = f"Target suffers destiny"
        self.info3 = f"earlier than expected"
        self.costType = "spend"

#Alfonse
class ScorchingSlashFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 50
        self.cost = 10
        self.name = 'Scorching Slash'
        self.info = f"+{self.cost} Heat"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "gain"

class SiroccoGustFoe(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 20
        self.cost = 10
        self.name = 'Sirocco Gust'
        self.info = f"-{self.cost} Heat"
        self.info2 = f"Deals {self.damage} damage"
        self.costType = "spend"

class BlastOfSpeedFoe(SelfSupport):
    def __init__(self):
        super().__init__()
        self.name = 'Scorching Slash'
        self.info = f"No cost to activate"
        self.info2 = f"Use Heat to dodge attacks"
        self.info3 = f"Each dodge costs 5 Heat"
        self.costType = "free"
 
# All characters have these stats.
class Character:
    def __init__(self, name="", hp=0):
        self.name = name
        self.hp = hp
        self.hpMax = hp
        self.blind = False
        self.redirect = None
        self.warp1 = False
        self.warp2 = False

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

class Sekibanki(Character):
    def __init__(self):
        super().__init__("Sekibanki", 32)
        self.sp = 0
        self.term = "Heads"
        self.skills = [FlyingHead(),RokurokubiFlight(),MultiplicativeHead(),SeventhHead(),DullahanNight()]

class Kogasa(Character):
    def __init__(self):
        super().__init__("Kogasa Tatara", 64)
        self.sp = 0
        self.term = "Terror"
        self.skills = [Danmaku(),RainyNight(),NightTrain(),KarakasaFlash()]

class Kurohebi(Character):
    def __init__(self):
        super().__init__("Kurohebi", 22)
        self.sp = 5
        self.term = "Darkness"
        self.skills = [BlindShot(),SlitSnake(),Imperceptible()]
        self.recover = False

class Medias(Character):
    def __init__(self):
        super().__init__("Medias Moritake", 62)
        self.sp = 0
        self.term = "Momentum"
        self.skills = [EmperorDance(),PenguinHighway(),EmperorsClaw()]

class William(Character):
    def __init__(self):
        super().__init__("William", 46)
        self.sp = 0
        self.term = "Fate"
        self.skills = [Warp(),Ellight(),Heal()]

class Neoma(Character):
    def __init__(self):
        super().__init__("Neoma", 38)
        self.sp = 0
        self.term = "Spirits"
        self.skills = []

class Alfonse(Character):
    def __init__(self):
        super().__init__("Alfonse Steadsteel", 50)
        self.sp = 0
        self.term = "Steam"
        self.skills = []

class Mark(Character):
    def __init__(self):
        super().__init__("Mark Mapleridge", 48)
        self.sp = 20
        self.term = "Spirit"
        self.skills = []

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
        self.hidehp = False
        self.blind = False
        self.redirect = None
        self.warp1 = False
        self.warp2 = False

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
        super().__init__("Kogasa Tatara", 192)
        self.sp = 0
        self.term = "Terror"
        self.extraTurns = False
        self.nextList = []
        self.targetList = []

class KurohebiFoe(Foe):
    def __init__(self):
        super().__init__("Kurohebi",132)
        self.sp = 10
        self.term = "Darkness"
        self.skip = 0
        self.recover = False
        self.counter = False
        self.counterSkill = SlitSnakeFoe()
        self.hidehp = True

class MediasFoe(Foe):
    def __init__(self):
        super().__init__("Medias Moritake",248)
        self.sp = 0
        self.term = "Momentum"
        self.deflection = False
        self.hit = True

class WilliamFoe(Foe):
    def __init__(self):
        super().__init__("William", 138)
        self.sp = 3
        self.term = "Fate"
        self.skip = 0

class NeomaFoe(Foe):
    def __init__(self):
        super().__init__("Neoma", 112)
        self.sp = 13
        self.term = "Spirits"

class AlfonseFoe(Foe):
    def __init__(self):
        super().__init__("Alfonse Steadsteel", 120)
        self.sp = 0
        self.term = "Heat"
        self.blast = False
        self.over = False
        self.cool = False

class MarkFoe(Foe):
    def __init__(self):
        super().__init__("Mark Mapleridge", 70)
        self.sp = ""
        self.term = ""

def box(text):
    # boxSize = os.get_terminal_size().columns - 2
    boxSize = 120
    print(f'{"":-^{boxSize+2}}')
    rows = len(text)
    for x in range(0,rows):
        if not text[x]:
            continue
        columns = len(text[x])
        margin = boxSize//columns
        print("|",end="")
        for y in text[x]:
            y = str(y)
            print(f'{y: ^{margin}}',end="")
        print("|")
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

def garble(s, prob=0.5):
    # Create a list of garbled characters | string.ascii_letters
    garbled_chars = [random.choice([" "]) if random.random() < prob else c for c in s]

    # Join the garbled characters back into a string
    garbled_s = ''.join(garbled_chars)
    
    return garbled_s

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
    if skill.type == "onetarget" or skill.type == "onesupport" or skill.type == "onedebuff":
        if skill.type == "onetarget" or skill.type == "onedebuff":
            party = getPartyList(char,False,True)
        elif skill.type == "onesupport":
            party = getPartyList(char,False,False)
        if len(party) != 1:
            display = [[f'-- Choose a target for {skill.name} --'],
                       [str(party.index(unit)+1)+ ". " + unit.name for unit in party]]
            box(display)
            result = ask(1,len(party))
            result = party[result-1]
        else:
            result = party[0]
        return result
    if skill.type == "twosupport":
        party = getPartyList(char,False,False)
        result = []
        while True:
            display = [[f'-- Choose a target for {skill.name} --'],
                    [str(party.index(unit)+1)+ ". " + unit.name for unit in party]]
            box(display)
            input = ask(1,len(party))
            result.append(party[input-1])
            if len(result) == 2:
                break

def useSkill(unit,skill):
    #skip damage step
    skip = False
    #skip reaction step
    skipAll = False
    #Nosfeatsu crit
    crit = False
    #Skills specail stats
    if isinstance(skill,MasterSpark):
        unit.dodge = True
    elif isinstance(skill,DullahanNightFoe):
        skill.damage = unit.sp*4
    elif isinstance(skill,DullahanNight):
        skill.damage = unit.sp*3
    elif isinstance(skill,LunaFoe):
        if random.random() <= 0.5:
            crit = True
            time.sleep(pause)
            print(f"Critical!")
    if skill.costType == "spend":
        unit.sp -= skill.cost
        time.sleep(pause)
        print(f"{unit.name} spends {skill.cost} {unit.term},")
    if skill.costType == "spendall":
        spent = unit.sp
        unit.sp = 0
        time.sleep(pause)
        print(f"{unit.name} spends {spent} {unit.term},")
    elif skill.costType == "uses":
        skill.uses -= 1
    elif skill.costType == "gain":
        unit.sp += skill.cost
        time.sleep(pause)
        print(f"{unit.name} gains {skill.cost} {unit.term},")

    if skill.type == "onetarget" or skill.type == "partyattack":
        targetList = []
        time.sleep(pause)
        print(f"{unit.name} used {skill.name}!")
        if skill.type == "onetarget":
            if isinstance(unit,Character):
                targetList.append(chooseTarget(unit,skill))
            if isinstance(unit,Foe):
                targetList.append(unit.nextTarget)
            if unit.redirect:
                targetList = [unit.redirect]
                time.sleep(pause)
                print(f"{unit.name}'s attack is redirected at {unit.redirect.name}!")
        if skill.type == "partyattack":
            targetList = getPartyList(unit,False,True)
        for target in targetList:
            if target.warp1:
                for x in getPartyList(unit,False,False)+getPartyList(unit,False,True):
                    if x.warp2:
                        target = x
            if target.warp2:
                for x in getPartyList(unit,False,False)+getPartyList(unit,False,True):
                    if x.warp1:
                        target = x
            if target.hp == 0:
                time.sleep(pause)
                print (f"{target.name} is already defeated!")
                skipAll = True
            damage = skill.damage
            if isinstance(skill,LunaFoe) and crit:
                damage *= 2
            if isinstance(target,Kurohebi) and target.sp != 0 and unit.blind == False and getattr(target, 'dodge', False) == False and skipAll != True:
                time.sleep(pause)
                print (f"{target.name} is cloaked in darkness!")
                target.sp -= 1
                target.dodge = True
            if getattr(target, "blast", False) and target.sp >= 5 and skipAll != True:
                time.sleep(pause)
                print (f"{target.name} is using blasts of heated air to dodge!")
                target.sp -= 5
                target.dodge = True
            if getattr(unit, "deflection", False) and skipAll != True:
                if getattr(target, 'graze', False):
                    time.sleep(pause)
                    print(f"{unit.name} caught {target.name}'s dodge!")
                    target.graze = False
                elif getattr(target, 'dodge', False):
                    time.sleep(pause)
                    print(f"{unit.name} caught {target.name}'s dodge!")
                    target.dodge = False
                else:
                    time.sleep(pause)
                    print(f"{unit.name} overshot {target.name} trying to read a dodge!")
                    skipAll = True
            if getattr(target, 'graze', False) and skipAll != True:
                target.sp += damage
                time.sleep(pause)
                print(f"Reimu gains {damage} points as she grazes it!")
                skip = True
            elif hasattr(target, 'counter') and unit in target.counter and skipAll != True:
                time.sleep(pause)
                print(f"{target.name} anticipated the attack!")
                time.sleep(pause)
                print(f"{target.name} dodges and counters!")
                target.nextTarget = unit
                useSkill(target,target.counterSkill)
                skip = True
            elif unit.blind and skipAll != True:
                time.sleep(pause)
                print(f"{unit.name} can't see!")
                time.sleep(pause)
                print(f"{target.name} dodges the attack!")
                skip = True
            elif getattr(target, 'dodge', False) and skipAll != True:
                time.sleep(pause)
                print(f"{target.name} dodges the attack!")
                skip = True
            elif target.term == "Heads" and target.sp != 0 and skipAll != True:
                time.sleep(pause)
                print (f"{target.name} blocks the attack with one of her heads!")
                target.sp -= 1
                damage = round(damage/2)
            elif target.term == "Heat" and skipAll != True:
                if target.sp <= 20:
                    time.sleep(pause)
                    print (f"{target.name}'s armor absorbs part of the blow!")
                    if isinstance(target,Foe):
                        target.sp += 2
                    if isinstance(target,Character):
                        target.sp += 5
                    damage = round(damage/2)
                else:
                    time.sleep(pause)
                    print (f"{target.name}'s vulnerable!")
                    damage = round(damage*2)
            if skip != True and skipAll != True:
                hpBefore = target.hp
                target.hp -= damage
                if target.hp <= 0:
                    target.hp = 0
                time.sleep(pause)
                print (f'{target.name} took {hpBefore-target.hp} damage!')
                if isinstance(skill,Nosferatu) or crit:
                    hpHealed = unit.hp
                    unit.hp = min(unit.hpMax,(unit.hp + round((hpBefore-target.hp)/2)))
                    hpHealed = unit.hp - hpHealed
                    time.sleep(pause)
                    print(f"{unit.name} recovered {hpHealed} health!")
                if isinstance(skill,RokurokubiFlight):
                    unit.sp += 1
                    time.sleep(pause)
                    print(f"{unit.name} gained 1 Head!")
                if isinstance(skill,BlindShotFoe) or isinstance(skill,ImperceptibleFoe):
                    target.blind = 2
                    time.sleep(pause)
                    print(f"{target.name} is blinded!")
                if isinstance(skill,BlindShot):
                    if random.random() <= 0.1:
                        target.blind = 2
                        time.sleep(pause)
                        print(f"{target.name} is blinded!")  
                if target.hp <= 0:
                    time.sleep(pause)
                    print (f'{target.name} is defeated!')
                    for x in getPartyList(unit,False,False)+getPartyList(unit,False,True):
                        if x.term == "Spirits":
                            x.sp += 5
                            time.sleep(pause)
                            print (f'{x.name} gained 5 Spirits!')
                if unit.term == "Momentum":
                    unit.sp += hpBefore-target.hp
                    time.sleep(pause)
                    print (f'{unit.name} gained {hpBefore-target.hp} Momentum!')
                for x in getPartyList(unit,False,False)+getPartyList(unit,False,True):
                    if x.term == "Terror":
                        x.sp += hpBefore-target.hp
                        time.sleep(pause)
                        print (f'{x.name} gained {hpBefore-target.hp} Terror!')

    elif skill.type == "selfsupport":
        time.sleep(pause)
        print(f"{unit.name} used {skill.name}!")
        if isinstance(skill,Graze):
            unit.graze = True
        if isinstance(skill,Concentrate):
            unit.sp += 5
            time.sleep(pause)
            print(f"{unit.name} recovered 5 Magic!")
        if isinstance(skill, ExaltedFalchionFoe) or isinstance(skill, ExaltedFalchion) or isinstance(skill, HealFoe):
            hpBefore = unit.hp
            unit.hp = min(unit.hpMax,unit.hp+skill.heal)
            time.sleep(pause)
            print(f"{unit.name} recovered {unit.hp-hpBefore} health!")
        if isinstance(skill,MultiplicativeHead):
            unit.sp += 3
            time.sleep(pause)
            print(f"{unit.name} gained 3 Heads!")
        
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
        if isinstance(skill, Heal):
            hpBefore = target.hp
            target.hp = min(target.hpMax,target.hp+skill.heal)
            time.sleep(pause)
            print(f"{target.name} recovered {target.hp-hpBefore} health!")
        if isinstance(skill,NightTrain):
            time.sleep(pause)
            print(f"{target.name} is hidden!")
            target.dodge = True

    elif skill.type == "twosupport":
        if isinstance(unit,Character):
            targets = chooseTarget(unit,skill)
        if isinstance(unit,Foe):
            targets = unit.nextTarget
        time.sleep(pause)
        print(f"{unit.name} used {skill.name}!")
    
    elif skill.type == "onedebuff":
        if isinstance(unit,Character):
            target = chooseTarget(unit,skill)
        if isinstance(unit,Foe):
            target = unit.nextTarget
        time.sleep(pause)
        print(f"{unit.name} used {skill.name}!")
        if target.hp == 0:
            time.sleep(pause)
            print (f"{target.name} is already defeated!")
            for x in getPartyList(unit,False,False)+getPartyList(unit,False,True):
                if x.term == "Fate":
                    x.sp += 1
                    time.sleep(pause)
                    print(f"{x.name} gained 1 Fate!")
            return
        if isinstance(skill,Imperceptible):
            target.blind = 2
            time.sleep(pause)
            print(f"{target.name} is blinded!")
        if isinstance(skill,WarpFoe):
            target.redirect = unit.warpTarget
            #time.sleep(pause)
            #print(f"{target.name}'s attacks are being redirected!")
        if isinstance(skill,InexorableDestinyFoe):
            target.hp = 0
            time.sleep(pause)
            print(f"{target.name} collapsed!")
            for x in getPartyList(unit,False,False)+getPartyList(unit,False,True):
                if x.term == "Spirits":
                    x.sp += 5
                    time.sleep(pause)
                    print (f'{x.name} gained 5 Spirits!')

    for x in getPartyList(unit,False,False)+getPartyList(unit,False,True):
        if x.term == "Fate":
            x.sp += 1
            time.sleep(pause)
            print(f"{x.name} gained 1 Fate!")

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
        if result.costType == "spend" or result.costType == "spendall":
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
                [f"Health {foe.hp}/{foe.hpMax}" if not foe.hidehp else garble(f"Health {foe.hp}/{foe.hpMax}",prob = 1.0) for foe in enemies],
                [healthbar(foe.hp,foe.hpMax,50) for foe in enemies],
                [str(foe.sp)+" "+foe.term for foe in enemies]]
    boxList2 = [["-- Party --"],
                [char.name for char in characters],
                [f"HP {char.hp}/{char.hpMax}" for char in characters],
                [healthbar(char.hp,char.hpMax,10) for char in characters],
                [str(char.sp)+" "+char.term for char in characters]]
    if isinstance(foes[0],KurohebiFoe):
        garbleness = foes[0].sp / 20
        boxList1 = [[garble(s,prob=garbleness) for s in sublist] for sublist in boxList1]
        boxList2 = [[garble(s,prob=garbleness) for s in sublist] for sublist in boxList2]
    box(boxList1)
    box(boxList2)

def unitTurn(unit):
    if isinstance(unit,Character):
        if isinstance(unit,Kurohebi):
            if unit.sp == 0 and unit.recover == False:
                unit.recover = True
                time.sleep(pause)
                print(f"{unit.name} spends the turn recovering.")
                return
        if isinstance(unit,Robin):
            if (unit.skills[0].uses+unit.skills[1].uses+unit.skills[2].uses+unit.skills[3].uses+unit.skills[4].uses) == 0:
                time.sleep(pause)
                print(f"{unit.name}'s weapons are all broken.")
                return
        if isinstance(unit,William):
            if unit.sp == 0:
                time.sleep(pause)
                print(f"{unit.name} has no Fate to change.")
                return
            if unit.sp < 3 and len(getPartyList(unit,False,False)) == 1:
                time.sleep(pause)
                print(f"{unit.name} has no Fate to change.")
                return
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
    party = getPartyList(foe,False,True)
    if targetWeak:
        foe.nextTarget = min(party, key=lambda x: x.hp / x.hpMax)
    else:
        foe.nextTarget = random.choice(party)
    party.remove(foe.nextTarget)
    text = []
    if foe.insightTarget == 0:
        text.append(f"{foe.name} is going to attack {foe.nextTarget.name}!")
        text.append(f"{foe.name}'s heads are gathering around {foe.nextTarget.name}.")
        text.append(f"{foe.name} seems focused on {foe.nextTarget.name}.")
        if random.choice([True,False]):
            text.append(f"{foe.name} strikes a dramatic pose pointing at {foe.nextTarget.name}.")
    if foe.insightTarget == 1:
        if len(party) >= 1:
            decoy = random.choice(party)
            fakeList = [foe.nextTarget.name,decoy.name]
            random.shuffle(fakeList)
            text.append(f"{foe.name}'s heads are gathering around {fakeList[0]} and {fakeList[1]}.")
        if targetWeak:
            text.append(f"{foe.name} is planning to go for the weak link.")
        else:
            text.append(f"{foe.name}'s heads are hard to keep track of.")
    foe.insightDisplay = random.choice(text) 

def kogasaAI(foe):
    text = []
    target = random.choice(getPartyList(foe,False,True))
    if foe.sp >= 60:
        foe.nextSkill = KarakasaFlashFoe()
        foe.nextTarget = target
        text.append(f"The constant rain abruptly stops falling...")
        text.append(f"All at once the night is deafeningly silent...")
    elif foe.sp >= 30  and random.choice([True,False]):
        foe.extraTurns = True
        foe.nextList = [[DanmakuFoe(),target],[NightTrainFoe(),target]]
        text.append(f"The sound of a train starts to fill the night...")
        text.append(f"{foe.name} is sneaking up behind {target.name}.")
        text.append(f"{foe.name} thinks that she can scare {target.name}.")
    elif foe.sp >= 15 and random.choice([True,False]):
        foe.extraTurns = True
        foe.nextList = [[DanmakuFoe(),target],[RainyNightFoe(),target]]
        text.append(f"The rain is getting worse...")
        text.append(f"{target.name} spots {foe.name} hiding behind a box.")
        text.append(f"{target.name} can see {foe.name}'s umbrella poking out from around a corner.")
    else:
        foe.nextSkill = DanmakuFoe()
        foe.nextTarget = target
        if turnNumber == 1:
            text.append(f"{foe.name} is nowhere in sight.")
        else:
            text.append(f"The rain contines to fall...")
    foe.insightDisplay = random.choice(text) 

def kurohebiAI(foe):
    text = []
    party = getPartyList(foe,False,True)
    foe.nextTarget = random.choice(party)
    party.remove(foe.nextTarget)
    if foe.recover == True:
        foe.recover = False
        foe.sp = 10
    if foe.sp == 0:
        foe.skip = 1
        text.append(f"{foe.name} is wide open!")
        foe.recover = True
        foe.nextSkill = ""
    else:
        skillList = [BlindShotFoe(),BlindShotFoe()]
        if foe.sp >= 2:
            skillList.extend([SlitSnakeFoe(),SlitSnakeFoe()])
        if foe.sp >= 3:
            skillList.extend([ImperceptibleFoe()])
        foe.nextSkill = random.choice(skillList)
    if isinstance(foe.nextSkill,BlindShotFoe):
        foe.counter = []
        if len(party) != 0:
            text.append(f"{foe.name} is feinting at {random.choice(party).name}!")
            text.append(f"{random.choice(party).name} is out of range of {foe.name}'s attacks.")
        text.append(f"{foe.name} is targeting {foe.nextTarget.name} next!")
        text.append(f"{foe.nextTarget.name} is exactly where {foe.name} wants.")
    elif isinstance(foe.nextSkill,SlitSnakeFoe):
        if len(party) > 1:
            foe.counter = [foe.nextTarget,random.choice(party)]
            text.append(f"{foe.name} is anticipating {foe.counter[0].name} and {foe.counter[1].name} attacks.")
            text.append(f"{foe.name} is ready to ambush {foe.counter[0].name} and {foe.counter[1].name}!")
        else:
            foe.counter = [foe.nextTarget]
            text.append(f"{foe.name} is anticipating {foe.counter[0].name} attacks.")
            text.append(f"{foe.name} is ready to ambush {foe.counter[0].name}!")
        foe.skip = 1
    elif isinstance(foe.nextSkill,ImperceptibleFoe):
        foe.counter = []
        text.append(f"{foe.name} has disappeared out of sight!")
        text.append(f"{foe.name} is flickering in and out of view.")
    garbleness = (foe.sp/15)
    foe.insightDisplay = garble(random.choice(text),prob=garbleness)

def mediasAI(foe):
    text = []
    party = getPartyList(foe,False,True)
    random.shuffle(party)
    target = party.pop()
    foe.nextTarget = target
    if len(party) != 0:
        decoy = party.pop()
        names = [target.name,decoy.name]
        random.shuffle(names)
    else:
        decoy = False
        names = None
    foe.deflection = random.choice([True, False, False, False])
    if foe.deflection:
        foe.hit = False
    else:
        foe.hit = True
    if foe.sp >= 30:
        foe.nextSkill = EmperorsClawFoe()
        foe.nextTarget = target
        foe.insight = random.randint(0, 10)
    elif foe.sp >= 10:
        foe.nextSkill = PenguinHighwayFoe()
        foe.nextTarget = target
        foe.insight = random.randint(0, 6)
    else:
        foe.nextSkill = EmperorDanceFoe()
        foe.nextTarget = target
        foe.insight = random.randint(0, 3)
    if foe.insight in [0,3]:
        if foe.deflection:
            text.append(f"{foe.name} is aiming for {target.name}'s dodge!")
            text.append(f"{foe.name} is leading their attack for {target.name}.")
        else:
            text.append(f"{foe.name} is aiming straight for {target.name}!")
            text.append(f"{foe.name}'s next target is {target.name}.")
    elif foe.insight in [1,5,9]:
        text.append(f"{foe.name}'s movement is too confusing to follow!")
        text.append(f"{foe.name} is ricocheting unpredictably!")
    elif foe.insight in [2,6,10]:
        if decoy != False:
            text.append(f"{foe.name} is aiming for {names[0]} or {names[1]}!")
            text.append(f"{foe.name} might attack {names[0]} or {names[1]}.")
        if foe.deflection:
            text.append(f"{foe.name} is trying to lead their attack to catch a dodge!")
            text.append(f"{foe.name} isn't making a direct attack.")
        else:
            text.append(f"{foe.name} is going for a direct attack!")
            text.append(f"{foe.name}'s aim is undeviating!")
    elif foe.insight in [4,7,8]:
        if isinstance(foe.nextSkill,EmperorsClawFoe):
            text.append(f"{foe.name} is sliding too fast to keep track of!")
            text.append(f"You've lost sight of {foe.name}...")
        elif isinstance(foe.nextSkill,PenguinHighwayFoe):
            text.append(f"{foe.name} is sliding very quickly.")
            text.append(f"{foe.name} is moving at a breakneck pace.")
        elif isinstance(foe.nextSkill,EmperorDanceFoe):
            text.append(f"{foe.name} is sliding around.")
            text.append(f"{foe.name} is moving at a decent speed.")
    foe.insightDisplay = random.choice(text)

def williamAI(foe):
    text = []
    party = getPartyList(foe,False,True)
    random.shuffle(party)
    target = party.pop()
    foe.nextTarget = target
    if len(party) != 0:
        redirect = party.pop()
        foe.warpTarget = redirect
        useSkill(foe,WarpFoe())
        text.append(f"{foe.name} is redirecting {target.name}'s attack at {redirect.name}!")
        text.append(f"{target.name}'s attacks will hit {redirect.name} instead of {foe.name}.")
        text.append(f"{foe.name} used Warp on {target.name}!")
        text.append(f"{foe.name} is changing the target of {target.name}'s attacks!")
        text.append(f"{redirect.name} is the target of whoever got warped.")
        text.append(f"{foe.name} is redirecting someone's attack.")
    if foe.sp >= 9:
        foe.nextSkill = HealFoe()
        text.append(f"{foe.name} is going to heal himself!")
    elif foe.sp >= 3:
        foe.nextSkill = EllightFoe()
        text.append(f"{foe.name} is using his Ellight tome.")
    else:
        foe.skip = 1
        text.append(f"{foe.name} doesn't have enough Fate.")
    foe.insightDisplay = random.choice(text)

def neomaAI(foe):
    text = []
    party = getPartyList(foe,False,True)
    random.shuffle(party)
    foe.sp += 3
    if foe.sp >= 12:
        foe.nextSkill = InexorableDestinyFoe()
        target = random.choice(party)
        text.append(f"{foe.name} is advancing {target.name}'s clock of fate.")
        text.append(f"{foe.name} is bringing about another end.")
        text.append(f"The inevitable is never forbidden.")
        text.append(f"{target.name}'s destiny approaches.")
    elif foe.sp >= 2 and random.choice([True,False]):
        foe.nextSkill = LunaFoe()
        target = min(party, key=lambda x: x.hp / x.hpMax)
        text.append(f"Orbs of dark energy float around {target.name}.")
        if random.random() <= 0.66:
            text.append(f"Dark energy swirls in the air.")
    else:
        foe.nextSkill = FluxFoe()
        target = min(party, key=lambda x: x.hp / x.hpMax)
        text.append(f"A shadowy sigil appears at {target.name}'s feet.")
        if random.random() <= 0.66:
           text.append(f"Shadows dance despite the darkness.") 
    foe.nextTarget = target
    foe.insightDisplay = random.choice(text)

def alfonseAI(foe):
    text = []
    party = getPartyList(foe,False,True)
    random.shuffle(party)
    target = party.pop()
    decoy = False
    if party != 0:
        decoy = party.pop()
    if foe.sp > 20 and foe.cool == True:
        time.sleep(pause)
        print(f"{foe.name}'s armor finishes cooling and closes back into place.")
        foe.sp = 0
        foe.cool = False
        foe.over = False
    if foe.sp > 20 and foe.cool == False:
        foe.cool = True
        foe.skip = 1
        text.append(f"{foe.name} is stuck while his armor cools.")
    elif foe.sp <= 5:
        foe.nextSkill = ScorchingSlashFoe()
        text.append(f"{foe.name} is preparing to strike {target.name}.")  
    elif foe.sp >= 10 and random.choice([True,False]):
        foe.nextSkill = SiroccoGustFoe()
        text.append(f"{foe.name} lowers his sword and raises a palm towards {target.name}.")
    else:
        foe.skip = 1
        foe.blast = True
        text.append(f"{foe.name}'s armor is shimmering with the heat coming off it.")
    foe.nextTarget = target
    foe.insightDisplay = random.choice(text)

def markAI(foe):
    pass

def insightTurn():
    display = []
    for char in chars:
        if char.hp > 0:
            if isinstance(char,Sekibanki):
                char.sp += 3
                time.sleep(pause)
                print(f"{char.name} gained 3 Heads!")
            if isinstance(char,Kurohebi):
                if char.sp == 0 and char.recover == True:
                    char.recover = False
                    char.sp = 5
                    time.sleep(pause)
                    print(f"{char.name} recovered 5 Darkness!")
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
        if getattr(char, 'blast', False):
            char.blast = False
        for skill in char.skills:
            if skill.costType == "cooldown":
                if skill.cooldown != 0:
                    skill.cooldown -= 1
        if char.blind == 2:
            char.blind = True
        elif char.blind:
            char.blind = False
            time.sleep(pause)
            print(f"{char.name} recovered from blindness!")
        if char.redirect:
            time.sleep(pause)
            print(f"{char.name}'s attacks are no longer being redirected!")
            char.redirect = None
        if char.warp1:
            char.warp1 = False
        if char.warp2:
            char.warp2 = False

    for foe in foes:
        if getattr(foe, 'dodge', False):
            foe.dodge = False
        if getattr(foe, 'blast', False):
            foe.blast = False
        if isinstance(foe,RobinFoe):
            foe.sp = foe.nextSkill.name
            foe.term = f"{foe.nextSkill.uses}{foe.nextSkill.info}"
        if foe.blind:
            foe.blind = False
            time.sleep(pause)
            print(f"{foe.name} recovered from blindness!")
        if foe.redirect:
            time.sleep(pause)
            print(f"{foe.name}'s attacks are no longer being redirected!")
            foe.redirect = None
        if foe.warp1:
            foe.warp1 = False
        if foe.warp2:
            foe.warp2 = False

def battleLoop():
    global turnNumber
    turnNumber = 0
    while len([char for char in chars if char.hp > 0]) > 0 and len([foe for foe in foes if foe.hp > 0]) > 0:
        turnNumber += 1
        insightTurn()
        displayBattleScreen()
        for char in chars:
            if char.hp > 0:
                if hasattr(char, 'skip') and getattr(char, 'skip') > 0:
                    char.skip -= 1
                else:
                    unitTurn(char)
                    print()
                    time.sleep(endTurnPause)
            if not len([foe for foe in foes if foe.hp > 0]) > 0:
                break
            if isinstance(foes[0],AlfonseFoe) and foes[0].sp > 20:
                if not foes[0].over:
                    time.sleep(pause)
                    print (f"{foes[0].name}'s armor flips open to cool,")
                    time.sleep(pause)
                    print (f"He's unprotected!")
                    foes[0].over = True

        for foe in foes:
            if foe.hp > 0:
                if hasattr(foe, 'skip') and getattr(foe, 'skip') > 0:
                    foe.skip -= 1
                else:
                    unitTurn(foe)
                    print()
                    time.sleep(endTurnPause)
            if len([char for char in chars if char.hp > 0]) > 0:
                break
            if isinstance(foes[0],AlfonseFoe) and foes[0].sp > 20:
                if not foes[0].over:
                    time.sleep(pause)
                    print (f"{foes[0].name}'s armor flips open to cool,")
                    time.sleep(pause)
                    print (f"He's unprotected!")
                    foes[0].over = True
        cleanup()
    if not len([char for char in chars if char.hp > 0]) > 0:
        box([["Your party was defeated!"]])
        return False
    if not len([foe for foe in foes if foe.hp > 0]) > 0:
        box([["You defeated the boss!"]])
        return True

def startStory (file):
    return
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
    if readSave(3):
        charList.append(Sekibanki())
    if readSave(4):
        charList.append(Kogasa())
    if readSave(5):
        charList.append(Kurohebi())
    if readSave(6):
        charList.append(Medias())
    if readSave(7):
        charList.append(William())
    if readSave(8):
        charList.append(Neoma())
    if readSave(9):
        charList.append(Alfonse())
    if readSave(10):
        charList.append(Mark())
    charInt = [*range(1,len(charList)+1)]
    charListReturn = []
    for y in range(0,min(4,len(charList))):
        display = [["-- Character Select --"]]
        for x in charInt:
            display.append([f"{x}. {charList[x-1].name}"])
        box(display)
        n = askList(charInt)
        charInt.remove(n)
        charListReturn.append(charList[n-1])
        print (f"Selected {charListReturn[y].name}")
    return charListReturn
    
def area(place, actions):
    display = [[f"-- {place} --"], [], []]  # Initialize the third list for extra actions
    n = 0
    for action in actions:
        if n < 4:
            display[1].append(f"{n}. {action}")
        else:
            display[2].append(f"{n}. {action}")
        n += 1
    box(display)
    index = ask(0, len(actions)-1)
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
                box([["-- Insight --"]])
                box([["-- Boss --"]])
                box([["-- Party --"]])
                startStory("awake2")
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
            beginBattle(unit2[3],unit2[1],unit2[2])
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