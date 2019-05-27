from textGame import *

player = Player('player', x=0, y=0)

world = Terrain(5,5)

rattler1 = Npc('Fearsome Rattler', ['hhsssss...'])
rattler2 = Npc('Fearsome Rattler', ['hhsssss...'])


bottle = Weapon('glass bottle', 73)
topLeft = Square([0,0], 'ne')
topMiddle = Square([0,1], 'w')
topRight = Square([0,2], 'sw')
middleLeft = Square([1,0], 'n')
center = Square([1,1], 'Oh fuck me... I think that\'s a rattler...', occupants=[rattler1])
middleRight = Square([1,2], 'You\'ve gotta be kidding me', occupants=[rattler2])
bottomLeft = Square([2,0], 'ne')
bottomMiddle = Square([2,1], 'e', items=[bottle])
bottomRight = Square([2,2], 'se')




#init world
world.addSquare(topLeft)
world.addSquare(topMiddle)
world.addSquare(topRight)
world.addSquare(middleLeft)
world.addSquare(center)
world.addSquare(middleRight)
world.addSquare(bottomLeft)
world.addSquare(bottomMiddle)
world.addSquare(bottomRight)

#run game
game = Turn(player, world)
game.startGame()