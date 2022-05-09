from DeckOfCards import DeckOfCards
import random


'This is a program to play the card game Blackjack. '

#this is to show that the deck works correctly and that the shuffle works:
deck = DeckOfCards()
deck.print_deck()
deck.shuffle_deck()
deck.print_deck()

#Now let's start the game! 

print("Let's play Blackjack! \n")

letsplay = 'y'

# This loop allows the player to continue playing untill they decide they want to stop. 
while letsplay == "y": 
    
    #Create the deck of cards:
    deck = DeckOfCards()
    
    #Suffle the deck of cards
    deck.shuffle_deck()

    #deal two cards to the user
    card1 = deck.get_card()
    card2 = deck.get_card()
    
    #tell the user what their first two cards are
    print("Your first card is", card1)
    print("Your second card is", card2)
    
    #add the values of the two cards together and call it player_sum
    player_sum = card1.val + card2.val

    #tell the user what their current score is
    print("The sum of your first two cards is:", player_sum, "\n")
    
    #if the player has a blackjack or scores over 21, we automatically determine they don't want a hit
    if player_sum >= 21: 
        hit = 'n'
    
    #if they don't have a blackjack, we ask them if they want a hit
    else: 
        hit = input("Would you like a hit? y or n?")
        print("\n")
        
    
    #as long as the user still wants a hit, do this: 
    while hit == 'y':        
        
        #give the user another card and tell them what card it is
        newcard = deck.get_card()
        print("Your next card is", newcard)
        
        #add the value of this new card to the players score
        player_sum += newcard.val
        
        #tell the player what their total score is
        print("Your total is:", player_sum, "\n")
        
        #if the players score doesn't go above 21, they can continue to choose to hit
        if player_sum < 21: 
            hit = input("Would you like to hit? y or n? \n")
        
        #but if their score goes above 21, don't give them the option to hit
        else: 
            hit = 'n'
        
        
        
    
    #give the dealer a random number between 17 and 23. This is their score.         
    dealer = random.randint(17, 23)
       
    # tell the user what the dealer's score is. 
    print("The dealer's total is:", dealer)
    
    
    #This is the logic for who winns and who loses: 
    
    if player_sum == dealer:
        print("It's a tie. You lose...")
        
    elif player_sum == 21: 
        print("You got a Blackjack! You win!")
        
    elif dealer == 21: 
        print("The dealer got a Blackjack! You lose...")
        
    elif player_sum > 21: 
        print("Oh no! You got over 21 – you bust! ")    
        
    elif dealer > 21: 
        print("That means the dealer busts. You win! ")
    
    elif player_sum > dealer: 
        print("You scored higher than the dealer. You win!")
        
    elif dealer > player_sum: 
        print("That means the dealer scored higher than you. You lose. ")
    
    #ask the user if they want to play again or not. 
    letsplay = input("Do you want to play again? y or n?")
    print("\n")
    
    #if they don't want to play again, break out of the 'letsplay' loop
    if letsplay == 'n': 
        break
    
#thank the user for playing        
print("Thanks for playing! ")