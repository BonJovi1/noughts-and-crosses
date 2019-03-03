import sys
import random
import signal
import time
import copy
import traceback

class Team63():
	def __init__(self):
		self.bestVal = -10000
		#best move's location 
		self.bestcell = (-1, -1, -1)
		
		#Weight Variables
		self.cellWeight1 = 3
		self.cellWeight2 = 9
		self.smallboardwon = 27
		self.SBWeight1 = 81
		self.SBWeight2 = 243
		self.SBWon = 729 #won the game
		
		#Cell count variables
		self.cellcount1x = 0
		self.cellcount2x = 0 
		self.cellcount3x = 0 
		self.cellcount1o = 0
		self.cellcount2o = 0 
		self.cellcount3o = 0 

		#SB count variables
		self.SBcount1x = 0
		self.SBcount2x = 0 
		self.SBcount3x = 0 
		self.SBcount1o = 0
		self.SBcount2o = 0 
		self.SBcount3o = 0
		
		self.sbs_score = 0 
		self.game_score = 0

	def move(self, board, old_move, flag):
		self.bestVal = -10000
		self.bestcell = (-1, -1, -1)
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed 
		cells = board.find_valid_move_cells(old_move)
		#return cells[random.randrange(len(cells))]#instead of this, we have to use the algo to find optimal cell
		for cell in cells:
			#compute evaluation function for this move 
			# print(cell);
			board.big_boards_status[cell[0]][cell[1]][cell[2]] = flag;
			moveVal = self.minimax(board, 0, 0, cell, -10000, 10000)
			board.big_boards_status[cell[0]] [cell[1]] [cell[2]] = '-';
			if (moveVal > self.bestVal):
				self.bestcell = cell
				self.bestVal = moveVal

		# print self.bestcell
		return self.bestcell;

	def minimax(self, board, depth, isMax, cell, alpha, beta):

		score,status = self.heuristic(board);
		if depth == 3:
			return score
		#if max or min player has won
		if (status == 1): 
			return score

		#if it's a draw and no more moves possible
		if (self.isMovesLeft(board,cell)==0):
			return 0
		#else 
		if(isMax == 1):
			best = -10000;
			cells = board.find_valid_move_cells(cell)
			for i in cells:
				board.big_boards_status[i[0]] [i[1]] [i[2]] = 'x';
				best = max(best, self.minimax(board, depth+1, not(isMax), i, alpha, beta) );
				board.big_boards_status[i[0]] [i[1]] [i[2]] = '-';
				alpha = max( alpha, best)
				if (beta <= alpha):
					break
			return best;

		else:
			best = 10000;
			cells = board.find_valid_move_cells(cell)
			for i in cells:
				board.big_boards_status[i[0]] [i[1]] [i[2]] = 'o';
				best = min(best, self.minimax(board, depth+1, not(isMax), i, alpha, beta) );
				board.big_boards_status[i[0]] [i[1]] [i[2]] = '-';
				beta = min( beta, best)
				if (beta <= alpha):
					break
			return best;

	#calculating cellcount variables
	def calculate_sbScore(self, number_of_x, number_of_o):
		if(number_of_x == 1 and number_of_o == 0):
			self.cellcount1x ++;
		elif(number_of_x == 2 and number_of_o == 0):
			self.cellcount2x ++;
		elif(number_of_o == 1 and number_of_x == 0):
			self.cellcount1o ++;
		elif(number_of_o == 2 and number_of_x == 0):
			self.cellcount2o ++;
		elif(number_of_o == 3 and number_of_x == 0):
			self.cellcount3o ++;
		elif(number_of_x == 3 and number_of_o == 0):
			self.cellcount3x ++;

	#calculating cellcount variables
	def calculate_gameStatus(self, number_of_x, number_of_o):
		if(number_of_x == 1):
			self.SBcount1x ++;
		elif(number_of_x == 2):
			self.SBcount2x ++;
		elif(number_of_o == 1):
			self.SBcount1o ++;
		elif(number_of_o == 2):
			self.SBcount2o ++;
		elif(number_of_o == 3):
			self.SBcount3o ++;
		elif(number_of_x == 3):
			self.SBcount3x ++;

	def reinitialize(self):
		#re-initialize these values for next iteration of smallboards. 
		self.cellcount1x = 0
		self.cellcount2x = 0 
		self.cellcount3x = 0 
		self.cellcount1o = 0
		self.cellcount2o = 0 
		self.cellcount3o = 0

	def reinitialize_gameStatus(self):
		#re-initialize these values for next iteration of smallboards. 
		self.SBcount1x = 0
		self.SBcount2x = 0 
		self.SBcount3x = 0 
		self.SBcount1o = 0
		self.SBcount2o = 0 
		self.SBcount3o = 0

	#check if smallboard has been won
	def check_win(self):
		
		if(self.cellcount3x > 0):
			self.reinitialize();
			self.sbs_score += self.smallboardwon;
			return 1
		if(self.cellcount3o > 0):
			self.reinitialize();
			self.sbs_score -= self.smallboardwon;
			return 1
		
		return 0

	def check_win_gameStatus(self):
		
		if(self.SBcount3x > 0):
			self.reinitialize_gameStatus();
			self.game_score += self.SBWon;#change something
			return 1
		if(self.SBcount3o > 0):
			self.reinitialize_gameStatus();
			self.game_score -= self.SBWon;#change something
			return 1
		
		return 0


	def heuristic(self, board):
		# original heuristic
		# winner = board.find_terminal_state();
		# if(winner[0] == 'x'):
		# 	return 10;
		# elif(winner[0] == 'o'):
		# 	return -10;
		# else:
		# 	return 0;
		self.sbs_score = 0;
		self.game_score = 0;
		heuristic_score = 0;
		game_won = 0;
		#calculating smallboard score. We have the board object with us. Let's visit each smallboard and calculate its score
		#There are 3 rows of small boards 
		
		#First row of small boards i.e cell rows(0-2)
		index1 = 0;
		for k in range(2): #Big boards 1 and 2
			
			index2 = 0; #Column number of small boards, gets incremented at the end of this loop. 
			for l in range(3): # Going through 3 small boards in one big board
				
				#Rows of the smallboard
				for i in range(index1, index1+2):
					number_of_x = 0;
					number_of_o = 0;
					for j in range(index2, index2+2):
						if ( board.big_boards_status[k][i][j] == 'x'):
							number_of_x++;
						if ( board.big_boards_status[k][i][j] == 'o'):
							number_of_o++;
					self.calculate_sbScore(number_of_x, number_of_o)
				
				#checking if smallboard is won
				ans = check_win();
				if(ans == 1):
					continue;
				
					
				#Columns of the smallboard
				for i in range(index1, index1+2):
					number_of_x = 0;
					number_of_o = 0;
					for j in range(index2, index2+2):
						if ( board.big_boards_status[k][j][i] == 'x'):
							number_of_x++;
						if ( board.big_boards_status[k][j][i] == 'o'):
							number_of_o++;
					self.calculate_sbScore(number_of_x, number_of_o)

				#checking if smallboard is won
				ans = check_win();
				if(ans == 1):
					continue;
				
				#Major diagonal of the smallboard
				number_of_x = 0;
				number_of_o = 0;
				for i in range(index1, index1+2):
					if ( board.big_boards_status[k][i][i] == 'x'):
						number_of_x++;
					if ( board.big_boards_status[k][i][i] == 'o'):
						number_of_o++;
				self.calculate_sbScore(number_of_x, number_of_o)
				#checking if smallboard is won
				ans = check_win();
				if(ans == 1):
					continue;

				#for sb1, diagonal 2
				number_of_x = 0;
				number_of_o = 0;
				for i in range(index1, index1+2):
					if ( board.big_boards_status[k][i][2-i] == 'x'):
						number_of_x++;
					if ( board.big_boards_status[k][i][2-i] == 'o'):
						number_of_o++;
				self.calculate_sbScore(number_of_x, number_of_o)
				#checking if smallboard is won
				ans = check_win();
				if(ans == 1):
					continue;

				#applying our formula for calculating score for this smallboard
				total_myscore = (self.cellWeight1 * self.cellcount1x * self.cellcount1x) + (self.cellWeight2 * self.cellcount2x * self.cellcount2x)
				total_oppscore = (self.cellWeight1 * self.cellcount1o * self.cellcount1o) + (self.cellWeight2 * self.cellcount2o * self.cellcount2o)
				total = total_myscore - total_oppscore;
				self.sbs_score += total;

				#re-initialize these values for next iteration of smallboards.
				self.reinitialize();
				#Move on to next smallboard in that row of smallboards i.e cell columns += 3
				index2 += 3;

		#Second row of smallboards i.e cell rows(3-5)	
		index1 = 3;
		for k in range(2): #Big boards 1 and 2
			
			index2 = 0; #Column number of small boards, gets incremented at the end of this loop. 
			for l in range(3): # Going through 3 small boards in one big board
				
				#Rows of the smallboard
				for i in range(index1, index1+2):
					number_of_x = 0;
					number_of_o = 0;
					for j in range(index2, index2+2):
						if ( board.big_boards_status[k][i][j] == 'x'):
							number_of_x++;
						if ( board.big_boards_status[k][i][j] == 'o'):
							number_of_o++;
					self.calculate_sbScore(number_of_x, number_of_o)
				#checking if smallboard is won
				ans = check_win();
				if(ans == 1):
					continue;
					

				#Columns of the smallboard
				for i in range(index1, index1+2):
					number_of_x = 0;
					number_of_o = 0;
					for j in range(index2, index2+2):
						if ( board.big_boards_status[k][j][i] == 'x'):
							number_of_x++;
						if ( board.big_boards_status[k][j][i] == 'o'):
							number_of_o++;
					self.calculate_sbScore(number_of_x, number_of_o)
				#checking if smallboard is won
				ans = check_win();
				if(ans == 1):
					continue;
				
				#Major diagonal of the smallboard
				number_of_x = 0;
				number_of_o = 0;
				for i in range(index1, index1+2):
					if ( board.big_boards_status[k][i][i] == 'x'):
						number_of_x++;
					if ( board.big_boards_status[k][i][i] == 'o'):
						number_of_o++;
				self.calculate_sbScore(number_of_x, number_of_o)
				#checking if smallboard is won
				ans = check_win();
				if(ans == 1):
					continue;

				#for sb1, diagonal 2
				number_of_x = 0;
				number_of_o = 0;
				for i in range(index1, index1+2):
					if ( board.big_boards_status[k][i][2-i] == 'x'):
						number_of_x++;
					if ( board.big_boards_status[k][i][2-i] == 'o'):
						number_of_o++;
				self.calculate_sbScore(number_of_x, number_of_o)
				#checking if smallboard is won
				ans = check_win();
				if(ans == 1):
					continue;

				#applying our formula for calculating score for this smallboard
				total_myscore = (self.cellWeight1 * self.cellcount1x * self.cellcount1x) + (self.cellWeight2 * self.cellcount2x * self.cellcount2x)
				total_oppscore = (self.cellWeight1 * self.cellcount1o * self.cellcount1o) + (self.cellWeight2 * self.cellcount2o * self.cellcount2o)
				total = total_myscore - total_oppscore;
				self.sbs_score += total;

				#re-initialize these values for next iteration of smallboards. 
				self.reinitialize();
				#Move on to next smallboard in that row of smallboards i.e cell columns += 3
				index2 += 3;

		#Third row of smallboards i.e cell rows(6-8)
		index1 = 6;
		for k in range(2): #Big boards 1 and 2
			
			index2 = 0; #Column number of small boards, gets incremented at the end of this loop. 
			for l in range(3): # Going through 3 small boards in one big board
				
				#Rows of the smallboard
				for i in range(index1, index1+2):
					number_of_x = 0;
					number_of_o = 0;
					for j in range(index2, index2+2):
						if ( board.big_boards_status[k][i][j] == 'x'):
							number_of_x++;
						if ( board.big_boards_status[k][i][j] == 'o'):
							number_of_o++;
					self.calculate_sbScore(number_of_x, number_of_o)
				#checking if smallboard is won
				ans = check_win();
				if(ans == 1):
					continue;
					

				#Columns of the smallboard
				for i in range(index1, index1+2):
					number_of_x = 0;
					number_of_o = 0;
					for j in range(index2, index2+2):
						if ( board.big_boards_status[k][j][i] == 'x'):
							number_of_x++;
						if ( board.big_boards_status[k][j][i] == 'o'):
							number_of_o++;
					self.calculate_sbScore(number_of_x, number_of_o)
				#checking if smallboard is won
				ans = check_win();
				if(ans == 1):
					continue;
				
				#Major diagonal of the smallboard
				number_of_x = 0;
				number_of_o = 0;
				for i in range(index1, index1+2):
					if ( board.big_boards_status[k][i][i] == 'x'):
						number_of_x++;
					if ( board.big_boards_status[k][i][i] == 'o'):
						number_of_o++;
				self.calculate_sbScore(number_of_x, number_of_o)
				#checking if smallboard is won
				ans = check_win();
				if(ans == 1):
					continue;

				#for sb1, diagonal 2
				number_of_x = 0;
				number_of_o = 0;
				for i in range(index1, index1+2):
					if ( board.big_boards_status[k][i][2-i] == 'x'):
						number_of_x++;
					if ( board.big_boards_status[k][i][2-i] == 'o'):
						number_of_o++;
				self.calculate_sbScore(number_of_x, number_of_o)
				#checking if smallboard is won
				ans = check_win();
				if(ans == 1):
					continue;

				#applying our formula for calculating score for this smallboard
				total_myscore = (self.cellWeight1 * self.cellcount1x * self.cellcount1x) + (self.cellWeight2 * self.cellcount2x * self.cellcount2x)
				total_oppscore = (self.cellWeight1 * self.cellcount1o * self.cellcount1o) + (self.cellWeight2 * self.cellcount2o * self.cellcount2o)
				total = total_myscore - total_oppscore;
				self.sbs_score += total;

				#re-initialize these values for next iteration of smallboards. 
				self.reinitialize();
				#Move on to next smallboard in that row of smallboards i.e cell columns += 3
				index2 += 3;

		#Okay, now we have calculate score of each smallboard. Now let's calculate game status or game_score!
		#GameStatus ---------------------------------------
		ind1 = 0
		for k in range(2):#BigBoard 1 & 2
			ind2 = 0;
			
			for i in range(ind1, ind1+2):
				number_of_x = 0;
				number_of_o = 0;
				for j in range(ind2, ind2+2):
					if ( board.small_boards_status[k][i][j] == 'x'):
						number_of_x++;
					if ( board.small_boards_status[k][i][j] == 'o'):
						number_of_o++;
				self.calculate_gameStatus(number_of_x, number_of_o)
			ans = check_win_gameStatus();
			if(ans == 1):
				game_won = 1
				continue;

			for i in range(ind1, ind1+2):
				number_of_x = 0;
				number_of_o = 0;
				for j in range(ind2, ind2+2):
					if ( board.small_boards_status[k][j][i] == 'x'):
						number_of_x++;
					if ( board.small_boards_status[k][j][i] == 'o'):
						number_of_o++;
				self.calculate_gameStatus(number_of_x, number_of_o)
			ans = check_win_gameStatus();
			if(ans == 1):
				game_won = 1
				continue;

			number_of_x = 0;
			number_of_o = 0;
			for i in range(ind1, ind1+2):
				if ( board.small_boards_status[k][i][i] == 'x'):
					number_of_x++;
				if ( board.small_boards_status[k][i][i] == 'o'):
					number_of_o++;
			self.calculate_gameStatus(number_of_x, number_of_o)
			ans = check_win_gameStatus();
			if(ans == 1):
				game_won = 1
				continue;

			number_of_x = 0;
			number_of_o = 0;
			for i in range(ind1, ind1+2):
				if ( board.small_boards_status[k][i][2-i] == 'x'):
					number_of_x++;
				if ( board.small_boards_status[k][i][2-i] == 'o'):
					number_of_o++;
			self.calculate_gameStatus(number_of_x, number_of_o)
			ans = check_win_gameStatus();
			if(ans == 1):
				game_won = 1
				continue;

			total_myscore = (self.SBWeight1 * self.SBcount1x * self.SBcount1x) + (self.SBWeight2 * self.SBcount2x * self.SBcount2x)
			total_oppscore = (self.SBWeight1 * self.SBcount1o * self.SBcount1o) + (self.SBWeight2 * self.SBcount2o * self.SBcount2o)
			self.game_score += total_myscore - total_oppscore;
			self.reinitialize_gameStatus();

		#So now we calculate the heuristic score for that node in the tree.
		heuristic_score = self.sbs_score + self.game_score
		return(heuristic_score, game_won)

	def isMovesLeft(self, board, cell):
		cells = board.find_valid_move_cells(cell)
		if not cells:
			return 0;
		else:
			return 1;










		