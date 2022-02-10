# Compiling
# Working
# Checkered

from mpi4py import MPI
import sys

import math

# takes all neighbourhoods of the cell at towers[i][j]
# updates health[i][j] according to the rules of the game
# returns the updated health

# a = above
# la = left above
# l = left
# lb = left below
# b = below
# rb = right below
# r = right
# ra = right above
def update(towers, healths, a, la, l, lb, b, rb, r, ra, i, j):
	if(towers[i][j] == '.'): return healths
	dict_ = {'.':0, 'o':1, '+':2}
	
	healths[i][j] = healths[i][j] - dict_[a] if towers[i][j] != a else healths[i][j]
	healths[i][j] = healths[i][j] - dict_[b] if towers[i][j] != b else healths[i][j]
	healths[i][j] = healths[i][j] - dict_[l] if towers[i][j] != l else healths[i][j]
	healths[i][j] = healths[i][j] - dict_[r] if towers[i][j] != r else healths[i][j]
	if(la == 'o' and towers[i][j] == '+'): healths[i][j] -= 1
	if(lb == 'o'and towers[i][j] == '+'): healths[i][j] -= 1
	if(ra == 'o'and towers[i][j] == '+'): healths[i][j] -= 1
	if(rb == 'o'and towers[i][j] == '+'): healths[i][j] -= 1

	return healths

# P = x^2 (perfect square) 
# P will always be an even number.

comm = MPI.COMM_WORLD
size = comm.Get_size()  # number of processors
rank = comm.Get_rank()  # which process (rank=0 --> manager process)

inputfile = sys.argv[1]
outputfile = sys.argv[2]


# manager process
if rank == 0: 
	f = open(inputfile, "r")
	line0 = (f.readline()).split(" ")
	N = int(line0[0])  # number of rows in the matrix
	W = int(line0[1])  # number of waves to iterate - total wave time : W * 8
	T = int(line0[2])  # number of towers placed at the start of the each round
	workers = size - 1
	root = math.sqrt(workers)
	cell_per_worker = int(N // (root))  # number of rows for each worker processor - (checkered-type)

	for i in range(1, size):
		comm.send(N, dest=i, tag=7) # send N (number of rows) to worker processor with rank = i (from 1 to size - 1)
	for i in range(1, size):
		comm.send(W, dest=i, tag=8)  # send W (number of waves) to worker processor with rank = i (from 1 to size - 1)
	for i in range(1, size):
		comm.send(cell_per_worker, dest=i, tag=9)   # send (number of rows) to worker processor with rank = i (from 1 to size - 1)

	# iterate through the rounds
	A = N / cell_per_worker
	for round in range(W):
		board = [[0 for i in range(N)] for j in range(N)]
		line1 = (f.readline()).split(", ")  # o (coordinates) 
		line2 = (f.readline()).split(", ")  # + (coordinates)
		for i in range(T):
			coordinates = line1[i].split(" ")
			x = int(coordinates[0])
			y = int(coordinates[1])
			board[x][y] = 1                 # place o (attack power = 1)
		for i in range(T):
			coordinates = line2[i].split(" ")
			x = int(coordinates[0])
			y = int(coordinates[1])
			board[x][y] = 2		            # place + (attack power = 2)
		
		for i in range(1, size):
			row_start = int((i - 1)/A) * cell_per_worker
			row_end = row_start + cell_per_worker #not inclusive
			col_start = int((i - 1)%A) * cell_per_worker 
			col_end =  col_start + cell_per_worker #not inclusive
			comm.send([x[col_start:col_end] for x in board[row_start:row_end]], dest=i, tag=10)
	f.close()
	# writing the output
	f = open(outputfile, "w")
	output = [[0 for i in range(N)] for j in range(N)]
	for i in range(1,size):
		towers = comm.recv(source=i, tag=57)  # receive towers (lists) from worker procesors one by one
		
		row_start = int((i - 1)/A) * cell_per_worker
		row_end = row_start + cell_per_worker #not inclusive
		col_start = int((i - 1)%A) * cell_per_worker 
		col_end =  col_start + cell_per_worker #not inclusive
		
		for i in range(row_start, row_end):
			for j in range(col_start, col_end):
				output[i][j] = towers[i - row_start][j - col_start]

	# write the output to the output file
	for i in range(N):
		for j in range(N):
			f.write(output[i][j])
			if j != N - 1:
				f.write(" ")
		if i!= N - 1:
			f.write("\n")	
	f.close()
else:
	N = comm.recv(source=0, tag=7) # receive number of rows from manager processor
	W = comm.recv(source=0, tag=8) # receive number of waves from manager processor
	cell_per_worker = comm.recv(source=0, tag=9) # receive number of rows per worker from manager processor
	towers = [['.' for i in range(cell_per_worker)]for j in range(cell_per_worker)] #  towers 
	healths = [[0 for i in range(cell_per_worker)]for j in range(cell_per_worker)]  # healths

	for wave in range(W):
		board = comm.recv(source=0, tag=10) # receive the board from manager
		for i in range(cell_per_worker):  
			for j in range(cell_per_worker):
				if board[i][j] == 1 and towers[i][j] == '.': # if it is empty and board[i][j] = 1, put 'o'
					towers[i][j] = 'o'
					healths[i][j] = 6
				elif board[i][j] == 2 and towers[i][j] == '.': # if it is empty and board[i][j] = 2, put '+'
					towers[i][j] = '+'
					healths[i][j] = 8
		# It is guaranteed that processer number is odd, which means that number of worker processors are even.
		# Indices of worker processors start from 1 and go to n (n being even)	

		A = N / cell_per_worker

		## Tags (order)
		# 11: above
		# 12: below
		# 13: left
		# 14: right
		# 15: above right
		# 16: below right
		# 17: above left
		# 18: below left


		# Receive order
		# from below
		# from above
		# from right
		# from left
		# from below left
		# from above left
		# from below right
		# from above right
		for _ in range(8):  # 8 rounds for each wave

		### ODD : send first, then receive
		### EVEN : receive first, then send

			from_above = ["." for _ in range(cell_per_worker)]
			from_below = ["." for _ in range(cell_per_worker)]
			from_left = ["." for _ in range(cell_per_worker)]
			from_right = ["." for _ in range(cell_per_worker)]
			from_right_above = "."
			from_right_below = "."
			from_left_above = "."
			from_left_below = "."	

			#### First, swap the rows (top or bottom)
			# p1 p2 p3 p4  --> odd
			# p5 p6 p7 p8  --> even
			# p9 p10 p11 p12  --> odd
			# p13 p14 p15 p16 --> even

			odd1 = ((rank - 1) // A) % 2 == 0
			if rank <= A:  # top above row (odd)
				if(odd1):
					comm.send(towers[cell_per_worker-1], dest=rank+A, tag=12)  # below
					from_below = comm.recv(source=rank+A, tag=11)  # from below
				else:
					from_below = comm.recv(source=rank+A, tag=11)  # from below
					comm.send(towers[cell_per_worker-1], dest=rank+A, tag=12)  # below
			elif rank > A*(A-1):  # last row (even)
				if(odd1):
					comm.send(towers[0], dest=rank-A, tag = 11)   # above
					from_above = comm.recv(source=rank-A, tag = 12)   # from above
				else:
					from_above = comm.recv(source=rank-A, tag = 12)   # from above
					comm.send(towers[0], dest=rank-A, tag = 11)   # above
			else:  # intermediate rows
				if(odd1):
					comm.send(towers[0], dest=rank-A, tag=11)   # above
					comm.send(towers[cell_per_worker-1], dest=rank+A, tag=12)  # below
					from_below = comm.recv(source=rank+A, tag=11)  # from below
					from_above = comm.recv(source=rank-A, tag=12)   # from above
				else:
					from_below = comm.recv(source=rank+A, tag=11)  # from below
					from_above = comm.recv(source=rank-A, tag=12)   # from above
					comm.send(towers[0], dest=rank-A, tag=11)   # above
					comm.send(towers[cell_per_worker-1], dest=rank+A, tag=12)  # below


			
			#### Secondly, swap the columns (rows)
			#  odd  even  odd   even
			# p1    p2    p3    p4  p
			# p5    p6    p7    p8  
			# p9    p10   p11   p12  
			# p13   p14   p15   p16 

			odd2 = (rank%2 == 1)
			if(rank%A==1):   # first column (odd)
				if(odd2):
					comm.send([towers[x][cell_per_worker - 1] for x in range(cell_per_worker)], dest=rank+1, tag=14) # right
					from_right = comm.recv(source=rank+1, tag=13) # from right
				else:
					from_right = comm.recv(source=rank+1, tag=13) # from right
					comm.send([towers[x][cell_per_worker - 1] for x in range(cell_per_worker)], dest=rank+1, tag=14) # right
			elif(rank%A==0):   # last column (even)
				if(odd2):
					comm.send([towers[x][0] for x in range(cell_per_worker)], dest=rank-1, tag=13) # left
					from_left = comm.recv(source=rank-1, tag=14) # from left
				else:
					from_left = comm.recv(source=rank-1, tag=14) # from left
					comm.send([towers[x][0] for x in range(cell_per_worker)], dest=rank-1, tag=13) # left
			else:
				if(odd2):
					comm.send([towers[x][0] for x in range(cell_per_worker)], dest=rank-1, tag=13) # left
					comm.send([towers[x][cell_per_worker - 1] for x in range(cell_per_worker)], dest=rank+1, tag=14) # right	
					from_right = comm.recv(source=rank+1, tag=13) # from right
					from_left = comm.recv(source=rank-1, tag=14) # from left		
				else:
					from_right = comm.recv(source=rank+1, tag=13) # from right
					from_left = comm.recv(source=rank-1, tag=14) # from left	
					comm.send([towers[x][0] for x in range(cell_per_worker)], dest=rank-1, tag=13) # left
					comm.send([towers[x][cell_per_worker - 1] for x in range(cell_per_worker)], dest=rank+1, tag=14) # right
			
			#### Thirdly, swap the corners from left below to right above
			
			# p1 (odd)    p2 (odd)   p3 (odd)   p4  (odd)   --> odd 
			# p5 (even)   p6  (even)   p7 (even)  p8  (even)  --> even
			# p9 (odd)    p10 (odd)  p11 (odd)  p12 (odd)   --> odd
			# p13(even)   p14 (even)   p15 (even) p16 (even) --> even

			odd3 = odd1

			if(rank == 1): # no sending
				pass
			elif(rank == A*A): # no sending either
				pass
			elif(rank <= A or rank%A==0): # first row or last column (don't send to right above) (notice that very first worker and last worker is not included)
				if(odd3):
					comm.send(towers[cell_per_worker-1][0], dest=rank+A-1, tag=18) # below left	
					from_left_below = comm.recv(source=rank+A-1, tag=15) # from below left
				else:
					from_left_below = comm.recv(source=rank+A-1, tag=15) # from below left
					comm.send(towers[cell_per_worker-1][0], dest=rank+A-1, tag=18) # below left	
			elif(rank > A*(A-1) or rank%A==1):  # last row or first column
				if(odd3):
					comm.send(towers[0][cell_per_worker-1], dest=rank-A+1, tag=15)  # above right
					from_right_above = comm.recv(source=rank-A+1, tag=18)  # from above right
				else:
					from_right_above = comm.recv(source=rank-A+1, tag=18)  # from above right
					comm.send(towers[0][cell_per_worker-1], dest=rank-A+1, tag=15)  # above right
			else:
				if(odd3):
					comm.send(towers[0][cell_per_worker-1], dest=rank-A+1, tag=15)  # above right
					comm.send(towers[cell_per_worker-1][0], dest=rank+A-1, tag=18) # below left	
					from_left_below = comm.recv(source=rank+A-1, tag=15) # from below left
					from_right_above = comm.recv(source=rank-A+1, tag=18)  # from above right
				else:
					from_left_below = comm.recv(source=rank+A-1, tag=15) # from below left
					from_right_above = comm.recv(source=rank-A+1, tag=18)  # from above right
					comm.send(towers[0][cell_per_worker-1], dest=rank-A+1, tag=15)  # above right
					comm.send(towers[cell_per_worker-1][0], dest=rank+A-1, tag=18) # below left	
					
			#### Lastly, swap the corners from right below to left above
			
			# p1 (odd)    p2 (odd)   p3 (odd)   p4  (odd)   --> odd 
			# p5 (even)   p6  (even)   p7 (even)  p8  (even)  --> even
			# p9 (odd)    p10 (odd)  p11 (odd)  p12 (odd)   --> odd
			# p13(even)   p14 (even)   p15 (even) p16 (even) --> even

			odd4 = odd1


			if(rank == A): # no sending : p4
				pass
			elif(rank == A*(A-1) + 1): # no sending either : p13
				pass
			elif(rank <= A or rank%A==1): # first row or first column (don't send to left above) (notice that p4 and p13 is not included)
				if(odd3):
					comm.send(towers[cell_per_worker-1][cell_per_worker-1], dest=rank+A+1, tag=16)  #below right
					from_right_below = comm.recv(source=rank+A+1, tag=17)  # from below right
				else:
					from_right_below = comm.recv(source=rank+A+1, tag=17)  # from below right
					comm.send(towers[cell_per_worker-1][cell_per_worker-1], dest=rank+A+1, tag=16)  #below right
			elif(rank > A*(A-1) or rank%A==0):  # last row or last column
				if(odd3):
					comm.send(towers[0][0], dest=rank-A-1, tag = 17) # above left
					from_left_above = comm.recv(source=rank-A-1, tag = 16) # from above left
				else:
					from_left_above = comm.recv(source=rank-A-1, tag = 16) # from above left
					comm.send(towers[0][0], dest=rank-A-1, tag = 17) # above left
			else:
				if(odd3):
					comm.send(towers[cell_per_worker-1][cell_per_worker-1], dest=rank+A+1, tag=16)  #below right
					comm.send(towers[0][0], dest=rank-A-1, tag = 17) # above left
					from_left_above = comm.recv(source=rank-A-1, tag = 16) # from above left
					from_right_below = comm.recv(source=rank+A+1, tag=17)  # from below right
				else:
					from_left_above = comm.recv(source=rank-A-1, tag = 16) # from above left
					from_right_below = comm.recv(source=rank+A+1, tag=17)  # from below right
					comm.send(towers[cell_per_worker-1][cell_per_worker-1], dest=rank+A+1, tag=16)  #below right
					comm.send(towers[0][0], dest=rank-A-1, tag = 17) # above left

			## from left/right --> i
			## from below/above --> j
			#### PLAY THE ROUND ####
			if cell_per_worker == 1:  # special situation where number of cells per worker is 1
				a = from_above[0]
				la = from_left_above
				l = from_left[0]
				lb = from_left_below
				b = from_below[0]
				rb = from_right_below
				r = from_right[0]
				ra = from_right_above

				healths = update(towers, healths, a, la, l, lb, b, rb, r, ra, i, j)
			else:
				for i in range(cell_per_worker):
					for j in range(cell_per_worker):
						if(i==0):
							if(j==0):  # first row first column
								a = from_above[j]  # from_above[0]
								la = from_left_above
								l = from_left[i]  
								lb = from_left[i + 1]
								b = towers[i + 1][j]
								rb = towers[i + 1][j + 1]
								r = towers[i][j + 1]
								ra = from_above[j + 1]

								healths = update(towers, healths, a, la, l, lb, b, rb, r, ra, i, j)
							elif(j==cell_per_worker-1):    # first row last column
								a = from_above[j]
								la = from_above[j - 1]
								l = towers[i][j - 1]
								lb = towers[i+1][j-1]
								b = towers[i+1][j]
								rb = from_right[i+1]
								r = from_right[i]
								ra = from_right_above

								healths = update(towers, healths, a, la, l, lb, b, rb, r, ra, i, j)
							else:    # first row - intercells
								a = from_above[j]
								la = from_above[j - 1]
								l = towers[i][j-1]
								lb = towers[i+1][j-1]
								b = towers[i+1][j]
								rb = towers[i+1][j+1]
								r = towers[i][j+1]
								ra = from_above[j + 1]

								healths = update(towers, healths, a, la, l, lb, b, rb, r, ra, i, j)
						elif(i==cell_per_worker - 1):
							if(j == 0):
								a = towers[i - 1][j]
								la = from_left[i - 1]
								l = from_left[i]
								lb = from_left_below
								b = from_below[j]
								rb = from_below[j+1]
								r = towers[i][j+1]
								ra = towers[i-1][j+1]

								healths = update(towers, healths, a, la, l, lb, b, rb, r, ra, i, j)
							elif(j == cell_per_worker-1):
								a = towers[i - 1][j]
								la = towers[i - 1][j - 1]
								l = towers[i][j - 1]
								lb = from_below[j - 1]
								b = from_below[j]
								rb = from_right_below
								r = from_right[i]
								ra = from_right[i - 1]

								healths = update(towers, healths, a, la, l, lb, b, rb, r, ra, i, j)
							else:
								a = towers[i - 1][j]
								la = towers[i - 1][j - 1]
								l = towers[i][j - 1]
								lb = from_below[j - 1]
								b = from_below[j]
								rb = from_below[j + 1]
								r = towers[i][j + 1]
								ra = towers[i - 1][j + 1]

								healths = update(towers, healths, a, la, l, lb, b, rb, r, ra, i, j)
						else:
							if(j == 0):
								a = towers[i - 1][j]
								la = from_left[i - 1]
								l = from_left[i]
								lb = from_left[i + 1]
								b = towers[i + 1][j]
								rb = towers[i + 1][j + 1]
								r = towers[i][j + 1]
								ra = towers[i - 1][j + 1]

								healths = update(towers, healths, a, la, l, lb, b, rb, r, ra, i, j)
							elif(j == cell_per_worker-1):
								a = towers[i - 1][j]
								la = towers[i - 1][j - 1]
								l = towers[i][j - 1]
								lb = towers[i + 1][j - 1]
								b = towers[i + 1][j]
								rb = from_right[i + 1]
								r = from_right[i]
								ra = from_right[i - 1]

								healths = update(towers, healths, a, la, l, lb, b, rb, r, ra, i, j)
							else:
								a = towers[i - 1][j]
								la = towers[i - 1][j - 1]
								l = towers[i][j - 1]
								lb = towers[i + 1][j - 1]
								b = towers[i + 1][j]
								rb = towers[i + 1][j + 1]
								r = towers[i][j + 1]
								ra = towers[i - 1][j + 1]

								healths = update(towers, healths, a, la, l, lb, b, rb, r, ra, i, j)

			# update the healths
			for i in range(cell_per_worker):
				for j in range(cell_per_worker):
					if healths[i][j] <= 0:
						towers[i][j] = '.'
						healths[i][j] = 0
	# send back the towers to the manager processor
	for i in range(1,size):
		comm.send(towers, dest=0, tag=57)