import copy
import sys, os
import random
import time
from boards import Bit_board
from boards import Standard_board

random.seed(42)

#This dictionary will store the hash as a key, and the move and the associated value of that move (1 if x can win, -1 if o can win, and 0 for draw) as values

transposition_dictionary = {}

#Creates a 2d list (two-dimensional as there is a list for each player) containing long numbers. It goes to 47 because (for the bitboard) that is the largest index where pieces can be placed (top right position on the board) 

transposition_table = [[random.randrange(1,2**64 - 1) for cell in range(0, 48, 1)] for pieces in range(0,2,1)]

#A function that uses the above two-dimensional list and the placements of crosses and naughts on the bitboard to generate a hash 

def compute_hash(position_one, position_two):
	player1 = position_one
	player2 = position_two
	h = 0
	for i in range(0, 48, 1):
		if player1 & (1 << i):
			h = h ^ transposition_table[0][i]
		elif player2 & (1 << i):
			h = h ^ transposition_table[1][i]			
	return h              

#Ensures text gets printed to the console without delay

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
sys.stdout = Unbuffered(sys.stdout)

play = Standard_board()		

def negamax(theclass, depth, alpha, beta, colour, best_move_so_far):
	alpha_orig = copy.deepcopy(alpha)
	h = compute_hash(theclass.position_one, theclass.position_two)
	if h in transposition_dictionary and transposition_dictionary[h][2] >= depth:
		if transposition_dictionary[h][3] == "exact":
			return [transposition_dictionary[h][0], transposition_dictionary[h][1]]
		elif transposition_dictionary[h][3] == "lower":
			alpha = max(alpha, transposition_dictionary[h][0])
		elif transposition_dictionary[h][3] == "upper":
			beta = min(beta, transposition_dictionary[h][0])
		if alpha >= beta:
			return [transposition_dictionary[h][0], transposition_dictionary[h][1]] 
		return [transposition_dictionary[h][0], transposition_dictionary[h][1]]  
	theclass.connected_four()
	if theclass.gameover == True:
		if theclass.xwin == 1:
			return [((10000000 * 4 * 5) / theclass.turn) * colour, ""]
		elif theclass.owin == -1:
			return [((-10000000 * 4 * 5) / theclass.turn) * colour, ""]
	elif theclass.draw == True:
		return [0, ""]
	elif depth == 0:
		return [theclass.evaluation_function(), ""]

	best_value = -float("Inf")
	moves = theclass.available_moves()
	centredmoves = []
	if 4 in moves:
		centredmoves.append(4)
	if 3 in moves:
		centredmoves.append(3)
	if 5 in moves:
		centredmoves.append(5)
	if 2 in moves:
		centredmoves.append(2)
	if 6 in moves:
		centredmoves.append(6)
	if 1 in moves:
		centredmoves.append(1)
	if 7 in moves:
		centredmoves.append(7)
	best_move = centredmoves[0]	
	for move in centredmoves:
		if best_move_so_far != None:
			move = best_move_so_far
			best_move_so_far = None
		copied = copy.deepcopy(theclass)
		copied.make_move(move-1)
		hypothetical_value = max(best_value, -1 * negamax(copied, depth - 1, -beta, -alpha, -colour, best_move_so_far)[0])
		if hypothetical_value > best_value:
			best_value = hypothetical_value
			best_move = move
		alpha = max(alpha, best_value)
		if alpha >= beta:
			break
	if hypothetical_value <= alpha_orig:
		transposition_dictionary[h] = [best_value, best_move, depth, "upper"]
	elif hypothetical_value >= beta:
		transposition_dictionary[h] = [best_value, best_move, depth, "lower"] 
	else:
		transposition_dictionary[h] = [best_value, best_move, depth, "exact"]
	return [best_value, best_move]


	
def iterative_deepening(theclass, alpha, beta, colour):
	depth = 0
	moves = theclass.available_moves()
	centredmoves = []
	if 4 in moves:
		centredmoves.append(4)
	if 3 in moves:
		centredmoves.append(3)
	if 5 in moves:
		centredmoves.append(5)
	if 2 in moves:
		centredmoves.append(2)
	if 6 in moves:
		centredmoves.append(6)
	if 1 in moves:
		centredmoves.append(1)
	if 7 in moves:
		centredmoves.append(7)
	best_move_so_far = centredmoves[0]
	start_time = time.time()
	while start_time - time.time() >= -10 and depth <= 20:
		depth += 1
		list_of_best_value_and_move = negamax(theclass, depth, alpha, beta, colour, best_move_so_far)
		best_move_so_far = list_of_best_value_and_move[1]
	return list_of_best_value_and_move

twoai = input("Want to watch a game played by two AIs? Y or N?: ")

while twoai.lower() != "y" and twoai.lower() != "n":
	twoai = input("Please enter either Y for yes or N for no: ")

if twoai.lower() == "y":
	while play.evanorodd < 43:
		play.printer()
		if play.evanorodd % 2 == 0:
			bitted = Bit_board(play.board)
			bitted.get_position_and_mask()
			bitted.turn = 0
			aimove = iterative_deepening(bitted, -float("Inf"), float("Inf"), 1)[1]
			play.inputter(aimove)
			print("\nAI dropped a piece in column {column}.".format(column=aimove))
			play.checker()
			if play.gameover == True and play.draw != True:
				play.printer()
				break
			elif play.draw == True:
				print("\nThe game is drawn!")
				play.printer()
				break	
		elif play.evanorodd % 2 != 0:
			bitted = Bit_board(play.board)
			bitted.get_position_and_mask()
			bitted.turn = 1
			aimove = iterative_deepening(bitted, -float("Inf"), float("Inf"), -1)[1]
			play.inputter(aimove)
			print("\nAI dropped a piece in column {column}.".format(column=aimove))
			play.checker()
			if play.gameover == True and play.draw != True:
				play.printer()
				break
			elif play.draw == True:
				print("\nThe game is drawn!")
				play.printer()
				break
elif twoai.lower() == "n":
	ai = input("Would you like to play against an AI? Y or N?: ")

	while ai.lower() != "y" and ai.lower() != "n":
		ai = input("Please enter either Y for yes or N for no: ")
	if ai.lower() == "n":
		while play.evanorodd < 43:
			play.printer()
			try:
				columnnumber = int(input("Enter a column number from one to seven: "))
			except ValueError:
				columnnumber = int(input("\nPlease give an integer!: "))
			play.inputter(columnnumber)
			play.checker()
			if play.gameover == True and play.draw != True:
				play.printer()
				break
			elif play.draw == True:
				print("\nThe game is drawn!")
				play.printer()
				break
	elif ai.lower() == "y":
		iffirst = input("Would you like to go first? Y or N?: ")
		while iffirst.lower() != "y" and iffirst.lower() != "n":
			iffirst = input("Please enter either Y for yes or N for no: ")
		if iffirst.lower() == "y":	
			while play.evanorodd < 43:
				play.printer()
				if play.evanorodd % 2 == 0:
					try:
						columnnumber = int(input("Enter a column number from one to seven: "))
					except ValueError:
						columnnumber = int(input("\nPlease give an integer!: "))
					play.inputter(columnnumber)
					play.checker()
					if play.gameover == True and play.draw != True:
						play.printer()
						break
					elif play.draw == True:
						print("\nThe game is drawn!")
						play.printer()
						break
			
				elif play.evanorodd % 2 != 0:
					bitted = Bit_board(play.board)
					bitted.get_position_and_mask()
					bitted.turn = 1
					aimove = iterative_deepening(bitted, -float("Inf"), float("Inf"), -1)[1]
					play.inputter(aimove)
					print("\nAI dropped a piece in column {column}.".format(column=aimove))
					play.checker()
					if play.gameover == True and play.draw != True:
						play.printer()
						break
					elif play.draw == True:
						print("\nThe game is drawn!")
						play.printer()
						break
		if iffirst.lower() == "n": 	
			while play.evanorodd < 43:
				play.printer()
				if play.evanorodd % 2 == 0:
					bitted = Bit_board(play.board)
					bitted.get_position_and_mask()
					bitted.turn = 0
					aimove = iterative_deepening(bitted, -float("Inf"), float("Inf"), 1)[1]
					play.inputter(aimove)
					print("\nAI dropped a piece in column {column}.".format(column=aimove))
					play.checker()
					if play.gameover == True and play.draw != True:
						play.printer()
						break
					elif play.draw == True:
						print("\nThe game is drawn!")
						play.printer()
						break
				elif play.evanorodd % 2 != 0:
					try:
						columnnumber = int(input("Enter a column number from one to seven: "))
					except ValueError:
						columnnumber = int(input("\nPlease give an integer!: "))
					play.inputter(columnnumber)
					play.checker()
					if play.gameover == True and play.draw != True:
						play.printer()
						break
					elif play.draw == True:
						print("\nThe game is drawn!")
						play.printer()
						break
