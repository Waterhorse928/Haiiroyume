import math

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

    def update(self):
        self.info = f'Graze {self.sp}'

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

def displayBattleScreen(boss,chars):
    characters = [char for char in (chars) if char != 0]
    numberOfChar = len(characters)
    boxList1 = [[boss.name],[f"Health {boss.hp}/{boss.hpMax}"],[healthbar(boss.hp,boss.hpMax,50)],[boss.info]]
    boxList2 = [[char.name for char in characters],
                [f"HP {char.hp}/{char.hpMax}" for char in characters],
                [healthbar(char.hp,char.hpMax,10) for char in characters],
                [char.info for char in characters]]
    box(boxList1)
    if numberOfChar > 0:
        box(boxList2)


def battleLoop(boss,chars):
    while True:
        displayBattleScreen(boss,chars)

        break

battleLoop(Marisa_Boss(),[Reimu(),Reimu(),Reimu(),Reimu(),Reimu()])