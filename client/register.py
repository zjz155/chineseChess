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

font = pygame.font.Font("STKAITI.TTF", 16)
user_text_surface = font.render("用户名/注册用户名", True, (0,0, 255))
code_text_surface = font.render("用户密码/注册密码", True, (0,0, 255))

login_img_dir = './images/login.png'
login_img = pygame.image.load(login_img_dir).convert_alpha()
login_img=pygame.transform.scale(login_img, (70, 70))
pygame.font.init()
class Register:    
    #初始化登入界面,screen游戏窗口                     
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
    
    #登入界面：
    # 客户端   
    #   输入: 用户名 密码c
    #   发送：'L '+用户名+ ' ' + 密码
    def login_display(self):        
        username = []
        userpwd = []    
        userpassword = []
        usernamestr = ''
        userpasswordstr = ''
        flag = 1
        input_field = 0
        print("登入: 等待用户输入....")         
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)  
            fontobject = pygame.font.Font(None,32) 
       
            self.screen.blit(self.img,self.rect)   
            self.screen.blit(login_img,(480,300))          
            self.screen.blit(fontobject.render(usernamestr, 1, (0,0,0)),(465,223))
            self.screen.blit(fontobject.render(userpasswordstr, 1, (0,0,0)),(465,268))            

            if flag == 1:
                self.screen.blit(user_text_surface,(465,223))           
                self.screen.blit(code_text_surface,(465,268)) 

            pygame.display.flip()

            mousexy = pygame.mouse.get_pos()            
            event = pygame.event.poll() 
            if event.type == MOUSEBUTTONDOWN:  
                flag = 0
                print("mousexy:",mousexy)
                if 410 < mousexy[0] < 629 and 214 < mousexy[1] < 245:
                    input_field = 1        
                if 410 < mousexy[0] < 629 and 246 < mousexy[1] <286:
                    input_field = 2
                if 486 < mousexy[0] < 547 and 322 < mousexy[1] < 348:
                    input_field = 3
                #输入用户名
                if input_field == 1:
                    userpasswordstr = ''.join(userpassword)
                    usernamestr = ''.join(username)+'|'
                    # input_field = 1
                #输入用户密码
                elif input_field == 2:
                    usernamestr = ''.join(username)
                    userpasswordstr = ''.join(userpassword) +"|"
                    # input_field = 2

                elif input_field == 3:
                    username = ''.join(username)
                    userpwd = ''.join(userpwd)
                    msg = "L " + username +' ' + userpwd
                    #向服务器发送用户信息
                    self.sockfd.send(msg.encode())  
                    #等待服务器验信息               
                    data = self.sockfd.recv(255).decode()
                    #验证通过：进入大厅
                    if data != '' and data == 'ok usrname password':
                        print(msg)
                        break
                    else:
                        username = []
                        userpwd = []    
                        userpassword = []
                        usernamestr = ''
                        userpasswordstr = ''
                        flag = 1


                else:
                    print("mousexy:",mousexy)

            #输入检测
            elif event.type == KEYDOWN:
                userpasswordstr = ''.join(userpassword)
                #输入用户名
                # if 410 < mousexy[0] < 629 and 214 < mousexy[1] < 245:   
                if input_field == 1:                 
                    if 32<= event.key < 127:                                                
                        print(event.key)
                        username.append(chr(event.key))
                        usernamestr = ''.join(username)+'|' 
                    #回退删除，backspace检测
                    elif event.key == 8 and username != []:
                        username.pop()  
                        usernamestr = ''.join(username)+'|' 

                #输入用户密码
                # elif 410 < mousexy[0] < 629 and 246 < mousexy[1] <286:
                if input_field == 2:
                    usernamestr = ''.join(username)                 
                    if 47< event.key < 127:
                        userpwd.append(chr(event.key))
                        userpassword.append('*')
                        userpasswordstr = ''.join(userpassword) +"|"
                    #回退删除，backspace检测
                    elif event.key == 8 and userpassword != []:
                        userpassword.pop()  
                        userpasswordstr = ''.join(userpassword)+'|'
                #ESC，退出
                elif event.key == K_ESCAPE:
                    os._exit(0)

                else:
                    pass
                ##用户输入用户名、密码后，回车确认                  
                if event.key == 13 and username != [] and userpwd != []:    
                    username = ''.join(username)
                    userpwd = ''.join(userpwd)
                    msg = "L " + username +' ' + userpwd
                    #向服务器发送用户信息
                    self.sockfd.send(msg.encode())  
                    #等待服务器验信息               
                    data = self.sockfd.recv(255).decode()
                    #验证通过：进入大厅
                    if data !='' and data == 'ok usrname password':
                        print(msg)
                        break   
                        #fd1.send(UserPlayer)                                           
                        
                    #验不通过，用户端提示，重新输入
                    else:
                        print(data)                     
                
            elif event.type == QUIT:
                os._exit(0) 
            else:
                pass
            
        fd1.send(UserHall)  

    def exit_game(self):
        # 事件获取  
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            print("请求退出")
            if event.key == K_ESCAPE:
                os._exit(0)
                sys.exit()
        if event.type == QUIT:
            print("请求退出")
            os._exit(0)
            sys.exit()