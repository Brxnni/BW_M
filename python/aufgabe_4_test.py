"""
Soll testen, ob die angegebene Strategie auch wirklich für alle Felder m*n für m,n >= 3 funktioniert.
"""

import os
import copy
import time
import numpy as np
from typing import Self

RED = "\033[91m"
BLUE = "\033[94m"
END = "\033[0m"

# fuck you im doing oop now
class Move:
	def __init__(self, *args):
		if len(args) == 2:
			start, end = args
			# automatic sorting, just in case
			start, end = min([start, end]), max([start, end])
			self.idxs = range(start, end+1)
			self.mode = "range"
		elif len(args) == 1:
			self.idxs = list(sorted(args[0]))
			self.mode = "individual"
	def abs(self):
		return len(self.idxs)
	def __repr__(self) -> str:
		if self.mode == "range":
			return f"<Move {self.idxs[0]}:{self.idxs[-1]}>"
		else:
			return f"<Move {' '.join([ str(i) for i in self.idxs])}>"

class Field:
	def __init__(self, m, n):
		# m = height, n = width in 2D representation
		# if m < 3 or n < 3: raise ValueError("m,n !>= 3")
		if m < 5 or n < 5: raise ValueError("m,n !>= 5 (buggy for 3 and 4 lmaoo)")

		self.m, self.n = m, n

		self.fields = [0 for _ in range(2*n+2*m-4)]
		self.corners = [0, n-1, n+m-2, n+m+n-3] # nice

		# pre-generate list of all possible moves
		self.moves = []
		# top left <-> top right
		for i in range(self.corners[0], self.corners[1]+1):
			for j in range(i+1, self.corners[1]+1):
				self.moves.append(Move(i, j))
		# bottom left <-> bottom right
		for i in range(self.corners[2], self.corners[3]+1):
			for j in range(i+1, self.corners[3]+1):
				self.moves.append(Move(i, j))
		# top left <-> bottom left
		for i in range(self.corners[3], len(self.fields)+1):
			for j in range(i+1, len(self.fields)+1):
				lst = list(range(i, j+1))
				lst = [ idx if idx < len(self.fields) else 0 for idx in lst ]
				self.moves.append(Move(lst))
		# top right <-> bottom right
		for i in range(self.corners[1], self.corners[2]+1):
			for j in range(i+1, self.corners[2]+1):
				self.moves.append(Move(i, j))
		for i in range(len(self.fields)):
			self.moves.append(Move(i, i))

	def isempty(self) -> bool:
		return all([ not f for f in self.fields ])

	def isfull(self) -> bool:
		return all(self.fields)

	def copy(self) -> Self:
		return copy.deepcopy(self)

	def render(self) -> None:
		def rd(field): return {0:"[]", 1:f"{RED}[]{END}", 2:f"{BLUE}[]{END}"}[field]

		os.system("cls")
		# first row
		print("".join([ rd(self.fields[i]) for i in range(self.corners[0], self.corners[1]+1) ]))
		# middle rows
		for r in range(self.m - 2):
			print(rd(self.fields[-1-r]) + " "*(self.n-2)*2 + rd(self.fields[self.n+r]))
		# last row
		print("".join([ rd(self.fields[i]) for i in range(self.corners[3], self.corners[2]-1, -1) ]))
		time.sleep(1)

	def get_valid_moves(self) -> list[Move]:
		fields = [ bool(f) for f in self.fields ]

		if self.isempty():
			return self.moves
		if self.isfull():
			return []

		def is_range(nums: list[int]) -> bool:
			return nums == list(range(min(nums), max(nums)+1))

		def idxs_adjacent(idxs: list[int]) -> bool:
			mn, mx = min(idxs), max(idxs)

			# no wrapping
			if mx - mn + 1 == len(idxs):
				return is_range(idxs)

			# wrapping
			if 0 in idxs and len(self.fields) - 1 in idxs:
				diffs = list(np.diff(idxs))
				jump = next(idx for idx, d in enumerate(diffs) if d != 1)

				first_part = idxs[:jump+1]
				second_part = idxs[jump+1:]

				return is_range(first_part) and is_range(second_part)

			return False

		valid = []
		for move in self.moves:
			move_possible = True

			# overlapping fields
			for idx in move.idxs:
				if fields[idx]:
					move_possible = False
					break

			if not move_possible: continue

			marked_idxs = [ i for i in range(len(fields)) if fields[i] or i in move.idxs ]
			print(move, marked_idxs, idxs_adjacent(marked_idxs))
			if not idxs_adjacent(marked_idxs):
				continue

			valid.append(move)

		return valid

	def makeMove(self, move: Move, playerNum: int) -> None:
		for idx in move.idxs:
			self.fields[idx] = playerNum

def optimalRenateMove(f: Field) -> Move:
	m, n = f.m, f.n
	l = len(f.fields)
	fields = [ bool(fd) for fd in f.fields ]

	# Starting move
	if f.isempty():
		# Corner
		if n == m: return Move(0,0)
		# Line
		else: return Move(0, f.n-1)
	else:
		if n == m:
			# Keep symmetry alive
			if (not fields[f.corners[1]]) or (not fields[f.corners[3]]):
				try: count_top = fields[f.corners[0]:f.corners[1]+1].index(False)
				except: count_top = n
				count_left = m - (fields[f.corners[3]:l] + [True]).index(True)
				diff = abs(count_top - count_left)

				if count_left > count_top: return Move(count_top, count_top+diff-1)
				else: return Move(l-count_left-diff+1, l-count_left)
			else:
				count_right = fields[f.corners[1]:f.corners[2]+1].index(False)
				count_bottom = n - (fields[f.corners[2]:f.corners[3]+1] + [True]).index(True)
				diff = abs(count_right - count_bottom)

				if n - count_right == 2 and n - count_bottom == 2:
					raise SystemError("HELP")
				elif n - count_bottom == 0:
					return Move(f.corners[1]+count_right, f.corners[2]-1)
				elif n - count_bottom == 1:
					return Move(f.corners[1]+count_right, f.corners[2])

				if count_bottom > count_right: return Move(f.corners[1]+count_right-1, f.corners[1]+count_right+diff-1, )
				else: return Move(f.corners[3]-count_bottom-diff+1, f.corners[3]-count_bottom)
		if n != m:
			count_left = m - (fields[f.corners[3]:l] + [True]).index(True)
			try: count_right = fields[f.corners[1]:f.corners[2]+1].index(False)
			except: count_right = m

			# One entire side to do
			if all([f.corners[1] <= idx <= f.corners[2] for idx in [ idx for idx, v in enumerate(fields) if not v ]]):
				print("one entire side left")
				from_top = fields[f.corners[1]:f.corners[2]+1].index(False)
				from_bottom = list(reversed(fields[f.corners[1]:f.corners[2]+1])).index(False)
				return Move(f.corners[1]+from_top, f.corners[2]-from_bottom)
			# Behaviour for 2x2 corner
			if m - count_right == 1:
				print(1); time.sleep(1)
				p = m - count_left
				return Move(f.corners[2], f.corners[3]-p)
			elif m - count_right == 0:
				print(2); time.sleep(1)
				p = m - count_left
				return Move(f.corners[2]+1, f.corners[3]-p)
			elif m - count_left == 1:
				print(3); time.sleep(1)
				p = m - count_right
				return Move(f.corners[2]+p, f.corners[3])
			elif m - count_left == 0:
				print(4); time.sleep(1)
				p = m - count_right
				return Move(f.corners[2]+p, f.corners[3]-1)
			# Keep symmetry
			else:
				print("calc diff")
				diff = abs(count_left - count_right)

				if count_left > count_right: return Move(f.corners[1]+count_right, f.corners[1]+count_right+diff-1)
				else: return Move(l-count_left-diff+1, l-count_left)

F = Field(5, 12)
F.makeMove(optimalRenateMove(F), 1)
F.render()

def tryAllMoves(f: Field):
	moves = f.get_valid_moves()
	if not moves:
		print("renate won!")
		time.sleep(0.5)
		return
	for move in moves:
		g = f.copy()
		g.makeMove(move, 2)
		g.render()
		g.makeMove(optimalRenateMove(g), 1)
		g.render()
		tryAllMoves(g)

tryAllMoves(F)

# def tryall(field, turn):
# 	# field.render()
# 	moves = field.get_valid_moves()
# 	moves = sorted(moves, key=Move.abs, reverse=True)

# 	if moves:
# 		for move in moves:
# 			g = field.copy()
# 			g.makeMove(move, turn)
# 			tryall(g, {1:2,2:1}[turn])
# 	else:
# 		print("player", turn, "lost")

# N != M
# F = Field(5, 12)
# F.makeMove(optimalRenateMove(F), 1)
# F.render()

# F.makeMove(Move(12,13), 2)
# F.render()
# F.makeMove(optimalRenateMove(F), 1)
# F.render()

# F.makeMove(Move(26,27), 2)
# F.render()
# F.makeMove(optimalRenateMove(F), 1)
# F.render()

# F.makeMove(Move(14,15), 2)
# F.render()
# F.makeMove(optimalRenateMove(F), 1)
# F.render()

# N == M
# G = Field(6, 6)
# G.makeMove(optimalRenateMove(G), 1)
# G.render()

# G.makeMove(Move(18,19), 2)
# G.render()
# G.makeMove(optimalRenateMove(G), 1)
# G.render()

# G.makeMove(Move(3,5), 2)
# G.render()
# G.makeMove(optimalRenateMove(G), 1)
# G.render()

# G.makeMove(Move(12,14), 2)
# G.render()
# G.makeMove(optimalRenateMove(G), 1)
# G.render()

# G.makeMove(Move(11,11), 2)
# G.render()
# G.makeMove(optimalRenateMove(G), 1)
# G.render()
