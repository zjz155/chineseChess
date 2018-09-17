import pygame
from chessclass import *
'''
此模块用于创建初始化棋盘
初棋局初始化：参数 列表   棋盘坐标相对窗口(0,0)点相对位移
chess_display_init(chessobjects,relativex,relativey)
'''
#创建棋盘返回一个棋盘surface,和棋盘对象
def ChessBoard_display_init(objList,screen_center):
	ChessBoard_dir = './images/board.png'
	ChessBoard_img = pygame.image.load(ChessBoard_dir).convert_alpha()
	ChessBoard1 = ChessBoard(screen_center,ChessBoard_img)
	# screen.blit(ChessBoard1.image,ChessBoard1.rect)	
	objList.append(ChessBoard1)
	#返回一个棋盘surface
	return (ChessBoard_img,ChessBoard1)

#布第一排棋子 车马相仕 帅 仕相马车
def chess_display_init1(objList,chesscolor,x,y):

	#左半棋控制
	start = 1 
	end = 6	
	direc =1

	#第一次布左半棋，第二次布右半棋
	for i in [1,2]:
		for j in range(start,end,direc):

			#获得棋子的目录
			ChessPieces_dir = './images/{}{}.png'.format(chesscolor,str(j))
			#载入对应目录下的棋了图像
			ChessPieces_img = pygame.image.load(ChessPieces_dir).convert_alpha()
			#实例化棋子对像并初化出生点中心位置
			ChessPieces1 = ChessPieces(x,y,ChessPieces_img,ChessPieces_dir[9:])
			#保存对象
			objList.append(ChessPieces1)
			x += 56
			# screen.blit(ChessPieces1.image,ChessPieces1.rect)
		#右半棋控制
		direc = -1
		start = 4
		end = 0	

#布第二排棋子	 炮
def chess_display_init2(objList,chesscolor,x,y):


	if chesscolor == 'chessred':
		ChessPieces_dir = './images/chessred6.png'
		ChessPieces_img = pygame.image.load(ChessPieces_dir).convert_alpha()
		ChessPieces1 = ChessPieces(x,y,ChessPieces_img,ChessPieces_dir[9:])
		objList.append(ChessPieces1)
		ChessPieces1 = ChessPieces(6*56 + x,y,ChessPieces_img,ChessPieces_dir[9:])
		objList.append(ChessPieces1)
	else:
		ChessPieces_dir = './images/chessblack6.png'
		ChessPieces_img = pygame.image.load(ChessPieces_dir).convert_alpha()
		ChessPieces1 = ChessPieces(x,y,ChessPieces_img,ChessPieces_dir[9:])
		objList.append(ChessPieces1)
		ChessPieces1 = ChessPieces(6*56 + x,y,ChessPieces_img,ChessPieces_dir[9:])
		objList.append(ChessPieces1)

#布第三排棋子	 兵
def chess_display_init3(objList,chesscolor,x,y):
	
	for j in range(5):
		ChessPieces_dir = './images/{}{}.png'.format(chesscolor,'7')
		ChessPieces_img = pygame.image.load(ChessPieces_dir).convert_alpha()
		ChessPieces1 = ChessPieces(x,y,ChessPieces_img,ChessPieces_dir[9:])
		objList.append(ChessPieces1)
		x += 112
		# screen.blit(ChessPieces1.image,ChessPieces1.rect)

#初始化棋子对象的位置
def chess_display_init(chessobjects,relativex,relativey):
	#布红棋，第一排棋子 车马相仕 帅 仕相马车
	chess_display_init1(chessobjects,'chessred',40+ relativex, 40 + relativey)
	#布第二排棋子	 炮
	chess_display_init2(chessobjects,'chessred', 96 + relativex, 152 + relativey)
	#布第三排棋子	 兵
	chess_display_init3(chessobjects,'chessred', 40 + relativex, 208 + relativey)

	#布黑棋，第一排棋子 车马相仕 帅 仕相马车
	chess_display_init1(chessobjects,'chessblack',40 + relativex, 544 + relativey)
	#布第二排棋子	 炮
	chess_display_init2(chessobjects,'chessblack', 96 + relativex, 432 +relativey)
	#布第三排棋子	 兵
	chess_display_init3(chessobjects,'chessblack', 40 + relativex, 376 + relativey)



if __name__ =='__main__':
	print('this is a module for chinese chess')