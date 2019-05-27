class Person:
    def __init__(self, name, movement, wealth, inventory = [], health=100, damage=10):
        self.name = name
        self.movement = movement
        self.wealth = wealth
        self.inventory = inventory
        self.health = health
        self.damage = damage

    def change_health(self, health_change):
        self.health += health_change


class Npc(Person):
    def __init__(self, name, dialog ,movement=1, wealth=0, damage=50, gifts = [], activateItems=[], rewards = [], rewardDialog = []) :
        Person.__init__(self, name, movement, wealth)
        self.gifts = gifts
        self.activateItems = activateItems
        self.rewards = rewards
        self.dialog = dialog 
        self.dialogCounter = 0
        self.rewardDialog = rewardDialog
        self.rewardDialogCounter = 0
        self.damage = damage

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
        success = False
        if playerItem in self.activateItems:
            print(self.rewardDialog[self.rewardDialogCounter])
            success = True
            for item in self.rewards:
                answer = input('Do you want ' + item.name + '?: ')
                if answer == 'y':
                    self.rewards.remove(item)
                    gainedItems.append(item)
        return gainedItems, success 

class MovingNpc(Npc):
    def __init__(self, name, dialog, startingLoc = [], movementPattern=[], movement=1, wealth=0, gifts = [], activateItems=[], rewards = [], rewardDialog = []) :
        Npc.__init__(self, name, dialog ,movement, wealth, gifts, activateItems, rewards, rewardDialog)
        self.movementPattern = movementPattern
        self.movementCounter = 0
        self.x = startingLoc[0]
        self.y = startingLoc[1]

    def nextCommand(self):
        command = self.movementPattern[self.movementCounter]
        if self.movementCounter == len(self.movementPattern)-1:
            self.movementCounter = 0
        else:
            self.movementCounter += 1
        return command


class Object:
    def __init__(self, name, activateItems=[], heldItems=[]):
        self.name = name
        self.activateItems = activateItems
        self.heldItems = heldItems 

    def activate(self, playerItem):
        gainedItems = []
        success = False
        if playerItem in self.activateItems:
            success = True
            for item in self.heldItems:
                success = True
                answer = input('Do you want ' + item.name + '?: ')
                if answer == 'y':
                    self.heldItems.remove(item)
                    gainedItems.append(item)
        return gainedItems, success


class Player(Person):
    def __init__(self, name):
        Person.__init__(self, name, 1, 100)
        self.x = 1
        self.y = 3
        
    def addItem(self,item):
        self.inventory.append(item)

    def removeItem(self, item):
        self.inventory.remove(item)
        
                
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
    def __init__(self, location, description, items=[], occupants=[], objects=[], barriers = ''):
        self.location = location
        self.items = items
        self.description = description
        self.occupants = occupants
        self.objects = objects
        self.barriers = barriers 
    
    def removeItem(self, item):
        self.items.remove(item)
        
    def addItem(self,item):
        self.items.append(item)
        
    def addOccupants(self, person):
        self.occupants.append(person)

    def checkBarrier(self, direction, isPlayer):
        if direction in self.barriers:
            if isPlayer:    
                print('Something is blocking your way.')
            return False
        else:
            return True

        
class Terrain:
    def __init__(self, xSize, ySize):
        self.squares = [[Square([x,y],'You get the feeling you\'ve gone too far...',barriers='') for y in range(ySize)] for x in range(xSize)]
        for square in self.squares[0]:
            square.barriers += 'w'
        for square in self.squares[xSize-1]:
            square.barriers += 'e'
        for square_array in self.squares:
            square_array[0].barriers += 'n'
            square_array[ySize-1].barriers += 's'
        
        self.xSize = xSize
        self.ySize = ySize

    def addSquare(self, square):
        self.squares[square.location[0]][square.location[1]] = square 

    def shareBarriers(self):
        for square_array in self.squares:
            for square in square_array:
                if (self.xSize-1 > square.location[0] > 0) and (self.ySize-1 > square.location[1] > 0):
                    if 'e' in square.barriers:
                        self.squares[square.location[0]+1][square.location[1]].barriers += 'w'
                    if 'w' in square.barriers:
                        self.squares[square.location[0]-1][square.location[1]].barriers += 'e'
                    if 'n' in square.barriers:
                        self.squares[square.location[0]][square.location[1]-1].barriers +='s'
                    if 's' in square.barriers:
                        self.squares[square.location[0]][square.location[1]+1].barriers += 'n'
          
class Turn():
    def __init__(self, player, terrain, smartNpcs=[]):
        self.player = player
        self.terrain = terrain
        self.square = terrain.squares[player.x][player.y]
        self.newRoom = True
        self.playGame = True
        self.smartNpcs = smartNpcs

    def addSmartNpc(self, npc):
        self.smartNpcs.append(npc)

    def command(self, action, actor):
        # used to check if a movement command went through
        success = False

        # check if a player is commanding 
        isPlayer = type(actor) is Player

        # set current sqaure of actor 
        if not isPlayer:
            currSquare = self.terrain.squares[actor.x][actor.y]
        else:
            currSquare = self.square

        if action in 'nsew':
            if action=='n' and currSquare.checkBarrier('n', isPlayer):
                actor.y += -1
                success = True
            elif action =='s' and currSquare.checkBarrier('s', isPlayer):
                actor.y += 1
                success = True
            elif action == 'e' and currSquare.checkBarrier('e', isPlayer):
                actor.x += 1
                success = True
            elif action == 'w' and currSquare.checkBarrier('w', isPlayer):
                actor.x += -1
                success = True
    
        elif action == 'no':
            pass
        elif action == 'inv':
            for item in self.player.inventory:
                print(item.name,'x',item.quantity)
        elif action == 'loc':
            print(self.player.x, self.player.y)
        elif 'use ' in action and ' on ' in action:
            itemName = action[4:action.find(' on ')]
            obLoc = action.find(' on ') + 4
            objectName = action[obLoc:]
            objGainedItems = []
            occGainedItems = []
            npcGainedItems = []
            for item in self.player.inventory:
                if itemName == item.name:
                    for curObject in self.square.objects:
                        if curObject.name == objectName:
                            objGainedItems, status = curObject.activate(item)
                    for occupant in self.square.occupants:
                        if occupant.name == objectName:
                            occGainedItems, status = occupant.activate(item)
                            if status:
                                self.player.removeItem(item)
                    for smartNpc in self.smartNpcs:
                        if smartNpc.name == objectName and self.player.x == smartNpc.x and self.player.y == smartNpc.y:
                            npcGainedItems, status = smartNpc.activate(item)
                            if status:
                                self.player.removeItem(item)


            for gain in objGainedItems + occGainedItems + npcGainedItems:
                self.player.addItem(gain)

        elif action[0:3] == 'use':
            itemName = action[4:]
            for item in self.player.inventory:
                if itemName == item.name:
                    item.use()
        elif action[0:4] == 'take':
            itemName = action[5:]
            takeAll = False
            if itemName == 'all':
                takeAll = True
            for item in self.square.items:
                if itemName == item.name or takeAll:
                    self.player.addItem(item)
                    self.square.removeItem(item)

        elif action[0:7] == 'talk to':
            npc = action[8:]
            for occupant in self.square.occupants:
                if occupant.name == npc:
                    giftedItems = occupant.speak()
                    for item in giftedItems:
                        self.player.addItem(item)

            for smartNpc in self.smartNpcs:
                if smartNpc.name == npc and self.player.x == smartNpc.x and self.player.y == smartNpc.y:
                    giftedItems = smartNpc.speak()
                    for item in giftedItems:
                        self.player.addItem(item)

            newAction = input('Command: ')
            success = self.command(newAction, actor)

        elif action[0:4] == 'fight':
            print('you\'re trying to fight')
            npc = action[5:]
            for occupant in self.square.occupants:
                if occupant.name == npc:
                    print('Your health: ', self.player.health, ' Opponent\'s health: ', occupant.health)
                    while(self.player.health>0 and occupant.health>0):
                        occupant.change_health(self.player.damage)
                        self.player.change_health(occupant.damage)
                        print('Your health: ', self.player.health, ' Opponent\'s health: ', occupant.health)

                    print('fight is done')



        elif action == 'exit':
            self.playGame = False

        if success and (type(actor) is Player):
            self.newRoom = True 
        elif type(actor) is Player:
            self.newRoom = False

        return success

        
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

        for npc in self.smartNpcs:
            self.command(npc.nextCommand(), npc)
            #print(npc.x,npc.y)
            if (self.player.x == npc.x) and (self.player.y == npc.y):
                print(npc.name, 'passes by.')
            
        action = input('Command: ')
        self.command(action, self.player)
        self.square = self.terrain.squares[self.player.x][self.player.y]

    def startGame(self):
        while self.playGame:
            self.nextTurn()
