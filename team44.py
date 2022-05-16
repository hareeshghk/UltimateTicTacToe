import sys
import random


class Player44:
	def __init__(self):
		
		self.bflags = ('x','o')
		self.pos = {}
		self.block_corr = { 0:[1,3] , 1:[0,2] , 2:[1,5] , 3:[0,6] , 4:[4] , 5:[2,8] , 6:[3,7] , 7:[6,8] , 8:[5,7]}
		self.cells={0:[(i,j) for i in range(3)for j in range(3)],
					1:[(i,3+j) for i in range(3)for j in range(3)],
					2:[(i,6+j) for i in range(3)for j in range(3)],
					3:[(i+3,j) for i in range(3)for j in range(3)],
					4:[(i+3,j+3) for i in range(3)for j in range(3)],
					5:[(i+3,j+6) for i in range(3)for j in range(3)],
					6:[(i+6,j) for i in range(3)for j in range(3)],
					7:[(i+6,j+3) for i in range(3)for j in range(3)],
					8:[(i+6,j+6) for i in range(3)for j in range(3)]}

	def count(self,cnt_x,cnt_o,cnt_n):

		if (cnt_x == 2 and cnt_o == 1) or (cnt_x == 1 and cnt_o == 2) or (cnt_n == 3 ) or (cnt_x == cnt_o == cnt_n ==1):
			return  0
		elif cnt_x == 2 :
			return 10
		elif cnt_o == 2 :
			return -10
		elif cnt_x == 1:
			return 1
		elif cnt_o == 1:
			return -1
		elif cnt_o == 3:
			return -100
		elif cnt_x == 3:
			return 100

	def calc(self,val):
		if val <= -2:                           # val = [-3,-2]
			tmp = -10+(val+2)*90
			return tmp

		elif val <= -1:                         # val = (-2,-1]
			tmp = -1 + (val+1)*9
			return tmp

		elif val <= 1:		                    # val = (-1,1]
			return val

		elif val <= 2:                          # val = (1,2]
			tmp = 1+(val-1)*9
			return tmp

		elif val <= 3:                          # val = (2,3]
			tmp = 10+(val-2)*90
			return tmp
	
	def utilit(self,boardmy,blockmy):
		t = []
		u_b = [0]*9
		vert={0:(0,0), 1:(0,3), 2:(0,6), 3:(3,0), 4:(3,3), 5:(3,6), 6:(6,0), 7:(6,3), 8:(6,6)}
		
		for i in range(9):
			if blockmy[i] == '-':
				t.append(i)
			elif blockmy[i] == 'o':
				u_b[i] = -1
			elif blockmy[i] == 'x':
				u_b[i] = 1
		for j in range(len(t)):
			x = vert[t[j]][0]
			y = vert[t[j]][1]
			u = 0
			for p in range(x,x+3):

				cnt_x,cnt_o,cnt_n = 0,0,0

				for q in range(y,y+3):
					if boardmy[p][q] == 'x':
						cnt_x += 1
					elif boardmy[p][q] == 'o':
						cnt_o += 1
					elif boardmy[p][q] == '-':
						cnt_n += 1
				u += self.count(cnt_x,cnt_o,cnt_n)
			for q in range(y,y+3):

				cnt_x,cnt_o,cnt_n = 0,0,0

				for p in range(x,x+3):
					if boardmy[p][q] == 'x':
						cnt_x += 1
					elif boardmy[p][q] == 'o':
						cnt_o += 1
					elif boardmy[p][q] == '-':
						cnt_n += 1
				u += self.count(cnt_x,cnt_o,cnt_n)
			cnt_x,cnt_o,cnt_n = 0,0,0	
			for p in range(3):

				if boardmy[x+p][y+p] == 'x':
					cnt_x += 1
				elif boardmy[x+p][y+p] == 'o':
					cnt_o += 1
				elif boardmy[x+p][y+p] == '-':
					cnt_n += 1
			u += self.count(cnt_x,cnt_o,cnt_n)

			cnt_x,cnt_o,cnt_n = 0,0,0
			for p in range(3):

				if boardmy[x+p][y+2-p] == 'x':
					cnt_x += 1
				elif boardmy[x+p][y+2-p] == 'o':
					cnt_o += 1
				elif boardmy[x+p][y+2-p] == '-':
					cnt_n += 1
			u += self.count(cnt_x,cnt_o,cnt_n)

			if u >= 80:
				u = 80
			elif u <= -80:
				u = -80
			u_b[t[j]] = u/80.0
		uti = 0
		r = 0
		while r <= 6:
			m = u_b[r]+u_b[r+1]+u_b[r+2]
			uti += self.calc(m)
			r += 3
		r = 0
		while r <= 2:
			m = u_b[r]+u_b[r+3]+u_b[r+6]
			uti += self.calc(m)
			r += 1
		m = u_b[0]+u_b[4]+u_b[8]
		uti += self.calc(m)

		m = u_b[2]+u_b[4]+u_b[6]
		uti += self.calc(m)

		return uti 

	def valid_block(self, my_block, my_move):
		B = self.block_corr[(my_move[0]%3)*3 + (my_move[1]%3)]
		if len(B) == 1 :
			if my_block[4] == '-':
				return [4]
			else:
				return []
		else:
			if my_block[B[0]] == '-' and my_block[B[1]] == '-':
				return B
			elif my_block[B[0]] == '-':
				return [B[0]]
			elif my_block[B[1]] == '-':
				return [B[1]]
			else:
				return []
		
	def alphabeta(self,my_board,my_block,my_move,my_flag,depth,alpha,beta):
		#print my_move, depth ,'(x,y),depth'
		if depth==4:
			h = self.utilit(my_board,my_block)
			return (h, h, h)
		if depth%2 == 0:
			utility = 100000

		else:
			utility = -100000
		p=self.valid_block(my_block,my_move)
		if len(p)==0:
			for i in range(9):
				if my_block[i]=='-':
					p.append(i)
		for j in range(len(p)):
			b = self.cells[p[j]]
			for k in b:
				if my_board[k[0]][k[1]] == '-':
					if alpha > beta:
						break
					tmpboard = [['-'for q in range(9)]for q in range(9)]
					for i in range(9):
						for j in range(9):
							tmpboard[i][j] = my_board[i][j]

					#update block

					tmpboard[k[0]][k[1]] = my_flag
					if my_flag == 'x':
						ind = 1
						
					else:
						ind = 0
					
					value = self.alphabeta(tmpboard,my_block,k,self.bflags[ind],depth+1,alpha,beta)
					if depth%2 == 0:
						if beta > value[0]:
							beta = value[0]
						if utility > value[0]:
							utility = value[0]
					else:
						if alpha < value[0]:
							alpha = value[0]
						if utility < value[0]:
							utility = value[0]
					
			if alpha > beta:
				break
		if depth!=0:
			if depth == 1:
				self.pos[utility] = my_move
			return (utility, alpha, beta)
		if depth == 0:
			print(my_flag)
			return sorted(self.pos.items())[len(self.pos)-1][1]

	def move(self, board, block, old_move, flag):
		if old_move[0] == -1 :
			return (1,1) 
		myflag = flag
		mymove = old_move
		myboard = [['-'for i in range(9)]for i in range(9)]
		myblock = ['-'for i in range(9)]
		for i in range(9):
			for j in range(9):
				myboard[i][j] = board[i][j]
		for i in range(9):
			myblock[i] = block[i]
		else:
			move = self.alphabeta(myboard, myblock, mymove, myflag ,0, -10000 ,10000)
			print(flag)
			return move



	










