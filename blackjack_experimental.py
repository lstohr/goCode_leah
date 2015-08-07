from random import shuffle

suits = ('Clubs','Spades','Hearts','Diamonds')
ranks = ('2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace')

class Card:

	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
		self.name = self.rank + " of " + self.suit
		if self.rank =="Jack" or self.rank== "Queen" or self.rank =="King":
			self.rank = "10"
		if self.rank=="Ace":
			self.rank = "11"
		self.value = int(self.rank)

class Deck:

	def __init__(self):
		self.cards = []
		for suit in suits:
			for rank in ranks:
				self.cards.append(Card(suit, rank))
	
	def num_cards_in_deck(self):
		return len(self.cards)

	def shuffle(self):
		shuffle(self.cards)

	def deal_two(self, deal_to):
		deal_to.get_card(self.cards.pop())
		deal_to.get_card(self.cards.pop())
				
	def deal_one(self, deal_to):
		deal_to.get_card(self.cards.pop())

class Player:
	def __init__(self, name):
		self.name = name
		self.cards_in_hand = []
		self.value_of_hand = 0

	def get_card(self, card):
		self.cards_in_hand.append(card)
		self.check_hand()

	def check_hand(self):
		self.bust = None
		self.value_of_hand = 0
		for card in self.cards_in_hand:
			self.value_of_hand += card.value
		for card in self.cards_in_hand:
			if card.rank == "11" and self.value_of_hand > 21:
				self.value_of_hand -= 10
		if self.value_of_hand > 21:
			self.bust = True

		return self.value_of_hand

	def blackjack_check(self):
		have_ace = False
		have_ten = False
		for card in self.cards_in_hand:
			if "11" in card.rank:
				have_ace = True
		if have_ace == True:
			for card in self.cards_in_hand:
				if "10" in card.rank:
					have_ten = True
		if have_ace == True and have_ten == True:
			print "Blackjack!!"
		
class BlackJackInterface:

	def __init__(self):
		self.people_at_table = [Player("Dealer")]
		self.dealer = self.people_at_table[0]
		
	def dealer_logic(self, deck):
		self.dealer.check_hand()
		while self.dealer.check_hand() <= 16:
			print "Dealer is taking a card. \n"
			deck.deal_one(self.dealer)
			self.dealer.check_hand()
			self.table_view_all_cards() 
			if self.dealer.value_of_hand > 21:
				print "Yay, dealer busts!"
				self.dealer.bust = True
				return 
		print "\nDealer is staying.\n"
		
	def player_logic(self, deck):
		bust = None
		stayed = None
		while bust == None and stayed == None:
			print "Would you like to hit or stay?"
			choice = raw_input("Enter 'hit' or 'stay' >>> ").lower()
			if choice == "hit":
				deck.deal_one(self.people_at_table[1])
				self.people_at_table[1].check_hand()
				if self.people_at_table[1].value_of_hand > 21:
					self.table_view_dealer_down()
					print "Oh no, bust!"
					bust = True
				else:
					self.table_view_dealer_down()
			if choice == "stay":
				stayed = True
				print "Ok, no more cards for you."
				


	def ui_loop(self):
		print "**** You've Entered the Black Jack Game ******"
		self.people_at_table.append(Player(raw_input("Before we play our first hand, what is your name? > ")))
		print "Great, welcome to the table %s!" % self.people_at_table[1].name + " We have a brand new deck of cards to play with. Better shuffle them first."
		keep_playing = "yes"
		print "Ok, shuffled." 

		while keep_playing == "yes":
			self.play_hand()
			keep_playing = raw_input("Would you like to play another hand? Enter 'yes' or 'no' >>> ")
		print "Ok, byeeeeeeeee"
		
	def play_hand(self):
		
		self.people_at_table[1].bust = None # reset for new hand
		self.people_at_table[1].cards_in_hand = [] # reset for new hand
		self.dealer.cards_in_hand = [] # reset for new hand
		
		working_deck = Deck()	# creates new instance of class Deck which we will use for the game
		working_deck.shuffle() # shuffles deck
		
		working_deck.deal_two(self.dealer)	# deals to Dealer
		working_deck.deal_two(self.people_at_table[1])	# deals to first player
		
		print "Now dealing: \n"

		self.table_view_dealer_down()
		self.people_at_table[1].blackjack_check()
		self.player_logic(working_deck)
		
		if self.people_at_table[1].bust:
			print "You lost that one, maybe the next hand."
		else:
			self.dealer_logic(working_deck)
			if self.dealer.bust == True and self.people_at_table[1].bust == None:
				print "You win!"
			else:
				print "The dealer had a " + self.dealer.cards_in_hand[0].name + " down..."
				print "...for a total of " + str(self.dealer.check_hand())
				if self.dealer.check_hand() > self.people_at_table[1].check_hand():
					print "Aww, you lose."
				elif self.dealer.check_hand() == self.people_at_table[1].check_hand():
					print "Push!"
				else:
					print "Sweet, you won!"


	def table_view_dealer_down(self):
		print "------------------- table ------------------------"
		for player in self.people_at_table:
			if player.name == "Dealer":
				print player.name + " has: "
				print "-a face down card-"
				for ind in range(1,len(player.cards_in_hand)):
					print player.cards_in_hand[ind].name
				print "Which is a value of: ??" #+ str(player.check_hand())
				print "\n"
			else:
				print player.name + " has: "
				for card in player.cards_in_hand:
					print card.name
				print "Which is a value of: " + str(player.check_hand())
				print "--------------------------------------------"

	def table_view_all_cards(self):
		print "------------------- table ------------------------"
		for player in self.people_at_table:

				print player.name + " has: "
				for card in player.cards_in_hand:
					print card.name
				print "Which is a value of: " + str(player.check_hand())
				print "\n"
		print "--------------------------------------------"





game = BlackJackInterface()
game.ui_loop()
 


