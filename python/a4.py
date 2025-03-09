"""
Soll testen, ob die angegebene Strategie auch wirklich für alle Felder m*n für m,n >= 3 funktioniert.
"""

import os
import copy
import time
import numpy as np
from typing import Self

# "high intensity" ansi farben
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
END = "\033[0m"

def clear(full=False) -> None:
	if full:
		os.system("cls")
		return

	num_lines = os.get_terminal_size().lines
	# cleart terminal ohne kurzes schwarzes blinken
	print(f"\033[{num_lines+1}A\033[2K", end="")

# oop :3
class Move:
	def __init__(self, *args):
		if len(args) == 2:
			start, end = args
			start, end = min([start, end]), max([start, end])
			self.idxs = list(range(start, end+1))
			self.mode = "range"
		elif len(args) == 1:
			self.idxs = list(sorted(args[0]))
			self.mode = "individual"
		else:
			raise ValueError()

	def abs(self):
		return len(self.idxs)

	def __repr__(self) -> str:
		if self.mode == "range":
			return f"<Move {self.idxs[0]}:{self.idxs[-1]}>"
		else:
			return f"<Move {' '.join([ str(i) for i in self.idxs])}>"

	def __eq__(self, other: Self):
		return self.idxs == other.idxs

class Field:
	def __init__(self, m, n):
		# m = höhe, n = breite (in 2d-zeichnung)
		if m < 3 or n < 3: raise ValueError("m,n !>= 3")

		self.m, self.n = m, n
		self.l = 2*n+2*m-4

		self.fields = [0 for _ in range(2*n+2*m-4)]
		self.corners = [0, n-1, n+m-2, n+m+n-3] # nice

		# liste an allen möglichen zügen im voraus berechnen
		self.moves = []
		# einzelne felder
		for i in range(len(self.fields)):
			self.moves.append(Move(i, i))
		# oben links <-> oben rechts
		for i in range(self.corners[0], self.corners[1]+1):
			for j in range(i+1, self.corners[1]+1):
				self.moves.append(Move(i, j))
		# oben rechts <-> unten rechts
		for i in range(self.corners[1], self.corners[2]+1):
			for j in range(i+1, self.corners[2]+1):
				self.moves.append(Move(i, j))
		# unten links <-> unten rechts
		for i in range(self.corners[2], self.corners[3]+1):
			for j in range(i+1, self.corners[3]+1):
				self.moves.append(Move(i, j))
		# oben links <-> unten links
		for i in range(self.corners[3], len(self.fields)+1):
			for j in range(i+1, len(self.fields)+1):
				lst = list(range(i, j+1))
				lst = [ idx if idx < len(self.fields) else 0 for idx in lst ]
				self.moves.append(Move(lst))

	def is_empty(self) -> bool:
		return all([ not f for f in self.fields ])

	def is_full(self) -> bool:
		return all(self.fields)

	def copy(self) -> Self:
		return copy.deepcopy(self)

	def render(self, clear_term=True) -> None:
		def rd(field): return ["",RED+BOLD,BLUE+BOLD][field] + "[]" + END

		if clear_term: clear()
		# obere reihe
		print("".join([ rd(self.fields[i]) for i in range(self.corners[0], self.corners[1]+1) ]))
		# kanten links und rechts
		for r in range(self.m - 2):
			print(rd(self.fields[-1-r]) + " "*(self.n-2)*2 + rd(self.fields[self.n+r]))
		# untere reihe
		print("".join([ rd(self.fields[i]) for i in range(self.corners[3], self.corners[2]-1, -1) ]))

	def get_valid_moves(self) -> list[Move]:
		fields = [ bool(f) for f in self.fields ]

		if self.is_empty():
			return self.moves
		if self.is_full():
			return []

		def is_range(nums: list[int]) -> bool:
			return nums == list(range(min(nums), max(nums)+1))

		def idxs_adjacent(idxs: list[int]) -> bool:
			mn, mx = min(idxs), max(idxs)

			# normale range
			if mx - mn + 1 == len(idxs):
				return is_range(idxs)

			# mit sprung von idx 0 zu -1
			if 0 in idxs and len(self.fields) - 1 in idxs:
				diffs = list(np.diff(idxs))
				jump = next(idx for idx, d in enumerate(diffs) if d != 1)

				first_part = idxs[:jump+1]
				second_part = idxs[jump+1:]

				return is_range(first_part) and is_range(second_part)

			return False

		valid_moves = []
		for move in self.moves:

			move_possible = True
			# was schon markiert ist, darf nicht nochmal markiert werden
			for idx in move.idxs:
				if fields[idx]:
					move_possible = False
					break
			if not move_possible: continue

			# alle markierten felder müssen zusammenhängen
			marked_idxs = [ i for i in range(len(fields)) if fields[i] or i in move.idxs ]
			if not idxs_adjacent(marked_idxs):
				continue

			valid_moves.append(move)

		return valid_moves

	def make_move(self, move: Move, playerNum: int) -> None:
		if not move in self.get_valid_moves(): raise RuntimeError("Zug nicht erlaubt!", self.fields, move)
		for idx in move.idxs:
			self.fields[idx] = playerNum

# findet besten zug in p*p-Ecken
def pxp(f: Field, corner_idx: int) -> Move:
	m, n, l = f.m, f.n, f.l
	corners = f.corners
	fields = [ bool(fd) for fd in f.fields ]

	if corner_idx == 2:
		try: count_right = fields[corners[1]:corners[2]+1].index(False)
		except: count_right = m
		try: count_bottom = list(reversed(fields[corners[2]:corners[3]+1])).index(False)
		except: count_bottom = n

		empty_bottom = n - count_bottom
		empty_right = m - count_right

		if empty_bottom >= 2 and empty_right >= 2:
			req = abs(empty_bottom - empty_right)
			if empty_bottom > empty_right:	return Move(corners[3]-count_bottom-req+1, corners[3]-count_bottom)
			else:							return Move(corners[1]+count_right, corners[1]+count_right+req-1)
		elif empty_right == 0:
			return Move(corners[2]+1, corners[2]+empty_bottom-1)
		elif empty_right == 1:
			return Move(corners[2], corners[2]+empty_bottom-1)
		elif empty_bottom == 0:
			return Move(corners[2]-empty_right+1, corners[2]-1)
		elif empty_bottom == 1:
			return Move(corners[2]-empty_right+1, corners[2])

	elif corner_idx == 3:
		try: count_left = list(reversed(fields[corners[3]:] + [True])).index(False)
		except: count_left = m
		try: count_bottom = fields[corners[2]:corners[3]+1].index(False)
		except: count_bottom = n

		empty_bottom = n - count_bottom
		empty_left = m - count_left

		if empty_bottom >= 2 and empty_left >= 2:
			req = abs(empty_bottom - empty_left)
			if empty_bottom > empty_left:	return Move(corners[2]+count_bottom, corners[2]+count_bottom+req-1)
			else:							return Move(l-count_left-req+1, l-count_left)
		elif empty_left == 0:
			return Move(corners[2]+count_bottom, corners[3]-1)
		elif empty_left == 1:
			return Move(corners[2]+count_bottom, corners[3])
		elif empty_bottom == 0:
			return Move(corners[3]+1, l-count_left)
		elif empty_bottom == 1:
			return Move(corners[3], l-count_left)

	raise RuntimeError("Hilfe!!", fields)

# funktioniert nur für situationen, in denen es selbst von anfang an gespielt hat
def optimal_renate_move(f: Field) -> Move:
	m, n, l = f.m, f.n, f.l
	corners = f.corners
	fields = [ bool(fd) for fd in f.fields ]

	# erster zug
	if f.is_empty():
		# immer das feld mit index 0 bedecken, weil da die indexmathematik sonst zu aufwendig wäre xd
		if m == n:
			# ecke
			return Move(0,0)
		else:
			# ganze kante
			return Move(0, n-1)

	if n == m:
		# p*p-ecke
		if fields[corners[1]-1] and fields[corners[3]+1]:
			return pxp(f, 2)

		# symmetrie aufrecht erhalten -> irgendwann p*p ecke
		try: count_top = (fields[:corners[1]+1]).index(False)
		except ValueError: count_top = n

		try: count_left = list(reversed(fields[corners[3]:])).index(False) + 1
		except ValueError: count_left = m

		diff = abs(count_top - count_left)

		# linke kante hat mehr, an der oberen kompensieren
		if count_left > count_top:
			return Move(count_top, count_top+diff-1)
		else:
			return Move(l-count_left-diff+1, l-count_left)

	elif n != m:
		# gegner berührt noch nicht die andere kante? symmetrie aufrecht erhalten
		if (not fields[corners[2]-1]) and (not fields[corners[2]]) and (not fields[corners[3]+1]) and (not fields[corners[3]]):
			try: count_left = list(reversed(fields[corners[3]:])).index(False) + 1
			except ValueError: count_left = m

			count_right = fields[corners[1]:corners[2]+1].index(False)

			diff = abs(count_left - count_right)
			if diff == 0: raise RuntimeError("Hilfe :(")

			if count_left > count_right:
				return Move(corners[1]+count_right, corners[1]+count_right+diff-1)
			else:
				return Move(l-count_left-diff+1, l-count_left)

		# gegner hat kante berührt? p*p-ecke
		elif fields[corners[3]+1] and fields[corners[3]] and fields[corners[3]-1]:
			return pxp(f, 2)
		elif fields[corners[2]-1] and fields[corners[2]] and fields[corners[2]+1]:
			return pxp(f, 3)
		elif fields[corners[2]-1]:
			return pxp(f, 3)
		elif fields[corners[3]+1]:
			return pxp(f, 2)

	raise RuntimeError("Hilfe!!", fields)

VISITED = []
WAIT = 0
F = Field(5, 5)

def tryAllMoves(f: Field, movelist: list[Move]):
	movelist = copy.deepcopy(movelist)
	moves = f.get_valid_moves()
	moves.sort(key=Move.abs)

	if not moves:
		print("Renate gewinnt!")
		time.sleep(WAIT)
		return

	for move in moves:
		g = f.copy()
		movelist.append(move)
		print(movelist)
		g.make_move(move, 2)
		g.render(False)

		time.sleep(WAIT)

		rm = optimal_renate_move(g)
		movelist.append(rm)
		print(movelist)
		g.make_move(rm, 1)
		g.render(False)

		tryAllMoves(g, copy.deepcopy(movelist))

# clear(True)
m1 = optimal_renate_move(F)
F.make_move(m1, 1)
F.render(False)
tryAllMoves(F, [m1])
print(f"{BOLD}{YELLOW}Alle Zugkombinationen durchprobiert! Wenn keine Exception geworfen wurde, hat Renate eine sichere Gewinnstrategie :){END}")

# F.fields = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
# F.render()
# print(F.corners)
# print(optimal_renate_move(F))
