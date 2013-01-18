"""Standard 52 card deckmaker and BlackJack deck preparer""" 

class Deck(object):
    """ Contains all deck creation and value giving methods """

    def deck_builder(self):
        """ Returns a list of strings in "name 'of' suit" format """
        card_deck = []
        card_names = ['Ace', 'King', 'Queen', 'Jack', '10', '9',
                        '8', '7', '6', '5', '4', '3', '2']
        card_suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        suit_iters = 0
        while suit_iters != len(card_suits): # Makes deck list by iterating suit by card
            for name in card_names:
                card = name + ' of ' + card_suits[suit_iters]
                card_deck.append(card)
            suit_iters += 1
        return card_deck

    def bj_valuer(self):
        """ Returns dict with BJ values for each card, Aces value = 1 """
        deck = self.deck_builder()
        bj_deck = {}
        value = 0
        for card in deck:
            try:
                value = int(card[0:2])
            except ValueError:
                if card[0:3] == 'Ace':
                    value = 1
                else:
                    value = 10
            bj_deck[card] = value
        return bj_deck
