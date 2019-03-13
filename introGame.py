from textGame import *

player = Player('Colin')

# init terrain
world = Terrain(8,7)


gold = Item('gold', 5, 0)

bundle = Item('Carefully Wrapped Package',1,1)

alabaster = Npc('Alazi Alabaster', ['My daddy isn\'t here right now if that\'s what you\'re wondering.'] ,rewardDialog=['A small girl of 8 at the most approaches. \"D-do... Do you have it?? OH thank you thank you thank you Mister! I got into daddy\'s mead cabinet, and I don\'t know what would have happened if I hadn\'t gotten mom back by the time he got back from his travels.\" She unwraps the bundle, revealing a neatly stacked pile of bones.'], activateItems=[bundle],rewards= [gold])

AlabasterHouse = Square([2,1], 'This is the Alabaster House.',occupants=[alabaster])

dirtPatch = Square([1,2], 'This small mud puddle is not the best place to hang out. Your house is to the south.')

CrowsBottomCenter = Square([2,2], 'Looking around, Crow\'s Bottom leaves something to be desired... But who knows if there\'s even anything better out there? YOU\'VE certainly never been. The Alabaster house sits, unimpressively, to the North.' )

house = Square([1,3], 'You are in the small wooden box that you call home. It isn\'t much, but it keeps you dry. \nThere is a door on the east wall.')

post = Note('Crows Bottom Flyer',1,0,'''
ATTENTION! HELP!
I had an emotional night the other night.
It's not like me, but in a fit of feelings,
I lost control of my better judgement...
I buried something by the shore but I don't 
know where. If you can return it to me you'll be
paid handsomely.

Please and thank you,
A. Alabaster''')

townPost = Square([2,3], 'You are on an overgrown patch of dry land. Your house is to the West. There is a wooden post here with a flyer attached to it.', [post])

forest1 = Square([2,4], 'You are in a fairly overgrown forest. However you can make your way through the branches with some effort.')

forest2 = Square([2,5], 'The many branches hanging around your head and stabbing your neck make it difficult to walk. There seems to be a bit more light coming through the trees to the south.')

forest3 = Square([3,4], 'Every part of this forest looks so similar. I hope you don\'t get lost.')

forest4 = Square([3,5], 'Who knows what\'s lurking behind these leaves, and slithering around your feet... I hope this is worth it.')

forest5 = Square([4,4], 'Screw this. You are now against recycling. This is crazy.')

shovel = Item('shovel', 1, 1)

forest6 = Square([4,5], 'This is probably the prettiest part of the forest you\'ve been in.', [shovel])


burialSpot = Object('burial spot', [shovel], [bundle])

fisherman = Npc('Fisherman', ['He growls. \"Are you here like those other bastards? I\'m tryna enjoy my fishin\'. I\'ll show you where if you\'ll make it quick and scram.\" \n Burial spot learned.'])

shore = Square([2,6], 'A sandy shore talstretches almost up to the treeline. A grisled man sits on a log, clutching a bent fishing rod and a small glass bottle.', occupants=[fisherman], objects=[burialSpot])

grassyKnoll = Square([3,3], 'You are on a dirt path cutting through a pleasant meadow. You can make out some sort of structure to the East, and a thick treeline to the South.')

guard = Npc('Guard', ['He bellows. \"What business could YOU have with the royal guard?? A shovel? You should have just said so. I think I left one laying around in the forest somewhere.\"'])

guardPost = Square([4,3], 'There are two menacing, fully-armored, mean guards. I guess you don\'t KNOW they\'re mean. But... I mean, they\'re guards.', occupants=[guard])


world.addSquare(AlabasterHouse)
world.addSquare(dirtPatch)
world.addSquare(CrowsBottomCenter)
world.addSquare(house)
world.addSquare(townPost)
world.addSquare(forest1)
world.addSquare(forest2)
world.addSquare(forest3)
world.addSquare(forest4)
world.addSquare(forest5)
world.addSquare(forest6)
world.addSquare(shore)
world.addSquare(grassyKnoll)
world.addSquare(guardPost)

game = Turn(player, world)

while True:
    game.nextTurn()