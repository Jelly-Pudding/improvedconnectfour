import copy
import sys, os
import random
random.seed(42)

transposition_dictionary = {}

transposition_table = [[random.randrange(1,2**64 - 1) for cell in range(0, 50, 1)] for pieces in range(0,2,1)]

def compute_hash(mask, position):
	player1 = position
	player2 = position ^ mask
	h = 0
	for i in range(0, 50, 1):
		if player1 & (1 << i):
			h = h ^ transposition_table[0][i]
		elif player2 & (1 << i):
			h = h ^ transposition_table[1][i]			
	return h              

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


class Bitboard:
	turn = 0
	xwin = 0
	owin = 0
	gameover = False
	draw = False

	def __init__(self, board):
		self.oldboard = board

	def get_position_and_mask(self):
		self.position, self.mask = '', ''
		for j in range(13, 0, -2):
			self.mask += "0"
			self.position += "0"        
			for i in range(0, 6, 1):
				if self.oldboard[i][j] == "X" or self.oldboard[i][j] == "O":
					self.mask += "1"
				elif self.oldboard[i][j] == " ":
					self.mask += "0"
				if self.oldboard[i][j] == "X":
					self.position += "1"
				else:
					self.position += "0"
		self.position = int(self.position, 2)
		self.mask = int(self.mask, 2)



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
		new_position = self.position ^ self.mask
		new_mask = self.mask | (self.mask + (1 << (column*7)))
		self.position = new_position
		self.mask = new_mask

	def connected_four(self):
		#horizontal check  
		crosses = self.position
		mask = self.mask
		naughts = crosses ^ mask
		bitmaps = [crosses, naughts]
		for maps in bitmaps:
			# Horizontal check
			m = maps & (maps >> 7)
			if m & (m >> 14):
				if maps == crosses:
					self.xwin = 1
				elif maps == naughts:
					self.owin = -1
				self.gameover = True
				return
			# Diagonal \
			m = maps & (maps >> 6)
			if m & (m >> 12):
				if maps == crosses:
					self.xwin = 1
				elif maps == naughts:
					self.owin = -1
				self.gameover = True
				return
			# Diagonal /
			m = maps & (maps >> 8)
			if m & (m >> 16):
				if maps == crosses:
					self.xwin = 1
				elif maps == naughts:
					self.owin = -1
				self.gameover = True
				return
    			# Vertical
			m = maps & (maps >> 1)
			if m & (m >> 2):
				if maps == crosses:
					self.xwin = 1
				elif maps == naughts:
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

def minimax(theclass, is_maximizing, depth, alpha, beta):
	theclass.connected_four()
	h = compute_hash(theclass.mask, theclass.position)
	if h in transposition_dictionary:
		if transposition_dictionary[h][0] >= beta:
			return [transposition_dictionary[h][0], transposition_dictionary[h][1]] 
		if transposition_dictionary[h][0] <= alpha:
			return [transposition_dictionary[h][0], transposition_dictionary[h][1]]
		if alpha < transposition_dictionary[h][0] and transposition_dictionary[h][0] < beta:
			return [transposition_dictionary[h][0], transposition_dictionary[h][1]]
		alpha = max(alpha, transposition_dictionary[h][0])
		beta = min(beta, transposition_dictionary[h][0]) 
	if theclass.gameover == True:
		if theclass.xwin == 1:
			return [(10000000 - theclass.turn), ""]
		elif theclass.owin == -1:
			return [(-10000000 + theclass.turn), ""]
	elif theclass.draw == True:
		return [0, ""]
	elif depth == 0:
		return [0, ""]
	if is_maximizing == True:
		best_value = -float("Inf")
		a = -float("Inf")
		moves = theclass.available_moves()
		centredmoves = []
		if 4 in moves:
			centredmoves.append(4)
		if 3 in moves:
			centredmoves.append(3)
		if 6 in moves:
			centredmoves.append(6)
		if 2 in moves:
			centredmoves.append(2)
		if 5 in moves:
			centredmoves.append(5)
		if 1 in moves:
			centredmoves.append(1)
		if 7 in moves:
			centredmoves.append(7)
		best_move = centredmoves[0]	
		for move in centredmoves:
			copied = copy.deepcopy(theclass)
			copied.make_move(move-1)
			hypothetical_value = minimax(copied, False, depth - 1, a, beta)[0]
			if hypothetical_value > best_value:
				best_value = hypothetical_value
				best_move = move
			alpha = max(alpha, best_value)
			if alpha >= beta:
				break
			transposition_dictionary[h] = [best_value, best_move]
		return [best_value, best_move]
	elif is_maximizing == False:
		best_value = float("Inf")
		b = float("Inf")
		moves = theclass.available_moves()
		centredmoves = []
		if 4 in moves:
			centredmoves.append(4)
		if 3 in moves:
			centredmoves.append(3)
		if 6 in moves:
			centredmoves.append(6)
		if 2 in moves:
			centredmoves.append(2)
		if 5 in moves:
			centredmoves.append(5)
		if 1 in moves:
			centredmoves.append(1)
		if 7 in moves:
			centredmoves.append(7)
		best_move = centredmoves[0]
		for move in centredmoves:
			copied = copy.deepcopy(theclass)
			copied.make_move(move-1)
			hypothetical_value = minimax(copied, True, depth -1, alpha, b)[0]
			if hypothetical_value < best_value:
				best_value = hypothetical_value
				best_move = move
			beta = min(beta, best_move)
			if alpha >= beta:
				break
			transposition_dictionary[h] = [best_value, best_move]
		return [best_value, best_move] 

	

twoai = input("Want to watch a game played by two AIs? Y or N?: ")

while twoai.lower() != "y" and twoai.lower() != "n":
	twoai = input("Please enter either Y for yes or N for no: ")

if twoai.lower() == "y":
	while play.evanorodd < 43:
		play.printer()
		if play.evanorodd % 2 == 0:
			bitted = Bitboard(play.board)
			bitted.get_position_and_mask()
			aimove = minimax(bitted, True, 5, -float("Inf"), float("Inf"))[1]
			play.inputter(aimove)
			print("\nNew AI with depth 6 dropped a piece in column {column}.".format(column=aimove))
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
			aimove = minimax(bitted, False, 5, -float("Inf"), float("Inf"))[1]
			play.inputter(aimove)
			print("\nNew AI with depth 6 dropped a piece in column {column}.".format(column=aimove))
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
					aimove = minimax(bitted, False, 5, -float("Inf"), float("Inf"))[1]
					play.inputter(aimove)
					print("\nNew AI with depth 6 dropped a piece in column {column}.".format(column=aimove))
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
					aimove = minimax(bitted, True, 5, -float("Inf"), float("Inf"))[1]
					play.inputter(aimove)
					print("\nNew AI with depth 6 dropped a piece in column {column}.".format(column=aimove))
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
