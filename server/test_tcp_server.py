# tcp_server.py
# import gevent
# from gevent import monkey
# monkey.patch_all()
from socket import *
from multiprocessing import Process
from threading import Thread
from time import sleep
from login_server import *

def handler(connfd):

    global n
    while True:
        data = connfd.recv(1024).decode()
        if not data:
            break
        # 登入/注册
        elif data[0] == 'L':
            print("Receive message:", data.encode())  

            msg = login(data)

            #登入／注册验证通过
            connfd.send(msg.encode())
         
            if n == 1:
                chess_dl.append(connfd)
                print("第一个connfd", n)
            elif n == 2:
                chess_dl.append(connfd)
                print("第二个connfd", n)

            
        

        # 进入大厅选房间
        elif data[0] == 'H':
            print("Receive message:", data.encode())
            # data = data.split(' ') 

            # num_people[data[2]] += 1

            # num1 = num_people["first"]
            # num2 = num_people["second"]
            # num3 = num_people["thrid"]
            # num4 = num_people["fourth"]

            # msg = str(num1) + " " + str(num2) + " " + str(num3) + " " + str(num4)

            # connfd.send(msg.encode())

            #成功进入房间
            connfd.send(b'ok')

                
        #游戏开始，请求服务器数据
        elif data == 'status':
            i= chess_dl.index(connfd)
            if i % 2:
                connfd.send(b'ok red')
                print('ok red')
            elif i % 2 == 0:
                connfd.send(b'ok black')
                print('ok black')
                chess_dl[i-1].send(b'chessred#')

        #
        #网络走棋,以下勿随意改动    
        if len(chess_dl[1:]) >= 2:
            i= chess_dl.index(connfd)           
            if data[0] == 'm':
                d = data.split(' ')
                board_update = ' '.join(d)
                print('board_update', d)
                print('data.split(' '):', board_update)
                if d[1] == 'chessred': 
                    if i % 2 == 1 and chess_dl[i+1] != []:
                        chess_dl[i+1].send(board_update.encode()) 
                        # sleep(0.5)                                    
                        # red
                        chess_dl[i].send(b'chessblack#')
                        # black
                        chess_dl[i+1].send(b'chessblack#')
                        # sleep(0.5)
                        data = []               

                elif d[1] == 'chessblack':  
                    if i % 2 == 0 and chess_dl[i-1] != []:                         
                        chess_dl[i-1].send(board_update.encode()) 
                        print("sucess")
                        # sleep(0.5)                                    
                        # black
                        chess_dl[i].send(b'chessred#')                   
                        # red
                        chess_dl[i-1].send(b'chessred#')
                        # sleep(0.5)
                        data = []
            
            elif data[0] == 's':
                try:
                    if i % 2 == 1 and chess_dl[i+1] != []:
                        chess_dl[i+1].send(data.encode())

                    elif i % 2 == 0:
                        chess_dl[i-1].send(data.encode())

                except IndexError:
                    print("please Waiting......")
                    connfd.send(b'heart#')
                    continue  

        
        if data == 'heart':
            connfd.send(b'heart#') 
                

        

    connfd.close()

def link_handler():
    pass    

m = 0
n = 0
num_people = {'first':0,'second':0,'third':0,'fourth':0}
# 存放连接套接字
chess_dl = [0]
chess_dt = []
# 创建套接字
sockfd = socket(AF_INET, SOCK_STREAM)
# 绑定地址
# sockfd.bind(('172.60.20.56', 8000))
sockfd.bind(('127.0.0.1', 8002))

# 设置监听
sockfd.listen(1024)


if __name__ == "__main__":
    while True:
        print("Waiting for connect....")
        connfd, addr = sockfd.accept()
        n += 1
        if n == 3:
            n = 1
        #     chess_dl = []

        print("Connect from", addr)
        # t = Thread(name = 'tedu' + str(i),target = fun,args = (3,))
        # t.setDaemon(True)
        p = Thread(target=handler, args=(connfd,))
        p.setDaemon(True)
        p.start()
