# authors: Daniel Gribel, Joao Paulo Forny

import numpy as np
import random
import time
import copy

start_time = time.time()

def init_memory_quad(m, n, delta):
	M = np.zeros((m, n))
	for i in range(0, m):
		M[i, 0] = i*delta
	for j in range(0, n):
		M[0, j] = j*delta

	return M

def init_memory_linear(m, delta):
	CURRENT = [0 for i in range(m)]
	for i in range(0, m):
		CURRENT[i] = i*delta

	return CURRENT

# get cost in quadratic space: O(n^2) time, O(n^2) space
def get_cost_quad(x, y, delta, alpha):
	m = len(x)
	n = len(y)
	M = init_memory_quad(m+1, n+1, delta)
	
	for i in range(1, m+1):
		for j in range(1, n+1):
			mismatch = M[i-1, j-1]
			if x[i-1] != y[j-1]:
				mismatch = mismatch + alpha
			
			M[i, j] = min(mismatch, delta + M[i-1, j], delta + M[i, j-1])
	
	return M

# get cost in linear space: O(n^2) time, O(2n) space
def get_cost_linear(x, y, delta, alpha):
	m = len(x)
	n = len(y)

	CURRENT = init_memory_linear(m+1, delta)

	for j in range(1, n+1):
		LAST = copy.copy(CURRENT)
		CURRENT[0] = j*delta
		for i in range(1, m+1):
			mismatch = LAST[i-1]
			if x[i-1] != y[j-1]:
				mismatch = mismatch + alpha
			CURRENT[i] = min(mismatch, delta + LAST[i], delta + CURRENT[i-1])

	return CURRENT

# find sequence for quadratic storage: O(2n) time, O(n^2) space
def find_sequence_iterative(M, i, j, x, y, delta, alpha):
	while(i != 0 and j != 0):
		mismatch = M[i-1, j-1]
		if x[i-1] != y[j-1]:
			mismatch = mismatch + alpha
		if M[i, j] == mismatch:
			#print(x[i-1], y[j-1])
			i = i-1
			j = j-1
		else:
			if M[i,j] == delta + M[i-1, j]:
				i = i-1
			else:
				j = j-1

delta = 0.7
alpha = 1
alphabet = "abcd"

for i in range(0, 1):
	for j in range(0, 10):

		string_length = 10 * pow(2, i+1)
		
		x = [random.choice(alphabet) for _ in range(string_length)]
		y = [random.choice(alphabet) for _ in range(string_length)]
		
		M1 = get_cost_quad(x, y, delta, alpha)
		M2 = get_cost_linear(x, y, delta, alpha)
		find_sequence_iterative(M1, len(x), len(y), x, y, delta, alpha)

print(time.time() - start_time)