from items import Weapon, Armour

class Person:
    def __init__(self, name, movement, wealth, inventory = [], health=100, damage=10, defense=0):
        self.name = name
        self.movement = movement
        self.wealth = wealth
        self.inventory = inventory
        self.health = health
        self.damage = damage
        self.defense = defense

    def change_health(self, health_change):
        self.health += health_change

class Player(Person):
    def __init__(self, name, x=2, y=2):
        Person.__init__(self, name, 1, 100)
        self.x = x+1
        self.y = y+1
        fists = Weapon('fists', 50)
        clothes = Armour('peasant clothes', 2)
        self.weapons = [fists]
        self.armours = [clothes]
        self.equipWeapon(fists)
        self.equipArmour(clothes)
        
    def addItem(self,item):
        self.inventory.append(item)

    def removeItem(self, item):
        self.inventory.remove(item)

    def addWeapon(self, weapon):
        self.weapons.append(weapon)

    def removeWeapon(self, weapon):
        self.weapons.remove(weapon)

    def equipWeapon(self, weapon):
        if weapon in self.weapons:
            self.weapon = weapon
            self.damage = weapon.damage

    def equipArmour(self, armour):
        if armour in self.armours:
            self.armour = armour
            self.defense = armour.defense