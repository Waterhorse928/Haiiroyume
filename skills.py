class Skill():
    def __init__(self):
        pass

class OneTargetAttack(Skill):
    def __init__(self):
        super().__init__()
        self.type = 0

class HomingAmulet(OneTargetAttack):
    def __init__(self):
        super().__init__()
