from chessclass import *
from displayinit import *
from setting import *
import pygame
from multiprocessing import Process,Pipe

fd1,fd2 = Pipe()
UserLogin = 50
UserMenu = 51
UserHall = 52
UserPlayer = 53

#窗口大小
WIDTH,HEIGHT = (1044,586)
#记录棋盘中心相对于(0,0)的坐标
chessboard_center = (265,293) 

IP = addr
PORT = port

# 初始化
pygame.init()
# 创建一个窗口
screen = pygame.display.set_mode((WIDTH,HEIGHT))
# 窗口名称
pygame.display.set_caption('中国象棋')
screen.fill((255,255,255,255))
#获取窗口中心坐
screen_center = screen.get_rect().center
#print('screen_center ',screen_center)
#窗口中心坐标 相对于 棋盘中心相坐标 的偏移量
relativex,relativey = screen_center[0] - chessboard_center[0],screen_center[1] - chessboard_center[1]
grid_size = 56
 #记录格点相对于棋盘左上角的坐标 
grid_left_top_point = (40,40)
grid_right_bottom_point = (488,544)
#棋盘宫格上下左右的边界
grid_lef_top_margin = (40 + relativex,40 + relativey)
grid_right_bottom_margin = (488+ relativex,544 + relativey)

limit_board1 = 40 + relativey + grid_size * 4
limit_board2 = 40 + relativey + grid_size * 5

#将、士 大本营限制
#左 、右x 坐标
limit_palace_x1 = 40 + relativex + grid_size*2
limit_palace_x2 = 40 + relativex + grid_size*6
#将、士 大本营限制
#上、下 y 坐标
limit_palace_up_y = 40 + relativey + grid_size *3
limit_palace_down_y = 544 + relativey - grid_size *3

#棋盘、棋子对象存放列表[ChessBordObject,ChessPieces1,ChessPieces2,....,ChessPieces32]
chessobjects = []
#棋盘地图字典
board={}
#棋盘上棋子的位置信息字典{(x,y):cheessobject}
chess_xy_obj = {}
chess_xy_name ={}
#棋盘上棋子的坐标(x,y), 
chess_pos =[]

#绘制棋盘,chessboard[0]为棋盘surface,chessboard[1]为棋盘对象
chessboard = ChessBoard_display_init(chessobjects,screen_center)
#布棋，chessobjects[1] ------chessobjects[32] 将保存32个棋子对象，
chess_display_init(chessobjects,relativex,relativey)
#------------以上至此完成了空窗口设置，棋盘，棋子对象的生成----------------#
#----------------------------------------------------------------------#     

select1_dir = './images/select1.png'
select1_img = pygame.image.load(select1_dir).convert_alpha()
select1 = SelectState(select1_img,'select1')

for i,obj in zip(list(range(1,33)),chessobjects[1:]): 

    if obj.name[-5:] == '7.png':
        if obj.rect.center[1] < screen_center[1]:
            obj.limit_board1 = limit_board1
        else:
            obj.limit_board2 = limit_board2


    #将、士 大本营行走限制
    if obj.name[-5:] == '5.png' or obj.name[-5:] == '4.png':         
        obj.limit_palace_x1 = limit_palace_x1
        obj.limit_palace_x2 = limit_palace_x2

        if obj.rect.center[1] < screen_center[1]:
            obj.limit_palace_y = limit_palace_up_y 
        else:
            obj.limit_palace_y = limit_palace_down_y 


            


for i,obj in zip(list(range(1,33)),chessobjects[1:]):
    chess_xy_name[obj.rect.center] = obj.name
    chess_xy_obj[obj.rect.center] = obj
    chess_pos.append(obj.rect.center)


#棋盘地图字典
x = 40+ relativex
y = 40 + relativey
board={}
board2={}
for i in range(10):
    for i in range(9):
        board[(x,y)] = 0
        board[(x,y)] = 0
        x +=grid_size
    x = 40+ relativex
    y +=grid_size
board.update(chess_xy_obj)
board2.update(chess_xy_name)



# print('-----------------------------chess_xy_name----------------------------------')
# print('----------------------------------------------------------------------------')
# print(chess_xy_name)
# print('----------------------------------------------------------------------------')
# print('----------------------------------------------------------------------------')

# print('----------------------------------------------------------------------------')
# print('----------------------------------------------------------------------------')
# print('-------------------------board----------------------------------------------')
# print(board)
# print('----------------------------------------------------------------------------')
# print('----------------------------------------------------------------------------')

# print('--------------------------board2--------------------------------------------')
# print(board2)
# print('----------------------------------------------------------------------------')
# print('----------------------------------------------------------------------------')

# print("relativex,relativey",relativex,relativey)
