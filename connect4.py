import copy
import sys, os
import random
import time
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


#Below lies the Bitboard class. To help one visualise the bitboard, the printer function can be used.

class Bitboard:
	turn = 0
	xwin = 0
	owin = 0
	gameover = False
	draw = False

	def __init__(self, board):
		self.oldboard = board

	def get_position_and_mask(self):
		self.position_one, self.position_two, self.mask, self.hidden_row = "", "", "", "" 
		for j in range(13, 0, -2):
			#creates the hidden row at the top of the highets visible row (row 6)
			self.hidden_row += "1"
			self.mask += "0"
			self.position_one += "0"
			self.position_two += "0"        
			for i in range(0, 6, 1):
				if self.oldboard[i][j] == "X" or self.oldboard[i][j] == "O":
					self.hidden_row += "0"
					self.mask += "1"
				elif self.oldboard[i][j] == " ":
					self.hidden_row += "0" 
					self.mask += "0"
				if self.oldboard[i][j] == "X":
					self.position_one += "1"
				else:
					self.position_one += "0"
				if self.oldboard[i][j] == "O":
					self.position_two += "1"
				else:
					self.position_two += "0"
		#This variable can be used for the class's printer function
		self.position_one = int(self.position_one, 2)
		self.position_two = int(self.position_two, 2)
		self.mask = int(self.mask, 2)
		self.hidden_row = int(self.hidden_row, 2)

	def printer(self):
		print("The mask:")
		print(bin(2**48 + self.mask)[3:])
		print("The hidden row:")
		print(bin(2**49 + self.hidden_row)[3:])
		print("One position:")
		print(bin(2**48 + self.position_one)[3:])
		print("Other position:")
		print(bin(2**48 + self.position_two)[3:])

	def available_moves(self):
		moves = []
		positionone = self.mask & (1 << 5)                                  
		positiontwo = self.mask & (1 << 12)            
		positionthree = self.mask & (1 << 19)            
		positionfour = self.mask & (1 << 26)            
		positionfive = self.mask & (1 << 33)
		positionsix = self.mask & (1 << 40)                 
		positionseven = self.mask & (1 << 47)  
		if positionone == 0:
			moves.append(1)
		if positiontwo == 0:
			moves.append(2)
		if positionthree == 0:
			moves.append(3) 
		if positionfour == 0:
			moves.append(4)
		if positionfive == 0:
			moves.append(5)
		if positionsix == 0:
			moves.append(6)         
		if positionseven == 0:
			moves.append(7)                  
		return moves

	def make_move(self, column):
		self.turn += 1
		if self.turn % 2 != 0:
			newmask = self.mask | (self.mask + (1 << (column*7)))
			new_position_one = self.position_two ^ newmask
			self.mask = newmask
			self.position_one = new_position_one
		elif self.turn % 2 == 0:
			newmask = self.mask | (self.mask + (1 << (column*7)))
			new_position_two = self.position_one ^ newmask
			self.mask = newmask
			self.position_two = new_position_two

	def evaluation_function(self):
		
		count = 0
		bitmaps = [self.position_one, self.position_two]

		'''

		This function counts up connect 3s along columns, rows, and diagonals. It gives points when
		connect 3s are formed, giving two points for every row and diagonal and one point for every
		column (as rows and diagonals can often provide two spots for a possible connect four to
		form - whereas a column only provides one spot which is directly above it). The function deducts
		the necessary amount of points when the opponent blocks a possibility for a connect four to form. 
		It also deducts points in cases where it is impossible to ever form a connect 4 from the existing 
		connect 3. For example, if row 4, 5 and 6 form a vertical connect 3, it doesn't matter since there
		is no more room above row 6 to form a connect 4. 

		'''

		#vertical

		for idx in range(len(bitmaps)):
			if idx == 0:
				newposition = bitmaps[0]
				otherposition = bitmaps[1]
			if idx == 1:
				newposition = bitmaps[1]
				otherposition = bitmaps[0]
			#print("The position initially:")
			#print(bin(2**48 + newposition)[3:])
			newposition = newposition & (newposition >> 1)
			#print("Right shifted:")
			#print(bin(2**48 + newposition)[3:])
			if newposition & (newposition >> 1):
				newposition = newposition & (newposition >> 1)
				#print("Shifted again:")
				#print(bin(2**48 + newposition)[3:])
				if idx == 0:
					#There will be a one for every connect 3
					number_of_three_columns = bin(2**48 + newposition)[3:].count("1")
					count += number_of_three_columns
				elif idx == 1:
					number_of_three_columns = bin(2**48 + newposition)[3:].count("1")
					count -= number_of_three_columns
				for index, item in enumerate(bin(2**48 + newposition)[3:]):
					if item == "1":
						#Subtracts points if the opponent places above their connect 3
						if bin(2**48 + otherposition)[3:][index-3] == "1":	
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1
						#Subtracts points if there is no room for a connect four (i.e. if the "hidden row" is above the connect 3)
						if bin(2**49 + self.hidden_row)[3:][index-2] == "1":
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1
	
		
		#horizontal checker

		for idx in range(len(bitmaps)):
			if idx == 0:
				newposition = bitmaps[0]
				otherposition = bitmaps[1]
			if idx == 1:
				newposition = bitmaps[1]
				otherposition = bitmaps[0]
			#print("The position")
			#print(bin(2**48 + newposition)[3:])
			#print("Right shifted:")
			newposition = newposition & (newposition >> 7)
			#print(bin(2**48 + newposition)[3:])
			if newposition & (newposition >> 7):
				newposition = newposition & (newposition >> 7)
				#print(True)
				#print("Final look of position:")
				#print(bin(2**48 + newposition)[3:])
				if idx == 0:
					number_of_3_horizontals = bin(2**48 + newposition)[3:].count("1")
					count += number_of_3_horizontals * 2
				elif idx == 1:
					number_of_3_horizontals = bin(2**48 + newposition)[3:].count("1")
					count -= number_of_3_horizontals * 2
				for index, item in enumerate(bin(2**48 + newposition)[3:]):
					if item == "1":
						#print(index)
						try:
							#adjusts score if the opponent is on the left
							if bin(2**48 + otherposition)[3:][index+7] == "1":
								if idx == 0:
									count -= 1
								elif idx == 1:
									count += 1
						except IndexError:
							#There will be an index error if column 1, 2 and 3 are filled (because, depending on the row, the index will be somewhere between 42 and 47)
							#Because there is no room on the left side for another piece, the score gets adjusted accordingly.
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1
							#print("Index Error " + str(index))
						#adjusts score if the opponet is on the right
						if bin(2**48 + otherposition)[3:][index-21] == "1" and index-21 >= 0:
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1
						if index-21 < 0:
							#if the index goes into the negatives, then columns 5, 6 and 7 are filled (as the index would be between 14-19 depending on the row). There is no space on the right-hand side(so the score is adjusted accordingly) 
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1

		

		#positive diagonal

		
		for idx in range(len(bitmaps)):
			if idx == 0:
				newposition = bitmaps[0]
				otherposition = bitmaps[1]
			if idx == 1:
				newposition = bitmaps[1]
				otherposition = bitmaps[0]
			#print("The position initially:")
			#print(bin(2**48 + newposition)[3:])
			newposition = newposition & (newposition >> 8)
			#print("Right shifted:")
			#print(bin(2**48 + newposition)[3:])
			if newposition & (newposition >> 8):
				newposition = newposition & (newposition >> 8)
				#print("Shifted again:")
				#print(bin(2**48 + newposition)[3:])
				if idx == 0:
					number_of_three_positive_diagonals = bin(2**48 + newposition)[3:].count("1")
					count += number_of_three_positive_diagonals * 2
				elif idx == 1:
					number_of_three_positive_diagonals = bin(2**48 + newposition)[3:].count("1")
					count -= number_of_three_positive_diagonals * 2
				for index, item in enumerate(bin(2**48 + newposition)[3:]):
					if item == "1":
						#print(index)
						#Checks if the opponent has filled the space above the connect three positive diagonal
						if bin(2**48 + otherposition)[3:][index-24] == "1" and index-24 >= 0:	
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1
						#It will be less than 0 when columns 5, 6, and 7 are filled. The score is adjusted as there's no room to the right.
						if index -24 < 0:
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1
						#Checks if the opponent has filled the space below the connect three positive diagonal
						try:
							if bin(2**48 + otherposition)[3:][index+8] == "1":
								if idx == 0:
									count -= 1
								elif idx == 1:
									count += 1
						except IndexError:
							#There will be indices that yield an index error here, but they have been dealt with in other if else statements 
							pass	
						#Indices where only one space will ever be available to form a connect four along a positive diagonal. (44 actually has no spaces, but it is accounted for below)
						if index == 47 or index == 46 or index == 45 or index == 44 or index == 40 or index == 33 or index == 26 or index == 19:
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1
						#No more space above these indices, so the score is adjusted accordingly. Index 23 is accounted for above as 23 minus 24 is less than 0. 
						if index == 44 or index == 37 or index == 30:
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1

		#negative diagonal

		for idx in range(len(bitmaps)):
			if idx == 0:
				newposition = bitmaps[0]
				otherposition = bitmaps[1]
			if idx == 1:
				newposition = bitmaps[1]
				otherposition = bitmaps[0]
			#print("The position initially:")
			#print(bin(2**48 + newposition)[3:])
			newposition = newposition & (newposition >> 6)
			#print("Right shifted:")
			#print(bin(2**48 + newposition)[3:])
			if newposition & (newposition >> 6):
				newposition = newposition & (newposition >> 6)
				#print("Shifted again:")
				#print(bin(2**48 + newposition)[3:])
				if idx == 0:
					number_of_three_positive_diagonals = bin(2**48 + newposition)[3:].count("1")
					count += number_of_three_positive_diagonals * 2
				elif idx == 1:
					number_of_three_positive_diagonals = bin(2**48 + newposition)[3:].count("1")
					count -= number_of_three_positive_diagonals * 2
				for index, item in enumerate(bin(2**48 + newposition)[3:]):
					if item == "1":
						#print("original index = " + str(index))
						#If the opponent blocks the three-piece negative diagonal from above, the score gets adjusted
						try:
							if bin(2**48 + otherposition)[3:][index+6] == "1":	
								if idx == 0:
									count -= 1
								elif idx == 1:
									count += 1
						#There will be an IndexError if columns 1, 2 and 3 are filled (indices 42-45 depending on the row). No more space to the left, so scores are adjusted.
						except IndexError:
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1
							#print("Index Error - negative diagonal")				
						#Indices where there is only room to form one possible connect four
						if index == 45 or index == 38 or index == 31 or index == 24 or index == 17 or index == 16:
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1
						#If the opponent blocks the three-piece negative diagonal from below, the score gets adjusted
						if bin(2**48 + otherposition)[3:][index-18] == "1" and index-18 >= 0:
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1
						#No more space available above these indices, so the score gets adjusted.
						if index == 35 or index == 28 or index == 21 or index == 15:
							if idx == 0:
								count -= 1
							elif idx == 1:
								count += 1
						#Special case for index 14 since there is no more space above it and there is no room for a negative connect four below it. 
						if index == 14:
							if idx == 0:
								count -= 2
							elif idx == 1:
								count += 2
		
		#print(count)
		return count
	def connected_four(self):
		one_player = self.position_one
		other_player = self.position_two
		bitmaps = [one_player, other_player]
		for maps in bitmaps:
			# Horizontal check
			m = maps & (maps >> 7)
			if m & (m >> 14):
				if maps == one_player:
					if self.turn % 2 != 0:
						self.xwin = 1
					elif self.turn % 2 == 0:
						self.owin = -1
					self.gameover = True
					return
				elif maps == other_player:
					if self.turn % 2 != 0:
						self.xwin = 1
					elif self.turn % 2 == 0:
						self.owin = -1
					self.gameover = True
					return 
			# Negative diagonal
			m = maps & (maps >> 6)
			if m & (m >> 12):
				if maps == one_player:
					if self.turn % 2 != 0:
						self.xwin = 1
					elif self.turn % 2 == 0:
						self.owin = -1
					self.gameover = True
					return
				elif maps == other_player:
					if self.turn % 2 != 0:
						self.xwin = 1
					elif self.turn % 2 == 0:
						self.owin = -1
					self.gameover = True
					return
			# Positive diagonal
			m = maps & (maps >> 8)
			if m & (m >> 16):
				if maps == one_player:
					if self.turn % 2 != 0:
						self.xwin = 1
					elif self.turn % 2 == 0:
						self.owin = -1
					self.gameover = True
					return
				elif maps == other_player:
					if self.turn % 2 != 0:
						self.xwin = 1
					elif self.turn % 2 == 0:
						self.owin = -1
					self.gameover = True
					return
    			# Vertical
			m = maps & (maps >> 1)
			if m & (m >> 2):
				if maps == one_player:
					if self.turn % 2 != 0:
						self.xwin = 1
					elif self.turn % 2 == 0:
						self.owin = -1
					self.gameover = True
					return
				elif maps == other_player:
					if self.turn % 2 != 0:
						self.xwin = 1
					elif self.turn % 2 == 0:
						self.owin = -1
					self.gameover = True
					return
		#checks for the draw
		one = self.mask & (1 << 5)
		two = self.mask & (1 << 12)
		three = self.mask & (1 << 19)
		four = self.mask & (1 << 26)
		five = self.mask & (1 << 33)
		six = self.mask & (1 << 40)
		seven = self.mask & (1 << 47)
		if one != 0 and two != 0 and three != 0 and four != 0 and five != 0 and six != 0 and seven != 0:
			self.draw = True

class ConnectFour():
	turn = 0
	evanorodd = 0
	gameover = False
	draw = False
	xwin = 0
	owin = 0
	
	def __init__(self):
		self.board = [[" " for column in range(15)] for row in range(6)]
		for row_index, row in enumerate(self.board):
			for col_index, item in enumerate(row):
				if col_index % 2 == 0:
					self.board[row_index][col_index] = "|"

	def printer(self):
		if self.gameover == True:
			print("\nThe final board state:")
		else:
			print("\nTurn {turn}.".format(turn=self.turn))
		print("\n  1   2   3   4   5   6   7")
		for row in self.board:
			for item in row:
				print(item, end = " ")
			print()
	def available_moves(self):
		moves = []
		for i in range(1, 14, 2):
			if self.board[0][i] == " ":
				moves.append(i)
		return moves

	def inputter(self, col_index):
		self.turn += 1
		self.evanorodd += 1
		num = col_index * 2 - 1
		if num >=1 and num <= 13 and num % 2 != 0:
			if self.board[0][num] == " ":
				for i in range(5, -1, -1):
					if self.board[i][num] == " ":
						if self.evanorodd % 2 != 0:
							self.board[i][num] = "X"
							break
						else:
							self.board[i][num] = "O"
							break
			else:
				self.evanorodd -= 1
				print("\nI'm afraid that column is full. Choose another one.")
		else:
			self.evanorodd -= 1
			print("\nYou need to give a column number from one to seven.")
		
	def aiinputter(self, col_index):
		self.turn += 1
		self.evanorodd += 1
		for i in range(5, -1, -1):
			if self.board[i][col_index] == " ":
				if self.evanorodd % 2 != 0:
					self.board[i][col_index] = "X"
					break
				else:
					self.board[i][col_index] = "O"
					break
	def checker(self):
		# checks vertical
		for row in range(5, 2, -1):
			for column in range(1, 14, 2):
				if self.board[row][column] == self.board[row-1][column] and self.board[row][column] == self.board[row-2][column] and self.board[row][column] == self.board[row-3][column]:
					if self.board[row][column] == "X":
						print("\nThe game is over! Crosses win with a vertical connect four!")
						self.gameover = True
						self.xwin = 1
						return
					elif self.board[row][column] == "O":
						print("\nThe game is over! Naughts win with a vertical connect four!")
						self.gameover = True
						self.owin = -1
						return
		# checks horizontal
		for row in range(5, -1, -1):
			for column in range(1, 8, 2):
				if self.board[row][column] == self.board[row][column+2] and self.board[row][column] == self.board[row][column+4] and self.board[row][column] == self.board[row][column+6]:
					if self.board[row][column] == "X":
						print("\nThe game is over! Crosses win with a horizontal connect four!")
						self.gameover = True
						self.xwin = 1
						return
					elif self.board[row][column] == "O":
						print("\nThe game is over! Naughts win with a horizontal connect four!")
						self.gameover = True
						self.owin = -1
						return
		# checks diagonal going from left to right
		for row in range(5, 2, -1):
			for column in range(1, 8, 2):
				if self.board[row][column] == self.board[row-1][column+2] and self.board[row][column] == self.board[row-2][column+4] and self.board[row][column] == self.board[row-3][column+6]:
					if self.board[row][column] == "X":
						print("\nThe game is over! Crosses win along a positive diagonal!")
						self.gameover = True
						self.xwin = 1
						return
					elif self.board[row][column] == "O":
						print("\nThe game is over! Naughts win along a positive diagonal!")
						self.gameover = True
						self.owin = -1
						return
		# checks diagonal going from right to left
		for row in range(5, 2, -1):
			for column in range(13, 6, -2):
				if self.board[row][column] == self.board[row-1][column-2] and self.board[row][column] == self.board[row-2][column-4] and self.board[row][column] == self.board[row-3][column-6]:
					if self.board[row][column] == "X":
						print("\nThe game is over! Crosses win along a negative diagonal!")
						self.gameover = True
						self.xwin = 1
						return
					elif self.board[row][column] == "O":
						print("\nThe game is over! Naughts win along a negative diagonal!")
						self.gameover = True
						self.owin = -1
						return
		#checks if everywhere is full
		spaces_left = sum(row.count(" ") for row in self.board)
		if spaces_left == 0 and self.xwin != 1 and self.owin != -1:
			self.draw = True
			self.gameover = True

play = ConnectFour()		

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
	while start_time - time.time() >= -12 and depth <= 20:
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
			bitted = Bitboard(play.board)
			bitted.get_position_and_mask()
			bitted.turn = 0
			aimove = iterative_deepening(bitted, -float("Inf"), float("Inf"), 1)[1]
			play.inputter(aimove)
			print("\nNew AI with depth 5 dropped a piece in column {column}.".format(column=aimove))
			play.checker()
			if play.gameover == True and play.draw != True:
				play.printer()
				break
			elif play.draw == True:
				print("\nThe game is drawn!")
				play.printer()
				break	
		elif play.evanorodd % 2 != 0:
			bitted = Bitboard(play.board)
			bitted.get_position_and_mask()
			bitted.turn = 1
			aimove = iterative_deepening(bitted, -float("Inf"), float("Inf"), -1)[1]
			play.inputter(aimove)
			print("\nNew AI with depth 5 dropped a piece in column {column}.".format(column=aimove))
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
					bitted = Bitboard(play.board)
					bitted.get_position_and_mask()
					bitted.turn = 1
					aimove = iterative_deepening(bitted, -float("Inf"), float("Inf"), -1)[1]
					play.inputter(aimove)
					print("\nNew AI with depth 11 dropped a piece in column {column}.".format(column=aimove))
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
					bitted = Bitboard(play.board)
					bitted.get_position_and_mask()
					bitted.turn = 0
					aimove = iterative_deepening(bitted, -float("Inf"), float("Inf"), 1)[1]
					play.inputter(aimove)
					print("\nNew AI with depth 9 dropped a piece in column {column}.".format(column=aimove))
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
