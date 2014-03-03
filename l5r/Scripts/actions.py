#------------------------------------------------------------------------------
# Constant and Variables Values
#------------------------------------------------------------------------------

Chi = ("Chi", "84895650-69ef-483f-93bc-9def2b9b7fed")
Force = ("Force", "a40f5a18-2a70-46ca-814d-0ad6963db239")
Chi_Lower = ("Chi_Lower", "eac0f42f-d696-4e20-9d3f-aa91f3ace4fa")
Force_Lower = ("Force_Lower", "495b401f-8d92-4af2-b1e4-e637c952b1eb")
Sake = ("Sake", "6062029c-640e-4c87-9d90-8905ea2872c0")
Fire = ("Fire", "945fb1f1-0794-4f3b-a3f2-ac4576308bb0")
Poison = ("Poison", "8f0a96c6-6f54-4da2-97f9-85e8f721b6e9")
Gold = ("Gold", "b45d337d-72ae-43b4-847f-2b951d1820d6")
Madness = ("Madness", "c7312c64-e69f-4984-9bd1-24fc320e39d7")
Fudo = ("Fudo", "4b5a3d9e-ece1-40fd-8a9a-356900449342")

AttackColor = "#ff0000"
AbilityColor = "#0000ff"
phaseId = 0
phases = [
    '{} is currently in the Straighten Phase',
    "It is now {}'s Events Phase",
    "It is now {}'s Action Phase",
    "It is now {}'s Attack Phase",
    "It is now {}'s Dynasty Phase",
    "It is now {}'s End Phase"]

#------------------------------------------------------------------------------
# Table Actions
#------------------------------------------------------------------------------

def gamesetup(group, x = 0, y = 0):
	global ds
	mute()
	if ds and not confirm("Are you sure you want to setup for a new game? (This action should only be done after a table reset)"): return
	ds = None
	if not table.isTwoSided() and not confirm(":::WARNING::: This game is designed to be played on a two-sided table. Things will be extremely uncomfortable otherwise!! Please start a new game and makde sure the  the appropriate button is checked. Are you sure you want to continue?"): return
	chooseSide()
	deck = me.piles['Fate Pile']
	stronghold = me.piles['Stronghold Pile']
	debugNotify("Checking Deck", 3)
	if len(deck) == 0:
		whisper ("Please load a deck first!")
		return
	if len(stronghold) == 0 or len(stronghold) > 1:
		whisper ("Your deck need a Stronghold Card!")
		return
	resetAll()
	for card in me.piles['Stronghold Pile']:
		card.moveTo(me.hand)
	for card in me.hand:
		if card.Type != 'Stronghold':
			whisper(":::Warning::: You are not supposed to have any cards in your hand when you start the game")
			card.moveToBottom(me.piles['Fate Pile'])
			continue
		else:
			ds = card.Clan()
			me.setGlobalVariable('ds', ds)
	if not ds:
		confirm("You need to have your Stronghold when you try to setup the game. If you have it in your deck, please look for it and put it in your hand before running this function again")
		return

def showCurrentPhase(group, x = 0, y = 0):
    notify(phases[phaseId].format(me))

def nextPhase(group, x = 0, y = 0):
    global phaseId
    phaseId += 1
    showCurrentPhase(group)

def goToStraight(group, x = 0, y = 0):
    global phaseId
    phaseId = 0
    mute()
    myCards = (card for card in table
                    if card.controller == me)
    for card in myCards: 
        card.orientation &= ~Rot90
    notify("{} straightens all cards and enters the Event Phase".format(me))

def goToEventPhase(group, x = 0, y = 0):
    global phaseId
    phaseId = 1
    showCurrentPhase(group)

def goToActionPhase(group, x = 0, y = 0):
    global phaseId
    phaseId = 2
    showCurrentPhase(group)

def goToAttacktPhase(group, x = 0, y = 0):
    global phaseId
    phaseId = 3
    showCurrentPhase(group)

def goToDynastyPhase(group, x = 0, y = 0):
    global phaseId
    phaseId = 4
    showCurrentPhase(group)

def goToEndPhase(group, x = 0, y = 0):
    global phaseId
    phaseId = 5
    showCurrentPhase(group)
    
def respond(group, x = 0, y = 0):
    notify('{} REACTION!'.format(me))

def clearAll(group, x = 0, y = 0):
    notify("{} clears all targets and combat.".format(me))
    for card in group:
      card.target(False)
      if card.controller == me and card.highlight in [AttackColor, AbilityColor]:
          card.highlight = None

def roll6(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls {} on a 6-sided die.".format(me, n))

def roll20(group, x = 0, y = 0):
    mute()
    n = rnd(1, 20)
    notify("{} rolls {} on a 20-sided die.".format(me, n))

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))

def bow(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        notify('{} bowed {}'.format(me, card))
    else:
        notify('{} unbowed {}'.format(me, card))

def attack(card, x = 0, y = 0):
	mute()
	if card.highlight == AttackColor:
		card.highlight = None
	else:
		card.highlight = AttackColor
		notify('{} attacks with {}'.format(me, card))

def reveal(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} turns {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} revealed {} from the Province Area.".format(me, card))

def useability(card, x = 0, y = 0):
	mute()
	if card.highlight == AbilityColor:
		card.highlight = None
	else:
		card.highlight = AbilityColor
		notify("{} uses {}'s ability.".format(me, card))

def discardToFate(card, x = 0, y = 0):
    mute()
    card.moveTo(me.piles['Fate Discard Pile'])
    notify("{} sends {} to the Fate Discard Pile.".format(me, card))

def discardToDynasty(card, x = 0, y = 0):
    mute()
    card.moveTo(me.piles['Dynasty Discard Pile'])
    notify("{} sends {} to the Dynasty Discard Pile.".format(me, card))
	
def removedFromGame(card, x = 0, y = 0):
	mute()
	card.moveTo(me.piles['Removed Pile'])
	notify("{} sends {} to the the Removed Pile.".format(me, card))
    

def addChi(card, x = 0, y = 0):
    mute()
    notify("{} raises {}'s Chi by 1.".format(me, card))
    card.markers[Chi] += 1

def subChi(card, x = 0, y = 0):
    mute()
    notify("{} lowers {}'s Chi by 1.".format(me, card))
    card.markers[Chi_Lower] += 1

def addForce(card, x = 0, y = 0):
    mute()
    notify("{}raises {}'s Force by 1.".format(me, card))
    card.markers[Force] += 1

def subForce(card, x = 0, y = 0):
    mute()
    notify("{} lowers {}'s Force by 1.".format(me, card))
    card.markers[Force_Lower] += 1

def sake(card, x = 0, y = 0):
    mute()
    notify("{} places a Sake Token on {}.".format(me, card))
    card.markers[Sake] += 1

def fire(card, x = 0, y = 0):
    mute()
    notify("{} places a Fire Token on {}.".format(me, card))
    card.markers[Fire] += 1

def gold(card, x=0, y= 0):
	mute()
	notify("{} places a Gold Token on {}.".format(me, card))
	card.markers[Gold] += 1
	
def poison(card, x=0, y= 0):
	mute()
	notify("{} places a Poison Token on {}.".format(me, card))
	card.markers[Poison] += 1
	
def madness(card, x = 0, y = 0):
    mute()
    notify("{} places a Madness Token on {}.".format(me, card))
    card.markers[Madness] += 1

def fudo(card, x = 0, y = 0):
    mute()
    notify("{} places a Fudo Token on {}.".format(me, card))
    card.markers[Fudo] += 1
	
def deadToDynasty(card, x = 0, y = 0):
    mute()
    card.moveTo(me.piles['Dynasty Discard Pile'])
    card.orientation ^= Rot90
    notify("{} sends dead {} to the Dynasty Discard Pile.".format(me, card))

def startProvinceA(group, x = 0, y = 0):
	mute()
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", -120, 240, 1, False)
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", -40, 240, 1, False)
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", 40, 240, 1, False)
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", 120, 240, 1, False)
	
def startProvinceB(group, x = 0, y = 0):
	mute()
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", -120, -320, 1, False)
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", -40, -320, 1, False)
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", 40, -320, 1, False)
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", 120, -320, 1, False)

def createProvince2(group, x = 0, y = 0):
	mute()
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", 40, 240, 1, False)

def createProvince3(group, x = 0, y = 0):
	mute()
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", -40, 240, 1, False)

def createProvince4(group, x = 0, y = 0):
	mute()
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", -120, 240, 1, False)

def createProvince5(group, x = 0, y = 0):
	mute()
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", -200, 240, 1, False)

def createProvince6(group, x = 0, y = 0):
	mute()
	Province = table.create("be71da12-86ba-497c-b684-52948e2716a2", -280, 240, 1, False)

def provinceStrenght(card, x = 0, y = 0):
	mute()
	count = askInteger("The Provinces strenght:", 7)
	if count == None: return
	card.markers[Force] += count

def lobby(card, x = 0, y = 0):
	mute()
	card.orientation ^= Rot90
	if card.orientation & Rot90 == Rot90:
		card.orientation ^= Rot90
		notify('{} lobbied {}'.format(me, card))
		table.create("e3b8e6c4-18d4-4f9e-bc28-8a0e121d0967", 0, 0, 1, True)
	else:
		whisper('The {} is already bowed. Choose another personality.'.format(card))

#------------------------------------------------------------------------------
# Hand Actions
#------------------------------------------------------------------------------

def discard(card, x = 0, y = 0):
 mute()
 notify("{} discards {} from their hand.".format(me, card))
 card.moveTo(me.piles['Fate Discard Pile'])

def randomDiscard(group, x = 0, y = 0):
 mute()
 card = group.random()
 if card == None: return
 notify("{} randomly discards a card.".format(me))
 card.moveTo(me.piles['Fate Discard Pile'])


def rotate0(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot180
    if card.orientation & Rot180 == Rot180:
        notify('{} dishonored {}'.format(me, card))
    else:
        notify('{} rehonors {}'.format(me, card))

def favor(group, x = 0, y = 0):
    card, quantity = askCard({"Card Type":"Token"}, "and")
    if quantity == 0: return
    table.create(card, x, y, quantity)

def token(group, x = 0, y = 0):
    card, quantity = askCard({"Card Type":"Token"}, "and")
    if quantity == 0: return
    table.create(card, x, y, quantity)

def focushand(card, x = 0, y = 0):
	mute()
	card.moveToTable(0,0, True)
	notify("{} Focused.".format(me))
	
def checkText(card, x = 0, y = 0):
	mute()
	whisper('{} - Card Text:'.format(card.name))
	whisper('{}'.format(card.properties['Text Box']))
#------------------------------------------------------------------------------
# Deck Actions
#------------------------------------------------------------------------------

def draw(group, x = 0, y = 0):
 if len(group) == 0: return
 mute()
 group[0].moveTo(me.hand)
 notify("{} draws a card.".format(me))

def shufflefate(group):
  group.shuffle()


def shuffledynasty(group):
  group.shuffle()

def peek(card, x = 0, y = 0):
	card.peek()

def refillProvince(group, x = 0, y = 0):
    if len(group) == 0:return
    mute()
    group[0].moveToTable(0, 0, True)
    notify("{} refilled a Province.".format(me))

def moveToTable(group, x = 0, y = 0, faceDown = True):
    mute()
    group[0].moveToTable(0, 0, True)
    notify("{} Focused.".format(me))

def drawMany(group, count = None):
	mute()
	if len(group) == 0: return
	if count is None:
		count = askInteger("Draw how many cards?", 5)
		if count is None or count <= 0:
			return
	for c in group.top(count):
		c.moveTo(me.hand)
	notify("{} draws {} cards.".format(me, count))
	
def sendtobottomDyn(card, x = 0, y = 0):
	card.moveToBottom(me.piles['Dynasty Deck'])
	notify("{} moved the top card from the Dynasty Deck to the bottom.".format(me))
	
def sendtobottomFate(card, x = 0, y = 0):
	card.moveToBottom(me.piles['Fate Deck'])
	notify("{} moved the top card from the Fate Deck to the bottom.".format(me))