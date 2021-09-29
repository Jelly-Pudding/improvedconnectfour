import copy
import sys, os

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
						self.gameover = True
						self.xwin = 1
						print("\nThe game is over! Crosses win with a vertical connect four!")
						return
					elif self.board[row][column] == "O":
						self.gameover = True
						self.owin = -1
						print("\nThe game is over! Naughts win with a vertical connect four!")
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

def blockprint():
	sys.stdout = open(os.devnull, 'w')
def enableprint():
	sys.stdout = sys.__stdout__
	sys.stdout = Unbuffered(sys.stdout)


play = ConnectFour()

def old_evaluate(theclass):
	classer = theclass
	num_top_x = 0
	num_top_o = 0
	if classer.xwin == 1:
		return float("Inf")
	elif classer.owin == -1:
		return -float("Inf")
	else:
		#Gives points for going in the middle
		for row in range(5, -1, -1):
			if classer.board[row][7] == "X":
				num_top_x += 4
			elif classer.board[row][7] == "O":
				num_top_o += 4
		#Gives (less) points for going in the fifth column
		for row in range(5, -1, -1):
			if classer.board[row][5] == "X":
				num_top_x += 2
			elif classer.board[row][5] == "O":
				num_top_o += 2
		#Points for the ninth column
		for row in range(5, -1, -1):
			if classer.board[row][9] == "X":
				num_top_x += 2
			elif classer.board[row][9] == "O":
				num_top_o += 2
		x = count_streaks(classer, "X")
		o = count_streaks(classer, "O")	
		return (num_top_x - num_top_o) + (x - o)

def new_evaluate(theclass):
	classer = theclass
	num_top_x = 0
	num_top_o = 0
	if classer.xwin == 1:
		return float("Inf")
	elif classer.owin == -1:
		return -float("Inf")
	else:
		for row in range(5, -1, -1):
			if classer.board[row][7] == "X":
				num_top_x += 0.5
			elif classer.board[row][7] == "O":
				num_top_o += 0.5
			if classer.board[row][5] == "X":
				num_top_x += 0.1
			elif classer.board[row][5] == "O":
				num_top_o += 0.1
			if classer.board[row][9] == "X":
				num_top_x += 0.1
			elif classer.board[row][9] == "O":
				num_top_o += 0.1
		#Gives points for going near the bottom and middle
		for row in range(5, 2, -1):
			#points for middle
			if classer.board[row][7] == "X":
				num_top_x += 0.3
			elif classer.board[row][7] == "O":
				num_top_o += 0.3
			#points for fifth
			if classer.board[row][5] == "X":
				num_top_x += 0.2
			elif classer.board[row][5] == "O":
				num_top_o += 0.2
			#points for ninth
			if classer.board[row][9] == "X":
				num_top_x += 0.2
			elif classer.board[row][9] == "O":
				num_top_o += 0.2
		x = count_streaks(classer, "X")
		o = count_streaks(classer, "O")	
		return (num_top_x - num_top_o) + (x - o)

def newest_evaluate(theclass):
	classer = theclass
	num_top_x = 0
	num_top_o = 0
	for row in range(5, -1, -1):
		if classer.board[row][7] == "X":
			num_top_x += 0.2
		elif classer.board[row][7] == "O":
			num_top_o += 0.2
		if classer.board[row][5] == "X":
			num_top_x += 0.05
		elif classer.board[row][5] == "O":
			num_top_o += 0.05
		if classer.board[row][9] == "X":
			num_top_x += 0.05
		elif classer.board[row][9] == "O":
			num_top_o += 0.05
	#Gives points for going near the bottom and middle
	for row in range(5, 2, -1):
		#points for middle
		if classer.board[row][7] == "X":
			num_top_x += 0.2
		elif classer.board[row][7] == "O":
			num_top_o += 0.05
		#points for fifth
		if classer.board[row][5] == "X":
			num_top_x += 0.05
		elif classer.board[row][5] == "O":
			num_top_o += 0.05
		#points for ninth
		if classer.board[row][9] == "X":
			num_top_x += 0.05
		elif classer.board[row][9] == "O":
			num_top_o += 0.05
	for row in range(5, 2, -1):
		for column in range(5, 10, 2):
			if classer.board[row][column] == classer.board[row][column+2]:
				if classer.board[row][column] == "X" and classer.board[row][column+4] == " ":
					num_top_x += 2
				elif classer.board[row][column] == "O" and classer.board[row][column+4] == " ":
					num_top_o += 2
			if classer.board[row][column] == classer.board[row][column-2]:
				if classer.board[row][column] == "X" and classer.board[row][column-4] == " ":
					num_top_x += 2
				elif classer.board[row][column] == "O" and classer.board[row][column-4] == " ":
					num_top_o += 2
			if classer.board[row][column] == classer.board[row-1][column-2]:
				if classer.board[row][column] == "X" and classer.board[row-2][column-4] == " ":
					num_top_x += 0.5
				elif classer.board[row][column] == "O" and classer.board[row-2][column-4] == " ":
					num_top_o += 0.5
			if classer.board[row][column] == classer.board[row-1][column+2]:
				if classer.board[row][column] == "X" and classer.board[row-2][column+4] == " ":
					num_top_x += 0.5
				elif classer.board[row][column] == "O" and classer.board[row-2][column+4] == " ":
					num_top_o += 0.5
	x = count_streaks(classer, "X")
	o = count_streaks(classer, "O")	
	return (num_top_x - num_top_o) + (x - o)


def count_streaks(theclass, symbol):
	classer = theclass
	count = 0
	for row in range(5, -1, -1):
		for column in range(1, 14, 2):
			if classer.board[row][column] != symbol:
				continue
			#horizontal right
			if column <= 7:
				num_in_streak = 0
				for i in range(0, 7, 2):
					if classer.board[row][column + i] == symbol:
						num_in_streak += 1
					elif classer.board[row][column + i] != " ":
						num_in_streak = 0
						break
				count += num_in_streak
			#horizontal left
			if column >=7:
				num_in_streak = 0
				for i in range(0, 7, 2):
					if classer.board[row][column - i] == symbol:
						num_in_streak += 1
					elif classer.board[row][column -i] != " ":
						num_in_streak = 0
						break
				count += num_in_streak
			#up-right
			if row >= 3 and column <=7:
				num_in_streak = 0
				for i in range(4):
					if classer.board[row-i][column+i+i] == symbol:
						num_in_streak += 1
					elif classer.board[row-i][column+i+i] != " ":
						num_in_streak = 0
						break
				count += num_in_streak
			#down-right
			if row <=2 and column <=7:
				num_in_streak = 0
				for i in range(4):
					if classer.board[row+i][column+i+i] == symbol:
						num_in_streak += 1
					elif classer.board[row+i][column+i+i] != " ":
						num_in_streak = 0
						break
				count += num_in_streak
			#down-left
			if row <=2 and column >=7:
				num_in_streak = 0
				for i in range(4):
					if classer.board[row+i][column-i-i] == symbol:
						num_in_streak += 1
					elif classer.board[row+i][column-i-i] != " ":
						num_in_streak = 0
						break
				count += num_in_streak
			#up-left
			if row >=3 and column >= 7:
				num_in_streak = 0
				for i in range(4):
					if classer.board[row-i][column-i-i] == symbol:
						num_in_streak += 1
					elif classer.board[row-i][column-i-i] != " ":
						num_in_streak = 0
						break
				count += num_in_streak
			#up
			if row<=3:
				num_in_streak = 0
				for i in range(4):
					if classer.board[row-i][column] == symbol:
						num_in_streak += 1
					elif classer.board[row-i][column] != " ":
						num_in_streak = 0
						break
				count += num_in_streak
	return count		

def minimax(theclass, is_maximizing, depth, alpha, beta, evaluate_board):
	blockprint()
	classer = theclass
	classer.checker()
	if classer.gameover == True or depth == 0:
		if classer.gameover == True:
			if classer.xwin == 1:
				return [(10000000 - classer.turn), ""]
			elif classer.owin == -1:
				return [(-10000000 + classer.turn), ""]
			elif classer.draw == True:
				return [0, ""]
		elif depth == 0:
			return [evaluate_board(classer), ""]
	if is_maximizing == True:
		best_value = -float("Inf")
		moves = classer.available_moves()
		centredmoves = []
		if 7 in moves:
			centredmoves.append(7)
		if 5 in moves:
			centredmoves.append(5)
		if 11 in moves:
			centredmoves.append(11)
		if 3 in moves:
			centredmoves.append(3)
		if 9 in moves:
			centredmoves.append(9)
		if 1 in moves:
			centredmoves.append(1)
		if 13 in moves:
			centredmoves.append(13)
		best_move = centredmoves[0]
		for move in centredmoves:
			copied = copy.deepcopy(classer)
			copied.aiinputter(move)
			hypothetical_value = minimax(copied, False, depth - 1, alpha, beta, evaluate_board)[0]
			if hypothetical_value > best_value:
				best_value = hypothetical_value
				best_move = move
			alpha = max(alpha, best_value)
			if alpha >= beta:
				break
		enableprint()
		return [best_value, best_move]
	elif is_maximizing == False:
		best_value = float("Inf")
		moves = classer.available_moves()
		centredmoves = []
		if 7 in moves:
			centredmoves.append(7)
		if 5 in moves:
			centredmoves.append(5)
		if 11 in moves:
			centredmoves.append(11)
		if 3 in moves:
			centredmoves.append(3)
		if 9 in moves:
			centredmoves.append(9)
		if 1 in moves:
			centredmoves.append(1)
		if 13 in moves:
			centredmoves.append(13)
		best_move = centredmoves[0]
		for move in centredmoves:
			copied = copy.deepcopy(classer)
			copied.aiinputter(move)
			hypothetical_value = minimax(copied, True, depth -1, alpha, beta, evaluate_board)[0]
			if hypothetical_value < best_value:
				best_value = hypothetical_value
				best_move = move
			beta = min(beta, best_move)
			if alpha >= beta:
				break
		enableprint()
		return [best_value, best_move] 
 
twoai = input("Want to watch a game played by two AIs? Y or N?: ")

while twoai.lower() != "y" and twoai.lower() != "n":
	twoai = input("Please enter either Y for yes or N for no: ")

if twoai.lower() == "y":
	while play.evanorodd < 43:
		play.printer()
		if play.evanorodd % 2 == 0:
			aimove = minimax(play, True, 5, -float("Inf"), float("Inf"), newest_evaluate)[1]
			play.aiinputter(aimove)
			print("\nNew AI with depth 6 dropped a piece in column {column}.".format(column=int(aimove/2+0.5)))
			play.checker()
			if play.gameover == True and play.draw != True:
				play.printer()
				break
			elif play.draw == True:
				print("\nThe game is drawn!")
				play.printer()
				break	
		elif play.evanorodd % 2 != 0:
			aimove = minimax(play, False, 5, -float("Inf"), float("Inf"), new_evaluate)[1]
			play.aiinputter(aimove)
			print("\nOld AI with depth 6 dropped a piece in column {column}.".format(column=int(aimove/2+0.5)))
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
					aimove = minimax(play, False, 5, -float("Inf"), float("Inf"), newest_evaluate)[1]
					play.aiinputter(aimove)
					print("\nThe ai dropped a piece in column {column}.".format(column=int(aimove/2+0.5)))
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
					aimove = minimax(play, True, 5, -float("Inf"), float("Inf"), newest_evaluate)[1]
					play.aiinputter(aimove)
					print("\nThe ai dropped a piece in column {column}.".format(column=int(aimove/2+0.5)))
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
				


















