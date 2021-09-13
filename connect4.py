class ConnectFour():

	turn = 0
	evanorodd = 0
	gameover = False

	def __init__(self):
		self.board = [[" " for column in range(15)] for row in range(6)]
		for row_index, row in enumerate(self.board):
			for col_index, item in enumerate(row):
				if col_index % 2 == 0:
					self.board[row_index][col_index] = "|"


	def printer(self):
		if ConnectFour.gameover == True:
			print("\nThe final board state:")
		else:
			print("\nTurn {turn}.".format(turn=ConnectFour.turn))
		print("\n  1   2   3   4   5   6   7")
		for row in self.board:
			for item in row:
				print(item, end = " ")
			print()

	def inputter(self, col_index):
		ConnectFour.turn += 1
		ConnectFour.evanorodd += 1
		num = col_index * 2 - 1
		if num >=1 and num <= 13 and num % 2 != 0:
			if self.board[0][num] == " ":
				for i in range(5, -1, -1):
					if self.board[i][num] == " ":
						if ConnectFour.evanorodd % 2 != 0:
							self.board[i][num] = "X"
							break
						else:
							self.board[i][num] = "O"
							break
			else:
				ConnectFour.evanorodd -= 1
				print("\nI'm afraid that column is full. Choose another one.")
		else:
			ConnectFour.evanorodd -= 1
			print("\nYou need to give a column number from one to seven.")

	def checker(self):
		# checks vertical
		for row in range(5, 2, -1):
			for column in range(1, 14, 2):
				if self.board[row][column] == self.board[row-1][column] and self.board[row][column] == self.board[row-2][column] and self.board[row][column] == self.board[row-3][column]:
					if self.board[row][column] == "X":
						print("\nThe game is over! Crosses win with a vertical connect four!")
						ConnectFour.gameover = True
					elif self.board[row][column] == "O":
						print("\nThe game is over! Naughts win with a vertical connect four!")
						ConnectFour.gameover = True
		# checks horizontal
		for row in range(5, -1, -1):
			for column in range(1, 8, 2):
				if self.board[row][column] == self.board[row][column+2] and self.board[row][column] == self.board[row][column+4] and self.board[row][column] == self.board[row][column+6]:
					if self.board[row][column] == "X":
						print("\nThe game is over! Crosses win with a horizontal connect four!")
						ConnectFour.gameover = True
					elif self.board[row][column] == "O":
						print("\nThe game is over! Naughts win with a horizontal connect four!")
						ConnectFour.gameover = True
		# checks diagonal going from left to right
		for row in range(5, 2, -1):
			for column in range(1, 8, 2):
				if self.board[row][column] == self.board[row-1][column+2] and self.board[row][column] == self.board[row-2][column+4] and self.board[row][column] == self.board[row-3][column+6]:
					if self.board[row][column] == "X":
						print("\nThe game is over! Crosses win along a positive diagonal!")
						ConnectFour.gameover = True
					elif self.board[row][column] == "O":
						print("\nThe game is over! Naughts win along a positive diagonal!")
						ConnectFour.gameover = True
		# checks diagonal going from right to left
		for row in range(5, 2, -1):
			for column in range(13, 6, -2):
				if self.board[row][column] == self.board[row-1][column-2] and self.board[row][column] == self.board[row-2][column-4] and self.board[row][column] == self.board[row-3][column-6]:
					if self.board[row][column] == "X":
						print("\nThe game is over! Crosses win along a negative diagonal!")
						ConnectFour.gameover = True
					elif self.board[row][column] == "O":
						print("The game is over! Naughts win along a negative diagonal!")
						ConnectFour.gameover = True

play = ConnectFour()

while ConnectFour.evanorodd < 43:
	play.printer()
	try:
		columnnumber = int(input("Enter a column number from one to seven: "))
	except ValueError:
		columnnumber = int(input("\nPlease give an integer!: "))
	play.inputter(columnnumber)
	play.checker()
	if ConnectFour.gameover == True:
		play.printer()
		break
	if ConnectFour.evanorodd == 42:
		ConnectFour.gameover = True
		print("\nThe game is drawn!")
		play.printer()
		break
