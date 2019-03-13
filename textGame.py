class Person:
    def __init__(self, name, movement, wealth, inventory = []):
        self.name = name
        self.movement = movement
        self.wealth = wealth
        self.inventory = inventory

class Npc(Person):
    def __init__(self, name, dialog ,movement=1, wealth=0, gifts = [], activateItems=[], rewards = [], rewardDialog = []) :
        Person.__init__(self, name, movement, wealth)
        self.gifts = gifts
        self.activateItems = activateItems
        self.rewards = rewards
        self.dialog = dialog 
        self.dialogCounter = 0
        self.rewardDialog = rewardDialog
        self.rewardDialogCounter = 0

    def speak(self):
        print(self.name+':',self.dialog[self.dialogCounter])
        takenItems = []
        if len(self.gifts) > 0:
            for item in self.gifts:
                answer = input('Do you want ' + item.name + '?: ')
                if answer == 'y':
                    takenItems.append(item)
                    self.gifts.remove(item)
        return takenItems

    def activate(self, playerItem):
        gainedItems = []
        if playerItem in self.activateItems:
            print(self.rewardDialog[self.rewardDialogCounter])
            for item in self.rewards:
                answer = input('Do you want ' + item.name + '?: ')
                if answer == 'y':
                    self.rewards.remove(item)
                    gainedItems.append(item)
        return gainedItems 

class Object:
    def __init__(self, name, activateItems=[], heldItems=[]):
        self.name = name
        self.activateItems = activateItems
        self.heldItems = heldItems 

    def activate(self, playerItem):
        gainedItems = []
        if playerItem in self.activateItems:
            for item in self.heldItems:
                answer = input('Do you want ' + item.name + '?: ')
                if answer == 'y':
                    self.heldItems.remove(item)
                    gainedItems.append(item)
        return gainedItems 


class Player(Person):
    def __init__(self, name):
        Person.__init__(self, name, 1, 100)
        self.x = 1
        self.y = 3
        
    def addItem(self,item):
        self.inventory.append(item)
                
class Item:
    def __init__(self, name, quantity, weight):
        self.name = name
        self.quantity = quantity
        self.weight = weight
    def use(self):
        print('This item has no use at the moment.')

class Note(Item):
    def __init__(self, name, quantity, weight, text):
        Item.__init__(self, name, quantity, weight)
        self.text = text
        
    def use(self):
        print(self.text)
        
        
class Square():
    def __init__(self, location, description, items=[], occupants=[], objects=[]):
        self.location = location
        self.items = items
        self.description = description
        self.occupants = occupants
        self.objects = objects
    
    def removeItem(self, item):
        self.items.remove(item)
        
    def addItem(self,item):
        self.items.append(item)
        
    def addOccupants(self, person):
        self.occupants.append(person)
        
class Terrain:
    def __init__(self, xSize, ySize):
        self.squares = [[Square([x,y],'You get the feeling you\'ve gone too far...',[]) for y in range(ySize)] for x in range(xSize)] 
        
    def addSquare(self, square):
        self.squares[square.location[0]][square.location[1]] = square 
        
class Turn():
    def __init__(self, player, terrain):
        self.player = player
        self.terrain = terrain
        self.square = terrain.squares[player.x][player.y]
        self.newRoom = True

    def command(self, action):
        if action=='n':
            self.player.y = self.player.y-1
        elif action =='s':
            self.player.y = self.player.y+1
        elif action == 'e':
            self.player.x = self.player.x+1
        elif action == 'w':
            self.player.x = self.player.x-1
        elif action == 'no':
            pass
        elif action == 'inv':
            for item in self.player.inventory:
                print(item.name)
        elif action == 'loc':
            print(self.player.x, self.player.y)

        elif 'use ' in action and ' on ' in action:
            itemName = action[4:action.find(' on ')]
            obLoc = action.find(' on ') + 4
            objectName = action[obLoc:]
            gainedItems = []
            for item in self.player.inventory:
                if itemName == item.name:
                    for curObject in self.square.objects:
                        if curObject.name == objectName:
                            gainedItems = curObject.activate(item)
                    for occupant in self.square.occupants:
                        if occupant.name == objectName:
                            gainedItems = occupant.activate(item)
            for gain in gainedItems:
                self.player.addItem(gain)

        elif action[0:3] == 'use':
            itemName = action[4:]
            print(itemName)
            for item in self.player.inventory:
                if itemName == item.name:
                    item.use()
        elif action[0:4] == 'take':
            itemName = action[5:]
            for item in self.square.items:
                if itemName == item.name:
                    self.player.addItem(item)
                    self.square.removeItem(item)

        elif action[0:7] == 'talk to':
            ncp = action[8:]
            for occupant in self.square.occupants:
                if occupant.name == ncp:
                    giftedItems = occupant.speak()
                    for item in giftedItems:
                        self.player.addItem(item)
        
        else:
            print('not a command')
        if action in ['n','s','e','w']:
            self.newRoom = True 
        else:
            self.newRoom = False

        
    def nextTurn(self):
        if self.newRoom == True:
            print(self.terrain.squares[self.player.x][self.player.y].description)
            if len(self.square.items) > 0:
                print('You find: ')
                for item in self.square.items:
                    print(item.name)

            if len(self.square.occupants) > 0:
                print('Occupants: ')
                for occupant in self.square.occupants:
                    print(occupant.name)

            if len(self.square.objects) > 0:
                print('You see: ')
                for objects in self.square.objects:
                    print(objects.name)
        
        action = input('Command: ')
        self.command(action)
        self.square = self.terrain.squares[self.player.x][self.player.y]
