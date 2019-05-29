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
        if type(item) is Weapon:
            new_wep = True
            for i in range(0,len(self.weapons)):
                if item.name == self.weapons[i].name:
                    self.weapons[i].quantity += item.quantity
                    new_wep = False

            if new_wep:   
                self.weapons.append(item)
        else:
            new_item = True
            for i in range(0,len(self.inventory)):
                if item.name == self.inventory[i].name:
                    self.inventory[i].quantity += item.quantity
                    new_item = False

            if new_item:   
                self.inventory.append(item)

    # need to make removes stackable 
    def removeItem(self, item):
        self.inventory.remove(item)

    def addWeapon(self, item):
        new_wep = True
        for i in range(0,len(self.weapons)):
            if item.name == self.weapons[i].name:
                self.weapons[i].quantity += item.quantity
                new_wep = False

        if new_wep:   
            self.weapons.append(item)

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