import RPi.GPIO as GPIO
import shoot_logic as sl
import detection_logic as dl
import rotate_logic as rl
import button_logic as bl
import time

STEP_SIZE = 100

card_vals ={}
card_vals['2'] = 2
card_vals['3'] = 3
card_vals['4'] = 4
card_vals['5'] = 5
card_vals['6'] = 6
card_vals['7'] = 7
card_vals['8'] = 8
card_vals['9'] = 9
card_vals['0'] = 10
card_vals['10'] = 10
card_vals['1'] = 10
card_vals['J'] = 10
card_vals['Q'] = 10
card_vals['K'] = 10
card_vals['A'] = 1

def add_cards(idx):
	sum = 0

	for i in range(len(CARDS[idx])):
		key = CARDS[idx][i]
		val = card_vals[key]
		sum = sum + val

	return sum

""" SETUP """
GPIO.setmode(GPIO.BCM)

# Initialize card detection
# CAP = dl.init_detection()
# dl.detect_card(CAP)

# Initialize card shooting
# Pins 17 and 18 used for shooting cards
sl.init_shoot()

# Pins 5 and 6 are used for buttons
bl.init_buttons()

# Pin 22 and 23 used for rotating the base
rl.init_rotate()


""" CHOOSE NUM PLAYERS """
num = input("Number of players: ")
NUM_PLAYERS = int(num)
while NUM_PLAYERS < 1 and NUM_PLAYERS > 5:
	if NUM_PLAYERS < 1:
		print("Too few players")
	elif NUM_PLAYERS > 5:
		print("Too many players")

	num = input("Number of players: ")
	NUM_PLAYERS = int(num)

# dl.close_detection()
SCORES = [] # Keeps track of the scores of each player; player 0 is the dealer

""" DEAL CARDS """
CARDS = [] # index i is the cards that player i has

# 'player 0' is the dealer

	# it will return empty list []
	# it will return an element
CAP = dl.init_detection()
card = dl.detect_card(CAP)

dl.close_detection(CAP)
print(card)
cards = [card]

CARDS.append(cards)
SCORES.append(add_cards(0))
sl.shoot()

# Deal to the players
for i in range(NUM_PLAYERS):
	
	
	
	player_cards = []

	# rotate to player i
	rl.spin_clockwise(STEP_SIZE)

	# Deal two cards
	for _ in range(2):
		CAP = dl.init_detection()
		# throw away - gives camera enough time to recognize the next card
		# for _ in range(1): #change as necessary
		# 	dl.detect_card(CAP)

		# detecting the card
		card = dl.detect_card(CAP)
		
		player_cards.append(card)

		sl.shoot()
		dl.close_detection(CAP)
		time.sleep(1)

	# all the cards ex) [2,3] will be added to CARDS
	CARDS.append(player_cards)
	SCORES.append(add_cards(i))


# Rotate back
for i in range(NUM_PLAYERS):
	# rotate to player i
	rl.spin_anticlockwise(STEP_SIZE)

# DEBUGGING
print(f"dealer card: {CARDS[0][0]}")
for i in range(1, NUM_PLAYERS + 1):
	print(f"player {i} cards: {CARDS[i][0], CARDS[i][1]}")

print(f"Scores: {SCORES}")


""" GAME """
# for players
for i in range(1, NUM_PLAYERS + 1):
	# rotate to player i
	rl.spin_clockwise(STEP_SIZE)
	done = False
	player_cards = CARDS[i]

	while not done:
		print("hit?")
		has_hit = bl.poll_button()

		if has_hit:
			# throw away - gives camera enough time to recognize the next card
			# for _ in range(1): #change as necessary
			# 	dl.detect_card(CAP)
			CAP = dl.init_detection()
			next_card = dl.detect_card(CAP)
			# # detecting the card
			# next_card = '*'
			# while next_card == '*':
			# 	next_card = dl.detect_card(CAP)
			# 	print(next_card)

			player_cards.append(next_card)
			print("player's cards: ", player_cards)

			sl.shoot()
			dl.close_detection(CAP)
			if add_cards(i) > 21:
				done = True
				print("Bust!")
		else:
			done = True

		SCORES[i] = add_cards(i)


# Rotate back
for i in range(NUM_PLAYERS):
	# rotate to player i
	rl.spin_anticlockwise(STEP_SIZE)


done = False
player_cards = CARDS[0]

while not done:
	# throw away - gives camera enough time to recognize the next card
	# for _ in range(1): #change as necessary
	# 	dl.detect_card(CAP)
	CAP = dl.init_detection()
	# detecting the card
	# next_card = '*'
	# while next_card == '*':
	# 	next_card = dl.detect_card(CAP)
	# 	print(next_card)

	next_card = dl.detect_card(CAP)

	player_cards.append(next_card)
	print("dealer's cards: ", player_cards)

	sl.shoot()
	dl.close_detection(CAP)

	if add_cards(0) >= 17:
		done = True
		print("Dealer's card is over 17. Stop the game!")

	SCORES[0] = add_cards(0)

""" EXIT """
winners = []
ties = []
losers = []
dealer_score = SCORES[0]
result = {}

for i in range(1, len(SCORES)):
	score = SCORES[i]
	if score > 21:
		losers.append(i)
		result[i] = 'Lost'
	elif score <= 21 and dealer_score <= 21 and score < dealer_score:
		losers.append(i)
		result[i] = 'Lost'
	elif dealer_score > 21 and score <= 21:
		winners.append(i)
		result[i] = 'Won'
	elif dealer_score <= 21 and score > dealer_score and score <= 21:
		winners.append(i)
		result[i] = 'Won'
	elif score == dealer_score :
		ties.append(i)
		result[i] = 'Draw'

print("Dealer cards")
print(CARDS[0])
print("Player cards")
print(CARDS[1:len(SCORES)])
print(SCORES)
for i in range(1, len(SCORES)):
	print(f"Player {i} {result[i]}")

#dl.close_detection()



