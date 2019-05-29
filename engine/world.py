import sys, os

with open(os.devnull, 'w') as f:
    # disable stdout
    oldstdout = sys.stdout
    sys.stdout = f
    import pygame
    # enable stdout
    sys.stdout = oldstdout

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

    def removeOccupants(self, person):
        self.occupants.remove(person)

    def checkBarrier(self, direction, isPlayer):
        if direction in self.barriers:
            if isPlayer:    
                print('Something is blocking your way.')
            return False
        else:
            return True

class Terrain:
    def __init__(self, xSize, ySize, audio_path = None):
        xSize += 2
        ySize += 2
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

        if audio_path:
            audio_path = sys.path[0][:-6] + '/audio/' + audio_path
        
        pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1)

    def addSquare(self, square):
        self.squares[square.location[0]+1][square.location[1]+1] = square 

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

