# coding: utf-8
from enum import Enum

## Defines
# Poker Role
class RoleDefines(Enum):
	ROYAL_FLUSH = 0
	STRAIGHT_FLUSH = 1
	FOUR_CARD = 2
	FULL_HOUSE = 3
	FLUSH = 4
	STRAIGHT = 5
	THREE_CARD = 6
	TWO_PAIR = 7
	ONE_PAIR = 8
	NO_PAIR = 9
# Trump Rank
class RankDefines(Enum):
	ACE = 13
	TWO = 1
	THREE = 2
	FOUR = 3
	FIVE = 4
	SIX = 5
	SEVEN = 6
	EIGHT = 7
	NINE = 8
	TEN = 9
	JACK = 10
	QUEEN = 11
	KING = 12
	NUM_RANK = 13
	JOKER = 52
# Number of matches for each role
class CSRLineDefines(Enum):
	ONE_PAIR = 1
	TWO_PAIR = 2
	THREE_CARD = 3
	FULL_HOUSE = 4
	FOUR_CARD = 6
# Number of cards per suit
CARDS_PER_SUIT = RankDefines.NUM_RANK.value
# Trump Suit (String)
str_suit = [ "CL",
			 "DM",
			 "HT",
			 "SP" ]
# Trump Rank (String)
str_rank = [ "",
			 "2",
			 "3",
			 "4",
			 "5",
			 "6",
			 "7",
			 "8",
			 "9",
			 "10",
			 "J",
			 "Q",
			 "K",
			 "A" ]


## Functions
class PokerRole:
	# Get the target card suit
	def get_card_suit(self, card):
		return(card // CARDS_PER_SUIT)

	# Get the target card rank
	def get_card_rank(self, card):
		rank = card % CARDS_PER_SUIT
		if rank == 0:
			rank = RankDefines.ACE.value
		
		return rank

	# Count the number of matching places
	def count_same_rank_line(self, ranks):
		cnt = 0
		for i in range(0, len(ranks)):
			for j in range((i + 1), len(ranks)):
				if ranks[i] == ranks[j]:
					cnt += 1
		
		return cnt

	# Role judgment process (Flush)
	def is_flush(self, suits):
		is_ret = True
		for i in range(0, (len(suits) - 1)):
			if suits[i] != suits[(i + 1)]:
				is_ret = False
				break
		
		return is_ret

	# Role judgment process (Straight)
	def is_straight(self, ranks):
		is_ret = True
		for i in range(0, (len(ranks) - 2)):
			if (ranks[(i + 1)] - ranks[i]) != 1:
				is_ret = False
				break
		
		if is_ret == True:
			if (ranks[(len(ranks) - 1)] - ranks[(len(ranks) - 2)] == 1) or \
			   ((ranks[(len(ranks) - 2)] == RankDefines.FIVE.value) and (ranks[(len(ranks) - 1)] == RankDefines.ACE.value)):
				is_ret = True
			else:
				is_ret = False
		
		return is_ret

	# Dispaly Card (String)
	def disp_card_str(self, suits, ranks):
		card_str = []
		for i in range(0, len(suits)):
			card_str.append(str_suit[suits[i]] + "_" + str_rank[ranks[i]])
		
		print("Cards (String) :", card_str)

	# Sub Proc of determine a poker role 2
	def check_role_sub2(self, suits, ranks):
		role = RoleDefines.NO_PAIR.value
		
		ret_flush = self.is_flush(suits)
		if ret_flush == True:
			# FLUSH(Preliminary)
			role = RoleDefines.FLUSH.value

		if self.is_straight(ranks) == True:
			if ret_flush == True:
				if ranks[0] == RankDefines.TEN.value:
					# ROYAL FLUSH
					role = RoleDefines.ROYAL_FLUSH.value
				else:
					# STRAIGHT FLUSH
					role = RoleDefines.STRAIGHT_FLUSH.value
			else:
				# STRAIGHT
				role = RoleDefines.STRAIGHT.value

		return role

	# Sub Proc of determine a poker role 1
	def check_role_sub1(self, suits, ranks):
		role = RoleDefines.NO_PAIR.value
		csr_line = self.count_same_rank_line(ranks)
		
		if csr_line == CSRLineDefines.FOUR_CARD.value:
			# FOUR OF A KIND
			role = RoleDefines.FOUR_CARD.value
		elif csr_line == CSRLineDefines.FULL_HOUSE.value:
			# FULL HOUSE
			role = RoleDefines.FULL_HOUSE.value
		elif csr_line == CSRLineDefines.THREE_CARD.value:
			# THREE OF A KIND
			role = RoleDefines.THREE_CARD.value
		elif csr_line == CSRLineDefines.TWO_PAIR.value:
			# TWO PAIR
			role = RoleDefines.TWO_PAIR.value
		elif csr_line == CSRLineDefines.ONE_PAIR.value:
			# PAIR
			role = RoleDefines.ONE_PAIR.value
		else:
			# OTHER ROLE
			role = self.check_role_sub2(suits, ranks)

		return role
	
	# Remove invalid values, duplicates and sort
	def remove_inval_dup(self, cards):
		if len(cards) > 0:
			# Remove invalid values
			while max(cards) > RankDefines.JOKER.value:
				cards.remove(max(cards))
			while min(cards) < (RankDefines.TWO.value - 1):
				cards.remove(min(cards))
			
			# Remove duplicates and sort
			edit_cards = sorted(set(cards))
		else:
			edit_cards = []
		
		return edit_cards

	# Main Proc of determine a poker role
	def check_role_main(self, cards):
		role = RoleDefines.NO_PAIR.value
		# Remove invalid values, duplicates and sort
		edit_cards = self.remove_inval_dup(cards)
		#print("cards :", edit_cards)
		
		# Check the number of cards
		if len(edit_cards) == 5:
			# Determine if JOKER is included
			if edit_cards.count(RankDefines.JOKER.value) == 0:
				# Get card suit and rank list
				card_suits = []
				card_ranks = []
				for card in edit_cards:
					card_suits.append(self.get_card_suit(card))
					card_ranks.append(self.get_card_rank(card))
				# Display card (String)
				self.disp_card_str(card_suits, card_ranks)
				edit_suits = sorted(card_suits)
				#print("suits :", edit_suits)
				edit_ranks = sorted(card_ranks)
				#print("ranks :", edit_ranks)
				# Determine a poker role
				role = self.check_role_sub1(edit_suits, edit_ranks)

		return role

