import pygame,pygame.font
from screeninit import *
from multiprocessing import Process,Pipe
import threading
import os
from signal import *
import sys
from time import sleep,ctime 
from pygame.locals import *
# import gevent 
# from gevent import monkey
# # 需要在socket导入前执行,改变socket的属性
# monkey.patch_all()
from socket import *

pygame.mixer.init()

capture_music = pygame.mixer.Sound("./sound/capture.wav")
move_music = pygame.mixer.Sound("./sound/move.wav")

font = pygame.font.Font("STKAITI.TTF", 40)
red_text_surface = font.render("我是红方", True, (255, 0, 0))
black_text_surface = font.render("我是黑方", True, (0, 0, 0))
win_text_surface = font.render("我输了", True, (0, 255, 0))

 #创建 红方-黑方 精灵组
chessreds = pygame.sprite.Group()
chessblacks = pygame.sprite.Group()
selects = pygame.sprite.Group()


for i in range(1,17):
    chessreds.add(chessobjects[i])
for i in range(17,33):
    chessblacks.add(chessobjects[i])        
selects.add(select1)

class Play:

    def __init__(self,sockfd,screen,img_dir,status):
        img = pygame.image.load(img_dir).convert_alpha()
        # img = pygame.transform.scale(img, (1044, 586))
        self.sockfd = sockfd    
        self.screen = screen        
        self.img = img
        #获取图形对象有位置大小信息
        self.rect = self.img.get_rect()
        self.rect.center = self.screen.get_rect().center
        self.center = self.rect.center
        self.status = status

    #开始对弈
    def game_start(self):
        print('==============game_start==================')
        print("----------------正在玩游戏-----------------")
        print('==========================================')         

        data_list = 0
        flags = 0
        run = 0    

         # 请求分配红方/黑方
        while self.status == 0:

            self.sockfd.send('status'.encode())
            data = self.sockfd.recv(255).decode()
            print('请求分配红方/黑方:',data)
            if data == 'ok red':
                print("I'm red")    
                self.status = 'chessred'
            elif data == 'ok black':
                print("I'm black")
                self.status = 'chessblack' 
        

        if self.status == 'chessred':
                    
            print("红方")
        elif self.status == 'chessblack':
           
            print("黑方")

        #游戏开始   
        clock = pygame.time.Clock() 
        while True:
            clock.tick(60)
                                   

            chessblacks.update()
            chessreds.update()
            selects.update()

            # self.screen.blit(select1.image,select1.rect)
            self.screen.blit(chessobjects[0].image,chessobjects[0].rect)

            if self.status == 'chessred':
                self.screen.blit(red_text_surface, (80, 100))
            else:
                self.screen.blit(black_text_surface, (800, 500))
            
            chessblacks.draw(self.screen)
            chessreds.draw(self.screen)
            selects.draw(self.screen)
            # 双缓冲渲染 
            pygame.display.flip()

            n = 0
            #捕获退出操作           
            self.exit_game() 


            
            if self.status != data:
                self.sockfd.send(b'heart')                
            #客户端接受数据
            data = self.sockfd.recv(255).decode() 
            #区分前后上下文数据，判断数据传输完成
            data_list = data.split('#')
            data_list.pop()
            print("data_list",data_list)

            # data_list = ['chessred']

            #解析数据，根据数据进行不同功能的操作
            for data in data_list:
                if data == 'chessred' or data == 'chessblack':
                   self.do_chess(data)  
                # elif data[0][0] == 'm':
                #     print("data[0] = 'm'",data[0])
                elif data != '' and data[0] == 'm':
                    self.net_chess(data)  
                else:              
                    data = data.split(' ')
                    if data[0] == 's':
                        #同步光标
                        if self.status != data[1]:                        
                            x = int(data[2])
                            y = int(data[3])
                            selected = (x,y) 
                            #绘制光标
                            select1.rect.center = selected                          
                            selects.update()                                                      
                            selects.draw(self.screen)
                            pygame.display.flip()   
                           
                            print(data)
                            print("self.status:",self.status,data[1],selected)

                        else:
                            pass

                            # print(data) 
            print("我一直在运行") 

    def do_chess(self,chesscolor):  

        solider_list=[]
        # solder_active = 0
        solder_active = [0,0]
        solider_active_list = []
        # solder_target = 0
        solder_target = []
        solider_target_list = []
        flags = 0
        self.win_lose()
        if self.status == chesscolor:
            while True:                  
                #[(x,y),'chessname.png']         
                solider_active_list = chessboard[1].do_check_state(board)                       
                # print("solider_active_list",solider_active_list)                
                if solider_active_list != []: 

                    #向服务端发送点选行为:select x y chessname,select x y 0
                    action = 's' + ' ' + self.status + ' '+ str(solider_active_list[0][0]) + ' ' + str(solider_active_list[0][1]) + ' ' + str(solider_active_list[1]) + '#'
                    self.sockfd.send(action.encode())               
      
                    #点选处有对象
                    if solider_active_list[1] != 0 :   

                        #绘制光标
                        select1.rect.center = (solider_active_list[0][0],solider_active_list[0][1])
                        selects.update()
                        # self.screen.blit(select1.image,select1.rect)                        
                        selects.draw(self.screen)
                        pygame.display.flip()  

                        #获得待命的棋子对象名
                        solder_active_color = solider_active_list[1][:-5]                   
                        print('solder_active_color chesscolor',solder_active_color,chesscolor)  
                       

                        if solder_active_color == chesscolor:
                            #存放已方棋子
                            solder_active[0] = solider_active_list[0]                                       
                            print("solder_active[0] == solider_active_list[0]",solder_active[0],solider_active_list[0])
                            print("第一次",solder_active[0],solder_active_color)

                           
                        elif solder_active[0] != 0:
                            #存第二次选棋对象的坐标
                            solder_active[1] = solider_active_list[0]
                            solder_active_color = solider_active_list[1][:-4]

                            #如果两次选的都是己方棋，那么取消选棋
                            if solder_active_color == chesscolor:                           
                                solder_active = [0,0]
                               
                            else:
                                #成功走棋flag == 1
                                flags = chessboard[1].move_chess(board[solder_active[0]],solder_active[1],board)
                                if flags == 1:
                                    print("board[solder_active[0]]",board[solder_active[0]])
                                    #维护棋盘地图字典
                                    # board.update({solder_active:0})
                                    print("棋子原来所在位置solder_active[0]",solder_active[0])
                                    print("棋子移动到了位置solder_active[1]]",solder_active[1])
                    #点选处无对象
                    elif solder_active[0] :
                        solder_active[1] = solider_active_list[0]
                        #成功走棋flag == 1
                        flags = chessboard[1].move_chess(board[solder_active[0]],solder_active[1],board)
                        if flags == 1:
                            print("board[solder_active[0]]",board[solder_active[0]])
                            #维护棋盘地图字典
                            # board.update({solder_active:0})
                            print("棋子原来所在位置solder_active[0]",solder_active[0])
                            print("棋子移动到了位置solder_active[1]]",solder_active[1])   
                                  
                         
                    
                    
                if flags == 1: 
                     #绘制光标
                    select1.rect.center = (solider_active_list[0][0],solider_active_list[0][1])
                    selects.update()
                    # self.screen.blit(select1.image,select1.rect)                        
                    selects.draw(self.screen)
                    pygame.display.flip()                    

                    #本地走棋，判断是不是自已走棋。
                    if self.status == chesscolor and solider_active_list != []:         
                        msg = 'm' +' ' + chesscolor + ' ' + str(solder_active[0][0]) + ' '+str(solder_active[0][1]) + ' ' + str(solder_active[1][0]) + ' ' +str(solder_active[1][1]) + '#'
                        self.sockfd.send(msg.encode())
                        flags = 0
                        #精灵碰撞检测
                        if chesscolor == 'chessred':
                            hits = pygame.sprite.groupcollide(chessreds,chessblacks,False,True)
                        elif chesscolor == 'chessblack':
                            hits = pygame.sprite.groupcollide(chessblacks,chessreds,False,True) 

                        if hits:
                            capture_music.play() 
                        else:
                            move_music.play()

                        chesscolor = [0]                    
                        print(self.status,'recv',chesscolor)                    
                        # self.win_lose()
                        break
                 
                # print("我一直在运行")
                # print(self.status,'recv',chesscolor)
                self.exit_game() 

    #data 为网络走棋信息字符串“m chesscolor x y dx dy”
    def net_chess(self,data):
        print("----------网络走棋----------")
        data = data.split(' ')
        # pdb.set_trace()
        if data[1] != self.status:           
            # if data == '#': 
            #     #发送“#”告知服务器我在等待开局
            #     self.sockfd.send('#'.encode())
            # data = self.sockfd.recv(255).decode()               
            # print(chesscolor)               
          
            print("data[0] == 'm'",data[1])           
            color = data[1]
            chess_xy =tuple(data[-4:-2:1])
            chess_xy = (int(chess_xy[0]),int(chess_xy[1]))
            move_xy = tuple(data[-2:])
            move_xy = (int(move_xy[0]),int(move_xy[1]))
            #更新棋盘
            chessboard[1].move_chess(board[chess_xy],move_xy,board)
            flags = 1
            board[chess_xy]=0  

            print('chess_xy',chess_xy)
            print('move_xy',move_xy)

             #网络走棋
            if color == 'chessred':
                hits = pygame.sprite.groupcollide(chessreds,chessblacks,False,True)
            elif color == 'chessblack':
                hits = pygame.sprite.groupcollide(chessblacks,chessreds,False,True)

            flags = 0 

            if hits:
                capture_music.play() 
            else:
                move_music.play()

            chessblacks.update()
            chessreds.update()
            selects.update()                                 
            
            
            
            self.screen.blit(chessobjects[0].image,chessobjects[0].rect)
            # self.screen.blit(select1.image,select1.rect)  
            
            chessblacks.draw(self.screen)
            chessreds.draw(self.screen)
            selects.draw(self.screen)
            # 双缓冲渲染 
            pygame.display.flip() 
            #break       

            # elif chesscolor[0] == 's':
            #     self.screen.blit(house_img,board[chess_xy].rect)

    def exit_game(self):
        n = 0
        while n<50:
            # 事件获取  
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                print("请求退出")
                if event.key == K_ESCAPE:
                    os._exit(0)
                   
            elif event.type == QUIT:
                print("请求退出")
                os._exit(0)   

            n += 1    
    def win_lose(self):
        objName = []
        if self.status =='chessred':
            for obj in chessreds:
                objName.append(obj.name)
        
            if 'chessred5.png' not in objName:
                self.screen.blit(win_text_surface, (80, 140))
                pygame.display.flip()
        else:
            for obj in chessblacks:
                objName.append(obj.name)
        
            if 'chessblack5.png' not in objName:
                self.screen.blit(win_text_surface, (800, 460))
                pygame.display.flip()



    def select_chess(self):
        pass