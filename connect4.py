import copy
import random
class ConnectFour():

	turn = 0
	evanorodd = 0
	gameover = False
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
		moves.clear()

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
						break
					elif self.board[row][column] == "O":
						print("\nThe game is over! Naughts win with a vertical connect four!")
						self.gameover = True
						self.owin = -1
						break
		# checks horizontal
		for row in range(5, -1, -1):
			for column in range(1, 8, 2):
				if self.board[row][column] == self.board[row][column+2] and self.board[row][column] == self.board[row][column+4] and self.board[row][column] == self.board[row][column+6]:
					if self.board[row][column] == "X":
						print("\nThe game is over! Crosses win with a horizontal connect four!")
						self.gameover = True
						self.xwin = 1
						break
					elif self.board[row][column] == "O":
						print("\nThe game is over! Naughts win with a horizontal connect four!")
						self.gameover = True
						self.owin = -1
						break
		# checks diagonal going from left to right
		for row in range(5, 2, -1):
			for column in range(1, 8, 2):
				if self.board[row][column] == self.board[row-1][column+2] and self.board[row][column] == self.board[row-2][column+4] and self.board[row][column] == self.board[row-3][column+6]:
					if self.board[row][column] == "X":
						print("\nThe game is over! Crosses win along a positive diagonal!")
						self.gameover = True
						self.xwin = 1
						break
					elif self.board[row][column] == "O":
						print("\nThe game is over! Naughts win along a positive diagonal!")
						self.gameover = True
						self.owin = -1
						break
		# checks diagonal going from right to left
		for row in range(5, 2, -1):
			for column in range(13, 6, -2):
				if self.board[row][column] == self.board[row-1][column-2] and self.board[row][column] == self.board[row-2][column-4] and self.board[row][column] == self.board[row-3][column-6]:
					if self.board[row][column] == "X":
						print("\nThe game is over! Crosses win along a negative diagonal!")
						self.gameover = True
						self.xwin = 1
						break
					elif self.board[row][column] == "O":
						print("\nThe game is over! Naughts win along a negative diagonal!")
						self.gameover = True
						self.owin = -1
						break

	def aichecker(self):
		# checks vertical
		for row in range(5, 2, -1):
			for column in range(1, 14, 2):
				if self.board[row][column] == self.board[row-1][column] and self.board[row][column] == self.board[row-2][column] and self.board[row][column] == self.board[row-3][column]:
					if self.board[row][column] == "X":
						self.gameover = True
						self.xwin = 1
						break
					elif self.board[row][column] == "O":
						self.gameover = True
						self.owin = -1
						break
		# checks horizontal
		for row in range(5, -1, -1):
			for column in range(1, 8, 2):
				if self.board[row][column] == self.board[row][column+2] and self.board[row][column] == self.board[row][column+4] and self.board[row][column] == self.board[row][column+6]:
					if self.board[row][column] == "X":
						self.gameover = True
						self.xwin = 1
						break
					elif self.board[row][column] == "O":
						self.gameover = True
						self.owin = -1
						break
		# checks diagonal going from left to right
		for row in range(5, 2, -1):
			for column in range(1, 8, 2):
				if self.board[row][column] == self.board[row-1][column+2] and self.board[row][column] == self.board[row-2][column+4] and self.board[row][column] == self.board[row-3][column+6]:
					if self.board[row][column] == "X":
						self.gameover = True
						self.xwin = 1
						break
					elif self.board[row][column] == "O":
						self.gameover = True
						self.owin = -1
						break
		# checks diagonal going from right to left
		for row in range(5, 2, -1):
			for column in range(13, 6, -2):
				if self.board[row][column] == self.board[row-1][column-2] and self.board[row][column] == self.board[row-2][column-4] and self.board[row][column] == self.board[row-3][column-6]:
					if self.board[row][column] == "X":
						self.gameover = True
						self.xwin = 1
						break
					elif self.board[row][column] == "O":
						self.gameover = True
						self.owin = -1
						break



play = ConnectFour()

def evaluate_board(theclass):
	classer = theclass
	num_top_x = 0
	num_top_o = 0
	classer.aichecker()
	if classer.gameover == True:
		if classer.xwin == 1:
			return float("Inf")
		elif classer.owin == -1:
			return -float("Inf")
	else:
		for row in range(5, -1, -1):
			if classer.board[row][7] == "X":
				num_top_x += 1
			elif classer.board[row][7] == "O":
				num_top_o += 1
		return num_top_x - num_top_o			
def minimax(theclass, is_maximizing, depth, alpha, beta, evaluate_board):
	classer = theclass
	classer.aichecker()
	if classer.gameover == True or depth == 0:
		return [evaluate_board(classer), ""]
	if is_maximizing == True:
		best_value = -float("Inf")
		moves = classer.available_moves()
		random.shuffle(moves)
		best_move = moves[0]
		for move in moves:
			copied = copy.deepcopy(classer)
			copied.aiinputter(move)
			hypothetical_value = minimax(copied, False, depth - 1, alpha, beta, evaluate_board)[0]
			if hypothetical_value > best_value:
				best_value = hypothetical_value
				best_move = move
			alpha = max(alpha, best_value)
			if alpha >= beta:
				break
		return [best_value, best_move]
	elif is_maximizing == False:
		best_value = float("Inf")
		moves = classer.available_moves()
		random.shuffle(moves)
		best_move = moves[0]
		for move in moves:
			copied = copy.deepcopy(classer)
			copied.aiinputter(move)
			hypothetical_value = minimax(copied, True, depth -1, alpha, beta, evaluate_board)[0]
			if hypothetical_value < best_value:
				best_value = hypothetical_value
				best_move = move
			beta = min(beta, best_move)
			if alpha >= beta:
				break
		return [best_value, best_move] 
 


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
		if play.gameover == True:
			play.printer()
			break
		if play.evanorodd == 42:
			play.gameover = True
			print("\nThe game is drawn!")
			play.printer()
			break
elif ai.lower() == "y":
	while play.evanorodd < 43:
		play.printer()
		if play.evanorodd % 2 == 0:
			try:
				columnnumber = int(input("Enter a column number from one to seven: "))
			except ValueError:
				columnnumber = int(input("\nPlease give an integer!: "))
			play.inputter(columnnumber)
			play.checker()
			if play.gameover == True:
				play.printer()
				break
			if play.evanorodd == 42:
				play.gameover = True
				print("\nThe game is drawn!")
				play.printer()
				break
		
		elif play.evanorodd % 2 != 0:
			aimove = minimax(play, False, 6, -float("Inf"), float("Inf"), evaluate_board)[1]
			play.aiinputter(aimove)
			play.checker()
			print("\nThe ai dropped a piece in column {column}".format(column=int(aimove/2+0.5)))
			if play.gameover == True:
				play.printer()
				break
			if play.evanorodd == 42:
				play.gameover = True
				print("\nThe game is drawn!")
				play.printer()
				break
		



















