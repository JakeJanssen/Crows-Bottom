from engine import *

print('Welcome to the land of Crow\'s Bottom.')
player_name = input('Please enter your name: ')
print('Greetings ', player_name + '.')
print('''
You begin your journey in a lightly forested region far from home. 
Until this point you have lived as a simple man, tending to your crops and livestock. 
''')


player = Player(player_name, x=2, y=2)

world = Terrain(10,10,'outdoors_1.mp3')

gold1 = Item('gold',1,0)

payment = Item('gold', 20, 0)

thief_payment = Item('gold', 21, 0)

diary = Note('Vampire Diary',1,0,'''Today honestly felt pretty good.
Right at dusk I treated myself to fresh meal and then kicked the king out of his own castle!
My confidence is really growing here and I think I finally found a place I can call home.

I still miss Laura.
I had a dream about her last day. Hope she's well.

No I don't. 
Yes I do.

Come on Brandon, think positive. You were the one who drove a stake in her heart, you're on to bigger things now.

Then why do I feel so small?

xoxo''')

package = Item('Package',1,1)

walking_stick = Weapon('Walking Stick', 51)

shovel = Item('shovel', 1, 1)

silverSword = Weapon('Silver Sword', 100)

burialSpot = Object('burial spot', [shovel], [gold1])

vamp = Npc('Vampire', ['CLOSE THE DOOR! Can\'t you see there is daylight.'], damage=100, itemsOnDeath=[diary])

guard = Npc('Town Guard', ['''You must be the knight Maros sent to save us.
Oh thank god you are here! 
As discussed, the pay for your travels and soon to be heroics is right here.
Good luck Sir Maros and may god help you slay the creature!
'''], gifts = [payment])

gerald = Npc('Gerald', ['''Fuck off will you!?
Can't a man be left to cry when he wife was sucked dry by the vile thing last night.
'''])

priest = Npc('Priest', ['''Sir Maros! The painters have done you well, you truly do look like your portrait.
Unfortunately there has been a mishap with the sword for your task.
The church was raided last night and of course it was stolen. 
If it is not too much to impose, the theifs tend to hide south of the town and the guards are much too cowardly to confront them.
They should be no trouble for the warrior who killed three dragons with his bare hands though. 
'''])

thief = Npc('Thief', ['''Are you past the broken bend?
You: What?
Thief: Are you past *winks* the broken bend?
You: ...Oh yes of course, I broke it just yestermorning.
Thief: Are you a guard? You have to tell me if you are.
You: No, no. Just a fellow warrior of the dark curtain like yourself. 
Thief: Well then friend, let me show you my lastest loot.
*The thief pulls out a sword made entirely of silver*
Thief: My sources say it is well worth 1,200 gold but I will sell it to you for the fine price of 30.
You: 15
Thief: 25
You: 20
Thief: 21
You: 20 gold is my final offer.
Thief: I don't know if you have heard of my reputation, but I always get the final say. Either give me the gold or piss off. 
'''], activateItems=[thief_payment], rewards=[silverSword], rewardDialog=['Now scram.'])

graveDigger = Npc('Grave Digger', ['''Idiot, idiot, idiot! I am such a fool! 
You: Everything alright?
Grave Digger: Not at all, I owe some serious gold to the dice players down south and I just burried Gerald's wife with her pockets filled.
'''])

king = Npc('King Landom', ['''Sir Maros you have come! The vampire has taken my castle and refuses to leave.
End him for all that is holy!'''])

startSquare = Square([2,2], '''A sign points to the village of Truvilia, two miles to the east.
''')

path1 = Square([3,2], '''A couple of fallen branches lay along the path.
You see a village to the east of you. 
''', items = [walking_stick])

truvW = Square([4,2], '''You enter the town of Truvilia.
''', occupants = [guard])

truvC = Square([5,2], '''The town's sqaure. A church is to your north east.''')

truvN = Square([5,1], '''A brothel next to the town's church. ''', barriers = 'n', occupants = [gerald])


truvNC = Square([6,1], '''A simple church with some very striking altar boys.''', occupants=[priest], barriers='ne')

truvCE = Square([6,2], 'The beautiful gardens owned by the king.')

truvE = Square([7,2], '''The entrance to the castle. ''', occupants=[king])

castle = Square([8,2], '''The heart of Truvila. With new gothic decore.''', occupants=[vamp], barriers='nse')

market = Square([4,1], '''There is a small market.
The town walls surround the north and west.''', barriers = 'nw')

grave1 = Square( [4,3], '''Half of the town's graveyard. Many graves look freshly dug.
The town walls surround the south and west.''',
objects=[burialSpot], barriers='sw')

grave2 = Square([5,3], '''The grave keeper's quarters.
The town walls surround the south''', items=[shovel], occupants=[graveDigger], barriers='s')

southExit = Square([6,3], 'The southern exit.')

theifsPlace = Square([6,4], 'A small hut and poorly made fire are home to some sad man.', occupants=[thief])


world.addSquare(startSquare)
world.addSquare(path1)
world.addSquare(truvW)
world.addSquare(truvC)
world.addSquare(truvNC)
world.addSquare(truvE)
world.addSquare(truvN)
world.addSquare(truvCE)
world.addSquare(castle)
world.addSquare(market)
world.addSquare(grave1)
world.addSquare(grave2)
world.addSquare(southExit)
world.addSquare(theifsPlace)

game = Turn(player, world)
game.startGame()