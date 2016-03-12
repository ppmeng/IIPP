# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
          'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, 
                          [pos[0] + CARD_CENTER[0],pos[1] + CARD_CENTER[1]], CARD_SIZE)

        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        s = "Hand contains : "
        for card in self.cards:
            s += str(card) + ','
        return s
        
    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        ace_num = 0
        if len(self.cards) == 0:
            return value
        else:
            for n in range(0, len(self.cards)):
                suit = self.cards[n].get_rank()
                value += VALUES[suit]
                if suit == "A":
                    ace_num += 1
            if (ace_num > 0) and (value + 10 <= 21):
                value += 10
            return value
                
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        cardpos = pos[:]
        if len(self.cards) == 0:
            return
        for n in range(0, len(self.cards)):
            self.cards[n].draw(canvas, cardpos)
            cardpos[0] += 100
        
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cards.append(card)

    def shuffle(self):
        # shuffle the deck, use random.shuffle()
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        card = self.cards.pop()
        return card
    
    def __str__(self):
        # return a string representing the deck
        s = "Deck contains: "
        if self.cards == []:
            return s
        for card in self.cards:
            s += card +","
        return s


#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, score
    player = Hand()
    dealer = Hand()
    deck = Deck()
    
    deck.shuffle()
    card = deck.deal_card()
    player.add_card(card)
    card = deck.deal_card()
    player.add_card(card)
    card = deck.deal_card()
    dealer.add_card(card)
    card = deck.deal_card()
    dealer.add_card(card)
    
    if in_play:
        outcome = "You give up! New game start"
        score -= 1
    else:
        outcome = "New game start"
    
    in_play = True

def hit():
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global in_play, score, outcome
    if in_play:
        card = deck.deal_card()
        player.add_card(card)
        if player.get_value() > 21:
            outcome = "You have bust!New deal?"
            in_play = False
            score -= 1
    
def stand():
    global score, outcome, in_play
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if not in_play:
        return
    if player.get_value() > 21:
        outcome = "You have busted! New deal?"
        score -= 1
    else:
        while (dealer.get_value() < 17):
            card = deck.deal_card()
            dealer.add_card(card)
    if dealer.get_value() > 21:
        outcome = "dealer have busted! New deal?"
        score += 1
    else:
        if player.get_value() > dealer.get_value():
            outcome = "You win!New deal?"
            score += 1
        else:
            outcome = "You loose! New deal?"
            score -= 1
            
    in_play = False
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    pos = [100, 220]
    canvas.draw_text("Blackjack", (30,80), 40, "Orange")
    canvas.draw_text(outcome, (280,100), 22, "White")
    canvas.draw_text("Score = " + str(score), (280,130), 24, "White")
    canvas.draw_text("Dealer", (100, 200), 30, "Black")
    canvas.draw_text("Player", (100, 400), 30, "Black")
   
    dealer.draw(canvas, pos)
    player.draw(canvas, [pos[0], pos[1] + 200])
    if in_play:
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0],CARD_CENTER[1] + CARD_SIZE[1])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_SIZE, 
                          [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_SIZE)


deal()
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling

frame.start()
