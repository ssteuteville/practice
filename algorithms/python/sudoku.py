"""
Implementation of local stochastic search applied to solving a sudoku puzzle
"""
import re
from random import randrange
from math import sqrt
import sys
class puzzle(object):
	def __init__(self, filename):
		f = open(filename)
		m = re.search(r'(\d+)x(\d+)', f.readline())
		self.w = int(m.group(1))
		self.h = int(m.group(2))
		assert(self.w == self.h)
		self.grid = [[randrange(1, self.w + 1) for col in range(self.w)] for row in range(self.h)]
		self.fixed = set()
		for line in f.readlines():
			m = re.search(r'\((\d+)\,(\d+)\) (\d+)', line)
			i,j,v = int(m.group(1)), int(m.group(2)), int(m.group(3))
			self.fixed.add((i,j))
			self.grid[i][j] = v

		
	def __str__(self):
		return ('{}\n' * self.h).format(*[row for row in self.grid])


	def pick_random(self):
		while True:
			i,j = randrange(0, self.h), randrange(0, self.w)
			if (i,j) not in self.fixed:
				return (i,j)

	def check_col(self):
		count = 0
		for col in range(self.w):
			seen = []
			for row in range(self.h):
				seen.append(self.grid[row][col])
			if len(seen) != len(set(seen)):
				count += 1
		return count

	def check_row(self):
		count = 0
		for row in range(self.h):
			seen = []
			for col in range(self.w):
				seen.append(self.grid[row][col])
			if len(seen) != len(set(seen)):
				count += 1
		return count

	def check_square(self):
		square = int(sqrt(self.h))
		count = 0
		for row in range(0,self.h, square):
			for col in range(0,self.w, square):
				seen = []
				for _row in range(row, row + square):
					for _col in range(col, col + square):
						seen.append(self.grid[_row][_col])
				if len(seen) != len(set(seen)):
					count += 1
		return count


	def violations(self):
		return self.check_col() + self.check_row() + self.check_square()

	def update(self):
		i,j = self.pick_random()
		_min = self.violations()
		orig = _min
		temp = self.grid[i][j]
		min_val = temp
		for _ in range(1, self.w+1):
			if _ != temp:
				self.grid[i][j] = _
				violations = self.violations()
				if violations < _min:
					_min = violations
					min_val = _
		self.grid[i][j] = min_val

	def reset(self):
		count = 0
		while count < self.w:
			i, j = self.pick_random()
			self.grid[i][j] = randrange(1,self.w+1)
			count += 1

	def solve(self):
		violations = self.violations()
		count = 0
		while self.violations():
			self.update()
			if violations == self.violations():
				count += 1
			else:
				violations = self.violations()
				count = 0
			
			if count > 1000:
				self.reset()
				count = 0




if __name__=="__main__":
	p = puzzle(sys.argv[1])
	print(p)
	p.solve()
	print(p)