import sys
import random
import signal
import time
import copy
import traceback

class Team63():
	def __init__(self):
		self.bestVal = -1000
		#best move's location 
		self.bestcell = (-1, -1, -1);

	def move(self, board, old_move, flag):
		self.bestVal = -1000
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed 
		cells = board.find_valid_move_cells(old_move)
		#return cells[random.randrange(len(cells))]#instead of this, we have to use the algo to find optimal cell
		for cell in cells:
			#compute evaluation function for this move 
			print(cell);
			board.big_boards_status[cell[0]][cell[1]][cell[2]] = flag;
			moveVal = self.minimax(board, 0, 0, cell)
			board.big_boards_status[cell[0]] [cell[1]] [cell[2]] = '-';
			if (moveVal > self.bestVal):
				self.bestcell = cell
				self.bestVal = moveVal

		# print self.bestcell
		return self.bestcell;

	def minimax(self, board, depth, isMax, cell):

		score = 1
		if depth == 3:
			return score
		#if max or min player has won
		if (score == 10 or score == -10): 
			return score

		#if it's a draw and no mopre moves possible
		if (self.isMovesLeft(board,cell)==0):
			return 0
		#else 
		if(isMax == 1):
			best = -1000;
			cells = board.find_valid_move_cells(cell)
			for i in cells:
				board.big_boards_status[i[0]] [i[1]] [i[2]] = 'x';
				best = max(best, self.minimax(board, depth+1, not(isMax), i) );
				board.big_boards_status[i[0]] [i[1]] [i[2]] = '-';
			return best;

		else:
			best = 1000;
			cells = board.find_valid_move_cells(cell)
			for i in cells:
				board.big_boards_status[i[0]] [i[1]] [i[2]] = 'o';
				best = min(best, self.minimax(board, depth+1, not(isMax), i) );
				# print('Praffulloo')
				board.big_boards_status[i[0]] [i[1]] [i[2]] = '-';
			return best;

	def heuristic(self, board):
		winner = board.find_terminal_state();
		if(winner[0] == 'x'):
			return 10;
		elif(winner[0] == 'o'):
			return -10;
		else:
			return 0;

	def isMovesLeft(self, board, cell):
		cells = board.find_valid_move_cells(cell)
		if not cells:
			return 0;
		else:
			return 1;










		