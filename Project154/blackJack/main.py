import time
import random
import blackjackgame

if __name__ == "__main__":
    random.seed(time.time())

    # Welcome message
    print("----------------------------------------------------------------")
    print("                 ♠♣♥♦ WELCOME TO BLACKJACK ♠♣♥♦")
    print("----------------------------------------------------------------")

    # Player chooses policy
    while True:
        print("Choose policy: 0 - Stick >= 17")
        print("               1 - Stick >= Hard 17")
        inputPolicy = int(input("Enter policy: "))
        if inputPolicy == 0:
            break
        if inputPolicy == 1:
            break
        print("Invalid Input!\n")

    # Player chooses deck type
    while True:
        print("\nDeck Type: 0 - Infinite Deck")
        print("           1 - Single Deck")
        inputDeck = int(input("Enter deck type: "))
        if inputDeck == 0:
            break
        if inputDeck == 1:
            break
        print("Invalid Input!\n")

    inputIterations = int(input("\nNumber of games that you want to play: "))

    # Calculate time and number of wins, losses, ties
    start = time.time()
    wins, losses, ties, avg = blackjackgame.blackjackGame(inputPolicy, inputDeck, inputIterations)
    elapsed = time.time() - start

    print("--------------------------------------------------------")
    print("Inputs picked:", inputPolicy, inputDeck, inputIterations)
    print("Wins:", wins)
    print("Losses:", losses)
    print("Ties:", ties)
    print("Average Winning Percentage:", avg)
    print("Time taken:", elapsed)