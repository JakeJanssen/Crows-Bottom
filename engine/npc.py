from player import Person

class Npc(Person):
    def __init__(self, name, dialog ,movement=1, wealth=0, damage=10, gifts = [], activateItems=[], rewards = [], rewardDialog = []) :
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