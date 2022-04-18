import time
import random

# Calculates the possible hand values for either soft or hard
# First checks if there are any aces.
# If so, count the number of aces and find every possible pairing of those aces as 1's and 11's
# The possible = be the sum of the rest of the cards (sum(cards) - numAces) + those combinations of 1's and 11's
# Only add hands to the handValues list if it's less than or equal 21 since everything else is a bust. [] implies no non-bust hands
# Sum the card values and append if <= 21 if there are no aces
def calculateHandValues(cards):
    # Check if there are any aces in hand
    haveAces = 1 in cards
    # There are no hands initially, can only add a hand if it will not bust
    handValues = []


    # Have ace(s) case: soft hand
    if haveAces:
        numAces = cards.count(1)
        # Make every (x,y) pair of the num of aces counting as 1 or 11 (x -> 1, y -> 11)
        possibleAces = [(x,y) for x in [0, 1, 2, 3, 4] for y in [0, 1, 2, 3, 4] if x + y == numAces]
        temp = sum(cards) - numAces                                                           # Ex: I have two aces. (0,2) or (1,1) or (2,0) => two 11's or one 1, one 11 or two 1's
        possibleHands = [temp + (x * 1) + (y * 11) for (x,y) in possibleAces]  # add the rest of the cards with those possible ace values
        for i in possibleHands:
            if i <= 21:
                handValues.append(i)

    # No aces case: hard hand
    else:
        temp = sum(cards) # Sum the card values
        if temp <= 21:
            handValues.append(temp)
    return handValues

# Soft hand: https://www.blackjackapprenticeship.com/wp-content/uploads/2018/10/mini-blackjack-strategy-chart.png
def softHand(handVal, dealerCard):
    if handVal > 18:
        return "STAND"
    elif handVal == 18:
        if dealerCard in [9, 10, 1]:
            return "HIT"
        else:
            return "STAND"
    else:
        return "HIT"

# Hard hands: https://www.blackjackapprenticeship.com/wp-content/uploads/2018/10/mini-blackjack-strategy-chart.png
def hardHand(handVal, dealerCard):
    if handVal >= 17:
        return "STAND"
    elif handVal > 12:
        if dealerCard in [6, 7, 8, 9, 10, 1]:
            return "HIT"
        else:
            return "STAND"
    elif handVal == 12:
        if dealerCard in [4, 5, 6]:
            return "STAND"
        else:
            return "HIT"
    else:
        return "HIT"

# Hit or Stand for the Player Decisions
# This function looks at the player's cards, the dealer's cards, and the player policy to make the decision of Hit or Stand
def hitOrStand(playerCards, dealerCards, policy):
    handValues = calculateHandValues(playerCards)
    if policy == 0:
        for i in handValues:
            # Stand >= 17
            if i >= 17:
                return "STAND"
        return "HIT"

    else:
        if handValues[len(handValues) - 1] >= 17:
            return "STAND"
        else:
            return "HIT"

# Pick cards from a single deck (whenever a card is picked, the total number of cards in the deck decreases accordingly)
# Pick a card from the available cards and swaps that card with the first card available in the deck
# Then, it increments the firstCard value such that the chosen card (swapped one) is no longer in range
# Ex: [1,2,3,4] Let's say we choose 2.
#     [2,1,3,4] Swap 2 and first card (the first card in this case is 1)
#     firstCard = 0 + 1 = 1  The first available card is now set to index 1, which is 2 so the 3 can no longer be accessed.
# This modified deck and the first card that should be available are returned to maintain the deck across multiple player decisions (multiple HITs).
def pickCardsSingle(deck, cardAmt, firstCard):
    deckLength = 52 - firstCard
    for i in range(cardAmt):
        card = int(random.random() * deckLength) + firstCard
        deck[firstCard], deck[card] = deck[card], deck[firstCard]
        firstCard += 1
        deckLength = 52 - firstCard
    return deck, firstCard

# SINGLE DECK
# Create a single deck of card
# Player picks two cards
# Then, the dealer picks two card
# The player performs their decisions first, then decides to bust, stand, or hit 21
# Then the dealer performs their strategy
# If both the player and dealer don't bust or hit 21, they then have a showdown
# The winner is the one that has the bigger total card values, and it is a tie if both the dealer and player have the same card value
def singleDeck(policy):
    # No card is chosen initially
    deckStart = 0
    # Initial deck of cards
    deck = [1, 1, 1, 1,
            2, 2, 2, 2,
            3, 3, 3, 3,
            4, 4, 4, 4,
            5, 5, 5, 5,
            6, 6, 6, 6,
            7, 7, 7, 7,
            8, 8, 8, 8,
            9, 9, 9, 9,
            10, 10, 10, 10,
            10, 10, 10, 10,
            10, 10, 10, 10,
            10, 10, 10, 10]
    # Update deck and deckStart
    deck, deckStart = pickCardsSingle(deck, 2, deckStart)
    # PLayer gets 2 cards
    playerCards = [deck[0], deck[1]]

    # Update deck and decksStart
    deck, deckStart = pickCardsSingle(deck, 2, deckStart)
    # Dealer gets 2 cards
    dealerCards = [deck[2], deck[3]]

    playerDecision = ""
    # Function where player makes a decision until they decide to stand, bust, or hit 21
    while playerDecision != "STAND":
        # Calculate hand values
        handValues = calculateHandValues(playerCards)
        # Empty hand values = busted
        if handValues == []:
            return False
        # Player wins if they hit 21 (BlackJack)
        if handValues[0] == 21:
            return True
        # Player makes decision
        playerDecision = hitOrStand(playerCards, dealerCards, policy)
        # If the player decides to hit, they pick a card that will be added to their current cards
        if playerDecision == "HIT":
            deck, deckStart = pickCardsSingle(deck, 1, deckStart)
            playerCards.append(deck[deckStart - 1])

    dealerDecision = ""
    # Dealer's decision, same as player's
    while dealerDecision != "STAND":
        handValues = calculateHandValues(dealerCards)
        # Calculate hand values
        if handValues == []:
            return True
        # Dealer wins if they hit 21 (Blackjack)
        if handValues[0] == 21:
            return False
        # There is a soft hand at index 0 if there are nore than one handValue
        if handValues[0] == 17 and len(handValues) == 2:
            dealerDecision = "HIT"  # hit on soft 17
        elif handValues[0] >= 17:  # stand on anything > 17 or on hard 17
            dealerDecision = "STAND"
        else:
            dealerDecision = "HIT"  # hit when < 17 otherwise
        if dealerDecision == "HIT":  # Pick a card and add to the current cards if hit
            deck, deckStart = pickCardsSingle(deck, 1, deckStart)
            dealerCards.append(deck[deckStart - 1])

    #Showdown
    playerCardValue = calculateHandValues(playerCards)[0]
    dealerCardValue = calculateHandValues(dealerCards)[0]

    # Win = 1; Loss = 0; Tie = 2
    if playerCardValue > dealerCardValue:
        return 1  # return 1 because player wins
    elif playerCardValue < dealerCardValue:
        return 0  # return 2 because player losses
    else:
        return 2  # return 2 if tie

# Pick cards from an infinite deck
# Simply defines the possible values for the cards and picks one value randomly
def pickCardsInfinite():
    infinite = [1, 1, 1, 1,
                2, 2, 2, 2,
                3, 3, 3, 3,
                4, 4, 4, 4,
                5, 5, 5, 5,
                6, 6, 6, 6,
                7, 7, 7, 7,
                8, 8, 8, 8,
                9, 9, 9, 9,
                10, 10, 10, 10,
                10, 10, 10, 10,
                10, 10, 10, 10,
                10, 10, 10, 10]
    card = int(random.random() * 52)
    return infinite[card]

# INFINITE DECK
def infiniteDeck(policy):
    playerCards = [pickCardsInfinite(), pickCardsInfinite()]

    dealerCards = [pickCardsInfinite(), pickCardsInfinite()]

    playerDecision = ""
    while playerDecision != "STAND":
        handValues = calculateHandValues(playerCards)
        if handValues == []:
            return False
        if handValues[0] == 21:
            return True
        playerDecision = hitOrStand(playerCards, dealerCards, policy)
        if playerDecision == "HIT":
            playerCards.append(pickCardsInfinite())

    dealerDecision = ""
    while dealerDecision != "STAND":
        handValues = calculateHandValues(dealerCards)
        if handValues == []:
            return True # Dealer Bust
        if handValues[0] == 21:
            return False # Dealer Blackjack
        if handValues[0] == 17 and len(handValues) == 2:
            dealerDecision = "HIT"
        elif handValues[0] >= 17:
            dealerDecision = "STAND"
        else:
            dealerDecision = "HIT"
        if dealerDecision == "HIT":
            dealerCards.append(pickCardsInfinite())

    #SHOWDOWN
    playerCardValue = calculateHandValues(playerCards)[0]
    dealerCardValue = calculateHandValues(dealerCards)[0]

    # Win = 1; Loss = 0; Tie = 2
    if playerCardValue > dealerCardValue:
        return 1  # return 1 because player wins
    elif playerCardValue < dealerCardValue:
        return 0  # return 0 because player losses
    else:
        return 2  # return 2 for tie

# Function for counting the number of wins, losses, and ties
def blackjackGame(playerPolicy, deckType, n):
    random.seed(time.time())
    wins = 0
    losses = 0
    ties = 0

    for i in range(n):
        if deckType:
            wonGame = singleDeck(playerPolicy)
        else:
            wonGame = infiniteDeck(playerPolicy)
        if wonGame == 1:
            wins += 1
        elif wonGame == 0:
            losses += 1
        else:
            ties += 1

    if n - ties == 0:
        return wins, losses, ties, 0
    avg = wins / (n - ties) * 100
    return wins, losses, ties, avg