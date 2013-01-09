""" This is BlackJackHard"""

import deck
from sys import exit
from random import choice


class GameStructure(object):
    """ The game's organizes the game and offers instructions """
    def __init__(self):
        self.page_break = ('-=' * 40) + '\n'

    def game_map(self):
        """ Organizes the gameplay """
        game_result = None

        self.intro()
        self.instructions()
        while game_result == None:
            game_result = IN_betting.table_actions()
            print self.page_break
        if game_result == 'GAME_WON':
            self.win()
        elif game_result == 'GAME_LOST':
            self.lost()
        else:
            exit(1)
        
    def intro(self):
        """ Welcome screen """
        line = "/\\"
        welcome = "\n\n\t\t\t\tBlackJackHard\n\n"
        print line * 40, welcome, line * 40

    def instructions(self):

        print """\nBlackjack Instructions\n
        \rThe object of the game is to beat the dealer's hand without
        \rexceeding a count of 21 in order to win as much money from the dealer
        \r(the casino) as you can. All number cards are worth their stated
        \ramount, all face cards (except for aces) are worth 10, and aces are worth
        \r1 or 11. If you go over 21, you bust (lose).
        """
        print self.page_break

    def lost(self):
        print "You have no more chips! Get out of my casino!"
        print '\n' + self.page_break
        exit(0)

    def win(self):
        print "You have won! Now get out of my casino!"
        print '\n' + self.page_break
        exit(0)


class Betting(object):
    """ Manages bets and add/deducts chips depending on wins and losses"""
    def __init__(self):
        self.AI_CHIPS = 50
        self.AI_CHIPGOAL = 100

    def table_actions(self):
        legal_bet = False

        print "You currently have %d chips in your balance." % self.AI_CHIPS
        print "%d chips to go!" % (self.AI_CHIPGOAL - self.AI_CHIPS)
        print "How much would you like to bet?"

        while legal_bet == False:
            bet = raw_input('Your bet: ')

            try:
                int(bet)
            except ValueError:
                bet = 'invalid'

            if bet == 'invalid':
                print "Please enter a whole number."
            elif int(bet) <= 0:
                print "Please enter a positive, whole number."
            elif int(bet) > self.AI_CHIPS:
                print "You don't have that much, old chap."
            elif int(bet) == self.AI_CHIPS:
                print "All in! Brave call, good sir!"
                legal_bet = True
            elif int(bet) < self.AI_CHIPS:
                print "Mighty fine bet, good sir!"
                legal_bet = True
            else:
                print "Please input whole number between 1 and %s" % self.AI_CHIPS

        result = IN_hand.order_of_hand_actions()

        if result == 'W':
            self.AI_CHIPS += int(bet)
        elif result == 'L':
            self.AI_CHIPS -= int(bet)
        elif result == 'P':
            pass
        else:
            exit(1)

        if self.AI_CHIPS >= self.AI_CHIPGOAL:
            return 'GAME_WON'
        elif self.AI_CHIPS <= 0:
            return 'GAME_LOST'


class Hand(object):
    """ Plays the BJ hand and returns 'W', 'L' or 'P' for win, loss, or push. """
    AL_PLAYERS_HAND = []
    AL_DEALERS_HAND = []

    def hand_logic(self, command):
        N = IN_narration
        E = IN_evaluator

        if command[0:6] == 'PLAYER':
            new_list = N.narrator(command, self.AL_PLAYERS_HAND)
            if type(new_list) == list:
                self.AL_PLAYERS_HAND = new_list
                self.AS_RESULT = E.player_evaluator(self.AL_PLAYERS_HAND)
                if type(self.AS_RESULT) == list:
                    self.AS_RESULT = None
            elif type(new_list) == str:
                self.AS_RESULT = new_list
        elif command[0:6] == 'DEALER':
            new_list = N.narrator(command, self.AL_DEALERS_HAND)
            if type(new_list) == list:
                self.AL_DEALERS_HAND = new_list
                self.AS_RESULT = E.dealer_evaluator(self.AL_DEALERS_HAND)
            elif type(new_list) == str:
                self.AS_RESULT = new_list
        elif command[0:7] == 'COMPARE':
            comparison_amounts = E.comparison()
            N.narrator('COMPARE', comparison_amounts)
            return comparison_amounts
        elif command[0:4] == 'PUSH':
            self.AS_RESULT = N.narrator('PUSH', None)
        else:
            print 'you exited at hand_logic because it didn\'t stop'
            exit(1)


    def order_of_hand_actions(self):
        """ Runs the Blackjack hands """
        self.AS_RESULT = None
        self.AL_PLAYERS_HAND = []
        self.AL_DEALERS_HAND = []


        self.hand_logic('PLAYER_FIRST_DEAL')
        self.hand_logic('DEALER_FIRST_DEAL')

        ## this loops until player busts or stands
        while self.AS_RESULT == None:
            user_action = raw_input('Hit or Stand? ')
            if user_action.lower() == 'hit':
                self.hand_logic('PLAYER_HIT')
            elif user_action.lower() == 'stand':
                self.hand_logic('PLAYER_STAND')
                break
            else:
                print "Please enter Hit or Stand"

        ## this loops until there is a win or loss
        while self.AS_RESULT == None:
            self.hand_logic('DEALER_HIT')

        if self.AS_RESULT == 'compare':
            players_hand_value, dealers_hand_value = self.hand_logic('COMPARE')
            if players_hand_value > dealers_hand_value:
                self.hand_logic('PLAYER_WINS')
            elif players_hand_value < dealers_hand_value:
                self.hand_logic('DEALER_WINS')
            elif players_hand_value == dealers_hand_value:
                self.hand_logic('PUSH')
            else:
                exit(1)
        return self.AS_RESULT


class Narration(object):
    """ Organizes and print the game story """            

    PLAYER_FIRST_DEAL = "The dealer hands you two cards. Your hand: %s"
    DEALER_FIRST_DEAL = "The dealer deals himself. His hand: %s"
    PLAYER_HIT  = "The dealer hands you another card. Your hand: %s"
    DEALER_HIT  = "The dealer flips another card. His hand: %s"
    PLAYER_STAND = "You decide to stand."
    NEW_DECK = "The dealer gets a new deck and shuffles it."
    PLAYER_BUST = "Your hand busts. You LOSE." 
    DEALER_STAND = "The dealer stands."
    DEALER_BUST = "The dealer busts! You WIN!"
    PLAYER_WINS = "You WIN!"
    DEALER_WINS = "You LOSE."
    COMPARE = "Your hand is %d.\nThe dealer's hand is %d."
    PUSH = 'Your hands are equal. PUSH!'

    def player_first_deal(self, hand_list):
        dealt_cards = IN_cardmover.card_dealing(2)
        hand_list.extend(dealt_cards)
        print self.PLAYER_FIRST_DEAL % hand_list
        return hand_list
    
    def dealer_first_deal(self, hand_list):
        dealt_cards = IN_cardmover.card_dealing(1)
        hand_list.extend(dealt_cards)
        print self.DEALER_FIRST_DEAL % hand_list 
        return hand_list

    def player_hit(self, hand_list):
        dealt_cards = IN_cardmover.card_dealing(1)
        hand_list.extend(dealt_cards)
        print self.PLAYER_HIT % hand_list
        return hand_list

    def dealer_hit(self, hand_list):
        dealt_cards = IN_cardmover.card_dealing(1)
        hand_list.extend(dealt_cards)
        print self.DEALER_HIT % hand_list
        return hand_list
    
    def compare(self, comparison_amounts):
        print self.COMPARE % (comparison_amounts)

    def narrator(self, command, start_list):
        """ Game narration that is chosen with command parameter """

        if command == "PLAYER_FIRST_DEAL":
            return self.player_first_deal(start_list)
        elif command == "DEALER_FIRST_DEAL": 
            return self.dealer_first_deal(start_list)
        elif command == "PLAYER_HIT":
            return self.player_hit(start_list)
        elif command == "DEALER_HIT":
            return self.dealer_hit(start_list)
        elif command == "PLAYER_STAND":
            print self.PLAYER_STAND
        elif command == "PLAYER_BUST":
            print self.PLAYER_BUST
            return 'L'
        elif command == "DEALER_STAND":
            print self.DEALER_STAND
            return 'compare'
        elif command == "DEALER_BUST":
            print self.DEALER_BUST
            return 'W'
        elif command == 'PLAYER_WINS':
            print self.PLAYER_WINS
            return 'W'
        elif command == 'DEALER_WINS':
            print self.DEALER_WINS
            return 'L'
        elif command == 'COMPARE':
            self.compare(start_list)
        elif command == 'PUSH':
            print self.PUSH
            return 'P'
        else:
            exit(1)


class DeckClass(object):
    deck_session = deck.Deck()
    AD_ORIGINAL_DECK = deck_session.bj_valuer() 


class Evaluator(DeckClass):
    """ Checks player and dealer hands to determine busts, dealers
    next action, and comparing who wins. Returns result if the dealer
    or player hand values are met.
    """
    AI_PLAYERS_HAND = 0 
    AI_DEALERS_HAND = 0

    def comparison(self):
        return self.AI_PLAYERS_HAND, self.AI_DEALERS_HAND

    def dealer_evaluator(self, dealers_hand_list):
        value_sum = 0
        ace_in_hand = False

        for card in dealers_hand_list:
            value = self.AD_ORIGINAL_DECK[card]  
            value_sum += value
            if value == 1:
                ace_in_hand = True

        if value_sum <= 11 and ace_in_hand == True:
            value_sum += 10

        self.AI_DEALERS_HAND = value_sum

        if value_sum > 21:
            return IN_narration.narrator('DEALER_BUST', None)
        elif value_sum >= self.AI_PLAYERS_HAND and len(dealers_hand_list) > 1:
            return 'compare'
        elif value_sum >= 17 and ace_in_hand != 0:
            return 'compare'

    def player_evaluator(self, players_hand_list):
        value_sum = 0
        ace_in_hand = False

        for card in players_hand_list:
            card_value = self.AD_ORIGINAL_DECK[card]
            value_sum += card_value
            if card_value == 1:
                ace_in_hand = True

        if value_sum <= 11 and ace_in_hand == True:
            value_sum += 10

        self.AI_PLAYERS_HAND = value_sum

        if value_sum > 21:
            return IN_narration.narrator('PLAYER_BUST', None)


class Cardmover(DeckClass):
    """ Selects random cards from the deck dict, removes them from
    the dict, then send them to dealer or player lists (hands),
    """
    
    def __init__(self):
        self.AD_EDITABLE_DECK = self.AD_ORIGINAL_DECK.copy()

    def card_dealing(self, quantity):
        if len(self.AD_EDITABLE_DECK) <= 26:
            self.card_shuffler()
        return self.card_mover(quantity)


    def card_mover(self, quantity):
        """ Sends random cards to player and dealer lists (hands)
        and returns card strings.
        """
        hand_list = []

        for card in range(quantity):
            hand_list.append(self.card_picker())

        return hand_list

    def card_shuffler(self):
        print "The dealer is shuffling the cards..."
        self.AD_EDITABLE_DECK = self.AD_ORIGINAL_DECK.copy()

    def card_picker(self):
        """ Selects random card from deck dict """
        card = choice(self.AD_EDITABLE_DECK.keys())
        del self.AD_EDITABLE_DECK[card]
        return card        


IN_gamestructure = GameStructure()
IN_betting = Betting()
IN_cardmover = Cardmover()
IN_evaluator = Evaluator() 
IN_narration = Narration()
IN_hand = Hand()
IN_gamestructure.game_map()
