from items import Weapon, Armour
from player import Player

import sys, os

with open(os.devnull, 'w') as f:
    # disable stdout
    oldstdout = sys.stdout
    sys.stdout = f
    import pygame
    # enable stdout
    sys.stdout = oldstdout

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
        #print(action)
        #print(action[0:4])
        #action = action.lower()
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
            print(self.player.x-1, self.player.y-1)
        elif 'use ' in action and ' on ' in action:
            itemName = action[4:action.find(' on ')]
            obLoc = action.find(' on ') + 4
            # add something in so multiple items can be used 
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
                    '''if type(item) is Weapon:
                        self.player.addWeapon(item)
                        self.square.removeItem(item)

                    else:'''
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

        elif action[0:5] == 'fight':
            #print('you\'re trying to fight')
            npc = action[6:]
            for occupant in self.square.occupants:
                if occupant.name == npc:
                    #print('Your health: ', self.player.health, ' Opponent\'s health: ', occupant.health)
                    pid = 0
                    while(self.player.health>0 and occupant.health>0):
                        if (pid % 2):
                            self.player.change_health(-1*occupant.damage)
                        else:
                            occupant.change_health(-1*self.player.damage)

                        pid += 1
                        #print('Your health: ', self.player.health, ' Opponent\'s health: ', occupant.health)

                    #print('fight is done')

                    if(self.player.health>0):
                        print(npc, ' has been defeated.')
                        self.square.removeOccupants(occupant)
                        droppedItems = occupant.dropOnDeath()
                        if droppedItems:
                            print("You find: ")
                            for item in droppedItems:
                                print(item.name)
                                self.square.items.append(item)

                    else:
                        print('You have died.')
                        self.playGame = False

        # thresholds needed here %%%%%%%%%%%%%%%%%%%%%%
        elif action == 'health':
            hp = self.player.health
            if hp >= 90:
                print('hurt not that bad.')
            elif hp >= 75:
                print('definitely feeling something.')
            else:
                print('You\'re nearly dead.')


        elif action == 'weapons':
            print('___Weapons___')
            for weapon in self.player.weapons:
                print(weapon.name, 'x', weapon.quantity)

        elif action == 'stats':
            print('___Stats___')
            print('Weapon: ', self.player.weapon.name ,'Damage: ', self.player.damage)
            print('Armour: ', self.player.armour.name ,'Defense: ', self.player.defense)

        elif action[0:5] == 'equip':
            name = action[6:]
            for weapon in self.player.weapons:
                if name == weapon.name:
                    self.player.equipWeapon(weapon)
            for armour in self.player.armours:
                if name == armour.name:
                    self.player.equipArmour(armour)

        elif action == 'exit':
            self.playGame = False

        else:
            print('Invalid Command.')

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

        '''
        print(self.square.audio)
        if self.square.audio:
            print('in here')
            audio = sys.path[0][:-6] + '/audio/' + self.square.audio
            pygame.mixer.music.load(audio)
            pygame.mixer.music.play()

            '
            if self.terrain.audio_path:
                audio_path = sys.path[0][:-6] + '/audio/' + self.terrain.audio_path
                pygame.mixer.music.queue(audio_path)
                pygame.mixer.music.play(-1)
            '''

    def startGame(self):
        while self.playGame:
            self.nextTurn()