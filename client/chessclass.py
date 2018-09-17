import pygame
import pdb
'''
	此模块用于定义类及函数功能
	主要定义了棋盘类、棋子类及相关的函数功能'''

class ChessPieces(pygame.sprite.Sprite):
	"""docstring for ChessPieces"""
	def __init__(self,x,y,ChessPieces_img,name):
		pygame.sprite.Sprite.__init__(self)
		self.name = name
		#加图形
		self.image = ChessPieces_img
		self.image.set_colorkey((0,0,0))
		#self.image = pygame.transform.scale(self.image,(50,50))
		#获取图形对象有位置大小信息
		self.rect = self.image.get_rect()
		#更新图形对象的中心位置
		self.rect.center = (x,y)
		
	def update(self):
		pass
	def the_border_of_two(self,relativex,relativey,grid_size):
		limit_board1 = (40 + relativex,40 + relativey + grid_size * 5)
		limit_board2 = (40 + relativex,40 + relativey + grid_size * 6)

	def run_method(self,vector,destination_pos,board,grid_size):
		print('destination_pos = ',destination_pos,'vector = ',vector)
		vector_x = abs(vector[0])
		vector_y = abs(vector[1])
		#车
		if self.name[-5:] == '1.png':
			dack_num = 0
			point_list = []
			
			#走y轴
			if vector_x < 20:

				direction = int(vector[1] /vector_y)				
				#判断车到目标点其有几个点
				num = int (vector_y / grid_size)
				#如果车走的步数大于1，
				if  2 <= num:
					for i in range(1,num+1):
						point_list.append((self.rect.centerx,self.rect.centery + i*grid_size*direction))
					print('走y轴',point_list)
					#判断车到目标点之间有几个棋
					for i in point_list:					
						if board[i]:
							dack_num +=1
							if dack_num >=2:
								return 0		
				print('走y轴')				
				#原位置置0
				board[self.rect.center] = 0
				#改变棋子对象坐标
				self.rect.centery = destination_pos[1]	
				#维护棋盘字典			
				board[self.rect.center] = self
				return 1

			#走x轴
			elif vector_y < 20:

				direction = int(vector[0] /vector_x)				
				#判断车到目标点其有几个
				num = int (vector_x / grid_size)
				#车在大于1步的区间内不能有棋子
				if  2 <= num:
					for i in range(1,num+1):
						point_list.append((self.rect.centerx + i*grid_size*direction,self.rect.centery))
					print('走x轴',point_list)
					#判断车到目标点之间隔着棋
					for i in point_list:					
						if board[i]:
							dack_num +=1
							if dack_num >=2:
								return 0	
							

				print('走x轴')				
				#原位置置0
				board[self.rect.center] = 0
				#改变棋子对象坐标				
				self.rect.centerx = destination_pos[0]
				#维护棋盘字典			
				board[self.rect.center]= self
				return 1
			else:
				return 0
		# pdb.set_trace()
		
		#马
		if self.name[-5:] == '2.png':
			#走x轴
			if vector_y != 0 and vector_x / (vector_y) == 2:
				#计算马眼位置
				obstacle = (self.rect.centerx + vector[0]/2,self.rect.centery)
				if board[obstacle]:
					return 0
				else:
					# #原位置置0
					board[self.rect.center] = 0					
					#改变棋子对象坐标
					self.rect.centerx = destination_pos[0]
					self.rect.centery = destination_pos[1]
					#维护棋盘字典			
					board[self.rect.center]= self					
					print(self.rect.center)
					return 1
			elif vector_x != 0 and vector_y / vector_x == 2:
				#计算马眼位置
				obstacle = (self.rect.centerx,self.rect.centery + vector[1]/2)
				if board[obstacle]:
					return 0
				else:
					#原位置置0
					board[self.rect.center] = 0					
					#改变棋子对象坐标
					self.rect.centerx = destination_pos[0]
					self.rect.centery = destination_pos[1]
					#维护棋盘字典			
					board[self.rect.center]= self					
					print(self.rect.center)
					return 1
			else:
				return 0

		#象
		if self.name[-5:] == '3.png':
			#走x-y轴
			if vector_x == vector_y == 2 * grid_size:
				#计算象眼位置
				obstacle = (self.rect.centerx + vector[0] / 2,self.rect.centery + vector[1] / 2)
				if board[obstacle]:
					return 0
				else:
					#原位置置0
					board[self.rect.center] = 0
					#改变棋子对象坐标
					self.rect.centerx = destination_pos[0]
					self.rect.centery = destination_pos[1]
					#维护棋盘字典			
					board[self.rect.center]= self
					return 1			
			else:
				return 0
		#士
		if self.name[-5:] == '4.png':

			if destination_pos[0] == self.limit_palace_x1 or destination_pos[0] == self.limit_palace_x2:
				return 0

			if destination_pos[1] == self.limit_palace_y:
				return 0

			if vector_x == vector_y == grid_size:
				# #原位置置0
				board[self.rect.center] = 0
				#改变棋子对象坐标
				self.rect.centerx = destination_pos[0]
				self.rect.centery = destination_pos[1]
				#维护棋盘字典			
				board[self.rect.center]= self
				return 1
			else:
				return 0

		#将
		if self.name[-5:] == '5.png':	

			if destination_pos[0] == self.limit_palace_x1 or destination_pos[0] == self.limit_palace_x2:
				return 0

			if destination_pos[1] == self.limit_palace_y:
				return 0

			#走y轴
			if vector_x < 20 and vector_y == grid_size :
				print('走y轴')				
				#原位置置0
				board[self.rect.center] = 0
				#改变棋子对象坐标
				self.rect.centery = destination_pos[1]	
				#维护棋盘字典			
				board[self.rect.center] = self
				return 1
			#走x轴
			elif vector_y < 20 and vector_x == grid_size:
				print('走x轴')				
				#原位置置0
				board[self.rect.center] = 0
				#改变棋子对象坐标				
				self.rect.centerx = destination_pos[0]
				#维护棋盘字典			
				board[self.rect.center]= self
				return 1
			else:
				return 0
		#炮
		if self.name[-5:] == '6.png':
			point_list =[]
			dack_list =[]
			dack_num = 0
			#走y轴
			if vector_x < 20:
				#获得走棋方向
				direction = int(vector[1] /vector_y)				
				#判断炮到目标点其有几个
				num = int (vector_y / grid_size)
				#生成点坐标
				if 2<= num:
					for i in range(1,num+1):
						point_list.append((self.rect.centerx,self.rect.centery + i*grid_size*direction))
					print('走y轴',point_list)
				#判断炮到目标点之间有几个棋
				for i in point_list:					
					if board[i]:
						dack_list.append(board[i])
						dack_num +=1						
				if dack_num == 0 or dack_num ==2:
					# #原位置置0
					board[self.rect.center] = 0					
					#改变棋子对象坐标
					self.rect.centerx = destination_pos[0]
					self.rect.centery = destination_pos[1]
					#维护棋盘字典			
					board[self.rect.center]= self
					return 1
				elif 2 < dack_num:
					return 0
				else:
					pass				
			#走x轴
			elif vector_y < 20:
				#获得走棋方向
				direction = vector[0] /vector_x				
				#判断炮到目标点其有几个
				num = int(vector_y / grid_size)
				if 1 <= num:
					for i in range(1,num+1):
						point_list.append((self.rect.centerx + i*grid_size*direction,self.rect.centery))
				print('走x轴',point_list)

				#判断炮到目标点之间有几个棋
				for i in point_list:
					if board[i]:
						dack_list.append(board[i])
						dack_num +=1						
				if dack_num == 0 or dack_num ==2:
					# #原位置置0
					board[self.rect.center] = 0					
					#改变棋子对象坐标
					self.rect.centerx = destination_pos[0]
					self.rect.centery = destination_pos[1]
					#维护棋盘字典			
					board[self.rect.center]= self
					return 1
				elif 2 < dack_num:
					return 0
				else:
					pass

			
		#兵
		if self.name[-5:] == '7.png':

			if self.name == "chessred7.png":
				#不能后退
				if destination_pos[1] < self.rect.centery: 
					return 0
				#没过河，不能平移
				if destination_pos[1] <= self.limit_board1 and destination_pos[0] != self.rect.centerx:
					return 0
			else:				
				#不能后退
				if destination_pos[1] > self.rect.centery: 
					return 0
				#没过河，不能平移
				if  destination_pos[1] >= self.limit_board2 and destination_pos[0] != self.rect.centerx:
					return 0
			#走y轴
			if vector_x < 20 and vector_y == grid_size :
				print('走y轴')				
				# #原位置置0
				board[self.rect.center] = 0
				#改变棋子对象坐标
				self.rect.centery = destination_pos[1]	
				#维护棋盘字典			
				board[self.rect.center] = self
				return 1
			#走x轴
			elif vector_y < 20 and vector_x == grid_size:
				print('走x轴')				
				#原位置置0
				board[self.rect.center] = 0
				#改变棋子对象坐标				
				self.rect.centerx = destination_pos[0]
				#维护棋盘字典			
				board[self.rect.center]= self
				return 1
			else:
				return 0
		

class ChessBoard(pygame.sprite.Sprite):
	"""docstring for ChessBoard"""
	def __init__(self,coordinate,ChessBoard_img):
		pygame.sprite.Sprite.__init__(self)		
		#加图形
		self.image = ChessBoard_img
		self.image.set_colorkey((0,0,0))
		#获取图形对象有位置大小信息
		self.rect = self.image.get_rect()
		#更新图形对象的中心位置
		self.rect.center = coordinate	

	#chess_obj为选中的棋子对象;
	#pos为棋子对象想要移动的目标坐标;
	#计算出棋子落子处的位置向量大小，即x,y的偏移量;．
	def move_chess(self,chess_obj,pos,board):
		# print('在　move_chess（）　里')
		# print('mov chess....',chess_obj.name)
		if chess_obj == 0:
			return
		print('棋子原来所在位置',chess_obj.rect.center)
		destination_pos = MyTuple(pos)
		source_pos = MyTuple(chess_obj.rect.center)
		vector = destination_pos - source_pos
		if vector == (0,0):
			return
		#move = 1，成功，
		move = chess_obj.run_method(vector,destination_pos,board,56)
		if move:
			print('棋子移动到了位置',destination_pos)	
		return move

	#下棋时，左键点击棋盘：
	#此函数返将反回一个字典{(x,y),chess_name} or {(x,y),0}。
	def do_check_state(self,board):
		event = pygame.event.poll()					
		select = pygame.mouse.get_pressed()		
		if select[0]:
			while True:
				event = pygame.event.poll()
				if event.type == pygame.MOUSEBUTTONUP:	
					break
			mousex,mousey = pygame.mouse.get_pos()
			for t in board.keys():			
				if abs(mousex - t[0]) <= 20 and abs(mousey - t[1]) <= 20:
					if board[t] != 0 :
						#点选处有棋子对象[(x,y,chessname)]
						print("do_select ",[t,board[t].name])
						return [t,board[t].name]						
					else:
						#点选处没有棋子对象[(x,y,0)]
						print("do_move",[t,board[t]])
						return [t,board[t]]	
		return []			
	#棋盘的棋子位置地图
	def geographic_map(self):
		x = 40
		y = 40
		List=[]
		for i in range(10):
			for i in range(9):
				List.append((x,y))
				x +=grid_size
			x = 40
			y +=grid_size

		return List
	#更新棋盘的棋子位置地图
	def update(self):
		pass	
			
	def estimate(self):
		pass


class SelectState(pygame.sprite.Sprite):
	"""docstring for ChessPieces"""
	def __init__(self,SelectState_img,name,state = 0):
		pygame.sprite.Sprite.__init__(self)
		self.state = 0
		self.name = name
		#加图形
		self.image = SelectState_img
		self.image.set_colorkey((0,0,0))
		#self.image = pygame.transform.scale(self.image,(50,50))
		#获取图形对象有位置大小信息
		self.rect = self.image.get_rect()
		#更新图形对象的中心位置
		self.rect.center =(-9999,-9999)

	def update(self):
		pass
#聊天室类
class ChatRoom(object):
	"""docstring for ChatRoom"""
	def __init__(self, arg):
		super(ChatRoom, self).__init__()
		self.arg = arg
		
#元组相减
class MyTuple:
	def __init__(self,iterable = ()):
		self.data = [x for x in iterable]
	def __repr__(self):
		return 'MyList(%r)' % self.data

	def __getitem__(self, i):
		print("i =", i)
		return self.data[i]

	def __setitem__(self, i, val):
		self.data[i] = val
	
	def __sub__(self,rhs):
		L = []
		for i in range(2):
			L.append(self.data[i]-rhs.data[i])
		return tuple(L)

def generarte_location_information(x,y,chessobjects = [],chess_list = {},chess_pos = {}):
	#棋子对象所在坐标，存在 chess_pos 列表中
	for i,obj in zip(list(range(1,33)),chessobjects[1:]):
		chess_list[obj.rect.center] = obj
		chess_pos.append(obj.rect.center)	
	
	#棋盘地图字典	
	board_List={}
	for i in range(10):
		for i in range(9):
			board_List[(x,y)] = None
			x +=grid_size
		x = 40
		y +=grid_size
	board_List.update(chess_list)
	print('-----------------------------chess_pos------------------------------')
	print(chess_list.items())
	print('--------------------------------------------------------------------')

	print('--------------------------board_List-----------------------------------')
	print(board_List.items())
	print('--------------------------------------------------------------------')

if __name__ =='__main__':
	print('this is a module for chinese chess')