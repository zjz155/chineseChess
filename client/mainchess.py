import pygame
from multiprocessing import Process,Pipe
from screeninit import *
from socket import *
from register import *
from hall import *
from  play import *
import pdb


#登入背景图
login_img_dir = './images/login.jpg'
#大厅及游戏背景图
bg_img_dir = './images/background.jpg'

house_img_dir = './images/house.png'

house_img = pygame.image.load(house_img_dir).convert_alpha()
house_img=pygame.transform.scale(house_img, (100, 100))



pygame.font.init()
#创建套接字
sockfd = socket()
sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
#建立管送，用于各各功能模块间的通信
# fd1,fd2 = Pipe()



def chat_room(sockfd):
    while True:     
        sockfd.send('tcp_t2'.encode())
        print('data')
        data = sockfd.recv(1024).decode()
        print(data)     

#主函数
def user_interface():   
    print('前台程序显示界面...... ')
    
    user_register.login_display()    
    while True:     
        # user.exit_game()        
        print('前台程序显示界面...... ')
        #clock.tick(60)     
        data = fd2.recv()
        if data == UserLogin:   
            user_register.login_display()
        elif data == UserMenu:
            print('menu')
            user.menu()
        elif data == UserHall:
          user_hall.hall()
        elif data == UserPlayer:
           user_play.game_start()
        else:
            user_register.login_display()    

#创建套接字
sockfd = socket()
sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
#登入用户与服务器建立通信连接
sockfd.connect((IP,PORT))

#创建用户登入对象
user_register = Register(sockfd,screen,login_img_dir,0)
#创建用户大厅对象
user_hall = Hall(sockfd,screen,bg_img_dir,0)
#创建用户对战房间对象
user_play = Play(sockfd,screen,bg_img_dir,0)



#建立管送，用于各各功能模块间的通信
# fd1,fd2 = Pipe()
# user_interface()


# p_user_interface = threading.Thread(target=user_interface)
if __name__ =='__main__':   
    user_interface()

    
    
    


    

        

    
    
    
    


    
