import random

#first let's create a class called Card.
#This will give us the blueprint to create a card in general

class Card():
    def __init__(self, suit, face, value):
        self.suit = suit
        self.face = face
        self.val = value
        
    def __str__(self):
        return self.face + " of " + self.suit + ", value: " + str(self.val)

#then we will create a class called DeckOfCards
#this creates the specifics for each type of card in the deck
class DeckOfCards():
    def __init__(self):
        self.deck = []
        self.suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        self.faces = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        self.values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        self.play_idx = 0
        
        #now we will fill the list 'self.deck' with the cards. 
        #We will loop through the suits, and faces to create each individual card. 
        for suit in self.suits:
            i = 0
            for i in range(len(self.faces)):
                self.deck.append(Card(suit, self.faces[i], self.values[i]))
                
    #this function shuffles the objects in the list self.deck within the class DeckOfCards
    #essentially, this is shuffeling the deck
    def shuffle_deck(self):
        random.shuffle(self.deck)
    
    #this function prints the deck, and tells us what the face and suit of each card is    
    def print_deck(self):
        for card in self.deck:
            print(card.face, "of", card.suit)
        print("---")
    
    #this function is how the user draws a card from the list self.deck. 
    def get_card(self):
        self.play_idx += 1
        return self.deck[self.play_idx - 1]
        
    
        
        
    
        
        