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

def main_game_loop():
    char1 = Reimu()
    char2 = Marisa()
    boss = Marisa_Boss()
    while True:
        char1.update()
        char2.update()
        boss.update()
        box([[boss.name],[f"Health {boss.hp}/{boss.hpMax}"],[healthbar(boss.hp,boss.hpMax,50)],[boss.info]])
        box([[char1.name,char2.name],
             [f"HP {char1.hp}/{char1.hpMax}",f"HP {char2.hp}/{char2.hpMax}"],
             [healthbar(char1.hp,char1.hpMax,10),healthbar(char2.hp,char2.hpMax,10)],
             [char1.info,char2.info]])
        break

main_game_loop()