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

font = pygame.font.Font("STKAITI.TTF", 18)
text1_surface = font.render("号房间", True, (0,0, 255))
text2_surface = font.render("人", True, (0,0, 255))

house_img_dir = './images/house.png'
house_img = pygame.image.load(house_img_dir).convert_alpha()
house_img=pygame.transform.scale(house_img, (100, 100))

pygame.font.init()
class Hall:

    def __init__(self,sockfd,screen,img_dir,status):
        img = pygame.image.load(img_dir).convert_alpha()
        img = pygame.transform.scale(img, (1044, 586))
        self.sockfd = sockfd    
        self.screen = screen        
        self.img = img
        #获取图形对象有位置大小信息
        self.rect = self.img.get_rect()
        self.rect.center = self.screen.get_rect().center
        self.center = self.rect.center
        self.status = status

 #大厅房间号选则，点击在字母附近即可进入房间
    def hall(self):        
        
        print('==============hall======================')
        print("---------1号房间 2号房间 3号房间----------")
        print('=========================================')
        text = ''
        fontobject = pygame.font.Font(None,32)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            event = pygame.event.poll()
            mousexy = pygame.mouse.get_pos()            
            #大厅房间号选则,点击在字母附近即可进入房间  
            if event.type == MOUSEBUTTONDOWN:
                #first      
                if 324 <mousexy[0] < 446 and 425 < mousexy[1] <548:
                    self.sockfd.send('H first room player'.encode())    
                    #验证通过：进入大厅              
                    data = self.sockfd.recv(255).decode()
                    # self.hall_handler(data)
                    if data == 'ok':
                        print("I'm first room %s player"%data[3:])
                        break
                #second
                elif 281 < mousexy[0] < 427 and 308 < mousexy[1] < 405:
                    self.sockfd.send('H second room player'.encode())                   
                    #验证通过：进入大厅              
                    data = self.sockfd.recv(255).decode()
                    # self.hall_handler(data)
                    if data == 'ok':
                        print("I'm second room %s player"%data[3:])
                        break
                #third
                elif 345 < mousexy[0] < 452 and 211 < mousexy[1] < 338:
                    self.sockfd.send('H third room player'.encode())                    
                    #验证通过：进入大厅              
                    data = self.sockfd.recv(255).decode()
                    # self.hall_handler(data)
                    if data == 'ok':
                        print("I'm third room %s player"%data[3:])
                        break
                
                #fourth
                elif 532 < mousexy[0] < 684 and 96 < mousexy[1] < 190:
                    self.sockfd.send('H fourth room player'.encode())                   
                    data = self.sockfd.recv(255).decode()
                    #验证通过：进入大厅
                    # self.hall_handler(data)
                    if data == 'ok':
                        print("I'm fourth room %s player"%data[3:])
                        break
                else:
                    print('mousexy:',mousexy) 
            elif event.type == KEYDOWN:
                if event.key != 13 and event.key != K_ESCAPE:
                    text +=chr(event.key)                   
                elif event.key == K_ESCAPE:
                    os._exit(0) 
            elif event.type == QUIT:
                os._exit(0) 
            else:
                pass                  

                
            #显示大厅状态
            
            #绘制大厅背景
            self.screen.blit(self.img,(0,0))
            #绘制房间号:1 2, 3, 4    
           
            self.screen.blit(house_img,(345,400))
            self.screen.blit(house_img,(293,300))
            self.screen.blit(house_img,(345,200))
            self.screen.blit(house_img,(559,94))

            self.screen.blit(fontobject.render('1', 1, (0,0,0)),(360,500))  
            self.screen.blit(text1_surface,(370,500))  

            self.screen.blit(fontobject.render('2', 1, (0,0,0)),(300,400))
            self.screen.blit(text1_surface,(320,400)) 

            self.screen.blit(fontobject.render('3', 1, (0,0,0)),(370,300))
            self.screen.blit(text1_surface,(380,300))

            self.screen.blit(fontobject.render('4', 1, (0,0,0)),(574,190)) 
            self.screen.blit(text1_surface,(584,190))

            pygame.display.flip()
        fd1.send(UserPlayer)
         #大厅消息处理
    def hall_handler(self,data):
        #验证通过：进入大厅
        if data == 'ok red':
            print("I'm red")    
            self.status = 'chessred'                                    
        elif data == 'ok black':
            print("I'm black ")
            self.status = 'chessblack'  
        elif data == 'ok visitor':
            print("I'm visitor")
            self.status = 'visitor'
        else:
            print(data) 
