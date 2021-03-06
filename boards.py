class Bit_board:
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
					self.xwin = 1
					self.gameover = True
					return
				else:
					self.owin = -1
					self.gameover = True
					return 
			# Negative diagonal
			m = maps & (maps >> 6)
			if m & (m >> 12):
				if maps == one_player:
					self.xwin = 1
					self.gameover = True
					return
				else:
					self.owin = -1
					self.gameover = True
					return
			# Positive diagonal
			m = maps & (maps >> 8)
			if m & (m >> 16):
				if maps == one_player:
					self.xwin = 1
					self.gameover = True
					return
				else:
					self.owin = -1
					self.gameover = True
					return
    			# Vertical
			m = maps & (maps >> 1)
			if m & (m >> 2):
				if maps == one_player:
					self.xwin = 1
					self.gameover = True
					return
				else:
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

class Standard_board():
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