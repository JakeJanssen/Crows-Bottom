class Item:
    def __init__(self, name, quantity, weight):
        self.name = name
        self.quantity = quantity
        self.weight = weight
    def use(self):
        print('This item has no use at the moment.')

class Weapon(Item):
    def __init__(self, name, damage, weight=0, quanitiy=1):
        Item.__init__(self, name, quanitiy, weight)
        self.damage = damage

class Armour(Item):
    def __init__(self, name, defense, weight=0, quanitiy=1):
        Item.__init__(self, name, quanitiy, weight)
        self.defense = defense

class Note(Item):
    def __init__(self, name, quantity, weight, text):
        Item.__init__(self, name, quantity, weight)
        self.text = text
        
    def use(self):
        print(self.text)